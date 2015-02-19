"""
Implementation of a cuts class. This is a data-driven class
and doesn't actually need much code.
"""

class Cut:

	def __init__(self, name, description):
		self.name = name
		self.description = description

		self.passed = 0
		self.index = -1

	def __str__(self):
		return "Cut " + self.name + " at index " + str(self.index) + ": " + self.description

	def __repr__(self):
		return self.__str()
