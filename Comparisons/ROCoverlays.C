// =================================================================== //
//  Overlays ROC curves and Discriminators for comparison, by pT bin   //
// ___________________________________________________________________ //
#include "TGraph.h"

void ROCoverlays() {
  TFile *SoftLepton = TFile::Open("FullVariables/histos/AllHistograms.root"); 
  TFile *NoSLInfo = TFile::Open("../../NewVariables/DUSG/LDefault2/histos/AllHistograms.root");

  // loop over pT ranges
  for (Int_t i=7; i<8; i++){
    // Discriminators with SL information
    TH1F *SLC = (TH1F*)SoftLepton->Get(Form("histBDTG_C_Pt%i",i));
    TH1F *SLL = (TH1F*)SoftLepton->Get(Form("histBDTG_light_Pt%i",i));
    
    // Discriminators without SL information
    TH1F *DefC = (TH1F*)NoSLInfo->Get(Form("histBDTG_C_Pt%i",i));
    TH1F *DefL = (TH1F*)NoSLInfo->Get(Form("histBDTG_light_Pt%i",i));
    
    //ROC CvDUSG
    TGraph *SLCvL = (TGraph*)SoftLepton->Get(Form("ROC_C_light_%i",i));
    TGraph *noSLCvL = (TGraph*)NoSLInfo->Get(Form("ROC_C_light_%i",i));
  
    // Normalize Discriminators
    SLC->Scale(1./SLC->Integral());
    SLL->Scale(1./SLL->Integral());
    DefC->Scale(1./DefC->Integral());
    DefL->Scale(1./DefL->Integral());
    
    //Set colors
    noSLCvL->SetLineColor(kBlack);
    SLCvL->SetLineColor(kRed);

    noSLCvL->SetLineWidth(2); 
    SLCvL->SetLineWidth(2);     
    DefC->SetLineWidth(2);
    DefL->SetLineWidth(2);
    SLL->SetLineWidth(2); 
    SLC->SetLineWidth(2);
    
    TCanvas *cv = 0;
    TLegend *l = 0;
    TLatex *tex = 0;

    // Default Discriminators
    DefC->SetLineColor(kBlack);
    DefL->SetLineColor(kRed)

    cv = new TCanvas("cv","cv",800,800);
    cv->SetGridx();
    cv->SetGridy();
    DefL->SetTitle("No Soft Lepton Information");
    DefL->GetYaxis()->SetRangeUser(0,0.03);
    DefL->GetYaxis()->SetTitleOffset(1.6);
    DefL->GetYaxis()->SetTitle("Normalized Events");  
    DefL->GetXaxis()->SetTitle("BDT Output");
    DefL->Draw();
    DefC->Draw("same");
    gStyle->SetOptStat(0);

    l = new TLegend(0.55,0.8,0.90,0.9);
    l->SetBorderSize(0);
    l->SetFillStyle(0);
    l->AddEntry(DefC,"C Discriminator","l");
    l->AddEntry(DefL,"DUSG Discriminator","l");
    l->Draw();
    cv->Update();
    cv->SaveAs(Form("Default_Discriminators_%i.png",i));
    DefL->SetLineColor(kBlack);   

    // Soft Lepton Discriminators
    SLC->SetLineColor(kBlack);
    SLL->SetLineColor(kRed);

    cv = new TCanvas("cv","Reco",800,800);
    cv->SetGridx();
    cv->SetGridy();
    SLC->SetLineColor(kBlack);
    SLL->SetTitle("Soft Lepton Information");
    SLL->GetYaxis()->SetRangeUser(0,0.03);
    SLL->GetYaxis()->SetTitleOffset(1.6);
    SLL->GetYaxis()->SetTitle("Normalized Events");
    SLL->GetXaxis()->SetTitle("BDT Output");
    SLL->Draw();
    SLC->Draw("same");
    gStyle->SetOptStat(0);

    l = new TLegend(0.55,0.8,0.90,0.9);
    l->SetBorderSize(0);
    l->SetFillStyle(0);
    l->AddEntry(SLC,"C Discriminator","l");
    l->AddEntry(SLL,"DUSG Discriminator","l");
    l->Draw();
    cv->Update();
    cv->SaveAs(Form("SL_Discriminators_%i.png",i));
    SLC->SetLineColor(kBlue);


    // C Discriminators
    cv = new TCanvas("cv","C",800,800);
    cv->SetGridx();
    cv->SetGridy();
    SLC->Draw();
    SLC->SetTitle("Charm Discriminators");
    SLC->GetYaxis()->SetRangeUser(0,0.03);
    SLC->GetYaxis()->SetTitleOffset(1.6);
    SLC->GetYaxis()->SetTitle("Normalized Events");
    SLC->GetXaxis()->SetTitle("BDT Output");
    DefC->Draw("same");
    gStyle->SetOptStat(0);

    l = new TLegend(0.55,0.75,0.90,0.9);
    l->SetBorderSize(0);
    l->SetFillStyle(0);
    l->AddEntry(DefC,"No Soft Lepton Info","l");
    l->AddEntry(SLC,"With Soft Lepton Info","l");
    l->Draw();
    cv->Update();
    cv->SaveAs(Form("C_Discriminators_%i.png",i));
    
    // B Discriminators
    cv = new TCanvas("cv","B",800,800);
    cv->SetGridx();
    cv->SetGridy();
    SLL->SetTitle("DUSG  Discriminators");
    SLL->GetYaxis()->SetRangeUser(0,0.03);
    SLL->GetYaxis()->SetTitleOffset(1.6);
    SLL->GetYaxis()->SetTitle("Normalized Events");
    SLL->GetXaxis()->SetTitle("BDT Output");
    SLL->Draw();
    DefL->Draw("same");
    gStyle->SetOptStat(0);

    l = new TLegend(0.55,0.75,0.90,0.9);
    l->SetBorderSize(0);
    l->SetFillStyle(0);
    l->AddEntry(DefL,"No Soft Lepton Info","l");
    l->AddEntry(SLL,"With Soft Lepton Info","l");
    l->Draw();
    cv->Update();
    cv->SaveAs(Form("L_Discriminators_%i.png",i));
    
    // CvDUSG
    cv = new TCanvas("cv","",800,800);
    cv->SetLogy();
    cv->SetGrid(1,1);
    noSLCvL->SetTitle("CvDUSG, Inclusive");
    noSLCvL->Draw();
    SLCvL->Draw("same");
    
    l = new TLegend(0.55,0.2,0.9,0.35);
    l->SetBorderSize(0);
    l->SetFillStyle(0);
    l->AddEntry(SLCvL,"SL Variables","l");
    l->AddEntry(noSLCvL,"No SL Variables","l");
    l->Draw();
    cv->SaveAs(Form("CvDUSG_SL_%i.png",i));

  }
}
