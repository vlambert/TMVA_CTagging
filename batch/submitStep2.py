#!/usr/bin/env python


import commands
import re
import os
import FWCore.ParameterSet.Config as cms

import sys
sys.path.append('./')

from math import ceil
from tmva_training  import training_vars_float, training_vars_int, train, read,  readParallel

#outdir = '/scratch/leac/'

def processAllBatch(jobName, option, variables):

    cmsswpath = "/shome/vlambert/cmssw/CMSSW_5_3_3_patch2";
    jodir = "CTagging/AlternativeWeighting/Phys14AOD_13TeV_SoftLepton/Final/NewVariables/B"

    inDirName = "dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/vlambert/TMVA/CSVSLctag_73X/TTJets"

    #python job options
    pyName = 'run_'+jobName+'.py'
    fpy = open(pyName,'w')
    fpy.write('import os\n')
    fpy.write('import sys\n')
    fpy.write('from tmva_training  import train, read,  readParallel\n\n')
    fpy.write('bdtoptions ='+option+'\n\n')
    fpy.write('extravars = '+variables+'\n\n')
    fpy.write('train(bdtoptions, extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVNoVertexNoSoftLepton_B.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVNoVertexNoSoftLepton_C.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVNoVertexNoSoftLepton_DUSG.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVPseudoVertexNoSoftLepton_B.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVPseudoVertexNoSoftLepton_C.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVPseudoVertexNoSoftLepton_DUSG.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVRecoVertexNoSoftLepton_B.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVRecoVertexNoSoftLepton_C.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVRecoVertexNoSoftLepton_DUSG.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVNoVertexSoftMuon_B.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVNoVertexSoftMuon_C.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVNoVertexSoftMuon_DUSG.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVPseudoVertexSoftMuon_B.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVPseudoVertexSoftMuon_C.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVPseudoVertexSoftMuon_DUSG.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVRecoVertexSoftMuon_B.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVRecoVertexSoftMuon_C.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVRecoVertexSoftMuon_DUSG.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVNoVertexSoftElectron_B.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVNoVertexSoftElectron_C.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVNoVertexSoftElectron_DUSG.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVPseudoVertexSoftElectron_B.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVPseudoVertexSoftElectron_C.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVPseudoVertexSoftElectron_DUSG.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVRecoVertexSoftElectron_B.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVRecoVertexSoftElectron_C.root", extravars)\n')
    fpy.write('read("'+inDirName+'","CombinedSVRecoVertexSoftElectron_DUSG.root", extravars)\n')
    fpy.close()


    #bash script    
    scriptName = 'submit_'+jobName+'.sh'
    f = open(scriptName,'w')
    f.write('#!/bin/bash\n\n')
    f.write('OUTFILES="myout.txt myerr.txt weights/TMVAClassification_BDTG.weights.xml weights/TMVAClassification_BDTG.class.C TMVA_classification.root trainPlusBDTG_CombinedSVNoVertexNoSoftLepton_B.root trainPlusBDTG_CombinedSVNoVertexNoSoftLepton_C.root trainPlusBDTG_CombinedSVNoVertexNoSoftLepton_DUSG.root trainPlusBDTG_CombinedSVPseudoVertexNoSoftLepton_B.root trainPlusBDTG_CombinedSVPseudoVertexNoSoftLepton_C.root trainPlusBDTG_CombinedSVPseudoVertexNoSoftLepton_DUSG.root trainPlusBDTG_CombinedSVRecoVertexNoSoftLepton_B.root trainPlusBDTG_CombinedSVRecoVertexNoSoftLepton_C.root trainPlusBDTG_CombinedSVRecoVertexNoSoftLepton_DUSG.root trainPlusBDTG_CombinedSVNoVertexSoftMuon_B.root trainPlusBDTG_CombinedSVNoVertexSoftMuon_C.root trainPlusBDTG_CombinedSVNoVertexSoftMuon_DUSG.root trainPlusBDTG_CombinedSVPseudoVertexSoftMuon_B.root trainPlusBDTG_CombinedSVPseudoVertexSoftMuon_C.root trainPlusBDTG_CombinedSVPseudoVertexSoftMuon_DUSG.root trainPlusBDTG_CombinedSVRecoVertexSoftMuon_B.root trainPlusBDTG_CombinedSVRecoVertexSoftMuon_C.root trainPlusBDTG_CombinedSVRecoVertexSoftMuon_DUSG.root trainPlusBDTG_CombinedSVNoVertexSoftElectron_B.root trainPlusBDTG_CombinedSVNoVertexSoftElectron_C.root trainPlusBDTG_CombinedSVNoVertexSoftElectron_DUSG.root trainPlusBDTG_CombinedSVPseudoVertexSoftElectron_B.root trainPlusBDTG_CombinedSVPseudoVertexSoftElectron_C.root trainPlusBDTG_CombinedSVPseudoVertexSoftElectron_DUSG.root trainPlusBDTG_CombinedSVRecoVertexSoftElectron_B.root trainPlusBDTG_CombinedSVRecoVertexSoftElectron_C.root trainPlusBDTG_CombinedSVRecoVertexSoftElectron_DUSG.root"\n')
    f.write('TOPWORKDIR=/scratch/`whoami`\n')
    f.write('JOBDIR='+jobName+'\n')
    
    f.write('DATE_START=`date +%s`\n')
    f.write('echo "Job started at " `date`\n')
    f.write('cat <<EOF\n')
    f.write('## QUEUEING SYSTEM SETTINGS:\n')
    f.write('HOME=$HOME\n')
    f.write('USER=$USER\n')
    f.write('JOB_ID=$JOB_ID\n')
    f.write('JOB_NAME=$JOB_NAME\n')
    f.write('HOSTNAME=$HOSTNAME\n')
    f.write('TASK_ID=$TASK_ID\n')
    f.write('QUEUE=$QUEUE\n')
    f.write('EOF\n')
    
    f.write('STARTDIR=`pwd`\n')
    f.write('WORKDIR=$TOPWORKDIR/$JOBDIR\n')
    f.write('RESULTDIR=$STARTDIR/$JOBDIR\n')

    f.write('if test -e "$WORKDIR"; then\n')
    f.write('   echo "ERROR: WORKDIR ($WORKDIR) already exists! Aborting..." >&2\n')
    f.write('   exit 1\n')
    f.write('fi\n')
    f.write('mkdir -p $WORKDIR\n')
    f.write('if test ! -d "$WORKDIR"; then\n')
    f.write('   echo "ERROR: Failed to create workdir ($WORKDIR)! Aborting..." >&2\n')
    f.write('   exit 1\n')
    f.write('fi\n')

    f.write('cd $WORKDIR\n')
    f.write('cat <<EOF\n')
    
    f.write('## JOB SETTINGS:\n')
    f.write('STARTDIR=$STARTDIR\n')
    f.write('WORKDIR=$WORKDIR\n')
    f.write('RESULTDIR=$RESULTDIR\n')
    f.write('EOF\n')
    
    f.write('CMSSW_DIR='+cmsswpath+'\n')
    f.write('CMSSW_CONFIG_FILE=$CMSSW_DIR/src/'+jodir+'/'+pyName+'\n')
    f.write('source $VO_CMS_SW_DIR/cmsset_default.sh\n')
    f.write('cd $CMSSW_DIR/src\n')
    #f.write('eval `scramv1 runtime -sh`\n')
    f.write('cd /swshare/ROOT/root_v5.34.18_slc5_amd64_py26_pythia6; export LD_LIBRARY_PATH=/swshare/ROOT/pythia6/pythia6:; source bin/thisroot.sh; cd -\n')
    f.write('cd $WORKDIR\n')
    
    f.write('python $CMSSW_CONFIG_FILE > myout.txt 2>myerr.txt\n')
    #f.write('ls -l >myout.txt \n')
    f.write('cd $WORKDIR\n')
    f.write('if test x"$OUTFILES" != x; then\n')
    f.write('   mkdir -p $RESULTDIR\n')
    f.write('   mkdir -p $RESULTDIR/weights\n')
    f.write('   for n in $OUTFILES; do\n')
    f.write('       if test ! -e $WORKDIR/$n; then\n')
    f.write('          echo "WARNING: Cannot find output file $WORKDIR/$n. Ignoring it" >&2\n')
    f.write('       else\n')
    f.write('          cp -a $WORKDIR/$n $RESULTDIR/$n\n')
    f.write('          if test $? -ne 0; then\n')
    f.write('             echo "ERROR: Failed to copy $WORKDIR/$n to $RESULTDIR/$n" >&2\n')
    f.write('          fi\n')
    f.write('   fi\n')
    f.write('   done\n')
    f.write('fi\n')
    f.write('rm -rf $WORKDIR\n')
    f.write('DATE_END=`date +%s`\n')
    f.write('RUNTIME=$((DATE_END-DATE_START))\n')
    f.write('echo "Job finished at " `date`\n')
    f.write('echo "Wallclock running time: $RUNTIME s"\n')
    f.write('exit 0\n')
    f.close()
                                                                                                                                        
    os.system('chmod +x '+scriptName)
    submitToQueue = 'qsub -V -cwd -l h_vmem=6G -q long.q -N '+jobName+" "+scriptName
    print submitToQueue
    os.system(submitToQueue)



###########################################################################
###########################################################################

## Define jobs to be performed with Directory name, BDT options, and additional training variables

processAllBatch("BDefault", '[ "!H","!V","NTrees=1000","MinNodeSize=1.5%","BoostType=Grad","Shrinkage=0.10","UseBaggedGrad","GradBaggingFraction=0.5","nCuts=80","MaxDepth=2",]', '["trackSip2dSigAboveCharm_0", "trackSip3dSigAboveCharm_0","trackSip2dValAboveCharm_0", "trackSip3dValAboveCharm_0"]')

processAllBatch("BAll1", '[ "!H","!V","NTrees=1000","MinNodeSize=1.5%","BoostType=Grad","Shrinkage=0.10","UseBaggedGrad","GradBaggingFraction=0.5","nCuts=80","MaxDepth=2",]', '["jetChargePt1", "VertexChargePt1", "trackSip2dSigAboveQuarterCharm_0", "trackSip3dSigAboveQuarterCharm_0"]')

