"""
Configuration file loader.
"""

import ConfigParser
import os

# Used so trees from multiple versions do not get hadd'd together.
version = "0.3"

defaultFileName = ''
defaultConfigName = "tree-" + version

class TreemakerConfig:
	
	def __init__(self, configFileName):
		self.configFileName = configFileName
		self.setup(configFileName)

		# Command line options.
		self.force = False
		self.linear = False

	def parseOption(self, parser, section, option, default, type=None):
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
		return result

	def setup(self, parser, index):
		configParser = ConfigParser.RawConfigParser()
		configParser.read(configFile)

		# Parse the directory option.
		try:
			self.directory = configParser.get('dataset', 'directory')
			self.directory = os.path.abspath(os.path.expanduser(directory))
			if not os.path.exists(self.directory):
				print "Error: directory '" + directory + "' does not exist!"
				raise RuntimeError
		except:
			print "Error: Invalid option for 'directory' in config file."
		
		# Parse remaining options, using the wrapper method.
		self.isData = self.parseOption(configParser, 'dataset', 'is_data', False, 'bool')
		self.fileName = self.parseOption(configParser, 'dataset', 'output_file_name', defaultFileName)
		self.treeName = self.parseOption(configParser, 'dataset', 'output_tree_name', defaultFileName)
		
		# Parse the splitting options.
		self.splitInto = self.parseOption(configParser, 'dataset', 'split_into', None, 'int')
		self.splitBy = self.parseOption(configParser, 'dataset', 'split_by', None, 'int')
		if self.splitBy is not None and self.splitInto is not None:
			print "Error: cannot set both split_into and split_by at the same time."
		
		self.readPlugins(configParser)
	
	def readPlugins(self, configParser):
		self.pluginNames = []
		try:
			for name, value in configParser.items('plugins')
				if configParser.getboolean('plugins', name):
					self.pluginNames.append(name)
		except ConfigParser.NoSectionError:
			print "Error: Config file must have a 'plugins' section!"

def readConfiguration(configFile):
	"""	Reads the config file using configparser."""
	config = TreemakerConfig(configFile)
	return config