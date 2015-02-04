"""
Code to retrieve a list of labels in a given ntuple, using edmDumpEventContent.
"""

import subprocess

from DataFormats.FWLite import Events, Handle

def getModules(lineArray):
	

def getLabels(ntuple):
	process = subprocess.Popen(["edmDumpEventContent", ntuple], stdout=subprocess.PIPE)
	output = process.communicate()[0]
	firstLine = False
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

	modules = getModules(lineArray)
	labels = {}
	

# testing code:
getLabels("/eos/uscms/store/user/bjr/ntuples/gstar/Gstar_Hadronic_1500GeV_2WM/diffmo_v4_111_1_bZA.root")
