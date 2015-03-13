# TMVA_CTagging
This directory includes the code for the development of the CMS TMVA ctagger_v1. Below are instructions for preparing and running the training.


Training Samples
We will begin by assuming our ntuples are flat trees in flavour and category from the JetTagMVAExtractor or BTagAnalyzer, one level up from the original AOD/RECO files. The tree files will look like CombinedSVV2NoVertex_DUSG.root with the tree name CombinedSVV2NoVertex.

Below are the subsequent steps for preparing the training samples for the TMVA:
1) The samples most likely need to be skimmed to not cause a memory allocation error for the TMVA training. One can first skim the samples, selecting 20,000 events in each pt/eta bin for each flavour/vertex root file, to ensure that there are enough events in each pt/eta bin for the training. This is performed by TrainingFilter.py.

2) Make the trees really flat without vectors and set variables that are not defined for a given vertex category to a default value. For this, run your ntuples through createNewTree.py which will produce sets of new flat ntuples split in event range such as CombinedSVV2NoVertex\_DUSG\_0\_249999.root with the shared tree name “tree”.
*For the training, one can either combine these ntuples with hadd or leave them as is for the rest of the processing.

3) Produce the category normalization weights for the training sample with normalizationQCD.C (BiasFiles or SLBiasFiles for soft-lepton category) and save the output to a text such as QCD\_normweights.txt. These will be added as a weight branch “weight_norm” which flattens the vertex category distribution for the training sample.

4) Assuming the evaluation sample vertex category weights have been produced (look at procedures for Evaluation Samples, step 3), add the normalization and category weight branches to the flat ntuples with addWeightBranch.py. The combination of these weights will remove the training sample vertex category information and match it with that of the evaluation sample.

5) Create 2D Pt/Eta Histograms for the weighted ntuples with createEtaPtWeightHists.py (make sure “weight\_norm*weight_category” are set for the weight in Draw() for the histograms). There will be 12 histograms created, 9 for the individual flavour/category files and 3 combined histograms, one for each flavour.

6) Make the final weighted ntuples making sure that the new Pt/Eta histogram files are pointed to in addWeightBranch.py. There should be six new branches created:
-weight_etaPt : the Pt/Eta weight, specific for a flavour/category file (for category dedicated training)
-weight_etaPtInc: the Pt/Eta weight, inclusive for the flavour
-weight_category: the category weight from the evaluation sample
-weight_norm : the normalization weight from the training sample
-weight_flavour : the ratio of the flavour prevalences in the evaluation process
-weight : (weight\_etaPtInc) x (weight\_norm x weight\_category) x (weight\_flavour) – this can be used for combined trainings
The training samples are now ready for the training process with tmva_training.py. Make sure to create a directory called “weights” to save the output class and xml files from the training.

Evaluation Samples
1) Make the trees really flat without vectors and set variables that are not defined for a given vertex category to a default value. For this, run your ntuples through createNewTree.py which will produce sets of new flat ntuples split in event range such as CombinedSVV2NoVertex\_DUSG\_0\_249999.root with the shared tree name “tree”.

2) The evaluation trees can be skimmed as well to make the evaluation process faster. The script skimTT.py will reference the event ranges in the file names for the flat trees and copy new skimmed trees that contain 10% (this can easily be modified) of the events from each of the flavour/category files. The output will be one combined root file for each flavour/category such as CombinedSVV2NoVertex_DUSG.root.

*Remember not to use the same skimming process for the evaluation as done for the training since one wants to keep the physical vertex category distribution for the process in the evaluation.

3) Create the vertex category weights for the training samples with biasTTbar.C (BiasFiles or SLBiasFiles for soft-lepton categories) and save the output to a text file such as BiasDump.txt.
