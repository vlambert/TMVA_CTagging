'''

Creates 2D pt/eta histograms per flavour/category ntuple to make
jet pt and eta distributions flat. 

* vertex category histograms also combined to make combined histograms
  for each flavour

'''
import sys
sys.argv.append( '-b-' )
import os
from ROOT import *
from array import array
import time
import multiprocessing
import thread
import subprocess


def processNtuple(inFileName, inDirName, outDirName,category):
  
  print "Starting to process %s" %inFileName
  # retrieve the ntuple of interest
  inFile = TFile( "%s/%s" %(inDirName, inFileName) )
  inTreeName = "tree"
  mychain = gDirectory.Get( inTreeName )
  
  # output
  outFileName = "%s/%s_EtaPtWeightHisto.root" %(outDirName, inFileName.replace("skimmed_20k_eachptetabin_", "").rsplit(".",1)[0])
  print "Writing to %s" %outFileName
  outFile = TFile( outFileName, 'recreate' )

  histo = TH2D("jets", "jets", 50, -2.5, 2.5, 40, 4.17438727, 6.95654544315); # pt starting from 15 and until 1000
  #mychain.Draw("log(jetPt+50):jetEta >> +jets", "", "Lego goff");                                    # category - specific
  mychain.Draw("log(jetPt+50):jetEta >> +jets", "weight_norm*weight_category", "Lego goff");          # category - inclusive
  histo_lin = TH2D("jets_lin", "jets_lin", 50, -2.5, 2.5, 40, 15, 1000); 
  #mychain.Draw("jetPt:jetEta >> +jets_lin", "","Lego goff")                                          # category - specific
  mychain.Draw("jetPt:jetEta >> +jets_lin", "weight_norm*weight_category", "Lego goff")               # category - inclusive

  outFile.cd()
  histo.Write()
  histo_lin.Write()
  outFile.Close()
  inFile.Close()

def combineHist(inDirName,flavour):
  weightHistName = "jets_lin"
  print "Accessing file %s/CombinedSVRecoVertex_%s_EtaPtWeightHisto.root"%(inDirName,flavour)
  
  # Without soft lepton categories
  #RecoFileName = "%s/skimmed_20k_eachptetabin_CombinedSVRecoVertex_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  #PseudoFileName = "%s/skimmed_20k_eachptetabin_CombinedSVPseudoVertex_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  #NoVtxFileName = "%s/skimmed_20k_eachptetabin_CombinedSVNoVertex_%s_EtaPtWeightHisto.root" %(inDirName, flavour)

  # With soft lepton categories
  RecoNSLFileName = "%s/CombinedSVRecoVertexNoSoftLepton_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  PseudoNSLFileName = "%s/CombinedSVPseudoVertexNoSoftLepton_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  NoVtxNSLFileName = "%s/CombinedSVNoVertexNoSoftLepton_%s_EtaPtWeightHisto.root" %(inDirName, flavour) 
  RecoSMFileName = "%s/CombinedSVRecoVertexSoftMuon_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  PseudoSMFileName = "%s/CombinedSVPseudoVertexSoftMuon_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  NoVtxSMFileName = "%s/CombinedSVNoVertexSoftMuon_%s_EtaPtWeightHisto.root" %(inDirName, flavour) 
  RecoSEFileName = "%s/CombinedSVRecoVertexSoftElectron_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  PseudoSEFileName = "%s/CombinedSVPseudoVertexSoftElectron_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  NoVtxSEFileName = "%s/CombinedSVNoVertexSoftElectron_%s_EtaPtWeightHisto.root" %(inDirName, flavour) 

  #RecoFile = TFile( "%s" %( RecoFileName) )
  #PseudoFile = TFile( "%s" %( PseudoFileName) )
  #NoVtxFile = TFile( "%s" %( NoVtxFileName) )

  RecoNSLFile = TFile( "%s" %( RecoNSLFileName) )
  PseudoNSLFile = TFile( "%s" %( PseudoNSLFileName) )
  NoVtxNSLFile = TFile( "%s" %( NoVtxNSLFileName) )
  RecoSEFile = TFile( "%s" %( RecoSEFileName) )
  PseudoSEFile = TFile( "%s" %( PseudoSEFileName) )
  NoVtxSEFile = TFile( "%s" %( NoVtxSEFileName) )
  RecoSMFile = TFile( "%s" %( RecoSMFileName) )
  PseudoSMFile = TFile( "%s" %( PseudoSMFileName) )
  NoVtxSMFile = TFile( "%s" %( NoVtxSMFileName) )
  
  #RecoHist = RecoFile.Get(weightHistName)
  #PseudoHist = PseudoFile.Get(weightHistName)
  #NoVtxHist = NoVtxFile.Get(weightHistName)

  RecoNSLHist = RecoNSLFile.Get(weightHistName)
  PseudoNSLHist = PseudoNSLFile.Get(weightHistName)
  NoVtxNSLHist = NoVtxNSLFile.Get(weightHistName)
  RecoSMHist = RecoSMFile.Get(weightHistName)
  PseudoSMHist = PseudoSMFile.Get(weightHistName)
  NoVtxSMHist = NoVtxSMFile.Get(weightHistName)
  RecoSEHist = RecoSEFile.Get(weightHistName)
  PseudoSEHist = PseudoSEFile.Get(weightHistName)
  NoVtxSEHist = NoVtxSEFile.Get(weightHistName)

  #RecoHist.Add(PseudoHist)
  #RecoHist.Add(NoVtxHist)

  RecoNSLHist.Add(PseudoNSLHist)
  RecoNSLHist.Add(NoVtxNSLHist)
  RecoNSLHist.Add(PseudoSMHist)
  RecoNSLHist.Add(PseudoSEHist)
  RecoNSLHist.Add(NoVtxSMHist)
  RecoNSLHist.Add(NoVtxSEHist)
  RecoNSLHist.Add(RecoSMHist)
  RecoNSLHist.Add(RecoSEHist)

  HistoutFileName = "%s/CombinedSVInclusive_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  print "Writing Combined Histograms to %s"%HistoutFileName
  HistoutFile = TFile( HistoutFileName, 'recreate' )
  HistoutFile.cd()
  RecoNSLHist.Write()
  HistoutFile.Close()


def main():

  ROOT.gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()
  # create Pool
  p = multiprocessing.Pool(parallelProcesses)
  print "Using %i parallel processes" %parallelProcesses

  #QCD
  #combDirName = '/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/Histograms/IntermediateSL/'
  #outDirName = '/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/Histograms/IntermediateSL/'
  combDirName =  '/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/Histograms/WeightSL/'
  outDirName = '/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/Histograms/WeightSL/'
  inDirName = '/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/intermediate_SL/'
  #inDirName = '/scratch/vlambert/Phys14AOD/QCD_13TeV_defaultIVF/flat_skimmed/'

  flavourCategoryDict = {}

  for inFileName in os.listdir(inDirName):
    if inFileName.endswith(".root") and inFileName.startswith("Combined"):
      # processNtuple(inFileName, inDirName, outDirName)
      # break
      category = inFileName.replace("skimmed_20k_eachptetabin_", "").split("_",1)[0]
      flavour = inFileName.replace("skimmed_20k_eachptetabin_", "").split("_",2)[1]
      flavour = flavour.replace(".root","")
      key = "%s_%s" %(category, flavour)
      print key
      if key not in flavourCategoryDict:
        flavourCategoryDict[key] = []
      flavourCategoryDict[key].append(inFileName.replace("skimmed_20k_eachptetabin_", "").replace(".root", "_EtaPtWeightHisto.root"))
      p.apply_async(processNtuple, args = (inFileName, inDirName, outDirName, category))

  p.close()
  p.join()

  # loop over all output files of one category and flavour and hadd them
  outDirName = os.path.join(os.path.abspath(sys.path[0]), outDirName) # absolute path to be safe

  
  for key in flavourCategoryDict.keys():
    #hadd only of there's something to hadd
    if (len(flavourCategoryDict[key]) > 1):
      print "hadding key files"
      haddList = ""
      for fileName in flavourCategoryDict[key]:
        haddList += "%s " %fileName
      haddCommand = "pwd && hadd -f %s_EtaPtWeightHisto.root %s" %(key, haddList)
      if (haddList.find("skimmed_20k_eachptetabin_") >= 0):
        haddCommand = "pwd && hadd -f skimmed_20k_eachptetabin_%s_EtaPtWeightHisto.root %s" %(key, haddList)
      # print haddCommand
      lock=thread.allocate_lock()
      lock.acquire()
      haddProcess=subprocess.Popen(haddCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=outDirName)
      haddProcess.wait()
      lock.release()
      errors = haddProcess.stderr.read()
      if ( len(errors) > 0):
        print "WARNING, there has been an error!"
        print errors 
      print haddProcess.stdout.read()
      # delete split files
      for fileName in flavourCategoryDict[key]:
        print "deleting %s/%s"%(outDirName, fileName)
        os.remove("%s/%s"%(outDirName, fileName))
    else: # if nothing to hadd just move file
      if (flavourCategoryDict[key][0].find("skimmed_20k_eachptetabin_") >= 0):
        print "moving %s/%s to %s/%s_EtaPtWeightHisto.root" %(outDirName, flavourCategoryDict[key][0], outDirName, key)
        os.rename("%s/%s" %(outDirName, flavourCategoryDict[key][0]), "%s/skimmed_20k_eachptetabin_%s_EtaPtWeightHisto.root"%(outDirName, key))
      else:
        print "moving %s/%s to %s/%s_EtaPtWeightHisto.root" %(outDirName, flavourCategoryDict[key][0], outDirName, key)
        os.rename("%s/%s" %(outDirName, flavourCategoryDict[key][0]), "%s/%s_EtaPtWeightHisto.root"%(outDirName, key))

  print  "Combining files"     
  # Combine vertex categories for histograms
  #outDirName = '/scratch/vlambert/TMVA/WeightHistograms_tt'
  #parallelProcesses = multiprocessing.cpu_count()
  #p = multiprocessing.Pool(parallelProcesses)
  #print "Using %i parallel processes" %parallelProcesses
  flavours = ["C","B","DUSG"]
  for flav in flavours:
    combineHist(combDirName, flav)  
  #p.close()
  #p.join

if __name__ == "__main__":
  main()
