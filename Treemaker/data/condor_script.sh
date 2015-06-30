#!/bin/tcsh

source job_params

# First, create the output directory.
set OUTPUT_DIR=$1
set SPLIT_INDEX=$2
set ACTUAL_INDEX=$3
mkdir -p $OUTPUT_DIR

# Set up a fresh copy of the environment.
setenv HOME $_CONDOR_SCRATCH_DIR
scram project $CMSSW_RELEASE
cd $CMSSW_RELEASE
eval `scramv1 runtime -csh`
cd src
git clone https://github.com/TC01/Treemaker/
cp -r $_CONDOR_SCRATCH_DIR/plugins/* Treemaker/Treemaker/python/plugins/
scram build
cd $_CONDOR_SCRATCH_DIR

# Run the program here
$CMSSW_RELEASE/src/Treemaker/Treemaker/scripts/treemaker $ARGUMENTS $SPLIT_INDEX $ACTUAL_INDEX

# Output processing for return
cd $_CONDOR_SCRATCH_DIR
cd $OUTPUT_DIR
cp $_CONDOR_SCRATCH_DIR/*.root ./
cp $_CONDOR_SCRATCH_DIR/*.txt ./
