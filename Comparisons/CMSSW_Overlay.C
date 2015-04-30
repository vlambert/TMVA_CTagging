// ===================================================================== //
//  Overlays ROC curves and Discriminators for comparison, CMSSW v TMVA  //
// _____________________________________________________________________ //

#include "TGraph.h"
#include "TGraphErrors.h"

void CMSSW_Overlay() {
  //CMSSW Trainings
  TFile *MLP= TFile::Open("/shome/vlambert/cmssw/CMSSW_5_3_3_patch2/src/CTagging/DQM_CMSSW/DQM_CMSSWctag_MLP_IVF.root");
  TFile *LR = TFile::Open("/shome/vlambert/cmssw/CMSSW_5_3_3_patch2/src/CTagging/DQM_CMSSW/DQM_CMSSWctag_LR_IVF.root");

  //TMVA Trainings
  TFile *TMVA = TFile::Open("/shome/vlambert/cmssw/CMSSW_5_3_3_patch2/src/CTagging/AlternativeWeighting/January_Corrections_2015/histos/AllHistograms.root");

  // Create ROC curves from CMSSW files
  // MLP
  TH1F * ctag_effC = (TH1F*) MLP->Get("DQMData/Run 1/Btag/Run summary/CSVIVFV2ctag_GLOBAL/effVsDiscrCut_discr_CSVIVFV2ctag_GLOBALC");
  TH1F * ctag_effDUSG = (TH1F*) MLP->Get("DQMData/Run 1/Btag/Run summary/CSVIVFV2ctag_GLOBAL/effVsDiscrCut_discr_CSVIVFV2ctag_GLOBALDUSG");
  const Int_t n = 100;
  Double_t ctag_C[n], ctag_B[n], ctag_L[n], ctag_eC[n], ctag_eB[n], ctag_eL[n];
  for(int bin = 0; bin<n; bin++){
    ctag_C[bin] = ctag_effC->GetBinContent(bin+1);
    ctag_L[bin] = ctag_effDUSG->GetBinContent(bin+1);
    ctag_eC[bin] = ctag_effC->GetBinError(bin+1);
    ctag_eL[bin] = ctag_effDUSG->GetBinError(bin+1);
  }
  TGraphErrors *mlp = new TGraphErrors(n,ctag_C,ctag_L,ctag_eC,ctag_eL);

  // Likelihood Ratio
  TH1F * ctag_effC_lr = (TH1F*) LR->Get("DQMData/Run 1/Btag/Run summary/CSVIVFctag_GLOBAL/effVsDiscrCut_discr_CSVIVFctag_GLOBALC");
  TH1F * ctag_effDUSG_lr = (TH1F*) LR->Get("DQMData/Run 1/Btag/Run summary/CSVIVFctag_GLOBAL/effVsDiscrCut_discr_CSVIVFctag_GLOBALDUSG");
  Double_t ctag_C2[n], ctag_B2[n], ctag_L2[n], ctag_eC2[n], ctag_eB2[n], ctag_eL2[n];
  for(int bin2 = 0; bin2<n; bin2++){
    ctag_C2[bin2] = ctag_effC_lr->GetBinContent(bin2+1);
    ctag_L2[bin2] = ctag_effDUSG_lr->GetBinContent(bin2+1);
    ctag_eC2[bin2] = ctag_effC_lr->GetBinError(bin2+1);
    ctag_eL2[bin2] = ctag_effDUSG_lr->GetBinError(bin2+1);
  }
  TGraphErrors *lr = new TGraphErrors(n,ctag_C2,ctag_L2,ctag_eC2,ctag_eL2);


  //ROC CvLight
  TGraph *tmva = (TGraph*)histos->Get("ROC_C_light_7");

  //Set colors
  mlp->SetLineColor(kBlack);
  lr->SetLineColor(kBlue);
  tmva->SetLineColor(kRed);

  tmva->SetLineWidth(2);

  TCanvas *cv = 0;
  TLegend *l = 0;
  TLatex *tex = 0;

  // CvDUSG
  cv = new TCanvas("cv","cv",800,800);
  cv->SetLogy();
  cv->SetGridx();
  cv->SetGridy();
  tmva->Draw();
  lr->Draw("same");
  mlp->Draw("same");
  l = new TLegend(0.45,0.15,0.90,0.25);
  l->SetBorderSize(0);
  l->SetFillStyle(0);  
  l->AddEntry(mlp,"CMSSW MLP","l");
  l->AddEntry(lr,"CMSSW LR","l");
  l->AddEntry(tmva,"TMVA","l");
  l->Draw();
  cv->Update();
  cv->SaveAs("CvDUSG_CMSSW_v_TMVA.png");

}
