"""
Code to retrieve a list of labels in a given ntuple, using edmDumpEventContent.
"""

import subprocess

from DataFormats.FWLite import Events, Handle

# Label sub-dictionary, subclass of actual dict. Does lazy loading!
class LabelSubDict(dict):
	
	def __init__(self, *args, **kwargs):
		dict.__init__(self, *args, **kwargs)
		self.labelTypes = {}
		self.event = None
		self.filledMap = {}

	def __getitem__(self, key):
		value = dict.__getitem__(self, key)
		handleType = self.labelTypes[key][0]
		cmsLabel = self.labelTypes[key][1]

		# Implement lazy loading; if this is empty, fill it.
		if value == -1:
			value = Handle(handleType)
			dict.__setitem__(self, key, value)
			
		# Fill the label when requested.
		if self.event is not None and not self.filledMap[key]:
			self.event.getByLabel(cmsLabel, value)
			self.filledMap[key] = True

		return value

def getLabels(ntuple):
	# Run edmpDumpEventContent using subprocess.
	process = subprocess.Popen(["edmDumpEventContent", ntuple], stdout=subprocess.PIPE)
	output = process.communicate()[0]
	firstLine = False
	modules = []
	lines = []

	# Iterate over the output, create some data structures.
	for line in output.split("\n"):
		lineArray = line.split("   ")
		if not firstLine:
			firstLine = True
			continue
		if len(lineArray) <= 1:
			continue
		while '' in lineArray:
			lineArray.remove('')
		for i in xrange(len(lineArray)):
			lineArray[i] = lineArray[i].lstrip().rstrip()
			lineArray[i] = lineArray[i].lstrip('"').rstrip('"')

		lines.append(lineArray)
		if not lineArray[1] in modules:
			modules.append(lineArray[1])

	# Set up the dictionary tree with the module names.
	labels = {}
	for module in modules:
		labels[module] = LabelSubDict()

	# Fill the dictionary tree with the labels and handles.
	for line in lines:
		handleType = line[0]
		module = line[1]
		label = line[2]
#		handle = Handle(handleType)
		labels[module].labelTypes[label] = (handleType, (module, label))
		labels[module][label] = -1

	return labels	


def fillLabels(event, labels):
	for module, labelDict in labels.iteritems():
		labelDict.event = event
		for label, handle in labelDict.iteritems():
			labelDict.filledMap[label] = False
		#	cmsLabel = (module, label)
		#	event.getByLabel(cmsLabel, handle)
	return labels

# testing code:
# print getLabels("/eos/uscms/store/user/bjr/ntuples/gstar/Gstar_Hadronic_1500GeV_2WM/diffmo_v4_111_1_bZA.root")
