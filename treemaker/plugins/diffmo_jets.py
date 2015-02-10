import array

# TODO: turn this back into a knob somewhere.
numJets = 4

class Jet:

	def __init__(self, number, data):
		self.number = number
		self.data = data

		self.jetName = "jet" + str(number)
		
		self.initVars()

	def setup(self, variables):
		"""Initializes branch arrays for all jet variables. Returns a copy of the
		variables dictionary."""
		variables[self.jetName + 'pt'] = array.array('f', [-1.0])
		variables[self.jetName + 'mass'] = array.array('f', [-1.0])
		variables[self.jetName + 'eta'] = array.array('f', [100.0])
		variables[self.jetName + 'phi'] = array.array('f', [100.0])
		return variables

	def analyze(self, variables, labels):
		"""Runs the treemaking step. Labels is a dictionary containing already-
		loaded handles."""
		# Do the analysis step.
		jetCollection = 'PrunedCA8'
		if not self.data:
			jetCollection += "CORR"
		jetHandle = labels['diffmoca8pp']['PrunedCA8']
		fourVector = jetHandle.product()
		try:
			self.mass = fourVector[self.number - 1].M()
			self.eta = fourVector[self.number - 1].Eta()
			self.phi = fourVector[self.number - 1].Phi()
			self.pt = fourVector[self.number - 1].Pt()
		except:
			# If this fails, set all variables to defaults.
			self.initVars()

		variables = self.update(variables)
		return variables

	def reset(self, variables):
		"""Resets the jet variables and returns an updated copy of the variable
		array dictionary."""
		self.initVars()
		return self.update(variables)

	def update(self, variables):
		"""Updates the actual arrays, returns an updated copy of the variable
		dictionary."""
		variables[self.jetName + 'mass'][0] = self.mass
		variables[self.jetName + 'eta'][0] = self.eta
		variables[self.jetName + 'phi'][0] = self.phi
		variables[self.jetName + 'pt'][0] = self.pt
		return variables

	def initVars(self):
		"""Initializes the jet variables to default values."""
		self.mass = -1.0
		self.pt = -1.0
		self.eta = 100
		self.phi = 100
		self.csv = 0.0
		self.tau32 = 1.0
		self.tau21 = 1.0

jets = []
		
def setup(variables, isData):
	global jets
	for i in xrange(numJets):
		jets.append(Jet(i + 1, isData))
		variables = jets[i].setup(variables)
	return variables
	
def analyze(variables, labels, isData):
	for jet in jets:
		variables = jet.analyze(variables, labels)
	return variables
	
def reset(variables):
	for jet in jets:
		variables = jet.reset(variables)
	return variables
