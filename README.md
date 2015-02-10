Treemaker v0.1: 
An extensible Ntuple -> ROOT TTree maker.
Ben Rosser <brosser3@jhu.edu>
-----------------------------

TODO: write an introduction.

Writing Plugins:
----------------

To write a plugin, create a new Python file and land it in: plugins/.
The file needs to implement three methods, here is an example:

```
import array

def setup(variables, isData):
	variables['varname'] = array.array('f', [-1.0])
	return variables

def analyze(variables, labels, isData):
	handle = labels['module']['label']
	product = handle.product()
	# Product is likely a vector, so some more processing should happen here.
	variables['varname'][0] = product[0]
	return variables

def reset(variables):
	variables['varname'][0] = -1.0
	return variables

```

Here, ```variables``` and ```labels``` are both dictionaries.

The ```labels``` dictionary is produced by running ```edmDumpEventContent```
over the ntuples that are being converted. A 2D dictionary is then created;
a dictionary where the module names (ex: "diffmoca8pp") are keys for other
dictionaries, where the actual label names (ex: "PrunedCA8Jets") are keys
for Handle objects.

On every event, code is ran that automatically calls event.getByLabel() for
all labels in an ntuple, so you don't have to do this yourself. You can look
up the handles you need to do treemaking directly as seen above.

```variables``` is a dictionary mapping variable names to array objects. The
```setup()``` function is called in all plugins to create this dictionary;
TTree branches are then set up for each variable in that dictionary.

Then, when the ```analyze()``` step runs, 

```reset()``` is called after filling the ttree, to restore all arrays to their
default value.

The example code above would successfully add a single variable to a ttree, but
as you might expect, you can do much more complicated things in plugins. Take
a look at diffmo_jets.py for an example of a more complicated implementation
(that defines a Jet class and determines how many of them to keep).

For more help, look at other plugins that are shipped in this repository or
contact me directly for more information.
