# Treemaker - Changelog

Changelogs, derived from git history, for versions of Treemaker after
the first official release, v1.0.

### Treemaker v1.2

* Added support for running over a TTree in a (collection of) ROOT files,
in addition to being able to run over ntuples. Plugins can now declare
an input_type variable; if set to Tree, they will only be allowed to run
over Trees. Treemaker can be put into Tree mode using the new ```[input]```
section in a config file; have a look at [the example](https://github.com/TC01/Treemaker/blob/master/Treemaker/data/example_tree.cfg).

* Added support for running via xrood, and for deriving the list of xrootd
files to run over via a DAS query. If ```directory``` in a config file is
an XRD path (```root://...```), it will be assumed to be a directory, and
Treemaker will try to run over all ROOT files in that directory. If a DAS
query is provided (in the form ```das://prod/master:/NAME/OF/DATASET```),
we will query DAS to get the list of files to run over.

* Deprecated the ```reset``` method; ```reset``` can still be used if
necessary to call cleanup code in your plugin, but it's no longer required.
Treemaker will now automatically reset all declared variables back to their
original state.

### Treemaker v1.1

* Rewrote ```treepruner``` tool to be faster, more efficient, and to output
status information.
* Implemented ```drop``` function in Treemaker plugins. ```drop``` runs over
every event and returns ```True``` if the event should not be saved in the
output tree.
* Deprecated the ```makeCuts``` method in plugins. The ```analyze``` method
should now return a tuple of cuts and tree variables and should take the
current state of the cuts array. This allows a variable in a later-priority
plugin to depend on a cut in a plugin that has already run.
* Minor bugfixes, improvements to documentation.
