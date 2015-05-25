#!/bin/tcsh

source job_params

# First, create the output directory.
set OUTPUT_DIR=$1
mkdir -p $OUTPUT_DIR

# This should all be replaced with the script to set up our environment.
# Sadly, it has not been, because it didn't work for some reason
setenv HOME $_CONDOR_SCRATCH_DIR
setenv SCRAM_ARCH `scramv1 arch`
cd $CMSSW_RELEASE
eval `scramv1 runtime -csh`
cd src && scram build
cd $_CONDOR_SCRATCH_DIR

# Run the program here
$CMSSW_RELEASE/src/Treemaker/Treemaker/scripts/treemaker $ARGUMENTS

# Output processing for return
cd $_CONDOR_SCRATCH_DIR
cd $OUTPUT_DIR
cp $_CONDOR_SCRATCH_DIR/*.root ./
