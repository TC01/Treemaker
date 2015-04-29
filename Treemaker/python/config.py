"""
Configuration file loader.
"""

import ConfigParser

class TreemakerConfig:
	
	def __init__(self, parser, index=0):
		self.setup(parser, index)

	def setup(parser, index):
		configParser = ConfigParser.RawConfigParser()
		configParser.read(configFile)
		

def readConfiguration(configFile):
	"""	Reads the config file using condor 