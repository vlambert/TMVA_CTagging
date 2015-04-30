'''

Creates ROC curves and Efficiency plots from evaluation ntuples 
and stores them in new root file '/histos/AllHistograms.root'

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

flavourCutsDict = {}
flavourCutsDict["B"] = "flavour == 5"
flavourCutsDict["C"] = "flavour == 4"
flavourCutsDict["light"] = "flavour !=4 && flavour !=5"
flavourCutsDict["non-C"] = "flavour !=4"
flavourCutsDict["non-B"] = "flavour !=5"

categoryCutsDict = {}
categoryCutsDict["RecoVertexNoSoftLepton"] = "vertexLeptonCategory == 0"
categoryCutsDict["PseudoVertexNoSoftLepton"] = "vertexLeptonCategory == 1"
categoryCutsDict["NoVertexNoSoftLepton"] = "vertexLeptonCategory == 2"
categoryCutsDict["RecoVertexSoftMuon"] = "vertexLeptonCategory == 3"
categoryCutsDict["PseudoVertexSoftMuon"] = "vertexLeptonCategory == 4"
categoryCutsDict["NoVertexSoftMuon"] = "vertexLeptonCategory == 5"
categoryCutsDict["RecoVertexSoftElectron"] = "vertexLeptonCategory == 6"
categoryCutsDict["PseudoVertexSoftElectron"] = "vertexLeptonCategory == 7"
categoryCutsDict["NoVertexSoftElectron"] = "vertexLeptonCategory == 8"
categoryCutsDict["RecoVertex"] = "(vertexLeptonCategory == 0 || vertexLeptonCategory == 3 || vertexLeptonCategory == 6)"
categoryCutsDict["PseudoVertex"] = "(vertexLeptonCategory == 1 || vertexLeptonCategory == 4 || vertexLeptonCategory == 7)"
categoryCutsDict["NoVertex"] = "(vertexLeptonCategory == 2 || vertexLeptonCategory == 5 || vertexLeptonCategory == 8)"
categoryCutsDict["SLInfo"] = "vertexLeptonCategory > 2"
categoryCutsDict["noSLInfo"] = "vertexLeptonCategory < 3"

categories = []
categories.append("RecoVertexNoSoftLepton")
categories.append("PseudoVertexNoSoftLepton")
categories.append("NoVertexNoSoftLepton")
categories.append("RecoVertexSoftMuon")
categories.append("PseudoVertexSoftMuon")
categories.append("NoVertexSoftMuon")
categories.append("RecoVertexSoftElectron")
categories.append("PseudoVertexSoftElectron")
categories.append("NoVertexSoftElectron")
categories.append("RecoVertex")
categories.append("PseudoVertex")
categories.append("NoVertex")
categories.append("SLInfo")
categories.append("noSLInfo")
categories.append("Inclusive")

flavours = []
flavours.append("B")
flavours.append("C")
flavours.append("light")
flavours.append("non-C")
flavours.append("non-B")

PtBins = []
PtBins = []
PtBins.append
PtBins.append("jetPt > 15")
PtBins.append("15 < jetPt and jetPt <= 40")
PtBins.append("40 < jetPt and jetPt <= 60")
PtBins.append("60 < jetPt and jetPt <= 90")
PtBins.append("90 < jetPt and jetPt <= 150")
PtBins.append("150 < jetPt and jetPt <=400")
PtBins.append("jetPt > 400")
PtBins.append("jetPt > 30")
PtBins.append("jetPt > 150")


etaPtBins = []
etaPtBins.append
etaPtBins.append("15 < jetPt and jetPt <= 40 and abs(jetEta) <= 1.2")
etaPtBins.append("15 < jetPt and jetPt <= 40 and 1.2 < abs(jetEta) and abs(jetEta) <= 2.1")
etaPtBins.append("15 < jetPt and jetPt <= 40 and abs(jetEta) > 2.1")
etaPtBins.append("40 < jetPt and jetPt <= 60 and abs(jetEta) <= 1.2")
etaPtBins.append("40 < jetPt and jetPt <= 60 and 1.2 < abs(jetEta) and abs(jetEta) <= 2.1")
etaPtBins.append("40 < jetPt and jetPt <= 60 and abs(jetEta) > 2.1")
etaPtBins.append("60 < jetPt and jetPt <= 90 and abs(jetEta) <= 1.2")
etaPtBins.append("60 < jetPt and jetPt <= 90 and 1.2 < abs(jetEta) and abs(jetEta) <= 2.1")
etaPtBins.append("60 < jetPt and jetPt <= 90 and abs(jetEta) > 2.1")
etaPtBins.append("90 < jetPt and jetPt <= 150 and abs(jetEta) <= 1.2")
etaPtBins.append("90 < jetPt and jetPt <= 150 and 1.2 < abs(jetEta) and abs(jetEta) <= 2.1")
etaPtBins.append("90 < jetPt and jetPt <= 150 and abs(jetEta) > 2.1")
etaPtBins.append("150 < jetPt and jetPt <= 400 and abs(jetEta) <= 1.2")
etaPtBins.append("150 < jetPt and jetPt <= 400 and 1.2 < abs(jetEta) and abs(jetEta) <= 2.1")
etaPtBins.append("150 < jetPt and jetPt <= 400 and abs(jetEta) > 2.1")
etaPtBins.append("400 < jetPt and jetPt <= 600 and abs(jetEta)<= 1.2")
etaPtBins.append("400 < jetPt and jetPt <= 600 and abs(jetEta) > 1.2")
etaPtBins.append("jetPt > 600 and abs(jetEta) <= 1.2")
etaPtBins.append("jetPt > 600 and abs(jetEta) > 1.2")
  


def processNtuple(inFileName, inDirName, outDirName,):
  
  print "Starting to process %s" %inFileName
  # retrieve the ntuple of interest
  inFile = TFile( "%s/%s" %(inDirName, inFileName) )
  inTreeName = "tree"
  mychain = gDirectory.Get( inTreeName )
  
  # output
  outFileName = "%s/%s_Histograms.root" %(outDirName, inFileName.rsplit(".",1)[0])
  print "Writing to %s" %outFileName
  outFile = TFile( outFileName, 'recreate' )

  discriminantHistos = []
  nBins = 1000
  
  for flav in flavourCutsDict.keys():
    # Draw Discriminants by flavour
    discriminantHisto = TH1D("histBDTG_%s"%flav, "BDTG output for %s;BDTG value"%flav, nBins, -1, 1)
    mychain.Draw("BDTG >> +histBDTG_%s"%flav, flavourCutsDict[flav], "")
    discriminantHisto.Write()
    discriminantHistos.append(discriminantHisto)
    # Draw Discriminants in pT/eta bins
    for i in range(len(etaPtBins)):
      discriminantHisto = TH1D("histBDTG_%s_EtaPt%i"%(flav, i), "BDTG output for %s and %s;BDTG value"%(flav, etaPtBins[i]), nBins, -1, 1)
      mychain.Draw("BDTG >> +histBDTG_%s_EtaPt%i"%(flav, i), "(%s) && (%s)" %(flavourCutsDict[flav], etaPtBins[i].replace("and","&&")), "")
      discriminantHisto.Write()
      discriminantHistos.append(discriminantHisto)
    # Draw Discriminants by Category
    for cat in categoryCutsDict.keys():
      discriminantHisto = TH1D("histBDTG_%s_%s"%(flav, cat), "BDTG output for %s and %s;BDTG value"%(flav, cat), nBins, -1, 1)
      mychain.Draw("BDTG >> +histBDTG_%s_%s"%(flav, cat), "%s && %s"%(flavourCutsDict[flav], categoryCutsDict[cat]), "")
      discriminantHisto.Write()
      discriminantHistos.append(discriminantHisto)
    # Draw Discriminants by pT bin
    for j in range(len(PtBins)):
      discriminantHisto = TH1D("histBDTG_%s_Pt%i"%(flav, j), "BDTG output for %s and %s;BDTG value"%(flav, PtBins[j]), nBins, -1, 1)
      mychain.Draw("BDTG >> +histBDTG_%s_Pt%i"%(flav, j), "(%s) && (%s)" %(flavourCutsDict[flav], PtBins[j].replace("and","&&")), "")
      discriminantHisto.Write()
      discriminantHistos.append(discriminantHisto)
  
  outFile.Close()
  inFile.Close()


def makeROCCurves(outDirName):
  ''' Produce ROC curves and efficiency curves '''
  nBins = 100
  xBins = array("d")
  xBinsPlot = array("d")
  yBinsPlot = array("d")
  for i in range(0,nBins+2):
    xBins.append(float(i)/nBins)
  outFileName = "%s/AllHistograms.root" %(outDirName)
  print "Updating %s" %outFileName
  outFile = TFile.Open(outFileName, "update")
  histDictFlav = [[0 for x in range(len(PtBins))] for y in range(len(flavours))]
  histDictFlavEffs = [[0 for x in range(len(PtBins))] for y in range(len(flavours))]
  histDictFlavCat = [[0 for x in range(len(categories))] for y in range(len(flavours))]
  histDictFlavCatEffs = [[0 for x in range(len(categories))] for y in range(len(flavours))]
  for flav in range(len(flavours)):
    for j in range(len(PtBins)):
      histDictFlav[flav][j] = outFile.Get("histBDTG_%s_Pt%i"%(flavours[flav],j))
      histDictFlavEffs[flav][j] = array("d")
      integral = histDictFlav[flav][j].Integral(0, histDictFlav[flav][j].GetNbinsX()+1)
      for xbin in range(0, histDictFlav[flav][j].GetNbinsX()+2):
        histDictFlavEffs[flav][j].append(histDictFlav[flav][j].Integral(xbin, histDictFlav[flav][j].GetNbinsX()+1)/integral)
    for c in range(len(categories)):
      if c < (len(categories)-1):
        histDictFlavCat[flav][c] = outFile.Get("histBDTG_%s_%s"%(flavours[flav],categories[c]))
      else:
        histDictFlavCat[flav][c] = outFile.Get("histBDTG_%s"%(flavours[flav]))
      histDictFlavCatEffs[flav][c] = array("d")
      integral = histDictFlavCat[flav][c].Integral(0, histDictFlavCat[flav][c].GetNbinsX()+1)
      for xbin in range(0, histDictFlavCat[flav][c].GetNbinsX()+2):
        histDictFlavCatEffs[flav][c].append(histDictFlavCat[flav][c].Integral(xbin, histDictFlavCat[flav][c].GetNbinsX()+1)/integral)


  # Create Efficiency v. Discriminator bin plots
  canvas1 = TCanvas("c0","Eff",800,800)
  XbinEff = array("d")
  YbinEff = array("d")
  for flav in range(len(flavours)):
    for cat in range(len(categories)):
      del XbinEff[:]
      del YbinEff[:]
      for Xbin in range(0,histDictFlavCat[flav][cat].GetNbinsX()+1):
        YbinEff.append(histDictFlavCatEffs[flav][cat][Xbin])
        XbinEff.append(histDictFlavCat[flav][cat].GetBinCenter(Xbin))
      EffCurve = TGraph(len(XbinEff),XbinEff,YbinEff)
      EffCurve.GetXaxis().SetTitle("%s Discriminant"%(flavours[flav]))
      EffCurve.GetYaxis().SetTitle("%s efficiency"%(flavours[flav]))
      EffCurve.SetTitle("%s efficiency, %s"%(flavours[flav],categories[cat]))
      EffCurve.SetName("Efficiency_%s_discrim_%s"%(flavours[flav],categories[cat]))
      EffCurve.Draw("al")
      gPad.SetGridx(1)
      gPad.SetGridy(1)
      EffCurve.Write()

  # Create Efficiency Ratio (B/C and DUSG/C) v. Discriminator bin plots
  canvas1 = TCanvas("c0","Eff",800,800)
  XbinEffC = array("d")
  YbinEffC = array("d")
  XbinEffB = array("d")
  YbinEffB = array("d")
  XbinEffL = array("d")
  YbinEffL = array("d")
  for XbinC in range(0,histDictFlavCat[1][14].GetNbinsX()+1):
    YbinEffC.append(histDictFlavCatEffs[1][14][XbinC])
    XbinEffC.append(histDictFlavCat[1][14].GetBinCenter(XbinC))
  for XbinB in range(0,histDictFlavCat[0][14].GetNbinsX()+1):
    YbinEffB.append(histDictFlavCatEffs[0][14][XbinB])
    XbinEffB.append(histDictFlavCat[0][14].GetBinCenter(XbinB))
  for XbinL in range(0,histDictFlavCat[2][14].GetNbinsX()+1):
    YbinEffL.append(histDictFlavCatEffs[2][14][XbinL])
    XbinEffL.append(histDictFlavCat[2][14].GetBinCenter(XbinL))

  YbinEffCB = array("d")
  YbinEffCL = array("d")
  for entry in range(len(XbinEffC)):
    if YbinEffB[entry]!=0:
      YbinEffCB.append(YbinEffC[entry]/YbinEffB[entry])
    else:
      if YbinEffC[entry]==0:
        YbinEffCB.append(0.0)
      else:
        YbinEffCB.append(1000.0)
    if YbinEffL[entry]!=0:
      YbinEffCL.append(YbinEffC[entry]/YbinEffL[entry])
    else:
      if YbinEffC[entry]==0:
        YbinEffCL.append(0.0)
      else:
        YbinEffCL.append(1000.0)
  
  EffCurveB = TGraph(len(XbinEffC),XbinEffC,YbinEffCB)
  EffCurveB.GetXaxis().SetTitle("Discriminant")
  EffCurveB.GetYaxis().SetTitle("C/B efficiency")
  EffCurveB.SetTitle("C/B Efficiency")
  EffCurveB.SetName("Efficiency_C_B_discrim")
  EffCurveB.Draw("al")
  gPad.SetGridx(1)
  gPad.SetGridy(1)
  EffCurveB.Write()

  EffCurveL = TGraph(len(XbinEffC),XbinEffC,YbinEffCL)
  EffCurveL.GetXaxis().SetTitle("Discriminant")
  EffCurveL.GetYaxis().SetTitle("C/DUSG efficiency")
  EffCurveL.SetTitle("C/DUSG Efficiency")
  EffCurveL.SetName("Efficiency_C_light_discrim")
  EffCurveL.Draw("al")
  gPad.SetGridx(1)
  gPad.SetGridy(1)
  EffCurveL.Write()

  # Create ROC curves for vertex categories
  canvas2 = TCanvas("c2","ROC",800,800);
  for flav1 in range(len(flavours)):
    for flav2 in range(len(flavours)):
      for cat in range(len(categories)):
        del xBinsPlot[:]
        del yBinsPlot[:]
        yBins = array("d")
        for i in range(0,nBins+2):
          yBins.append(0.)
        integral1 = histDictFlavCat[flav1][cat].Integral(0, histDictFlavCat[flav1][cat].GetNbinsX()+1)
        discrimBin = histDictFlavCat[flav1][cat].GetNbinsX()+1 
        for currentBin in range(0,nBins+2):
          currentEff = histDictFlavCatEffs[flav1][cat][discrimBin]
          yBins[currentBin] = histDictFlavCatEffs[flav2][cat][discrimBin]
          while currentEff < xBins[currentBin] and discrimBin > 0:
            discrimBin -= 1
            currentEff = histDictFlavCatEffs[flav1][cat][discrimBin]
            yBins[currentBin] = histDictFlavCatEffs[flav2][cat][discrimBin]
          if (currentBin < (nBins+1) and currentEff < xBins[currentBin+1]):
            xBinsPlot.append(xBins[currentBin])
            yBinsPlot.append(yBins[currentBin])

        rocCurve = TGraph(len(xBinsPlot),xBinsPlot,yBinsPlot)
        rocCurve.GetXaxis().SetTitle("%s efficiency"%flavours[flav1])
        rocCurve.GetYaxis().SetTitle("%s efficiency"%flavours[flav2])
        rocCurve.SetTitle("%s vs. %s, %s"%(flavours[flav1], flavours[flav2], categories[cat]))
        rocCurve.SetName("ROC_%s_%s_%s"%(flavours[flav1], flavours[flav2],categories[cat]))
        rocCurve.GetYaxis().SetRangeUser(0.0001,1.0);
        rocCurve.GetXaxis().SetLimits(0.,1.0);
        rocCurve.Draw("al")
        gPad.SetGridx(1)
        gPad.SetGridy(1)
        gPad.SetLogy()
        #canvas2.SaveAs("%s/%s.png" %(outDirName, rocCurve.GetName()))
        rocCurve.Write()
        
  # Create ROC curves
  canvas = TCanvas("c1","ROC",800,800);
  for flav1 in range(len(flavours)):
    for flav2 in range(len(flavours)):
      for n in range(len(PtBins)):
        del xBinsPlot[:]
        del yBinsPlot[:]
        yBins = array("d")
        for i in range(0,nBins+2):
          yBins.append(0.)
        integral1 = histDictFlav[flav1][n].Integral(0, histDictFlav[flav1][n].GetNbinsX()+1)
        #del xBinsPlot[:]
        #del yBinsPlot[:]
        #print "ROC curve for flavor %s %s" %(flav1,flav2)
        # loop over efficiency values starting at 0 (i.e. highest bin)
        discrimBin = histDictFlav[flav1][n].GetNbinsX()+1
        for currentBin in range(0,nBins+2):
          # get discriminant bin for signal
          currentEff = histDictFlavEffs[flav1][n][discrimBin]
          yBins[currentBin] = histDictFlavEffs[flav2][n][discrimBin]
        #print "%i - %i: %f - %f - %f" %(currentBin, discrimBin, xBins[currentBin], currentEff, yBins[currentBin])
          while currentEff < xBins[currentBin] and discrimBin > 0:
            discrimBin -= 1
            currentEff = histDictFlavEffs[flav1][n][discrimBin]
            yBins[currentBin] = histDictFlavEffs[flav2][n][discrimBin]
            #print "while %i - %i: %f - %f - %f" %(currentBin, discrimBin, xBins[currentBin], currentEff, yBins[currentBin])
          #print "--------------"
          if (currentBin < (nBins+1) and currentEff < xBins[currentBin+1]):
            xBinsPlot.append(xBins[currentBin])
            yBinsPlot.append(yBins[currentBin])

        
        rocCurve = TGraph(len(xBinsPlot),xBinsPlot,yBinsPlot)
        rocCurve.GetXaxis().SetTitle("%s efficiency"%flavours[flav1])
        rocCurve.GetYaxis().SetTitle("%s efficiency"%flavours[flav2])
        rocCurve.SetTitle("%s vs. %s, %s"%(flavours[flav1], flavours[flav2], PtBins[n]))
        rocCurve.SetName("ROC_%s_%s_%i"%(flavours[flav1], flavours[flav2],n))
        rocCurve.GetYaxis().SetRangeUser(0.0001,1.0);
        rocCurve.GetXaxis().SetLimits(0.,1.0);
        #TH1D("ROC_%s_%s"%(flav1, flav2), "ROC curve for %s vs. %s;%s efficiency;%s efficiency"%(flav1, flav2, flav1, flav2), 100, -1, 1)
        rocCurve.Draw("al")
        gPad.SetGridx(1)
        gPad.SetGridy(1)
        gPad.SetLogy()
        #canvas.SaveAs("%s/%s.png" %(outDirName, rocCurve.GetName()))
        rocCurve.Write()
      #break
  outFile.Close()        
  


def main():

  ROOT.gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()
  
  # create Pool
  #p = multiprocessing.Pool(parallelProcesses)
  #print "Using %i parallel processes" %parallelProcesses
    
  outDirName = './histos/'
  inDirName = "./"
  fileList = []

  for inFileName in os.listdir(inDirName):
    if inFileName.endswith(".root") and inFileName.startswith("trainPlusBDTG_"):
      category = inFileName.replace("trainPlusBDTG_", "").split("_",1)[0]
      flavour = inFileName.replace("trainPlusBDTG_", "").split("_",2)[1]
      key = "%s_%s" %(category, flavour)
      print key
      fileList.append(inFileName.replace(".root", "_Histograms.root"))
      processNtuple(inFileName, inDirName, outDirName)
      # break
      #p.apply_async(processNtuple, args = (inFileName, inDirName, outDirName,))

  #p.close()
  #p.join()


  # loop over all output files of one category and flavour and hadd them
  outDirName = os.path.join(os.path.abspath(sys.path[0]), outDirName) # absolute path to be safe
  print "hadding key files"
  haddList = ""
  for fileName in fileList:
    haddList += "%s " %fileName
  haddCommand = "pwd && hadd -f AllHistograms.root %s" %(haddList)
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
  # for fileName in fileList:
  #   print "deleting %s/%s"%(outDirName, fileName)
  #   os.remove("%s/%s"%(outDirName, fileName))
  
  makeROCCurves(outDirName)
  

if __name__ == "__main__":
  main()
