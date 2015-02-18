"""
Implementation of a cuts class.
"""

class Cut:

	def __init__(self, name, description):
		self.name = name
		self.description = description

		self.passed = 0
		self.index = -1

	def __str__(self):
		return "Cut " + name + " at index " + index + ": " + description

	def __repr__(self):
		return self.__str()
