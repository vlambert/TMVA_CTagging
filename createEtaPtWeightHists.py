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
  #inTreeName = category
  mychain = gDirectory.Get( inTreeName )
  
  # output
  outFileName = "%s/%s_EtaPtWeightHisto.root" %(outDirName, inFileName.rsplit(".",1)[0])
  print "Writing to %s" %outFileName
  outFile = TFile( outFileName, 'recreate' )

  histo = TH2D("jets", "jets", 50, -2.5, 2.5, 40, 4.17438727, 6.95654544315); # pt starting from 15 and until 1000
  #mychain.Draw("log(jetPt+50):jetEta >> +jets", "", "Lego goff");
  mychain.Draw("log(jetPt+50):jetEta >> +jets", "weight_norm*weight_category", "Lego goff");   #after adding normalization and category weight branches
  histo_lin = TH2D("jets_lin", "jets_lin", 50, -2.5, 2.5, 40, 15, 1000); # pt starting from 15 and until 1000  , default nbins was 40
  #mychain.Draw("jetPt:jetEta >> +jets_lin", "","Lego goff")
  mychain.Draw("jetPt:jetEta >> +jets_lin", "weight_norm*weight_category", "Lego goff")  # after adding normalization and category weight branches

  outFile.cd()
  histo.Write()
  histo_lin.Write()
  outFile.Close()
  inFile.Close()

def combineHist(inDirName,flavour):
  weightHistName = "jets_lin"
  print "Accessing file %s/skimmed_20k_eachptetabin_CombinedSVV2RecoVertex_%s_EtaPtWeightHisto.root"%(inDirName,flavour)
  #RecoFileName = "%s/skimmed_20k_eachptetabin_CombinedSVV2RecoVertex_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  #PseudoFileName = "%s/skimmed_20k_eachptetabin_CombinedSVV2PseudoVertex_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  #NoVtxFileName = "%s/skimmed_20k_eachptetabin_CombinedSVV2NoVertex_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  RecoFileName = "%s/CombinedSVV2RecoVertex_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  PseudoFileName = "%s/CombinedSVV2PseudoVertex_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  NoVtxFileName = "%s/CombinedSVV2NoVertex_%s_EtaPtWeightHisto.root" %(inDirName, flavour) 
  RecoFile = TFile( "%s" %( RecoFileName) )
  PseudoFile = TFile( "%s" %( PseudoFileName) )
  NoVtxFile = TFile( "%s" %( NoVtxFileName) )
  
  RecoHist = RecoFile.Get(weightHistName)
  PseudoHist = PseudoFile.Get(weightHistName)
  NoVtxHist = NoVtxFile.Get(weightHistName)
  #print RecoHist.ClassName()
  RecoHist.Add(PseudoHist)
  RecoHist.Add(NoVtxHist)
  
  HistoutFileName = "%s/skimmed_20k_eachptetabin_CombinedSVV2Inclusive_%s_EtaPtWeightHisto.root" %(inDirName, flavour)
  print "Writing Combined Histograms to %s"%HistoutFileName
  HistoutFile = TFile( HistoutFileName, 'recreate' )
  HistoutFile.cd()
  RecoHist.Write()
  HistoutFile.Close()


def main():

  ROOT.gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()
  # create Pool
  p = multiprocessing.Pool(parallelProcesses)
  print "Using %i parallel processes" %parallelProcesses
  
  outDirName = '/scratch/vlambert/TMVA/WeightHistograms_norm'     # for individual category histograms
  combDirName = '/scratch/vlambert/TMVA/WeightHistograms_norm'    # for combined histograms
  inDirName = "/scratch/vlambert/TMVA/QCD_flat_skimmed_weighted/"
  
  flavourCategoryDict = {}

  for inFileName in os.listdir(inDirName):
    if inFileName.endswith(".root"):
      # processNtuple(inFileName, inDirName, outDirName)
      # break
      category = inFileName.replace("skimmed_20k_eachptetabin_", "").split("_",1)[0]
      flavour = inFileName.replace("skimmed_20k_eachptetabin_", "").split("_",2)[1]
      flavour = flavour.replace(".root","")
      key = "%s_%s" %(category, flavour)
      print key
      if key not in flavourCategoryDict:
        flavourCategoryDict[key] = []
      flavourCategoryDict[key].append(inFileName.replace(".root", "_EtaPtWeightHisto.root"))
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
  flavours = ["C","B","DUSG"]
  for flav in flavours:
    combineHist(combDirName, flav)  


if __name__ == "__main__":
  main()
