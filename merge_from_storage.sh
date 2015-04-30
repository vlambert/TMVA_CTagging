#!/bin/bash

maindirec=/pnfs/psi.ch/cms/trivcat/store/user/vlambert/TMVA/CSVSLctag_73X/CSVSLctag_IVFadapv1/VtxCharge_looseIVF

dirs_to_merge=(QCD_Pt-1000toInf_Tune4C_13TeV_pythia8_Phys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1_AODSIM_try2/QCD_HT_1000ToInf_13TeV-madgraph/crab_VariableExtraction73X_test2Phys14Sample_QCDHt1000toInf_vtxcharge_try2/150416_090846/0000 QCD_Pt-120to170_Tune4C_13TeV_pythia8_Phys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1_AODSIM/QCD_Pt-120to170_Tune4C_13TeV_pythia8/crab_VariableExtraction73X_test2Phys14Sample_QCDPt120to170_vtxcharge/150414_132349/0000 QCD_Pt-250to500_Tune4C_13TeV_pythia8_Phys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1_AODSIM/QCD_HT_250To500_13TeV-madgraph/crab_VariableExtraction73X_test2Phys14Sample_QCDHt250to500_vtxcharge/150414_132430/0000 QCD_Pt-30to50_Tune4C_13TeV_pythia8_Phys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1_AODSIM/QCD_Pt-30to50_Tune4C_13TeV_pythia8/crab_VariableExtraction73X_test2Phys14Sample_QCDPt30to50_vtxcharge/150414_132451/0000 QCD_Pt-500to1000_Tune4C_13TeV_pythia8_Phys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1_AODSIM/QCD_HT-500To1000_13TeV-madgraph/crab_VariableExtraction73X_test2Phys14Sample_QCDHt500to1000_vtxcharge/150414_133046/0000 QCD_Pt-80to120_Tune4C_13TeV_pythia8_Phys14DR-PU20bx25_trkalmb_castor_PHYS14_25_V1-v1_AODSIM/QCD_Pt-80to120_Tune4C_13TeV_pythia8/crab_VariableExtraction73X_test2Phys14Sample_QCDPt80to120_vtxcharge/150414_150257/0000) 

#dirs_to_merge=( 0000 )
#dirs_to_merge=( TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola_Summer12_DR53X-PU_S10_START53_V7A-v1_AODSIM )

homedirec=/scratch/vlambert/Phys14AOD/NewVariables_LooseDistSig/QCD

CAT=(CombinedSVRecoVertexSoftElectron CombinedSVPseudoVertexSoftElectron CombinedSVNoVertexSoftElectron CombinedSVRecoVertexNoSoftLepton CombinedSVPseudoVertexNoSoftLepton CombinedSVNoVertexNoSoftLepton CombinedSVRecoVertexSoftMuon CombinedSVPseudoVertexSoftMuon CombinedSVNoVertexSoftMuon)
FLAV=(B C DUSG)

#mkdir $homedirec
cd $homedirec

for l in ${dirs_to_merge[@]} ;
do
	for k in ${CAT[@]} ;
	do 
		for j in $( ls $maindirec/$l/${k}_B*); do printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}Bfiles.txt; done
		for j in $( ls $maindirec/$l/${k}_C*); do printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}Cfiles.txt; done
		if [ $k=="CombinedSVV2NoVertex" ]
		then
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_D*); do
				echo "at file number $countfiles" 
				((countfiles++))
				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 5 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}DUSGfiles.txt
			done
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_U*); do 
				echo "at file number $countfiles" 
				((countfiles++))
				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 5 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}DUSGfiles.txt
			done
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_S*); do 
				echo "at file number $countfiles" 
				((countfiles++))
				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 5 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}DUSGfiles.txt
			done
			let countfiles=0
			for j in $( ls $maindirec/$l/${k}_G*); do 
				echo "at file number $countfiles" 
				((countfiles++))
				if [ $countfiles -ne 1 ] ; then if [ $countfiles -eq 5 ] ; then countfiles=0 ; fi ; continue ; fi #this makes sure that only 1/12 files is used!
				printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}DUSGfiles.txt
			done
		else
			for j in $( ls $maindirec/$l/${k}_D*); do printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}DUSGfiles.txt; done
			for j in $( ls $maindirec/$l/${k}_U*); do printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}DUSGfiles.txt; done
			for j in $( ls $maindirec/$l/${k}_S*); do printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}DUSGfiles.txt; done
			for j in $( ls $maindirec/$l/${k}_G*); do printf "root://t3dcachedb.psi.ch:1094/$j " >> ${k}DUSGfiles.txt; done			
		fi
	done
done	

for k in ${CAT[@]} ;
do
	for i in ${FLAV[@]} ;
	do
#		echo cat ${k}${i}files.txt
		rootfiles=`cat ${k}${i}files.txt`
		hadd tmp.root $rootfiles
		mv tmp.root ${k}_${i}.root
	done
done
