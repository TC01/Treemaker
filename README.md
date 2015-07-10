Treemaker v1.0
--------------

Treemaker is a generic, extensible piece of Python software for turning
[EDM Ntuples](https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideEDMNtuples)
into [ROOT](http://root.cern.ch/) ttrees, written by Ben Rosser as an
undergraduate member of the [CMS collaboration](http://cms.cern.ch/) at CERN.

The name is generic because I could not come up with a better one in a 
short amount of time, but also because it's appropriate. :)

Currently, all documentation is available in this file. Some might be moved
into a wiki on this git repository or to a github pages site as it grows
in size.

# Introduction:

There are many reasons why you might want to do turn your trees into ntuples.

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
not be written directly to a TTree. So the project was put on hold.

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

# Installation:

We recommend you install the last stable release of Treemaker, tagged
"stable".

Treemaker is currently packaged as a CMSSW module; that means you can install
it as follows into a release of the [CMSSW framework](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCMSSWFramework).

There is currently not support for installing Treemaker outside of the
CMSSW framework. In theory, this is entirely possible, but (for example)
a setup.py has not yet been written that could convert the CMSSW module
layout into a standard Python distutils module.

This documentation assumes you have already set up a release of the CMSSW framework, 
and ran the ```cmsenv``` command.
For instructions on how to do this on cmslpc, see 
[here](http://uscms.org/uscms_at_work/physics/computing/setup/setup_software.shtml).

Once you have done that, run the following commands below.

```
cd ${CMSSW_BASE}/src 
git clone http://github.com/TC01/Treemaker/
cd Treemaker && git checkout stable && cd ..
scram build
```

# Documentation:

Between Treemaker v0.2/v0.3 and v1.0, a lot of stuff changed and the amount
of documentation grew significantly. You can find the documentation in the
[wiki](https://github.com/TC01/Treemaker/wiki) on this repository.

Please consult that if you have any questions.

# Usage:

The general Treemaker workflow is something like this:

1. Write plugins and put them in ```Treemaker/python/plugins```. The
documentation has a thorough discussion of how to do this, along with the
examples in the repository.

2. Create a list of plugins, in the order you want them to run, and save it
to a file ```plugins.list```. (The name doesn't really matter).

3. Run the following command over the dataset you wish to convert.
If it is data, and not Monte Carlo, add the ```-d``` flag. This will
automatically generate a config file.

```
treemaker-config -p plugins.list /path/to/dataset/
```

4. Run the following command:

```
treemaker -f _name_of_config_file_
```

5. Enjoy your ttrees!

It can be slightly more complicated than that if you want to use job splitting
or condor or anything slightly fancier. Consult the documentation for more.

# Credits:

## Developers

* Ben Rosser <brosser3@jhu.edu>

## Contributors: Code

* Marc Osherson

## Contributors: Suggestions

* Dave Fehling
* Nick Eminizer
* Petar Maksimovic
