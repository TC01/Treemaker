"""
Code to retrieve a list of labels in a given ntuple, using edmDumpEventContent.
"""

import subprocess

from DataFormats.FWLite import Events, Handle

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
		labels[module] = {}

	# Fill the dictionary tree with the labels and handles.
	for line in lines:
		handleType = line[0]
		module = line[1]
		label = line[2]
		handle = Handle(handleType)
		labels[module][label] = handle

	return labels	


def fillLabels(event, labels):
	for module, subdict in labels.iteritems():
		for label, handle in subdict.iteritems():
			cmsLabel = (module, label)
			event.getByLabel(cmsLabel, handle)
	return labels

# testing code:
# print getLabels("/eos/uscms/store/user/bjr/ntuples/gstar/Gstar_Hadronic_1500GeV_2WM/diffmo_v4_111_1_bZA.root")
