import imp
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

def loadPlugins(pluginNames, parameters):
	global plugins
	
	# Get a list of all possible plugin names
	names = getPossiblePluginNames(pluginNames.keys())
	pluginDict = {}

	# Now, use imp to load all the plugins we specified
	for name in names:
		try:
			test = sys.modules[name]
			print "*** Error: a module with the name " + name + " was already loaded!"
			sys.exit(1)
		except KeyError:
			fp, pathname, description = imp.find_module(name, __path__)
			try:
				plugin = imp.load_module(name, fp, pathname, description)
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
		print "*** Loading " + pluginOrder[i]
		plugins[i] = pluginDict[pluginOrder[i]]

	# If we choose to implement plugin dependencies, that should now be done.

	# Deal with unloaded plugins.
	# This should be a failure conditional.
	if len(pluginNames) != len(plugins):
		for name in pluginNames.keys():
			if not name in pluginDict.keys():
				print "ERROR: unable to load plugin " + name
		sys.exit(1)

	# Then return plugins, just in case.
	return plugins

def createCutsPlugins(cutArray):
	for plugin in plugins:
		cutArray = plugin.createCuts(cutArray)
	return cutArray

def setupPlugins(variables, isData):
	for plugin in plugins:
		variables = plugin.setup(variables, isData)
	return variables

def analyzePlugins(event, variables, labels, isData):
	for plugin in plugins:
		variables = plugin.analyze(event, variables, labels, isData)
	return variables

def makeCutsPlugins(event, variables, cuts, labels, isData):
	for plugin in plugins:
		cuts = plugin.makeCuts(event, variables, cuts, labels, isData)
	return cuts	

def resetPlugins(variables):
	for plugin in plugins:
		variables = plugin.reset(variables)
	return variables
