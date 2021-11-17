# hltGetConfiguration /dev/CMSSW_12_1_0/GRun/V13 > hlt.py

common_text='''
from hlt import process,_customInfo
from HLTrigger.Configuration.customizeHLTforRun3 import *
'''

for_confdb='''
### Drop for confdb ###
els = process.__dict__
for el in list(els):
    if  (type(els[el]) == cms.OutputModule) or (type(els[el]) == cms.EndPath)   or (type(els[el]) == cms.Service) or (type(els[el]) == cms.PSet) or (type(els[el]) == cms.ESProducer):
#        print("Deleting %s (%s)"%(el, type(els[el])))
        delattr(process, el)
'''

for_test='''
_customInfo["globalTag" ]= "auto:run2_data"
_customInfo["inputFile" ]=  ["file:/eos/cms/store/data/Run2018D/EphemeralHLTPhysics7/RAW/v1/000/323/790/00000/B543D251-40F1-CB46-A6A1-046CF3D78D6D.root"]
from HLTrigger.Configuration.customizeHLTforALL import customizeHLTforAll
process = customizeHLTforAll(process,"GRun",_customInfo)

#User-defined customization functions
from HLTrigger.Configuration.customizeHLTforCMSSW import customiseFor2018Input
process = customiseFor2018Input(process)

### Drop EndPaths ###
els = process.__dict__
for el in list(els):
    if  (type(els[el]) == cms.OutputModule) or (type(els[el]) == cms.EndPath) or el == "PrescaleService" or el == "datasets" or el == "streams":
        #print("Deleting %s (%s)"%(el, type(els[el])))
        delattr(process, el)
'''

#for funct in MUO_newIO;
#for funct in combined;
for funct in TRK_newTracking MUO_newTracking MUO_updateTkMu MUO_updateOpenMu MUO_updateNoVtx MUO_newIO MUO_newOI BTV_roiCalo_roiPF_DeepCSV BTV_roiCalo_globalPF_DeepCSV BTV_roiCalo_roiPF_DeepJet BTV_roiCalo_globalPF_DeepJet BTV_noCalo_roiPF BTV_globalCalo_globalPF BTV_addMCDeepJetPath BTV_addMCDeepJetROIForBTagPath BTV_moveToDeepJet BTV_moveToDeepJetROI combined;
do 
    fname=$funct".py"
    fnameDump=$funct"_dump.py"
    fnameLog=$fnameDump".log"
    echo "$common_text" > $fname
    if [ "$funct" = "combined" ]; then
        for funct2 in TRK_newTracking MUO_newTracking MUO_updateTkMu MUO_updateOpenMu MUO_updateNoVtx MUO_newIO MUO_newOI BTV_roiCalo_roiPF_DeepCSV BTV_roiCalo_roiPF_DeepJet;
        do
            echo -e "process = "$funct2"(process)\n" >> $fname
        done;
    else
        if [ "$funct" != "TRK_newTracking" ]; then
            echo -e "process = TRK_newTracking(process)\n" >> $fname
        fi;
        if [ "$funct" = "MUO_newIO" ]; then
            echo -e "process = MUO_newTracking(process)\n" >> $fname
        fi;
        if [ "$funct" = "BTV_addMCDeepJetROIForBTagPath" ]; then
            echo -e "process = BTV_noCalo_roiPF(process)\n" >> $fname
        fi;
        if [ "$funct" = "BTV_moveToDeepJetROI" ]; then
            echo -e "process = BTV_noCalo_roiPF(process)\n" >> $fname
            echo -e "process = BTV_addMCDeepJetPath(process)\n" >> $fname
        fi;
        echo -e "process = "$funct"(process)\n" >> $fname
    fi;
   echo -e $for_confdb >> $fname && edmConfigDump --prune $fname > $fnameDump & ## Run Dump for update on ConfDB
#    echo -e "$for_test" >> $fname && edmConfigDump --prune $fname > $fnameDump && CUDA_DEVICES= cmsRun $fnameDump >& $fnameLog & ## Run Test
done;

#process = TRK_newTracking(process)  New Tracking (patatrack tracks + single iteration)
######process = TAU_newL2sequence(process) # New L2 Tau reconstruction ### ERROR
#process = MUO_newTracking(process) ## New tracking (patatrack tracks + single iteration) in muon reco
#process = MUO_updateTkMu(process) ## Replace regional pixel tracks with global pixel tracks in TkMu triggers
#process = MUO_updateOpenMu(process) ## Replace regional pixel tracks with global pixel tracks in OpenMu triggers
#process = MUO_updateNoVtx(process) ## Replace regional pixel tracks with global pixel tracks in NoVtx triggers
#######process = MUO_newIO(process) ## New ML-based inside-out seeding for muon reconstruction #Conflict with #MUO_newTracking
#process = MUO_newOI(process) ## New ML-based outside-in muon for muon reconstruction

#process = BTV_roiCalo_roiPF_DeepCSV(process) ## Calo b-tagging: new regional calo b-tagging [new sequence] ## PF b-tagging: new regional DeepCSV PF b-tagging [new sequence] 
#process = BTV_roiCalo_globalPF_DeepCSV(process) ## Calo b-tagging: new regional calo b-tagging [new sequence] ## PF b-tagging: new global DeepCSV PF b-tagging 

#process = BTV_roiCalo_roiPF_DeepJet(process) ## Calo b-tagging: new regional calo b-tagging [new sequence] ## PF b-tagging: new regional DeepJet PF b-tagging [new sequence] 
#process = BTV_roiCalo_globalPF_DeepJet(process) # Calo b-tagging: new regional calo b-tagging [new sequence] ## PF b-tagging: new global DeepJet PF b-tagging 

#process = BTV_noCalo_roiPF(process) ## Calo b-tagging: none ## PF b-tagging: new regional PF b-tagging [new sequence]
#process = BTV_globalCalo_globalPF(process) ## Calo b-tagging: new "global" calo b-tagging ## PF b-tagging: new global PF b-tagging

#process = BTV_addMCDeepJetPath(process) ## Add MC_PFBTagDeepJet
#process = BTV_addMCDeepJetROIForBTagPath(process) ## Add MC_PFBTagDeepJetROIForBTag

#process = BTV_moveToDeepJet(process) ##Add a DeepJet version to all the paths with PF b-tagging
#process = BTV_moveToDeepJetROI(process)  ##Add a DeepJet version based on ROI PF to all the paths with PF b-tagging


#### Drop EndPaths ###
#els = process.__dict__
#for el in list(els):
#    if  (type(els[el]) == cms.OutputModule) or (type(els[el]) == cms.EndPath) or el == "PrescaleService" or el == "datasets" or el == "streams":
#        print("Deleting %s (%s)"%(el, type(els[el])))
#        delattr(process, el)

