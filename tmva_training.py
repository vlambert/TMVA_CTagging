import ROOT
import os
import multiprocessing
import array



# LR training variables
training_vars_float = [
  #"flavour",
  #"vertexCategory",
  #"jetPt",
  #"trackJetPt",
  #"jetEta",
  "trackSip2dSig_0",
  "trackSip2dSig_1",
  "trackSip2dSig_2",
  "trackSip3dSig_0", 
  "trackSip3dSig_1",
  "trackSip3dSig_2",
  "trackSip2dVal_0",
  #"trackSip2dVal_1",
  #"trackSip2dVal_2",
  "trackSip3dVal_0",
  "trackSip3dVal_1",
  #"trackSip3dVal_2",
  #"trackPtRel_0", "trackPtRel_1", "trackPtRel_2",
  #"trackPPar_0", "trackPPar_1", "trackPPar_2",
  #"trackEtaRel_0", "trackEtaRel_1", "trackEtaRel_2",
  #"trackDeltaR_0", "trackDeltaR_1", "trackDeltaR_2",
  #"trackPtRatio_0", "trackPtRatio_1", "trackPtRatio_2",
  #"trackPParRatio_0", "trackPParRatio_1", "trackPParRatio_2",
  #"trackJetDist_0","trackJetDist_1","trackJetDist_2",
  "trackDecayLenVal_0",
  #"trackDecayLenVal_1",
  #"trackDecayLenVal_2",
  "vertexMass_0",
  #"vertexEnergyRatio_0",
  #"trackSip2dSigAboveCharm_0",
  #"trackSip3dSigAboveCharm_0",
  "flightDistance2dSig_0",
  "flightDistance3dSig_0",
  #"flightDistance2dVal_0",    ?
  #"flightDistance3dVal_0",   ?
  #"trackSumJetEtRatio",
  "vertexJetDeltaR_0",
  #"trackSumJetDeltaR",
  #"trackSip2dValAboveCharm_0",
  #"trackSip3dValAboveCharm_0",
  #"vertexFitProb_0",
  #"chargedHadronEnergyFraction",
  #"neutralHadronEnergyFraction",
  #"photonEnergyFraction",
  #"electronEnergyFraction",
  #"muonEnergyFraction",
  "massVertexEnergyFraction_0",
  "vertexBoostOverSqrtJetPt_0",
  ]

training_vars_int = [
  "vertexNTracks_0",
  #"jetNSecondaryVertices",
  #"jetNTracks",
  #"chargedHadronMultiplicity",
  #"neutralHadronMultiplicity",
  #"photonMultiplicity",
  #"electronMultiplicity",
  #"muonMultiplicity",
  #"hadronMultiplicity",
  #"hadronPhotonMultiplicity",
  #"totalMultiplicity",
  ]



def train(bdtoptions):
  
  TMVA_tools = ROOT.TMVA.Tools.Instance()

  tree = ROOT.TChain('tree')

  files = [
    #"/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/weighted/skimmed_20k_eachptetabin_CombinedSVNoVertex_B.root",
    "/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/weighted/skimmed_20k_eachptetabin_CombinedSVNoVertex_C.root",
    "/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/weighted/skimmed_20k_eachptetabin_CombinedSVNoVertex_DUSG.root",
    #"/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/weighted/skimmed_20k_eachptetabin_CombinedSVPseudoVertex_B.root",
    "/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/weighted/skimmed_20k_eachptetabin_CombinedSVPseudoVertex_C.root",
    "/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/weighted/skimmed_20k_eachptetabin_CombinedSVPseudoVertex_DUSG.root",
    #"/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/weighted/skimmed_20k_eachptetabin_CombinedSVRecoVertex_B.root",
    "/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/weighted/skimmed_20k_eachptetabin_CombinedSVRecoVertex_C.root",
    "/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/weighted/skimmed_20k_eachptetabin_CombinedSVRecoVertex_DUSG.root",

    ]
  
  for f in files:
      print 'Opening file %s' %f
      tree.Add('%s' %f)
  
  signal_selection = 'flavour==4' # c
  background_selection = 'flavour!=4 && flavour!=5' # not b or c

  num_pass = tree.GetEntries(signal_selection)
  num_fail = tree.GetEntries(background_selection)

  print 'N events signal', num_pass
  print 'N events background', num_fail
  outFile = ROOT.TFile('TMVA_classification.root', 'RECREATE')

  factory = ROOT.TMVA.Factory(
                               "TMVAClassification", 
                               outFile, 
                               "!V:!Silent:Color:DrawProgressBar:Transformations=I"
                             ) 

  for var in training_vars_float:
    factory.AddVariable(var, 'F') # add float variable
  for var in training_vars_int:
    factory.AddVariable(var, 'I') # add integer variable

  factory.SetWeightExpression('weight_etaPtInc * weight_category * weight_norm')

  factory.AddSignalTree(tree, 1.)
  factory.AddBackgroundTree(tree, 1.)

  # import pdb; pdb.set_trace()

  factory.PrepareTrainingAndTestTree( ROOT.TCut(signal_selection), ROOT.TCut(background_selection),
                                      "nTrain_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

  
  factory.BookMethod( ROOT.TMVA.Types.kBDT,
                      "BDTG",
                      # "!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedGrad:GradBaggingFraction=0.9:SeparationType=GiniIndex:nCuts=500:NNodesMax=5"
                      ":".join(bdtoptions)
                    )

  factory.TrainAllMethods()

  # factory.OptimizeAllMethods()

  factory.TestAllMethods()

  factory.EvaluateAllMethods()

  outFile.Close()

##   ROOT.gROOT.LoadMacro('$ROOTSYS/tmva/test/TMVAGui.C')
##   ROOT.TMVAGui('TMVA_classification.root')
##   raw_input("Press Enter to continue...")


def trainMultiClass():

  classes = [
    ('flavour==5', 'B'),
    ('flavour==4', 'C'),
    ('flavour!=5 && flavour!=4', 'DUSG')
  ]

  for cl in classes:
    print 'N events', cl[1], tree.GetEntries(cl[0])

  outFile = ROOT.TFile('TMVA_multiclass.root', 'RECREATE')

  factory = ROOT.TMVA.Factory(
        "TMVAClassification", 
        outFile, 
        "!V:!Silent:Color:DrawProgressBar:Transformations=I:AnalysisType=Multiclass" ) 

  for var in training_vars_float:
    factory.AddVariable(var, 'F') # add float variable
  for var in training_vars_int:
    factory.AddVariable(var, 'I') # add integer variable

  # factory.SetWeightExpression('')

  for cl in classes:
    factory.AddTree(tree, cl[1], 1., ROOT.TCut(cl[0]))
  # factory.AddSignalTree(tree, 1.)
  # factory.AddBackgroundTree(tree, 1.)

  # import pdb; pdb.set_trace()

  factory.PrepareTrainingAndTestTree( ROOT.TCut(''), ROOT.TCut(''),  "SplitMode=Random:NormMode=NumEvents:!V")

  factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.05:UseBaggedGrad:GradBaggingFraction=0.9:SeparationType=GiniIndex:nCuts=500:NNodesMax=5" )

  # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_ADA", "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.2:MaxDepth=2:MinNodeSize=6")

  factory.TrainAllMethods()

  # factory.OptimizeAllMethods()

  factory.TestAllMethods()

  factory.EvaluateAllMethods()

  outFile.Close()

 #ROOT.gROOT.LoadMacro('$ROOTSYS/tmva/test/TMVAMultiClassGui.C')
 #ROOT.TMVAMultiClassGui('TMVA_multiclass.root')
 #raw_input("Press Enter to continue...")



def read(inDirName, inFileName):
  
  print "Reading", inFileName
  
  TMVA_tools = ROOT.TMVA.Tools.Instance()

  tree = ROOT.TChain('tree')

  tree.Add('%s/%s' %(inDirName, inFileName))

  reader = ROOT.TMVA.Reader('TMVAClassification_BDTG')

  varDict = {}
  for var in training_vars_float:
    varDict[var] = array.array('f',[0])
    reader.AddVariable(var, varDict[var])
  for var in training_vars_int:
    varDict[var] = array.array('f',[0])
    reader.AddVariable(var, varDict[var])


  reader.BookMVA("BDTG","weights/TMVAClassification_BDTG.weights.xml")

  bdtOuts = []
  flavours = []
  categories = []
  leptoncategories = []
  jetPts = []
  jetEtas = []

  for jentry in xrange(tree.GetEntries()):

    ientry = tree.LoadTree(jentry)
    nb = tree.GetEntry(jentry)

    for var in varDict:
      varDict[var][0] = getattr(tree, var)

    bdtOutput = reader.EvaluateMVA("BDTG")
    flavour = tree.flavour
    bdtOuts.append(bdtOutput)
    flavours.append(flavour)
    categories.append(tree.vertexCategory)
    leptoncategories.append(tree.vertexLeptonCategory)
    jetPts.append(tree.jetPt)
    jetEtas.append(tree.jetEta)

    if jentry%10000 == 0:
      print jentry, bdtOutput, flavour

  writeSmallTree = True

  if writeSmallTree:
    print "Writing small tree"

    BDTG = array.array('f',[0])
    flav = array.array('f',[0])
    cat = array.array('f',[0])
    lep = array.array('f',[0])
    jetPt = array.array('f',[0])
    jetEta = array.array('f',[0])

    fout = ROOT.TFile('trainPlusBDTG_%s.root'%(inFileName.replace(".root","")), 'RECREATE')
    outTree = ROOT.TTree( 'tree', 'c-tagging training tree' )
    outTree.Branch('BDTG', BDTG, 'BDTG/F')
    outTree.Branch('flavour', flav, 'flavour/F')
    outTree.Branch('vertexCategory', cat, 'vertexCategory/F')
    outTree.Branch('vertexLeptonCategory', lep, 'vertexLeptonCategory/F')
    outTree.Branch('jetPt', jetPt, 'jetPt/F')
    outTree.Branch('jetEta', jetEta, 'jetEta/F')


    for i in range(len((bdtOuts))):
      BDTG[0] = bdtOuts[i]
      flav[0] = flavours[i]
      cat[0] = categories[i]
      lep[0] = leptoncategories[i]
      jetPt[0] = jetPts[i]
      jetEta[0] = jetEtas[i]
      if i%10000==0:
        print i, bdtOuts[i], flavours[i]
      outTree.Fill()
      # treeout.Write()
    fout.Write()
    fout.Close()
  print "done", inFileName

def readParallel():

  print "start readParallel()"
  ROOT.gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()
  
  inDirName="/scratch/vlambert/Phys14AOD/TTbar_13TeV_defaultIVF/flat/"
  files = [
    #"CombinedSVNoVertex_B.root",
    #"CombinedSVNoVertex_C.root",
    #"CombinedSVNoVertex_DUSG.root",
    #"CombinedSVPseudoVertex_B.root",
    #"CombinedSVPseudoVertex_C.root",
    #"CombinedSVPseudoVertex_DUSG.root",
    #"CombinedSVRecoVertex_B.root",
    #"CombinedSVRecoVertex_C.root",
    #"CombinedSVRecoVertex_DUSG.root"
    "CombinedSVNoVertexNoSoftLepton_B.root",
    "CombinedSVNoVertexNoSoftLepton_C.root",
    "CombinedSVNoVertexNoSoftLepton_DUSG.root",
    "CombinedSVPseudoVertexNoSoftLepton_B.root",
    "CombinedSVPseudoVertexNoSoftLepton_C.root",
    "CombinedSVPseudoVertexNoSoftLepton_DUSG.root",
    "CombinedSVRecoVertexNoSoftLepton_B.root",
    "CombinedSVRecoVertexNoSoftLepton_C.root",
    "CombinedSVRecoVertexNoSoftLepton_DUSG.root",
    "CombinedSVNoVertexSoftMuon_B.root",
    "CombinedSVNoVertexSoftMuon_C.root",
    "CombinedSVNoVertexSoftMuon_DUSG.root",
    "CombinedSVPseudoVertexSoftMuon_B.root",
    "CombinedSVPseudoVertexSoftMuon_C.root",
    "CombinedSVPseudoVertexSoftMuon_DUSG.root",
    "CombinedSVRecoVertexSoftMuon_B.root",
    "CombinedSVRecoVertexSoftMuon_C.root",
    "CombinedSVRecoVertexSoftMuon_DUSG.root",
    "CombinedSVNoVertexSoftElectron_B.root",
    "CombinedSVNoVertexSoftElectron_C.root",
    "CombinedSVNoVertexSoftElectron_DUSG.root",
    "CombinedSVPseudoVertexSoftElectron_B.root",
    "CombinedSVPseudoVertexSoftElectron_C.root",
    "CombinedSVPseudoVertexSoftElectron_DUSG.root",
    "CombinedSVRecoVertexSoftElectron_B.root",
    "CombinedSVRecoVertexSoftElectron_C.root",
    "CombinedSVRecoVertexSoftElectron_DUSG.root"
    ]


  #IVF Variations
  #inDirName="/scratch/vlambert/Phys14AOD/IVFvariants/"
  #files = [
    #"CSVSLctag_IVFadap_distanceRatio_0/CSVSLctag_IVFadap_distanceRatio_0.root", 
    #"CSVSLctag_IVFadap_distanceRatio_10/CSVSLctag_IVFadap_distanceRatio_10.root", 
    #"CSVSLctag_IVFadap_distanceRatio_15/CSVSLctag_IVFadap_distanceRatio_15.root", 
    #"CSVSLctag_IVFadap_distanceRatio_5/CSVSLctag_IVFadap_distanceRatio_5.root", 
    #"CSVSLctag_IVFadap_distSig2dMin_0/CSVSLctag_IVFadap_distSig2dMin_0.root", 
    #"CSVSLctag_IVFadap_distSig2dMin_0p5/CSVSLctag_IVFadap_distSig2dMin_0p5.root", 
    #"CSVSLctag_IVFadap_distSig2dMin_1/CSVSLctag_IVFadap_distSig2dMin_1.root", 
    #"CSVSLctag_IVFadap_distSig2dMin_2/CSVSLctag_IVFadap_distSig2dMin_2.root", 
    #"CSVSLctag_IVFadap_seedMin3DIPSig_0/CSVSLctag_IVFadap_seedMin3DIPSig_0.root",
    #"CSVSLctag_IVFadap_seedMin3DIPSig_0p6/CSVSLctag_IVFadap_seedMin3DIPSig_0p6.root",
    #"CSVSLctag_IVFadap_seedMin3DIPSig_0p8/CSVSLctag_IVFadap_seedMin3DIPSig_0p8.root",
    #"CSVSLctag_IVFadap_seedMin3DIPSig_1/CSVSLctag_IVFadap_seedMin3DIPSig_1.root",
    #"CSVSLctag_IVFadap_seedMin3DIPVal_0/CSVSLctag_IVFadap_seedMin3DIPVal_0.root",
    #"CSVSLctag_IVFadap_seedMin3DIPVal_0p00125/CSVSLctag_IVFadap_seedMin3DIPVal_0p00125.root", 
    #"CSVSLctag_IVFadap_seedMin3DIPVal_0p0025/CSVSLctag_IVFadap_seedMin3DIPVal_0p0025.root", 
    #"CSVSLctag_IVFadap_seedMin3DIPVal_0p00375/CSVSLctag_IVFadap_seedMin3DIPVal_0p00375.root", 
    #"CSVSLctag_IVFadap_vertexMinDLen2DSig_0/CSVSLctag_IVFadap_vertexMinDLen2DSig_0.root", 
    #"CSVSLctag_IVFadap_vertexMinDLen2DSig_0p5/CSVSLctag_IVFadap_vertexMinDLen2DSig_0p5.root", 
    #"CSVSLctag_IVFadap_vertexMinDLen2DSig_1/CSVSLctag_IVFadap_vertexMinDLen2DSig_1.root", 
    #"CSVSLctag_IVFadap_vertexMinDLen2DSig_1p5/CSVSLctag_IVFadap_vertexMinDLen2DSig_1p5.root", 
    #"CSVSLctag_IVFadap_vertexMinDLen2DSig_2/CSVSLctag_IVFadap_vertexMinDLen2DSig_2.root", 
    #"CSVSLctag_IVFadap_vertexMinDLen2DSig_2p5CSVSLctag_IVFadap_vertexMinDLen2DSig_2p5.root", 
    #"CSVSLctag_IVFadap_vertexMinDLenSig_0/CSVSLctag_IVFadap_vertexMinDLenSig_0.root",
    #"CSVSLctag_IVFadap_vertexMinDLenSig_0p125/CSVSLctag_IVFadap_vertexMinDLenSig_0p125.root",
    #"CSVSLctag_IVFadap_vertexMinDLenSig_0p375/CSVSLctag_IVFadap_vertexMinDLenSig_0p375.root",
    #"CSVSLctag_IVFadap_vertexMinDLenSig_0p5/CSVSLctag_IVFadap_vertexMinDLenSig_0p5.root"
    #]


  #for inFileName in os.listdir(inDirName):
  #  if inFileName.endswith(".root") and not (inFileName.find("Eta") >= 0):
  #    files.append(inFileName)

  # create Pool
  #p = multiprocessing.Pool(parallelProcesses)
  #print "Using %i parallel processes" %parallelProcesses

  for f in files:
    # debug
     read(inDirName, f)
    # break
    # run jobs
    #p.apply_async(read, args = (inDirName, f,))

  #p.close()
  #p.join()
    


if __name__ == '__main__':
    bdtoptions = [ "!H",
                                 "!V",
                                 "NTrees=1000",
                                 "MinNodeSize=1.5%",
                                 "BoostType=Grad",
                                 "Shrinkage=0.10",
                                 "UseBaggedGrad",
                                 "GradBaggingFraction=0.5",
                                 "nCuts=80",
                                 "MaxDepth=2",
                               ]
    train(bdtoptions)
    # trainMultiClass()
    readParallel()

