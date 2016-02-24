"""
Code to retrieve a list of leaves in a given ttree.
TTree equivalent to labels.py
Based off of treeviewer code: https://github.com/TC01/rootscripts/blob/master/treeviewer
"""

import os
import sys

import ROOT

def getTreeLeaves(tree):
	leafDict = {}
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
		nextKey.Print()
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
	for leaf in leaves.iterkeys():
		leaves[leaf] = eval("tree." + leaf)