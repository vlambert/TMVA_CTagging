# Skims training ntuples so that each pt/eta bin for each flavour/vertex file has maximum 20k events

import sys
import os
sys.argv.append( '-b-' )
from ROOT import *
from array import array
import time
import math
import multiprocessing

def Filter(FileName, inDirectory, OutDirectory, TreeName, max_nb_ofjets, ptbins, etabins):
  inFile = "%s/%s"%(inDirectory,FileName)
  oldfile = TFile(inFile)
  oldtree = oldfile.Get(TreeName)

  nentries = oldtree.GetEntries()
  
  print "There are %i jets in the file %s, will select %i  in each pt/eta bin"%(nentries,FileName,max_nb_ofjets)
  
  jetpt = array( "f", [0. ] )
  jeteta = array( "f", [0. ] )
  flavour = array( "i", [0 ] )

  oldtree.SetBranchAddress("flavour",flavour);
  oldtree.SetBranchAddress("jetPt",jetpt);
  oldtree.SetBranchAddress("jetEta",jeteta);
  
  outFile = "%s/%s"%(OutDirectory,FileName)
  newfile = TFile(outFile,"recreate");
  newtree = oldtree.CloneTree(0);
    
  nbOfjets=[]
  nbOfjetsKept=[]
  nbOfjets_DUS=[]
  nbOfjetsKept_DUS=[]
  nbOfjets_G=[]
  nbOfjetsKept_G=[]
  for j in range(19):
    nbOfjets.append(0)
    nbOfjetsKept.append(0)
    nbOfjets_DUS.append(0)
    nbOfjetsKept_DUS.append(0)
    nbOfjets_G.append(0)
    nbOfjetsKept_G.append(0)
      
    
  if (FileName.find("DUSG") >=0):
    for i in xrange(nentries):
      oldtree.GetEntry(i)
      #print "flavour = %i"%flavour[0]
      if (flavour[0] < 21 ): 
        if ((jetpt[0]>=ptbins[0] and jetpt[0]<ptbins[1]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_DUS[0]+=1
          if (nbOfjets_DUS[0]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[0]+=1
        elif ((jetpt[0]>=ptbins[0] and jetpt[0]<ptbins[1]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_DUS[1]+=1
          if (nbOfjets_DUS[1]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[1]+=1
        elif ((jetpt[0]>=ptbins[0] and jetpt[0]<ptbins[1]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_DUS[2]+=1
          if (nbOfjets_DUS[2]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[2]+=1
        elif ((jetpt[0]>=ptbins[1] and jetpt[0]<ptbins[2]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_DUS[3]+=1
          if (nbOfjets_DUS[3]<max_nb_ofjets): 
            newtree.Fill()
            nbOfjetsKept_DUS[3]+=1
        elif ((jetpt[0]>=ptbins[1] and jetpt[0]<ptbins[2]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_DUS[4]+=1
          if (nbOfjets_DUS[4]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[4]+=1
        elif ((jetpt[0]>=ptbins[1] and jetpt[0]<ptbins[2]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_DUS[5]+=1
          if (nbOfjets_DUS[5]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[5]+=1
        elif ((jetpt[0]>=ptbins[2] and jetpt[0]<ptbins[3]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_DUS[6]+=1
          if (nbOfjets_DUS[6]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[6]+=1
        elif ((jetpt[0]>=ptbins[2] and jetpt[0]<ptbins[3]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_DUS[7]+=1
          if (nbOfjets_DUS[7]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[7]+=1
        elif ((jetpt[0]>=ptbins[2] and jetpt[0]<ptbins[3]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_DUS[8]+=1
          if (nbOfjets_DUS[8]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[8]+=1
        elif ((jetpt[0]>=ptbins[3] and jetpt[0]<ptbins[4]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_DUS[9]+=1
          if (nbOfjets_DUS[9]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[9]+=1
        elif ((jetpt[0]>=ptbins[3] and jetpt[0]<ptbins[4]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_DUS[10]+=1
          if (nbOfjets_DUS[10]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[10]+=1
        elif ((jetpt[0]>=ptbins[3] and jetpt[0]<ptbins[4]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_DUS[11]+=1
          if (nbOfjets_DUS[11]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[11]+=1
        elif ((jetpt[0]>=ptbins[4] and jetpt[0]<ptbins[5]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_DUS[12]+=1
          if (nbOfjets_DUS[12]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[12]+=1
        elif ((jetpt[0]>=ptbins[4] and jetpt[0]<ptbins[5]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_DUS[13]+=1
          if (nbOfjets_DUS[13]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[13]+=1
        elif ((jetpt[0]>=ptbins[4] and jetpt[0]<ptbins[5]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_DUS[14]+=1
          if (nbOfjets_DUS[14]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[14]+=1
        elif ((jetpt[0]>=ptbins[5] and jetpt[0]<ptbins[6]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_DUS[15]+=1
          if (nbOfjets_DUS[15]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[15]+=1
        elif ((jetpt[0]>=ptbins[5] and jetpt[0]<ptbins[6]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[3])):
          nbOfjets_DUS[16]+=1
          if (nbOfjets_DUS[16]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[16]+=1
        elif ((jetpt[0]>=ptbins[6] and jetpt[0]<ptbins[7]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_DUS[17]+=1
          if (nbOfjets_DUS[17]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[17]+=1
        elif ((jetpt[0]>=ptbins[6] and jetpt[0]<ptbins[7]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[3])):
          nbOfjets_DUS[18]+=1
          if (nbOfjets_DUS[18]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_DUS[18]+=1
	    				
      else:
        if ((jetpt[0]>=ptbins[0] and jetpt[0]<ptbins[1]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_G[0]+=1
          if (nbOfjets_G[0]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[0]+=1
        elif ((jetpt[0]>=ptbins[0] and jetpt[0]<ptbins[1]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_G[1]+=1
          if (nbOfjets_G[1]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[1]+=1
        elif ((jetpt[0]>=ptbins[0] and jetpt[0]<ptbins[1]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_G[2]+=1
          if (nbOfjets_G[2]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[2]+=1
        elif ((jetpt[0]>=ptbins[1] and jetpt[0]<ptbins[2]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_G[3]+=1
          if (nbOfjets_G[3]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[3]+=1
        elif ((jetpt[0]>=ptbins[1] and jetpt[0]<ptbins[2]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_G[4]+=1
          if (nbOfjets_G[4]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[4]+=1
        elif ((jetpt[0]>=ptbins[1] and jetpt[0]<ptbins[2]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_G[5]+=1
          if (nbOfjets_G[5]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[5]+=1
        elif ((jetpt[0]>=ptbins[2] and jetpt[0]<ptbins[3]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_G[6]+=1
          if (nbOfjets_G[6]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[6]+=1
        elif ((jetpt[0]>=ptbins[2] and jetpt[0]<ptbins[3]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_G[7]+=1
          if (nbOfjets_G[7]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[7]+=1
        elif ((jetpt[0]>=ptbins[2] and jetpt[0]<ptbins[3]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_G[8]+=1
          if (nbOfjets_G[8]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[8]+=1
        elif ((jetpt[0]>=ptbins[3] and jetpt[0]<ptbins[4]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_G[9]+=1
          if (nbOfjets_G[9]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[9]+=1
        elif ((jetpt[0]>=ptbins[3] and jetpt[0]<ptbins[4]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_G[10]+=1
          if (nbOfjets_G[10]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[10]+=1
        elif ((jetpt[0]>=ptbins[3] and jetpt[0]<ptbins[4]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_G[11]+=1
          if (nbOfjets_G[11]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[11]+=1
        elif ((jetpt[0]>=ptbins[4] and jetpt[0]<ptbins[5]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_G[12]+=1
          if (nbOfjets_G[12]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[12]+=1
        elif ((jetpt[0]>=ptbins[4] and jetpt[0]<ptbins[5]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
          nbOfjets_G[13]+=1
          if (nbOfjets_G[13]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[13]+=1
        elif ((jetpt[0]>=ptbins[4] and jetpt[0]<ptbins[5]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
          nbOfjets_G[14]+=1
          if (nbOfjets_G[14]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[14]+=1
        elif ((jetpt[0]>=ptbins[5] and jetpt[0]<ptbins[6]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_G[15]+=1
          if (nbOfjets_G[15]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[15]+=1
        elif ((jetpt[0]>=ptbins[5] and jetpt[0]<ptbins[6]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[3])):
          nbOfjets_G[16]+=1
          if (nbOfjets_G[16]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[16]+=1
        elif ((jetpt[0]>=ptbins[6] and jetpt[0]<ptbins[7]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
          nbOfjets_G[17]+=1
          if (nbOfjets_G[17]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[17]+=1
        elif ((jetpt[0]>=ptbins[6] and jetpt[0]<ptbins[7]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[3])):
          nbOfjets_G[18]+=1
          if (nbOfjets_G[18]<max_nb_ofjets):
            newtree.Fill()
            nbOfjetsKept_G[18]+=1
	    				
            
            
    for j in range(19):
      print "Tree %s has %i in pt/eta-bin and we keep %i"%(FileName,nbOfjets_DUS[j],nbOfjetsKept_DUS[j])
      print "Tree %s has %i in pt/eta-bin and we keep %i"%(FileName,nbOfjets_G[j],nbOfjetsKept_G[j])
      
    newtree.Print()
    newtree.AutoSave()
    
  else:
    for i in xrange(nentries):
      oldtree.GetEntry(i)
	 
      if ((jetpt[0]>=ptbins[0] and jetpt[0]<ptbins[1]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
        nbOfjets[0]+=1
	 
        if (nbOfjets[0]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[0]+=1
      elif ((jetpt[0]>=ptbins[0] and jetpt[0]<ptbins[1]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
        nbOfjets[1]+=1
	 
        if (nbOfjets[1]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[1]+=1
      elif ((jetpt[0]>=ptbins[0] and jetpt[0]<ptbins[1]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
        nbOfjets[2]+=1
	 
        if (nbOfjets[2]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[2]+=1
      elif ((jetpt[0]>=ptbins[1] and jetpt[0]<ptbins[2]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
        nbOfjets[3]+=1
	 
        if (nbOfjets[3]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[3]+=1
      elif ((jetpt[0]>=ptbins[1] and jetpt[0]<ptbins[2]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
        nbOfjets[4]+=1
	 
        if (nbOfjets[4]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[4]+=1
      elif ((jetpt[0]>=ptbins[1] and jetpt[0]<ptbins[2]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
        nbOfjets[5]+=1
	 
        if (nbOfjets[5]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[5]+=1
      elif ((jetpt[0]>=ptbins[2] and jetpt[0]<ptbins[3]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
        nbOfjets[6]+=1
	 
        if (nbOfjets[6]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[6]+=1
      elif ((jetpt[0]>=ptbins[2] and jetpt[0]<ptbins[3]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
        nbOfjets[7]+=1
	 
        if (nbOfjets[7]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[7]+=1
      elif ((jetpt[0]>=ptbins[2] and jetpt[0]<ptbins[3]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
        nbOfjets[8]+=1
	 
        if (nbOfjets[8]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[8]+=1
      elif ((jetpt[0]>=ptbins[3] and jetpt[0]<ptbins[4]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
        nbOfjets[9]+=1
	  
        if (nbOfjets[9]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[9]+=1
      elif ((jetpt[0]>=ptbins[3] and jetpt[0]<ptbins[4]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
        nbOfjets[10]+=1
	  
        if (nbOfjets[10]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[10]+=1
      elif ((jetpt[0]>=ptbins[3] and jetpt[0]<ptbins[4]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
        nbOfjets[11]+=1
	  
        if (nbOfjets[11]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[11]+=1
      elif ((jetpt[0]>=ptbins[4] and jetpt[0]<ptbins[5]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
        nbOfjets[12]+=1
	  
        if (nbOfjets[12]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[12]+=1
      elif ((jetpt[0]>=ptbins[4] and jetpt[0]<ptbins[5]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[2])):
        nbOfjets[13]+=1
	  
        if (nbOfjets[13]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[13]+=1
      elif ((jetpt[0]>=ptbins[4] and jetpt[0]<ptbins[5]) and (abs(jeteta[0])>=etabins[2] and abs(jeteta[0])<etabins[3])):
        nbOfjets[14]+=1
	  
        if (nbOfjets[14]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[14]+=1
      elif ((jetpt[0]>=ptbins[5] and jetpt[0]<ptbins[6]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
        nbOfjets[15]+=1
	  
        if (nbOfjets[15]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[15]+=1
      elif ((jetpt[0]>=ptbins[5] and jetpt[0]<ptbins[6]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[3])):
        nbOfjets[16]+=1
	  
        if (nbOfjets[16]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[16]+=1
      elif ((jetpt[0]>=ptbins[6] and jetpt[0]<ptbins[7]) and (abs(jeteta[0])>=etabins[0] and abs(jeteta[0])<etabins[1])):
        nbOfjets[17]+=1
	  
        if (nbOfjets[17]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[17]+=1
      elif ((jetpt[0]>=ptbins[6] and jetpt[0]<ptbins[7]) and (abs(jeteta[0])>=etabins[1] and abs(jeteta[0])<etabins[3])):
        nbOfjets[18]+=1
	  
        if (nbOfjets[18]<max_nb_ofjets):
          newtree.Fill()
          nbOfjetsKept[18]+=1
	  
	
	
    for j in range(19):
      print "Tree %s has %i in pt/eta bin %i and we keep %i"%(FileName,nbOfjets[j],j,nbOfjetsKept[j])
      
    newtree.Print()
    newtree.AutoSave()
	
      
  newfile.Write()
  newfile.Close()
  return

def main():
  ROOT.gROOT.SetBatch(True)
  parallelProcesses = multiprocessing.cpu_count()  
  
  InDirectory = "/scratch/vlambert/CSV_AK5_JTA03/Clean_Run/QCD_flat/"
  OutDirectory = "/scratch/vlambert/CSV_AK5_JTA03/Clean_Run/QCD_flat_skimmed/"
  
  if not os.path.exists(OutDirectory):
    print "Creating new output directory: %s"%OutDirectory
    os.makedirs(OutDirectory)


  max_nb_ofjets=20000
  ptbins = [15,40,60,90,150,400,600,10000]
  etabins = [0,1.2,2.1,2.4] 

  print "Using %i parallel processes" %parallelProcesses
  #p = multiprocessing.Pool(parallelProcesses)
  #create pool
  for inFileName in os.listdir(InDirectory):
    category = inFileName.rsplit("_",1)[0]    
    TreeName = "tree"
    #TreeName = category
    Filter(inFileName, InDirectory, OutDirectory, TreeName, max_nb_ofjets, ptbins, etabins)
    #p.apply_async(Filter , args = (inFileName, InDirectory, OutDirectory, TreeName, max_nb_ofjets, ptbins, etabins))
  
  #p.close()
  #p.join()

  print "done"

if __name__ == "__main__":
  main()
