'''

Compare Variable Distributions for QCD and ttbar

'''
from ROOT import *
import os

def main():

  variables = [
    #"flavour",
    #"vertexCategory",
    #"jetPt",
    #"trackJetPt",
    #"jetEta",
    #"jetChargeEt0p3",
    #"jetChargeEt0p6",
    #"jetChargeEt1",
    "jetChargePt0p1",
    "jetChargePt0p3",
    "jetChargePt0p5",
    "jetChargePt0p6",
    "jetChargePt1",
    "VertexChargePt0p3",
    "VertexChargePt0p5",
    "VertexChargePt0p6",
    "VertexChargePt1",
    #"trackSip2dSig_0",
    #"trackSip2dSig_1",
    #"trackSip2dSig_2",
    #"trackSip3dSig_0",
    #"trackSip3dSig_1",
    #"trackSip3dSig_2",
    #"trackSip2dVal_0", "trackSip2dVal_1", "trackSip2dVal_2",
    #"trackSip3dVal_0", "trackSip3dVal_1", "trackSip3dVal_2",
    #"trackPtRel_0", "trackPtRel_1", "trackPtRel_2",
    #"trackPPar_0", "trackPPar_1", "trackPPar_2",
    #"trackEtaRel_0",
    #"trackEtaRel_1",
    #"trackEtaRel_2",
    #"trackDeltaR_0",
    #"trackDeltaR_1",
    #"trackDeltaR_2",
    #"trackPtRatio_0", "trackPtRatio_1", "trackPtRatio_2",
    #"trackPParRatio_0", "trackPParRatio_1", "trackPParRatio_2",
    #"trackJetDist_0","trackJetDist_1","trackJetDist_2",
    #"trackDecayLenVal_0", "trackDecayLenVal_1", "trackDecayLenVal_2",
    #"vertexMass_0",
    #"vertexEnergyRatio_0",
    #"trackSip2dSigAboveHalfCharm_0",
    #"trackSip3dSigAboveHalfCharm_0",
    #"trackSip2dSigAboveCharm_0",
    #"trackSip3dSigAboveCharm_0",
    #"flightDistance2dSig_0",
    #"flightDistance3dSig_0",
    #"flightDistance2dVal_0",
    #"flightDistance3dVal_0",
    #"trackSumJetEtRatio",
    #"vertexJetDeltaR_0",
    #"trackSumJetDeltaR",
    #"trackSip2dValAboveHalfCharm_0",
    #"trackSip3dValAboveHalfCharm_0",
    #"trackSip2dValAboveCharm_0",
    #"trackSip3dValAboveCharm_0",
    #"vertexFitProb_0",
    #"chargedHadronEnergyFraction",
    #"neutralHadronEnergyFraction",
    #"photonEnergyFraction",
    #"electronEnergyFraction",
    #"muonEnergyFraction",
    #"massVertexEnergyFraction_0",
    #"vertexBoostOverSqrtJetPt_0",
    #"vertexNTracks_0",
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
    #"leptonPtRel_0",
    #"leptonPtRel_1",
    #"leptonPtRel_2",
    #"leptonSip3d_0",
    #"leptonSip3d_1",
    #"leptonSip3d_2",
    #"leptonDeltaR_0",
    #"leptonDeltaR_1",
    #"leptonDeltaR_2",
    #"leptonRatioRel_0",
    #"leptonRatioRel_1",
    #"leptonRatioRel_2",
    #"leptonEtaRel_0",
    #"leptonEtaRel_1",
    #"leptonEtaRel_2",
    #"leptonRatio_0",
    #"leptonRatio_1",
    #"leptonRatio_2",
    ]
  
  PtBins = []
  #PtBins.append("jetPt>15")
  #PtBins.append("15<jetPt && jetPt<=40")
  #PtBins.append("40<jetPt && jetPt<=60")
  #PtBins.append("60<jetPt && jetPt<=90")
  #PtBins.append("90<jetPt && jetPt<=150 && abs(jetEta)<1.2")
  #PtBins.append("150<jetPt && jetPt<=400")
  #PtBins.append("jetPt>400")
  PtBins.append("jetPt>30")
  #PtBins.append("jetPt>150")  
  
  qtree = TChain('tree')
  ttree = TChain('tree')
  
  tfiles = [
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVNoVertexNoSoftLepton_B.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVNoVertexNoSoftLepton_C.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVNoVertexNoSoftLepton_DUSG.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVNoVertexSoftElectron_B.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVNoVertexSoftElectron_C.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVNoVertexSoftElectron_DUSG.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVNoVertexSoftMuon_B.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVNoVertexSoftMuon_C.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVNoVertexSoftMuon_DUSG.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVPseudoVertexNoSoftLepton_B.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVPseudoVertexNoSoftLepton_C.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVPseudoVertexNoSoftLepton_DUSG.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVPseudoVertexSoftElectron_B.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVPseudoVertexSoftElectron_C.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVPseudoVertexSoftElectron_DUSG.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVPseudoVertexSoftMuon_B.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVPseudoVertexSoftMuon_C.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVPseudoVertexSoftMuon_DUSG.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVRecoVertexNoSoftLepton_B.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVRecoVertexNoSoftLepton_C.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVRecoVertexNoSoftLepton_DUSG.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVRecoVertexSoftElectron_B.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVRecoVertexSoftElectron_C.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVRecoVertexSoftElectron_DUSG.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVRecoVertexSoftMuon_B.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVRecoVertexSoftMuon_C.root",
    "/scratch/vlambert/Phys14AOD/NewVariables/TTJets/flat_skimmed/CombinedSVRecoVertexSoftMuon_DUSG.root",
    ]
  
  qfiles = [
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVNoVertexNoSoftLepton_B.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVNoVertexNoSoftLepton_C.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVNoVertexNoSoftLepton_DUSG.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVNoVertexSoftElectron_B.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVNoVertexSoftElectron_C.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVNoVertexSoftElectron_DUSG.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVNoVertexSoftMuon_B.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVNoVertexSoftMuon_C.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVNoVertexSoftMuon_DUSG.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVPseudoVertexNoSoftLepton_B.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVPseudoVertexNoSoftLepton_C.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVPseudoVertexNoSoftLepton_DUSG.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVPseudoVertexSoftElectron_B.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVPseudoVertexSoftElectron_C.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVPseudoVertexSoftElectron_DUSG.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVPseudoVertexSoftMuon_B.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVPseudoVertexSoftMuon_C.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVPseudoVertexSoftMuon_DUSG.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVRecoVertexNoSoftLepton_B.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVRecoVertexNoSoftLepton_C.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVRecoVertexNoSoftLepton_DUSG.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVRecoVertexSoftElectron_B.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVRecoVertexSoftElectron_C.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVRecoVertexSoftElectron_DUSG.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVRecoVertexSoftMuon_B.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVRecoVertexSoftMuon_C.root",
   "/scratch/vlambert/Phys14AOD/NewVariables/QCD/weighted/CombinedSVRecoVertexSoftMuon_DUSG.root",
    ]
  for file in tfiles:
    ttree.Add('%s' %file)
    
  for file2 in qfiles:
    qtree.Add('%s' %file2)

  # Set bin ranges for each variable
  nbinlist = {}
  upbin = {}
  downbin = {}
  nbinlist["jetPt"] = 50, 0 , 1800
  nbinlist["jetEta"] = 25, -2.5 , 2.5
  nbinlist["trackJetPt"] = 20, 0 , 100

  nbinlist["jetChargePt0p1"] = 66, -2.0 , 2.0
  nbinlist["jetChargePt0p3"] = 66, -2.0 , 2.0
  nbinlist["jetChargePt0p5"] = 40, -1.2 , 1.2
  nbinlist["jetChargePt0p6"] = 40, -1.2 , 1.2
  nbinlist["jetChargePt1"] = 40, -1.2 , 1.2

  nbinlist["VertexChargePt0p3"] = 40, -1.2 , 1.2
  nbinlist["VertexChargePt0p5"] = 40, -1.2 , 1.2
  nbinlist["VertexChargePt0p6"] = 40, -1.2 , 1.2
  nbinlist["VertexChargePt1"] = 40, -1.2 , 1.2

  nbinlist["trackSip2dSigAboveHalfCharm_0"] = 30, -10, 25
  nbinlist["trackSip3dSigAboveHalfCharm_0"] = 30, -10, 25
  nbinlist["trackSip2dValAboveHalfCharm_0"] = 25, -1, 0.5
  nbinlist["trackSip3dValAboveHalfCharm_0"] = 25, -1, 0.5

  nbinlist["trackSip2dSigAboveCharm_0"] = 30, -10, 25
  nbinlist["trackSip3dSigAboveCharm_0"] = 30, -10, 25
  nbinlist["trackSip2dValAboveCharm_0"] = 25, -1, 0.5
  nbinlist["trackSip3dValAboveCharm_0"] = 25, -1, 0.5

  nbinlist["trackSip2dSig_0"] = 30, -10, 40
  nbinlist["trackSip2dSig_1"] = 30, -10, 40
  nbinlist["trackSip2dSig_2"] = 30, -10, 40
  nbinlist["trackSip3dSig_0"] = 30, -10, 40
  nbinlist["trackSip3dSig_1"] = 30, -10, 40
  nbinlist["trackSip3dSig_2"] = 30, -10, 40

  nbinlist["trackSip2dVal_0"] = 20, -0.1, 0.3
  nbinlist["trackSip2dVal_1"] = 20, -0.1, 0.3
  nbinlist["trackSip2dVal_2"] = 20, -0.1, 0.3
  nbinlist["trackSip3dVal_0"] = 20, -0.1, 0.3
  nbinlist["trackSip3dVal_1"] = 20, -0.1, 0.3
  nbinlist["trackSip3dVal_2"] = 20, -0.1, 0.3

  nbinlist["jetNTracks"] = 25, 0 , 25

  nbinlist["leptonRatio_0"] = 20, 0 , 1
  nbinlist["leptonRatio_1"] = 20, 0 , 0.5
  nbinlist["leptonRatio_2"] = 20, 0 , 0.5
  
  nbinlist["leptonSip3d_0"] = 100, -100 , 100
  nbinlist["leptonSip3d_1"] = 100, -100 , 100
  nbinlist["leptonSip3d_2"] = 100, -100 , 100

  nbinlist["leptonPtRel_0"] = 20, 0 , 15
  nbinlist["leptonPtRel_1"] = 15, 0 , 10
  nbinlist["leptonPtRel_2"] = 10, 0 , 5


  nbinlist["leptonDeltaR_0"] = 20, 0 , 0.6
  nbinlist["leptonDeltaR_1"] = 20, 0 , 0.6
  nbinlist["leptonDeltaR_2"] = 20, 0 , 0.6  

  nbinlist["leptonRatioRel_0"] = 20, 0 , 0.1
  nbinlist["leptonRatioRel_1"] = 20, 0 , 0.1
  nbinlist["leptonRatioRel_2"] = 20, 0 , 0.1

  nbinlist["leptonEtaRel_0"] = 20, 0 , 0.2
  nbinlist["leptonEtaRel_1"] = 20, 0 , 0.2
  nbinlist["leptonEtaRel_2"] = 20, 0 , 0.2

  nbinlist["flightDistance2dSig_0"] = 50, 0, 50
  nbinlist["flightDistance3dSig_0"] = 50, 0, 50
  nbinlist["flightDistance2dVal_0"] = 20, 0, 10
  nbinlist["flightDistance3dVal_0"] = 20, 0, 10

  nbinlist["muonEnergyFraction"] = 10, 0, 0.4
  nbinlist["chargedHadronEnergyFraction"] = 30, 0, 1.0
  nbinlist["neutralHadronEnergyFraction"] = 30, 0, 1.0
  nbinlist["photonEnergyFraction"] = 30, 0, 1.0
  nbinlist["electronEnergyFraction"] = 30, 0, 1.0
  nbinlist["vertexEnergyFraction"] = 10, 0, 4.0

  nbinlist["muonMultiplicity"] = 6, 0, 6
  nbinlist["chargedHadronMultiplicity"] = 40, 0, 200
  nbinlist["neutralHadronMultiplicity"] = 18, 0, 18
  nbinlist["photonMultiplicity"] = 70, 0, 70
  nbinlist["electronMultiplicity"] = 5, 0, 5
  nbinlist["hadronMultiplicity"] = 20, 0, 200
  nbinlist["hadronPhotonMultiplicity"] = 20, 0, 200
  nbinlist["totalMultiplicity"] = 20, 0, 200

  nbinlist["trackDeltaR_0"] = 40, 0, 0.4
  nbinlist["trackDeltaR_1"] = 40, 0, 0.4
  nbinlist["trackDeltaR_2"] = 40, 0, 0.4
  nbinlist["trackEtaRel_0"] = 20, 0, 8
  nbinlist["trackEtaRel_1"] = 20, 0, 8
  nbinlist["trackEtaRel_2"] = 20, 0, 8
  nbinlist["trackPtRatio_0"] = 20, 0, 0.35
  nbinlist["trackPtRatio_1"] = 20, 0, 0.35
  nbinlist["trackPtRatio_2"] = 20, 0, 0.35
  nbinlist["trackPParRatio_0"] = 20, 0, 1.0
  nbinlist["trackPParRatio_1"] = 20, 0, 1.0
  nbinlist["trackPParRatio_2"] = 20, 0, 1.0
  nbinlist["trackJetDist_0"] = 20, -0.1, 0.0
  nbinlist["trackJetDist_1"] = 20, -0.1, 0.0
  nbinlist["trackJetDist_2"] = 20, -0.1, 0.0
  nbinlist["trackDecayLenVal_0"] = 20, 0, 6.0
  nbinlist["trackDecayLenVal_1"] = 20, 0, 6.0
  nbinlist["trackDecayLenVal_2"] = 20, 0, 6.0

  nbinlist["vertexJetDeltaR_0"] = 15, 0, 0.3
  nbinlist["jetNSecondaryVertices"] = 6, 0, 6
  nbinlist["trackSumJetDeltaR"] = 20, 0, 0.5
  nbinlist["vertexEnergyRatio_0"] = 15, 0, 1.5
  nbinlist["vertexMass_0"] = 40, 0, 20
  nbinlist["vertexNTracks_0"] = 10, 0, 10

  nbinlist["massVertexEnergyFraction_0"] =  30, 0, 1.1
  nbinlist["vertexBoostOverSqrtJetPt_0"] = 20, 0, 1.1

  
  # Loop over variables
  for var in variables:
    for i in range(len(PtBins)):
      ttsig = TH1F("ttsig","ttsig",nbinlist[var][0], nbinlist[var][1],nbinlist[var][2])
      ttbkg = TH1F("ttbkg","ttbkg",nbinlist[var][0], nbinlist[var][1], nbinlist[var][2])
      qcdsig = TH1D("qcdsig","qcdsig",nbinlist[var][0], nbinlist[var][1], nbinlist[var][2])
      qcdbkg = TH1D("qcdbkg","qcdbkg",nbinlist[var][0], nbinlist[var][1], nbinlist[var][2])

      ttree.Draw("%s>>ttsig"%(var),"%s && flavour==4"%(PtBins[i]),"goff")                   # tt, charm
      qtree.Draw("%s>>qcdsig"%(var),"%s && flavour==4"%(PtBins[i]),"goff")                  # qcd, charm

      ttsig.SetNameTitle("%s_tt_s"%var,"%s_tt_s"%var)
      qcdsig.SetNameTitle("%s_qcd_s"%var,"%s_qcd_s"%var)

      ttree.Draw("%s>>ttbkg"%(var),"%s && flavour==5"%(PtBins[i]),"goff")                 # tt, bottom
      qtree.Draw("%s>>qcdbkg"%(var),"%s && flavour==5"%(PtBins[i]),"goff")                # qcd, bottom
      #ttree.Draw("%s>>ttbkg"%(var),"%s && flavour!=5 && flavour!=4"%(PtBins[i]),"goff")  # tt, DUSG
      #qtree.Draw("%s>>qcdbkg"%(var),"%s && flavour!=5 && flavour!=4"%(PtBins[i]),"goff") # qcd, DUSG 


      ttbkg.SetNameTitle("%s_tt_b"%var,"%s_tt_b"%var)
      qcdbkg.SetNameTitle("%s_qcd_b"%var,"%s_qcd_b"%var)

      sum_ttsig = ttsig.Integral()
      sum_ttbkg = ttbkg.Integral()
      sum_qcdsig = qcdsig.Integral()
      sum_qcdbkg = qcdbkg.Integral()
      # If the histograms are not empty then normalize them
      if sum_ttsig !=0 and sum_ttbkg !=0 and sum_qcdsig !=0 and sum_qcdbkg !=0:
        ttsig.Scale(1./ttsig.Integral())
        qcdsig.Scale(1./qcdsig.Integral())
        ttbkg.Scale(1./ttbkg.Integral())
        qcdbkg.Scale(1./qcdbkg.Integral())
        ttsig.GetYaxis().SetRangeUser(0,0.3)
        ttbkg.GetYaxis().SetRangeUser(0,0.3)
        qcdsig.GetYaxis().SetRangeUser(0,0.3)
        qcdbkg.GetYaxis().SetRangeUser(0,0.3)

      # Set errors
      ttsig.Sumw2()
      ttbkg.Sumw2()
      qcdsig.Sumw2()
      qcdbkg.Sumw2()
      # Perform Kolmogorov Test
      KolmS = ttsig.KolmogorovTest(qcdsig)
      KolmB = ttbkg.KolmogorovTest(qcdbkg)
      Kolmott = ttsig.KolmogorovTest(ttbkg)
      Kolmoqcd = qcdsig.KolmogorovTest(qcdbkg)
      print "KolmoS = %f , KolmoB = %f"%(KolmS,KolmB)
      print "Kolmott = %f , Kolmoqcd = %f"%(Kolmott,Kolmoqcd)      

      # Start making plots
      ttsig.SetLineColor(kBlue)
      qcdsig.SetLineColor(kBlue)
      ttbkg.SetLineColor(kRed) 
      qcdbkg.SetLineColor(kRed)
      
      ttsig.SetLineWidth(2)
      qcdsig.SetLineWidth(2)
      ttbkg.SetLineWidth(2)
      qcdbkg.SetLineWidth(2) 

      qcdsig2=qcdsig.Clone()
      qcdsig2.SetLineColor(kRed)      
      ###  QCD v tt for signal
      cv = TCanvas("cv","cv",800,600)
      ttsig.SetTitle("%s, Signals"%(var))
      qcdsig2.SetTitle("%s, Signals"%(var))
      ttsig.Draw("he")
      ttsig.GetYaxis().SetTitleOffset(1.2); 
      ttsig.GetYaxis().SetTitle("Normalized Events")
      qcdsig2.Draw("samehe")
      gStyle.SetOptStat(0)
      lo = TLegend(0.70,0.75,0.9,0.9)
      lo.SetBorderSize(0);
      lo.SetFillStyle(0);
      lo.AddEntry(qcdsig2,"QCD","l")
      lo.AddEntry(ttsig,"t#bar{t}","l")
      lo.Draw()
      texo=TLatex()
      texo.SetTextSize(0.04)
      texo.SetTextFont(2)
      texo.SetNDC()
      texo.DrawLatex(0.15,0.85,"Agreement = %4f"%KolmS)
      texo.Draw()
      cv.SaveAs("%s_inclusive__CvB_%i.png"%(var,i))

      ### Create tile plot comparing sig/bkg for QCD/tt
      cv = TCanvas("cv","cv",800,600)
      cv.Divide(2,2)

      ## ttbar
      cv.cd(1)
      ttsig.SetTitle("%s, tt"%(var))
      ttbkg.SetTitle("%s, tt"%(var)) 
      ttbkg.Draw("he")
      ttbkg.GetYaxis().SetTitleOffset(1.2);
      ttbkg.GetYaxis().SetTitle("Normalized Events")
      ttsig.Draw("samehe")
      gStyle.SetOptStat(0)
      l1 = TLegend(0.55,0.8,0.9,0.9)
      l1.SetBorderSize(0);
      l1.SetFillStyle(0);
      l1.AddEntry(ttsig,"Signal","l")
      l1.AddEntry(ttbkg,"Background","l")
      l1.Draw()
      tex=TLatex()
      tex.SetTextSize(0.04)
      tex.SetTextFont(2)
      tex.SetNDC()
      tex.DrawLatex(0.15,0.85,"Agreement = %f"%Kolmott)

      ## QCD
      cv.cd(2)
      qcdsig.SetTitle("%s, qcd"%(var))
      qcdbkg.SetTitle("%s, qcd"%(var))
      qcdbkg.Draw("he")
      qcdbkg.GetYaxis().SetTitleOffset(1.2);
      qcdbkg.GetYaxis().SetTitle("Normalized Events")
      qcdsig.Draw("samehe")
      gStyle.SetOptStat(0)
      l2 = TLegend(0.55,0.8,0.9,0.9)
      l2.SetBorderSize(0);
      l2.SetFillStyle(0);
      l2.AddEntry(qcdsig,"Signal","l")
      l2.AddEntry(qcdbkg,"Background","l")
      l2.Draw()
      tex2=TLatex()
      tex2.SetTextSize(0.04)
      tex2.SetTextFont(2)
      tex2.SetNDC()
      tex2.DrawLatex(0.15,0.85,"Agreement = %f"%Kolmoqcd)
      
      ## Signals
      ttsig2=ttsig.Clone()
      cv.cd(3)
      ttsig.SetTitle("%s, Signals"%(var))
      qcdsig2.SetTitle("%s, Signals"%(var))
      ttsig.Draw("he")
      ttsig.GetYaxis().SetTitleOffset(1.2);
      ttsig.GetYaxis().SetTitle("Normalized Events")
      qcdsig2.Draw("samehe")
      gStyle.SetOptStat(0)
      l3 = TLegend(0.70,0.8,0.9,0.9)
      l3.SetBorderSize(0);
      l3.SetFillStyle(0);
      l3.AddEntry(qcdsig2,"QCD","l")
      l3.AddEntry(ttsig2,"t#bar{t}","l")
      l3.Draw()
      tex3=TLatex()
      tex3.SetTextSize(0.04)
      tex3.SetTextFont(2)
      tex3.SetNDC()
      tex3.DrawLatex(0.15,0.85,"Agreement = %4f"%KolmS)
      tex3.Draw()

      ## Backgrounds
      ttbkg2=ttbkg.Clone()
      qcdbkg2=qcdbkg.Clone()
      ttbkg2.SetLineColor(kBlue)
      cv.cd(4)
      qcdbkg2.SetTitle("%s, Backgrounds"%(var))
      ttbkg2.SetTitle("%s, Backgrounds"%(var))
      ttbkg2.Draw("he")
      ttbkg2.GetYaxis().SetTitleOffset(1.2);
      ttbkg2.GetYaxis().SetTitle("Normalized Events")
      qcdbkg2.Draw("samehe")
      gStyle.SetOptStat(0)
      l4 = TLegend(0.55,0.8,0.9,0.9)
      l4.SetBorderSize(0);
      l4.SetFillStyle(0);
      l4.AddEntry(qcdbkg2,"QCD","l")
      l4.AddEntry(ttbkg2,"t#bar{t}","l")
      l4.Draw()
      tex4=TLatex()
      tex4.SetTextSize(0.04)
      tex4.SetTextFont(2)
      tex4.SetNDC()
      tex4.DrawLatex(0.15,0.85,"Agreement = %4f"%KolmB)
      cv.SaveAs("%s_CvB_%i.png"%(var,i))

      #Clear histograms
      ttsig = 0
      ttbkg = 0
      qcdsig = 0
      qcdbkg = 0
if __name__ == "__main__":
  main()
