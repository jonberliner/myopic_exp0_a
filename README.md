- loadData.py is a script that downs the sql-stored data, converts to pandas dataframe, and cleans up quirks from data collection
- analysis0.py is treated like a runner script for analyses.
- jbfunctions contians:
    - jbload: functions that load data from across experiments into the same format for cross-comparison analysis
    - jbprep: prepping used in loadData
    - jbgp.pyx: cythonized gaussian process package
    - jbstats: functionalized routines that I seem to use a lot
    - jbsac: split-apply-combine routines
    - jbplot: plotting functions that take in dataframes and poop out pretty things
    - jbgp_fit.pyx: gp fitting routines
    - cythonize.sh: bash script that runs cythonSetup.py and builds in place
    - cythonSetup: cythonizes jbgp.pyx and jbgp_fit.pyx
