// ===================================================================== //
//                                                                       //
//            Skim Evaluation Sample to Random 10% of events             //
//                                                                       //
// ===================================================================== // 


#include <string>         // std::string

void Skimmer() {
 
  string filename[27]={"CombinedSVNoVertexNoSoftLepton_B.root","CombinedSVNoVertexNoSoftLepton_C.root","CombinedSVNoVertexNoSoftLepton_DUSG.root","CombinedSVPseudoVertexNoSoftLepton_B.root","CombinedSVPseudoVertexNoSoftLepton_C.root","CombinedSVPseudoVertexNoSoftLepton_DUSG.root","CombinedSVRecoVertexNoSoftLepton_B.root","CombinedSVRecoVertexNoSoftLepton_C.root","CombinedSVRecoVertexNoSoftLepton_DUSG.root","CombinedSVNoVertexSoftElectron_B.root","CombinedSVNoVertexSoftElectron_C.root","CombinedSVNoVertexSoftElectron_DUSG.root","CombinedSVPseudoVertexSoftElectron_B.root","CombinedSVPseudoVertexSoftElectron_C.root","CombinedSVPseudoVertexSoftElectron_DUSG.root","CombinedSVRecoVertexSoftElectron_B.root","CombinedSVRecoVertexSoftElectron_C.root","CombinedSVRecoVertexSoftElectron_DUSG.root","CombinedSVNoVertexSoftMuon_B.root","CombinedSVNoVertexSoftMuon_C.root","CombinedSVNoVertexSoftMuon_DUSG.root","CombinedSVPseudoVertexSoftMuon_B.root","CombinedSVPseudoVertexSoftMuon_C.root","CombinedSVPseudoVertexSoftMuon_DUSG.root","CombinedSVRecoVertexSoftMuon_B.root","CombinedSVRecoVertexSoftMuon_C.root","CombinedSVRecoVertexSoftMuon_DUSG.root"};
  TString treename[27]={"CombinedSVNoVertexNoSoftLepton","CombinedSVNoVertexNoSoftLepton","CombinedSVNoVertexNoSoftLepton","CombinedSVPseudoVertexNoSoftLepton","CombinedSVPseudoVertexNoSoftLepton","CombinedSVPseudoVertexNoSoftLepton","CombinedSVRecoVertexNoSoftLepton","CombinedSVRecoVertexNoSoftLepton","CombinedSVRecoVertexNoSoftLepton","CombinedSVNoVertexSoftElectron","CombinedSVNoVertexSoftElectron","CombinedSVNoVertexSoftElectron","CombinedSVPseudoVertexSoftElectron","CombinedSVPseudoVertexSoftElectron","CombinedSVPseudoVertexSoftElectron","CombinedSVRecoVertexSoftElectron","CombinedSVRecoVertexSoftElectron","CombinedSVRecoVertexSoftElectron","CombinedSVNoVertexSoftMuon","CombinedSVNoVertexSoftMuon","CombinedSVNoVertexSoftMuon","CombinedSVPseudoVertexSoftMuon","CombinedSVPseudoVertexSoftMuon","CombinedSVPseudoVertexSoftMuon","CombinedSVRecoVertexSoftMuon","CombinedSVRecoVertexSoftMuon","CombinedSVRecoVertexSoftMuon"};
  
  double fraction = 0.1;
  double rdmnr = -999;
  gRandom->Uniform();
  
  for(int k = 0; k<27; k++)
    {  
      //Get old file, old tree and set top branch address
      TString name = filename[k].c_str();
      TFile *oldfile = new TFile(name);
      TTree *oldtree = (TTree*)oldfile->Get(treename[k]); //CombinedSVNoVertex, CombinedSVRecoVertex, CombinedSVPseudoVertex
      Int_t nentries = (Int_t)oldtree->GetEntries();
      
      cout << "There are " << nentries << " jets in the file " << filename[k] << " will select " << 100*fraction << " percent of events in a random way" << endl;
   
      Int_t flavour;
      Double_t jetpt, jeteta, trackSumJetEtRatio, trackSumJetDeltaR;
      std::vector <double>  *trackSip3dSig, *trackSip2dSig, *trackPtRel, *trackDeltaR, *trackPtRatio, *trackJetDist, *trackDecayLenVal, *trackSip2dSigAboveCharm, *trackSip3dSigAboveCharm, *leptonPtRel, *leptonSip3d, *leptonDeltaR, *leptonRatioRel;
      oldtree->SetBranchAddress("flavour",&flavour);
      oldtree->SetBranchAddress("jetPt",&jetpt);
      oldtree->SetBranchAddress("jetEta",&jeteta);
      oldtree->SetBranchAddress("trackPtRel",&trackPtRel);
      
      //Create a new file + a clone of old tree in new file
      TFile *newfile = new TFile("skimmed_"+name,"recreate");
      TTree *newtree = oldtree->CloneTree(0);
      
      // Loop over all events
      for (Int_t i=0;i<nentries; i++)
	{
	  oldtree->GetEntry(i);
	  bool Skipevent = false;
	  if(trackPtRel != 0)
	    {
	      for(Int_t iVect = 0; iVect < trackPtRel->size(); iVect ++)
		{
		  if(trackPtRel->at(iVect) != trackPtRel->at(iVect) )
		    {
		      cout << "trackPtRel[" << iVect << "]: " << trackPtRel->at(iVect) << endl; 
		      Skipevent = true;
		    }
		}		
	    }
	  // Select random events
	  if(gRandom->Uniform() > fraction) Skipevent = true;
	  
	  if(Skipevent == true) continue;
	  
	  newtree->Fill();
	}
      
      // Store new tree
      newtree->Print();
      newtree->AutoSave();
 
      // Clean up
      delete oldfile;
      delete newfile;
    }
}
