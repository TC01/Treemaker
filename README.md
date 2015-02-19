Treemaker v0.2
--------------

This Treemaker (named generically, because A. it is fairly generic and
extremely extensible, and B. because I couldn't come up with a good name)
is designed to take EDM Ntuples containing events used
in analyses as part of CERN's [CMS collaboration](http://cms.cern.ch/) and 
turn them into [ROOT](http://root.cern.ch/) ttrees.

There are many reasons why you might want to do this:

* TTrees will generally be much smaller than ntuples, so they can be processed
on machines other than large clusters, like your personal laptop.
* A vanilla ROOT installation is capable of reading in TTrees, whereas to read
Ntuples you need the [CMS analysis framework](http://github.com/cms-sw/cmssw/).
* TTrees can be looped over *faster* than Ntuples, in that the software for
reading them is more efficient.
* Using a TTree maker allows you to extract only what you need for your 
particular analysis and leave other unnecessary data behind.

Many people have written treemakers, of course. However, most of the ones I've
seen have tended to work in the same way:

* They declare a long list of variables that will be read in from the ntuple.
* They write a really long method that runs on every event that creates new
variables to be written to a ttree.

I found this hardcoding distasteful, and so back in the summer of 2013 I
attempted to write a generic Ntuple -> TTree converter. And it worked! It 
programmatically derived the contents of an Ntuple and managed to figure out
the right way to write them to a TTree... except, unfortunately, for those
objects in an Ntuple that are part of the CMSSW framework and therefore could
not be written directly to a TTree.

So the project was put on hold.

After a year and a half of other work, I was asked to write another treemaker,
but we discussed the possibilities of implementing something more generic like
my original 2013 project. I was now, however, experienced enough to realize
that there was a better way to do this; and hence, Treemaker was born.

Treemaker is not perfectly *generic*, but it is *extensible*. By default,
all Treemaker does is reads in all the variables of an ntuple, and on every
event passes a copy of those variables to a list of plugins. Those plugins can
then choose to define new tree variables and fill them however they like.

The actual, ugly part-- having to deal with ROOT and FWLite and Ntuples and
Handles have, for the most part, been dealt with already by me in the core of
the Treemaker. That core is also responsible for opening all of the ntuples
(we use the Python multiprocessing module, which causes things to run about an
order of magnitude faster than they would when processing some ~250 files on
a 24-core machine) and setting up the event loop.

You are encouraged to submit any plugins you write upstream to this repository.

The Future:
-----------

See the Issues tracker for more info.

There are some things that could use some work, definitely. The treemaker
could, for example, put the cut report that it generates inside the ROOT
file rather than as a plaintext file.

More exposed control for plugins from the configuration file might be nice;
for example, allowing them to expose knobs rather than just "yes, run this"
or "no, do not run this".

I would also like to do some optimization of the way Handles are loaded
(to make it lazy instead of eager, thus causing significant speed
improvements), but we'll see if I ever actually get around to that.

Installation:
-------------

Treemaker is currently packaged as a CMSSW module; that means you can install
it as follows into a CMSSW release.

```
cd CMSSW_5_3_*\src
git clone http://github.com/TC01/Treemaker/
scram build
```

This will then install the ```treemaker``` command as a Python script
that you can run from any directory.

Run ```treemaker -h``` to get a sense of command line options.

Running:
--------

As we have discussed, the Treemaker is built around the concept of
plugins. Because we hope to hold a large number of plugins in this
repository, it would be bad if running the treemaker.

To solve this problem, as of Treemaker v0.2, configuration files
are now required. Config files are currently simple newline-delineated
files containing lists of plugins (there is an example config file
in this repository, under ```data/```. Only plugins listed in a config
file will be loaded and executed.

You must specify this file with the ```treemaker -c FILENAME``` option;
if you do not specify a config file, Treemaker will refuse to run.

Writing Plugins:
----------------

To write a plugin, create a new Python file and land it in: plugins/.
The file needs to implement five methods, here is an example:

```
import array

from Treemaker.Treemaker import cuts

def setup(variables, isData):
	variables['varname'] = array.array('f', [-1.0])
	return variables

def analyze(event, variables, labels, isData):
	handle = labels['module']['label']
	product = handle.product()
	# Product is likely a vector, so some more processing should happen here.
	variables['varname'][0] = product[0]
	return variables

def reset(variables):
	variables['varname'][0] = -1.0
	return variables

def createCuts(cutDict):
	cutDict['example'] = cuts.Cut('example', 'This is some example cut description').

def makeCuts(event, variables, cutDict, labels, isData):
	# This will always pass the cut, obviously we'd really do something
	# more interesting with the variables and labels dictionaries.
	cutDict['example'].passed = 1

```

Here, ```variables```, ```cutDict```,  and ```labels``` are all dictionaries.

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

Then, when the ```analyze()``` step runs, you can look up any handles you need
by their module and label names, do whatever processing you want, and then
fill the dictionary of variables and return a copy of it. The treemaker will
automatically call ```tree.Fill()``` after finishing calling all of these
methods.

```reset()``` is called after filling the ttree, to restore all arrays to their
default value.

The example code above would successfully add a single variable to a ttree, but
as you might expect, you can do much more complicated things in plugins. Take
a look at diffmo_jets.py for an example of a more complicated implementation
(that defines a Jet class and determines how many of them to keep).

The ```cuts``` functionality was added in version 0.2. Cuts are essentially
special variables that are stored in the resulting ttree as a single integer
array. This allows you to implement cuts you'll need later in your analysis
(for instance, such as triggers). When you then want to run an analysis,
you can quickly check if ```cuts[i]``` is 0 or 1 (or some other value) to
determine if the event passed whatever analysis was mapped to cut ```i```.

Because cuts are named, rather than numbered, a report file 
(```*_cuts_report.txt```) is generated after Treemaker finishes running with
a mapping between indices in the ```cuts``` array in the tree and the names
you will have given them in your plugins.

For more help, look at other plugins that are shipped in this repository or
contact me directly for more information.

Testing Plugins:
----------------

When debugging your code, please be sure to use the ```-l``` option. This
forces Treemaker to *not* use Python multiprocessing, which makes things
substantially slower. For unfortunate reasons, errors in your plugins
won't be printed to standard output if you run with multiprocessing; so
if you want to verify your ntuples are actually being processed, please
use the ```-l``` option.

Specifically; you will see the "started processing" message but never
a "finished processing" message. If you do not see the "finished" message,
that means an error is in your code somewhere, so please run with ```-l```
to debug.

There is currently a ticket open about these problems.

Credits:
--------

* Ben Rosser <brosser3@jhu.edu>
* Marc Osherson
* Petar Maksimovic
