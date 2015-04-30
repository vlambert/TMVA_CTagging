// ====================================================================== //
//                                                                        //                       
//           Create ttbar category biases from ttbar ntuples              //
//                                                                        //
// ====================================================================== // 

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "TString.h"
#include "TTree.h"
#include "TFile.h"
#include "TROOT.h"
#include "TObject.h"

using namespace std;

// define name Tree in calcEntries()

void calcEntries(string  flavour, string category, vector<double> & entries, string dir, string fix);

void biasTTbar(){
  
  string dir = "/scratch/vlambert/Phys14AOD/TTbar_13TeV_defaultIVF";
  string fix = "CombinedSV";
  
  string flavour[3] = {"C", "B", "DUSG"};
  string cat[9] = {"NoVertexNoSoftLepton", "PseudoVertexNoSoftLepton", "RecoVertexNoSoftLepton", "NoVertexSoftElectron", "PseudoVertexSoftElectron", "RecoVertexSoftElectron", "NoVertexSoftMuon", "PseudoVertexSoftMuon", "RecoVertexSoftMuon"};
  
  vector<double> entries[27];
  
  int nIter =0;
  
  for(int j=0; j<9; j++){//loop on categories
    for(int i =0; i<3; i++){//loop on flavours
      calcEntries(flavour[i], cat[j], entries[nIter], dir, fix);
      nIter++;
    }
  }
  
  ofstream myfile;
  string filename = "";
  for(int j=0; j<9; j++){//loop on categories	
    for(int k=0; k<3; k++){//loop on B and light
      cout<<"***************   "<<cat[j]<<"_"<<flavour[k]<<"   ***************"<<endl;
      filename = cat[j]+"_"+flavour[k]+"_ttbar_"+".txt";
      myfile.open (filename.c_str());
      for(int l = 0; l<19; l++ ){// loop on pt/eta bins defined in xml, 19
	int indexb = k+j*3;
	double bias = (double)(entries[indexb][l]);
	myfile << "<bias>"<<bias<<"</bias>\n";
	cout<<"<bias>"<<bias<<"</bias>"<<endl; 
      }
      myfile.close();
    }
  }  
}


void calcEntries(string flavour, string  category,  vector<double> & entries, string dir, string fix){	
  TFile * f = TFile::Open((dir+"/"+fix+category+"_"+flavour+".root").c_str());
  
  cout << "opening file: " << (dir+"/"+fix+category+"_"+flavour+".root").c_str() << endl;
  
  f->cd();
  //TTree * t =(TTree*)f->Get((fix+category).c_str());
  TTree * t = ((TTree*)f->Get("tree"));
  //definition of pt and eta bins should be the same as in the Train*xml files!!!
  //	entries.push_back(t->GetEntries());
  entries.push_back(t->GetEntries("jetPt>15&&jetPt<40&&TMath::Abs(jetEta)<1.2"));
  entries.push_back(t->GetEntries("jetPt>15&&jetPt<40&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
  entries.push_back(t->GetEntries("jetPt>15&&jetPt<40&&(!(TMath::Abs(jetEta)<2.1))"));
  entries.push_back(t->GetEntries("jetPt>40&&jetPt<60&&TMath::Abs(jetEta)<1.2"));
  entries.push_back(t->GetEntries("jetPt>40&&jetPt<60&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
  entries.push_back(t->GetEntries("jetPt>40&&jetPt<60&&(!(TMath::Abs(jetEta)<2.1))"));
  entries.push_back(t->GetEntries("jetPt>60&&jetPt<90&&TMath::Abs(jetEta)<1.2"));
  entries.push_back(t->GetEntries("jetPt>60&&jetPt<90&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
  entries.push_back(t->GetEntries("jetPt>60&&jetPt<90&&(!(TMath::Abs(jetEta)<2.1))"));
  entries.push_back(t->GetEntries("jetPt>90&&jetPt<150&&TMath::Abs(jetEta)<1.2"));
  entries.push_back(t->GetEntries("jetPt>90&&jetPt<150&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
  entries.push_back(t->GetEntries("jetPt>90&&jetPt<150&&(!(TMath::Abs(jetEta)<2.1))"));
  entries.push_back(t->GetEntries("jetPt>150&&jetPt<400&&TMath::Abs(jetEta)<1.2"));
  entries.push_back(t->GetEntries("jetPt>150&&jetPt<400&&TMath::Abs(jetEta)<2.1&&(!(TMath::Abs(jetEta)<1.2))"));
  entries.push_back(t->GetEntries("jetPt>150&&jetPt<400&&(!(TMath::Abs(jetEta)<2.1))"));
  entries.push_back(t->GetEntries("jetPt>400&&jetPt<600&&TMath::Abs(jetEta)<1.2"));
  entries.push_back(t->GetEntries("jetPt>400&&jetPt<600&&(!(TMath::Abs(jetEta)<1.2))"));
  entries.push_back(t->GetEntries("jetPt>600&&TMath::Abs(jetEta)<1.2"));
  entries.push_back(t->GetEntries("jetPt>600&&(!(TMath::Abs(jetEta)<1.2))"));
  //entries.push_back(t->GetEntries("jetPt>15"));
  
  cout << "jets have been put in pt and eta bins now" << endl;
  
}



