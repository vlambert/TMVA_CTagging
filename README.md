# TMVA_CTagging
This directory includes the code for the development of the CMS TMVA ctagger_v1. Below are instructions for preparing and running the training.

#### Accessing from storage and filtering training sample:
The scripts for merging the original ntuples created by the VariableExtractor and skimming are located in the "Filters/" directory. One can merge the individual output ntuples from the storage element with `merge\_from\_storage.sh` . 

Now the ntuples are flat trees in flavour and category. The tree files will look like CombinedSVNoVertex_DUSG.root with the tree name CombinedSVNoVertex.

#### Below are the subsequent steps for preparing the training samples for the TMVA:
1) The training QCD samples most likely need to be skimmed to not cause a memory allocation error for the TMVA training. One can first skim the samples, selecting 20,000 events in each pt/eta bin for each flavour/vertex root file, to ensure that there are enough statistics in each pt/eta bin for the training. This is performed by `Filter.C` .

2) The evaluation ttbar trees can be skimmed as well to make the evaluation process faster. The script `Skimmer.C` will randomly select 10% of the events from each of the flavour/category files. The output will be one combined root file for each flavour/category such as CombinedSVNoVertex_DUSG.root.
*Remember not to use the same skimming process for the evaluation as done for the training since one wants to keep the physical vertex category distribution for the process in the evaluation.

##### Flat ntuples
3) Now make the vectorized trees really flat and set variables that are not defined for a given vertex category to a default value. For this, run your ntuples through `createNewTree.py` which will produce sets of new flat ntuples split in event range such as CombinedSVNoVertex\_DUSG\_0\_249999.root with the shared tree name “tree”.
** This is done for both the QCD training samples and the ttbar samples

##### Event Weights
4) Produce the category normalization weights for the training sample with `normalizationQCD.C` (BiasFiles or SLBiasFiles for soft-lepton category) and save the output to a text such as QCD\_normweights.txt. These will be added as a weight branch “weight_norm” which flattens the vertex category distribution for the training sample.

5) Create the vertex category weights from ttbar for the training samples with `biasTTbar.C` (BiasFiles or SLBiasFiles for soft-lepton categories) and save the output to a text file such as BiasDump.txt.

6) Create initial 2D Pt/Eta Histogram for the flat and skimmed QCD ntuples with `createEtaPtWeightHists.py` (make sure “weight\_norm*weight_category” are set for the weight in Draw() for the histograms). There will be 12 histograms created, 9 for the individual flavour/category files and 3 combined histograms, one for each flavour. Make sure you used the lines marked 
'# category-specific'

7) Add the normalization and category weight branches to the flat ntuples with `addWeightBranch.py`. The combination of these weights will remove the training sample vertex category information and match it with that of the evaluation sample. You will also need to specify the histogram directory from step 6 to add the pt/eta weights. 

8) Create weighted 2D Pt/Eta Histograms for the weighted ntuples with `createEtaPtWeightHists.py` again but exchange the lines marked '#category -specific' with '#category - inclusive' and use the weighted ntuples from step 7.

9) Make the final weighted ntuples making sure that the new Pt/Eta histogram files are pointed to in `addWeightBranch.py`. There should be six new branches created:
-weight_etaPt : the Pt/Eta weight, specific for a flavour/category file (for category dedicated training)
-weight_etaPtInc: the Pt/Eta weight, inclusive for the flavour
-weight_category: the category weight from the evaluation sample
-weight_norm : the normalization weight from the training sample
-weight_flavour : the ratio of the flavour prevalences in the evaluation process
-weight : (weight\_etaPtInc) x (weight\_norm x weight\_category) x (weight\_flavour) – this can be used for combined trainings

* Note that you will need two histogram directories :
  - combhistoDirName should point to the weighted histograms made in step 8
  - histoDirName should point to the initial unweighted histograms made in step 6

#### Training
The training samples are now ready for the training process with `tmva_training.py`. This will perform the training on 50% of the QCD sample, an initial evaluation on the other 50% of the QCD sample and the evaluation on the specifed evaluation samples.Make sure to create a directory called “weights” to save the output class and xml files from the training. If you run the training interactively use,
python tmva_training.py > out.txt 
such that you can obtain the rankings of the training variables using Comparisons/rankings.py . 

The output of the initial evaluation on QCD is recorded in a root file, TMVA_classification.root . This contains various training information including the variable distributions and correlations, which can be viewed using the TMVAGui.

The output of the evaluation on ttbar is stored in ntuples such as trainPlusBDTG\_CombinedSVNoVertexSoftMuon_B.root. One can produce ROC curves and efficiency plots using makePlots.py . Other scripts to compare curves from various trainings are found in the "Comparisons/" directory.


