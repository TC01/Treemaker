#!/bin/tcsh

set CMSSW_RELEASE=$1
set OUTPUT_DIR=$2
set TREE_NAME=$3
set FILE_DIR=$4
set DATA_OPT=$5
set DATA_ARG=$6

# Do this first.
mkdir -p $OUTPUT_DIR

# This should all be replaced with the script to set up our environment.
# Sadly, it has not been, because it didn't work for some reason
setenv HOME $_CONDOR_SCRATCH_DIR
setenv SCRAM_ARCH `scramv1 arch`
cd $CMSSW_RELEASE
eval `scramv1 runtime -csh`
cd $_CONDOR_SCRATCH_DIR

# Run the program here
python run_treemaker.py --name $TREE_NAME --files $FILE_DIR $DATA_OPT $DATA_ARG

# Output processing for return
cd $_CONDOR_SCRATCH_DIR
cd $OUTPUT_DIR
cp $_CONDOR_SCRATCH_DIR/*.root ./
