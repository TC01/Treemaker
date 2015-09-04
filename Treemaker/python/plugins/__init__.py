import imp
import inspect
import os
import sys

# This plugin-loading code is stolen from myself, which is to say, I adapted
# an example in the Python imp documentation and then used it here:
# http://bitbucket.org/TC01/hex in an unrelated project.

plugins = []

## Helper functions.
def getScriptLocation():
	"""Helper function to get the location of a Python file."""
	location = os.path.abspath("./")
	if __file__.rfind("/") != -1:
		location = __file__[:__file__.rfind("/")]
	return os.path.join(location)

defaultLocation = getScriptLocation()

def getPossiblePluginNames(namesToLoad=[], location=defaultLocation):
	"""	Return a list of plugin names that we can try to import."""
	names = []
	for path, dirs, files in os.walk(location):
		if path == location:
			for filename in files:
				if not ".pyc" in filename or "__init__" in filename:
					filename = filename[:-len(".py")]
					if filename in namesToLoad or namesToLoad == []:
						names.append(filename)
	return names

def loadPlugins(pluginNames, parameters={}, silent=False):
	global plugins
	
	# Get a list of all possible plugin names
	names = getPossiblePluginNames(pluginNames.keys())
	pluginDict = {}
	if names == [] and not silent:
		print "ERROR: attempted to run Treemaker without specifying plugins!"
		print "The safest thing to do is fail."
		print "Please rerun Treemaker with the -c [config name] option, where [config name]"
		print "is a file containing newline-separated list of plugin names."
		sys.exit(1)

	# Now, use imp to load all the plugins we specified
	for name in names:
		try:
			test = sys.modules[name]
			if not silent:
				print "*** Error: a module with the name " + name + " was already loaded!"
				sys.exit(1)
		except KeyError:
			fp, pathname, description = imp.find_module(name, __path__)
			try:
				plugin = imp.load_module(name, fp, pathname, description)
				
				# Complain (once!) about deprecated function.
				if not silent:
					try:
						# If this doesn't trip an error, print a message.
						spec = inspect.getargspec(plugin.makeCuts)
						print "Error: deprecated makeCuts method is used in plugin '" + name + "'. Please see https://github.com/TC01/Treemaker/wiki/Deprecations"
					except AttributeError:
						pass

				plugin.parameters = parameters
				pluginDict[name] = plugin
				plugins.append(plugin)

			finally:
				if not fp is None:
					fp.close()

	# Sort plugins to make sure they got loaded in the right order.
	# Order is priority as specified in config file.
	pluginOrder = sorted(pluginDict, key = lambda name: pluginNames[name])
	for i in xrange(len(pluginOrder)):
		if not silent:
			print "*** Loading " + pluginOrder[i]
		plugins[i] = pluginDict[pluginOrder[i]]

	# If we choose to implement plugin dependencies, that should now be done.

	# Deal with unloaded plugins.
	# This should be a failure conditional.
	if len(pluginNames) != len(plugins) and not silent:
		for name in pluginNames.keys():
			if not name in pluginDict.keys():
				print "ERROR: unable to load plugin " + name
		sys.exit(1)

	# Then return plugins.
	return plugins

class PluginRunner:
	
	def __init__(self, plugins):
		# To preserve order and touch the fewest places, I will be lazy.
		# We really should have a Plugin class.
		self.plugins = plugins
		self.isDeprecated = []
		for plugin in self.plugins:
			numAnalyzeArgs = len(inspect.getargspec(plugin.analyze).args)
			if numAnalyzeArgs == 4:
				self.isDeprecated.append(True)
			else:
				self.isDeprecated.append(False)

	def createCutsPlugins(self, cutArray):
		for plugin in self.plugins:
			cutArray = plugin.createCuts(cutArray)
		return cutArray

	def setupPlugins(self, variables, isData):
		for plugin in self.plugins:
			variables = plugin.setup(variables, isData)
		return variables

	def analyzePlugins(self, event, variables, cuts, labels, isData):
		"""	Run the analyze and cut analyze routines. Also check if we should drop.
			For 'old' (up to Treemaker v1.0) formatted plugins, analyze and makeCuts
			are two separate calls.
			For 'new' (Treemaker v1.1 and onwards) plugins, this is one call."""
		shouldDrop = False
		count = 0
		for plugin in self.plugins:
			# If any plugin's drop method returns true, break. But not all
			# will have a drop method.
			if self.isDeprecated[count]:
				variables = plugin.analyze(event, variables, labels, isData)
				cuts = plugin.makeCuts(event, variables, cuts, labels, isData)				
			else:
				variables, cuts = plugin.analyze(event, variables, labels, isData, cuts)				
			count += 1
			try:
				if plugin.drop(event, variables, cuts, labels, isData):
					shouldDrop = True
					break
			except AttributeError:
				continue

		# Return a three-tuple of variables + cuts info and the shouldDrop flag.
		return variables, cuts, shouldDrop

	def resetPlugins(self, variables):
		for plugin in self.plugins:
			variables = plugin.reset(variables)
		return variables

