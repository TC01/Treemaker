import imp
import os
import sys

# This plugin-loading code is stolen from myself, which is to say, I adapted
# an example in the Python imp documentation and then used it here:
# http://bitbucket.org/TC01/hex in an unrelated project.

plugins = []

def loadPlugins(toLoad, useAll=False):
	# Get a list of all possible plugin names
	location = os.path.join(getScriptLocation())
	names = []
	for path, dirs, files in os.walk(location):
		if path == location:
			for filename in files:
				if not (".pyc" in filename or "__init__" in filename):
					filename = filename[:-len(".py")]
					names.append(filename)
					
	# Now, use imp to load all the plugins we specified
	global plugins
	for name in names:
		if useAll or name in toLoad:
			print "*** Loading " + name
			try:
				test = sys.modules[name]
			except KeyError:
				fp, pathname, description = imp.find_module(name, __path__)
				try:
					plugin = imp.load_module(name, fp, pathname, description)
					plugins.append(plugin)
				finally:
					if not fp is None:
						fp.close()

def createCutsPlugins(cuts, isData):
	for plugin in plugins:
		cuts = plugin.createCuts(cuts, isData)
	return cuts

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
		cuts = plugin.applyCuts(event, variables, cuts, labels, isData)
	return cuts	

def resetPlugins(variables):
	for plugin in plugins:
		variables = plugin.reset(variables)
	return variables

## Helper functions.
	
def getScriptLocation():
	"""Helper function to get the location of a Python file."""
	location = os.path.abspath("./")
	if __file__.rfind("/") != -1:
		location = __file__[:__file__.rfind("/")]
	return location
