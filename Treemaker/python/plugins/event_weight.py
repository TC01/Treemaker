import array

# Event weights, this is a pretty simple example of the 'parameters' magic.

from Treemaker.Treemaker import cuts

# Plugins don't need to declare their type if they run over an ntuple, but
# this one will as an example!

input_type = "Ntuple"

def setup(variables, isData):
	variables['weight'] = array.array('f', [1.0])
	return variables

def analyze(event, variables, labels, isData, cutArray):
	# load the weight specified in the config file, if there is one.
	try:
		variables['weight'][0] = float(parameters['weight'])
	except:
		pass
	return variables, cutArray

def createCuts(cutArray):
	return cutArray

