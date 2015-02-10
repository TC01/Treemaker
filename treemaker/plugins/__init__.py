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

def setupPlugins(vars):
	for plugin in plugins:
		vars = plugin.setup(vars)
	return vars

def analyzePlugins(vars, labels):
	for plugin in plugins:
		vars = plugin.analyze(vars, labels)
	return vars

def resetPlugins(vars):
	for plugin in plugins:
		vars = plugin.reset(vars)
	return vars
