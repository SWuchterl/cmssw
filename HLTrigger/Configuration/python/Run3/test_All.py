from hlt_data2018 import process
from HLTrigger.Configuration.customizeHLTforRun3 import *

process = TRK_newTracking(process) # New Tracking (patatrack tracks + single iteration)
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
process = BTV_roiCalo_globalPF_DeepJet(process) ## Calo b-tagging: new regional calo b-tagging [new sequence] ## PF b-tagging: new global DeepJet PF b-tagging 

#process = BTV_noCalo_roiPF(process) ## Calo b-tagging: none ## PF b-tagging: new regional PF b-tagging [new sequence]
#process = BTV_globalCalo_globalPF(process) ## Calo b-tagging: new "global" calo b-tagging ## PF b-tagging: new global PF b-tagging

#process = BTV_addMCDeepJetPath(process) ## Add MC_PFBTagDeepJet
#process = BTV_addMCDeepJetROIForBTagPath(process) ## Add MC_PFBTagDeepJetROIForBTag

#process = BTV_moveToDeepJet(process) ##Add a DeepJet version to all the paths with PF b-tagging
#process = BTV_moveToDeepJetROI(process)  ##Add a DeepJet version based on ROI PF to all the paths with PF b-tagging


### Drop EndPaths ###
els = process.__dict__
for el in list(els):
    if  (type(els[el]) == cms.OutputModule) or (type(els[el]) == cms.EndPath) or el == "PrescaleService" or el == "datasets" or el == "streams":
        print("Deleting %s (%s)"%(el, type(els[el])))
        delattr(process, el)

