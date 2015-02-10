Treemaker v0.1: 
An extensible Ntuple -> ROOT TTree maker.
Ben Rosser <brosser3@jhu.edu>
-----------------------------

TODO: write a lot more documentation.

Writing Plugins:
----------------

To write a plugin, create a new Python file and land it in: plugins/.
The file needs to implement three methods:

```
def setup(variables, isData):
	pass

def analyze(variables, labels, isData):
	pass

def reset(variables):
	pass

```

Here, ```variables``` and ```labels``` are both dictionaries.

(TODO: finish this documentation).

Take a look at the plugins that I am shipping for more information.
