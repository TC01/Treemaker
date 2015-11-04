# Treemaker - Changelog

Changelogs, derived from git history, for versions of Treemaker after
the first official release, v1.0.

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
