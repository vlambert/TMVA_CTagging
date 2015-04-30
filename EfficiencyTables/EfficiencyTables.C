//================================================================
//
// Creates 2D pT/eta Efficiency tables for C, B, DUSG selection 
//            using C-tagging BDT working points
//
//         Additionally creates Efficiency v. pT plots 
//
// root -l EfficiencyTables.C+'("trainPlusBDTG_BvC.root")'
//
//________________________________________________________________

#if !defined(__CINT__) || defined(__MAKECINT__)
#include <TROOT.h>                  // access to gROOT, entry point to ROOT system
#include <TSystem.h>                // interface to OS
#include <TFile.h>                  // file handle class
#include <TTree.h>                  // class to access ntuples
#include <TClonesArray.h>           // ROOT array class
#include <vector>                   // STL vector class
#include <iostream>                 // standard I/O
#include <iomanip>                  // functions to format standard I/O
#include <fstream>                  // functions for file I/O
#include <string>                   // C++ string class
#include <sstream>                  // class for parsing strings
#include <TH1F.h>                
#include <TCanvas.h>                
#include <TGraphAsymmErrors.h>                

#include "interface/EfficiencyUtils.hh"

#endif

void EfficiencyExample(const string inputfile, int option = -1) {
  
  //--------------------------------------------------------------------------------------------------------------
  // Settings 
  //============================================================================================================== 
  bool printdebug = false;


  //*****************************************************************************************
  //Make some histograms
  //*****************************************************************************************
  TH1F *histDenominatorPt = new TH1F ("histDenominatorPt","; p_{T} [GeV/c]; Number of Events", 10, 0 , 1000); // 50, 0, 100
  TH1F *histNumeratorPt = new TH1F ("histNumeratorPt","; p_{T} [GeV/c]; Number of Events", 10, 0 , 1000);
  TH1F *histDenominatorEta = new TH1F ("histDenominatorEta","; Eta; Number of Events", 50, -3 , 3);
  TH1F *histNumeratorEta = new TH1F ("histNumeratorEta","; Eta; Number of Events", 50, -3 , -3);

  TH2F *histNumeratorPtEta = new TH2F ("histNumeratorPtEta","",10, 0, 1000, 30, -3, 3); // 50, 0 , 100
  TH2F *histDenominatorPtEta = new TH2F ("histDenominatorPtEta","",10, 0, 1000, 30, -3, 3);
  //*******************************************************************************************
  //Read file
  //*******************************************************************************************                


  // Set BDT working point
  //Float_t BDTCut = -0.025;  // BvC loose
  Float_t BDTCut = 0.16;      // DUSGvC tight


  TFile *treeFile = new TFile(inputfile.c_str());
  TTree *tree = (TTree*)treeFile->Get("tree");
  
  Float_t jetPt, jetEta, BDTG;
  Float_t flavour;
  tree->SetBranchAddress("flavour", &flavour);
  tree->SetBranchAddress("jetPt", &jetPt);
  tree->SetBranchAddress("jetEta",&jetEta);
  tree->SetBranchAddress("BDTG",&BDTG);
  for (int n=0;n<tree->GetEntries();n++) { 
    tree->GetEntry(n);
    
    //if (flavour !=4) continue;  // Charm
    //if(flavour !=5) continue;  // Bottom
    if(flavour==4 || flavour==5) continue;  //Light

 
    //**** PT Eta ****
    if (fabs(jetEta) < 2.5 && fabs(jetPt) > 20) {
      histDenominatorPtEta->Fill(jetPt, jetEta);
      
      //Numerator
      if(BDTG > BDTCut) {
	histNumeratorPtEta->Fill(jetPt, jetEta);        
      }
      
    }
    
    
    //**** PT ****
    if (fabs(jetEta) < 2.5) {
      histDenominatorPt->Fill(jetPt);
      
      //Numerator
      if(BDTG > BDTCut) {
	histNumeratorPt->Fill(jetPt);        
      }
      
    }
    
    //**** Eta ****
    if (fabs(jetPt) > 30) {
      histDenominatorEta->Fill(jetEta);
      
      //Numerator
      if(BDTG > BDTCut) {
	histNumeratorEta->Fill(jetEta);        
      }
      
    }
  }
  
  
  //--------------------------------------------------------------------------------------------------------------
  // Make Efficiency Plots
  //==============================================================================================================
  
  TGraphAsymmErrors *efficiency_pt = hcc::createEfficiencyGraph(histNumeratorPt, histDenominatorPt, "MistagRate_Ctag_Pt" , vector<double>() ,  -99, -99, 0, 1);
  
  TH2F *efficiency_pteta = hcc::createEfficiencyHist2D(histNumeratorPtEta, histDenominatorPtEta, "MistagRate_Ctag_PtEta" , vector<double>() ,  vector<double>());  
  
  //--------------------------------------------------------------------------------------------------------------
  // Draw
  //==============================================================================================================
  TCanvas *cv =0;
  
  cv = new TCanvas("cv","cv",800,600);
  cv->SetRightMargin(0.15); 
  efficiency_pteta->SetStats(0);
  efficiency_pteta->Draw("colz");
  efficiency_pteta->SetTitle("");
  efficiency_pteta->GetYaxis()->SetTitle("Eta");
  efficiency_pteta->GetXaxis()->SetTitle("p_{T} [GeV/c]");
  efficiency_pteta->GetYaxis()->SetRangeUser(-2.51,2.51);
  efficiency_pteta->GetXaxis()->SetRangeUser(29.9,100.9);
  efficiency_pteta->GetZaxis()->SetRangeUser(0,1);
  cv->SaveAs("Efficiency_PtEta.gif");
  

  cv = new TCanvas("cv","cv",800,600);
  efficiency_pt->SetTitle("");
  efficiency_pt->GetYaxis()->SetTitle("Efficiency");
  efficiency_pt->GetXaxis()->SetTitle("p_{T} [GeV/c]");
  efficiency_pt->Draw("AP");
  efficiency_pt->GetYaxis()->SetRangeUser(0.0,1.4);
  cv->SaveAs("Efficiency_Pt.gif");

  //--------------------------------------------------------------------------------------------------------------
  // Output
  //==============================================================================================================
  TFile *file = TFile::Open("MistagRate.root", "UPDATE");
  file->cd();
  file->WriteTObject(efficiency_pteta, efficiency_pteta->GetName(), "WriteDelete");
  file->WriteTObject(efficiency_pt, efficiency_pt->GetName(), "WriteDelete");
  file->Close();
  delete file;       
  
}
