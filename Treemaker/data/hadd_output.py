#!/usr/bin/env python

import os
import shutil
import sys

def main():

	# Occasionally I am a bad programmer too; maybe fix this someday in the future.
	warning = "Warning! This script is only meant to be ran inside the working directory "
	warning += "of a condor job created by Treemaker! (https://github.com/TC01/Treemaker)"
	print warning

	outputFiles = []
	for path, dir, files in os.walk(os.getcwd()):
		if "output_" in path:
			for filename in files:
				if ".root" in filename:
					outputFiles.append(os.path.join(path, filename))

	outputPath = os.getcwd()	
	if len(outputFiles) == 1:
		shutil.move(outputFiles[0], outputPath)
	elif len(outputFiles) == 0:
		print "Error: no ROOT files in output directories, please check the logs/"
		sys.exit(1)
	else:
		# Job splitting always begins with IndexX.
		outputName = outputFiles[0].split("/")[-1][len("Index0_"):]
		os.system("hadd " + outputName + " output_*/*.root")

	# Clean up and remove the output_* directories.
	toRemove = []
	for path, dir, files in os.walk(os.getcwd()):
		if "output_" in path:
			toRemove.append(path)
	for removing in toRemove:
		shutil.rmtree(removing)

if __name__ == '__main__':
	main()
