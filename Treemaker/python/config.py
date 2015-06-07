"""
Configuration file loader.
"""

import ConfigParser
import os
import sys

# Used so trees from multiple versions do not get hadd'd together.
version = "0.3"

defaultFileName = ''
defaultTreeName = "tree-" + version

class TreemakerConfig:
	
	def __init__(self, configFileName):
		self.configFileName = configFileName
		self.setup(configFileName)

		# Command line options.
		self.force = False
		self.linear = False
		self.splitIndex = -1

	def parseOption(self, configParser, section, option, default, type=None):
		result = default
		try:
			if type == "int":
				result = configParser.getint(section, option)
			elif type == "bool":
				result = configParser.getboolean(section, option)
			else:
				result = configParser.get(section, option)
		except ConfigParser.NoOptionError:
			pass
		if type != "int" and type != "bool" and result.lstrip().rstrip() == "":
			result = default
		return result

	def setup(self, configFile):
		configParser = ConfigParser.RawConfigParser()
		configParser.optionxform = str
		configParser.read(configFile)

		# Parse the directory option.
		try:
			self.directory = configParser.get('dataset', 'directory')
			self.directory = os.path.abspath(os.path.expanduser(self.directory))
			if not os.path.exists(self.directory):
				print "Error: directory '" + directory + "' does not exist!"
				raise RuntimeError
		except:
			print "Error: Invalid option for 'directory' in config file."
		
		# Parse remaining options, using the wrapper method.
		self.isData = self.parseOption(configParser, 'dataset', 'is_data', False, 'bool')
		self.fileName = self.parseOption(configParser, 'dataset', 'output_file_name', defaultFileName)
		self.treeName = self.parseOption(configParser, 'dataset', 'output_tree_name', defaultTreeName)
		
		# Parse the splitting options.
		self.splitInto = self.parseOption(configParser, 'splitting', 'split_into', -1, 'int')
		self.splitBy = self.parseOption(configParser, 'splitting', 'split_by', -1, 'int')
		if self.splitBy != -1 and self.splitInto != -1:
			print "Error: cannot set both split_into and split_by at the same time."
		
		self.readPlugins(configParser)
	
	def readPlugins(self, configParser):
		self.plugins = {}
		try:
			for name, value in configParser.items('plugins'):
				integer = configParser.getint('plugins', name)
				if integer > 0:
					self.pluginNames[name] = integer
		except ConfigParser.NoSectionError:
			print "Error: Config file must have a 'plugins' section!"

def writeConfigFile(dataset, opts):
	configParser = ConfigParser.RawConfigParser()
	configParser.optionxform = str

	configParser.add_section('dataset')
	configParser.set('dataset', 'directory', dataset)
	configParser.set('dataset', 'is_data', str(opts.data))
	configParser.set('dataset', 'output_file_name', opts.name)
	configParser.set('dataset', 'output_tree_name', opts.treename)

	configParser.add_section('splitting')
	if opts.splitInto > 0 and opts.splitBy > 0:
		print "Error: cannot set both --split-into and --split-by to be nonnegative!"
		print "Treemaker will not know which setting to respect."
		sys.exit(1)
	configParser.set('splitting', 'split_into', opts.splitInto)
	configParser.set('splitting', 'split_by', opts.splitBy)
	
	configParser.add_section('plugins')
	pluginList = loadPluginList(opts.pluginList)
	for plugin in pluginList:
		configParser.set('plugins', plugin, 'True')

	# Write the config parser object to a file.
	outputName = opts.outputName
	if outputName == "":
		outputName = dataset.rpartition("/")[2]
	outputName += '.cfg'
	with open(outputName, 'wb') as outputFile:
		configParser.write(outputFile)

def loadPluginList(filename):
	pluginNames = []
	try:
		if filename == "":
			raise RuntimeError
		with open(filename) as pluginFile:
			for line in pluginFile:
				line = line.rstrip('\n')
				if not line.lstrip().rstrip() == "" and not line[0] == "#":
					pluginNames.append(line)
	except:
		print "Error reading from plugin list file, or no plugin list file passed."
		print "Running treemaker-config without specifying a plugin list is probably not what you want!"
		print "The generated config files will not have plugins. Please rerun with -p [plugin-list]."
		sys.exit(1)
	return pluginNames
