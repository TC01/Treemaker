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

def writeCutsReport(runner, name = None):
	"""	Helper method to write out a 'cut report' of the indexes and names of
		the cuts. If no name is given, writes to standard output."""

	# We can rely on the ordering here to make things be the same order.
	cutArray = {}
	cuts = runner.createCutsPlugins(cutArray)
	ordered = sorted(cuts)
	for i in xrange(len(ordered)):
		cutName = ordered[i]
		cuts[cutName].index = i
	
	if name is None:
		for cutName, cut in cuts.iteritems():
			print cut
	else:
		reportName = name.partition(".")[0] + "_cuts_report.txt"
		with open(reportName, 'wb') as report:
			for cutName, cut in cuts.iteritems():
				report.write(str(cut) + "\n")
