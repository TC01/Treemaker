"""
Code to retrieve a list of leaves in a given ttree.
TTree equivalent to labels.py
Based off of treeviewer code: https://github.com/TC01/rootscripts/blob/master/treeviewer
"""

import os
import sys

import ROOT

# Leaf sub-dictionary, subclass of actual dict. Does lazy loading!
# Based on the LabelSubDict. I didn't think we'd need this but maybe we do.
class LeafSubDict(dict):
	
	def __init__(self, *args, **kwargs):
		dict.__init__(self, *args, **kwargs)
		self.tree = None

	def __getitem__(self, key):
		value = dict.__getitem__(self, key)

		# Implement lazy loading; if this is empty, fill it.
		if value == None and self.tree is not None:
			exec("value = self.tree." + key)
			dict.__setitem__(self, key, value)

		return value

def getTreeLeaves(tree):
	leafDict = LeafSubDict()
	leaves = tree.GetListOfLeaves()
	for leaf in leaves:
		leafDict[leaf.GetName()] = None
	return leafDict

def parseKeyList(tObject, keys, leaves, pathName=''):
	iterator = ROOT.TListIter(keys)
	nextKey = iterator.Next()
	while not nextKey is None and nextKey != None:
		keyName = nextKey.GetName()
		newName = os.path.join(pathName, keyName)
		try:
			newObject = tObject.Get(keyName)
			if isinstance(newObject, ROOT.TTree):
				subLeaves = getTreeLeaves(newObject)
				leaves[newName] = subLeaves
			elif isinstance(newObject, ROOT.TDirectoryFile):
				leaves = parseKeyList(newObject, newObject.GetListOfKeys(), leaves, newName)
		except:
			pass
		nextKey = iterator.Next()
	return leaves

def getLeaves(rootFile):
	"""	Given the path to a ROOT file, this returns a dictionary
		(with all values initialized to zero formatted as follows:
			leaves[tree][leaf] = None
	"""
	leaves = {}
	try:
		tFile = ROOT.TFile(os.path.abspath(rootFile))
		keys = tFile.GetListOfKeys()
		leaves = parseKeyList(tFile, keys, leaves)
		tFile.Close()
	except IndexError:
		print "Error: invalid ROOT file specified!"
	except IOError:
		print "Error: invalid ROOT file specified!"
	return leaves

# PLEASE NOTE:
# getLeaves returns leaves[tree][leaf].
# fillLeaves takes the dictionary tree[leaf], *not* the full leaves dictionary.

def fillLeaves(tree, leaves, index):
	"""	Given a tree, fill it and fill the leaves (sub)dictionary."""
	tree.GetEntry(index)
	leaves.tree = tree
	for leaf in leaves.iterkeys():
		# Actually, do lazy loading.
		leaves[leaf] = None
	return leaves