#!/usr/bin/env python

import os

os.system("treemaker -f /eos/uscms/store/user/bjr/ntuples/gstar/Gstar_Hadronic_1500GeV_2WM -l")

## Results for nonlinear:

"""
   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000   13.771   13.771 <string>:1(<module>)
        1    0.000    0.000   13.769   13.769 profileTest.py:3(<module>)
        1    0.001    0.001   13.771   13.771 {execfile}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1   13.769   13.769   13.769   13.769 {posix.system}
"""

## Results for linear:

"""
   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000  262.241  262.241 <string>:1(<module>)
        1    0.000    0.000  262.239  262.239 profileTest.py:3(<module>)
        1    0.001    0.001  262.241  262.241 {execfile}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1  262.239  262.239  262.239  262.239 {posix.system}

"""
