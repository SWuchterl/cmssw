import FWCore.ParameterSet.Config as cms

from .Run3.runHLTPaths_cfg import fixMenu
from .Run3.fixIsoTrackHBHE import fixIsoTrackHBHE

## New Tracking (patatrack tracks + single iteration)
from .Run3.customizeHLTforRun3Tracking import customizeHLTforRun3Tracking
def TRK_newTracking(process): 
    process = customizeHLTforRun3Tracking(process)
    process = fixMenu(process)
    process = fixIsoTrackHBHE(process)
    return process


## New L2 Tau reconstruction
from .Run3.applyL2TauTag import update as TAU_newL2sequence

## New tracking (patatrack tracks + single iteration) in muon reco
from .Run3.customizeMuonHLTForRun3 import customizeMuonHLTForPatatrackWithIsoAndTriplets
def MUO_newTracking(process): 
    process = customizeMuonHLTForPatatrackWithIsoAndTriplets(process, newProcessName = "@currentProcess", loadPatatrack=False)
    return process

## New ML-based inside-out seeding for muon reconstruction
from .Run3.customizeMuonHLTForRun3 import customizeIOSeedingPatatrack
def MUO_newIO(process): 
    process = customizeIOSeedingPatatrack(process, newProcessName = "@currentProcess")
    return process

## New ML-based outside-in muon for muon reconstruction
from RecoMuon.TrackerSeedGenerator.customizeOIseeding import customizeOIseeding as MUO_newOI

## Replace regional pixel tracks with global pixel tracks in TkMu triggers
from .Run3.customizeMuonHLTForRun3 import customizeMuonHLTForPatatrackTkMu
def MUO_updateTkMu(process): 
    process = customizeMuonHLTForPatatrackWithIsoAndTriplets(process, newProcessName = "@currentProcess", loadPatatrack=False)
    return process

## Replace regional pixel tracks with global pixel tracks in OpenMu triggers
from .Run3.customizeMuonHLTForRun3 import customizeMuonHLTForPatatrackOpenMu
def MUO_updateOpenMu(process): 
    process = customizeMuonHLTForPatatrackWithIsoAndTriplets(process, newProcessName = "@currentProcess", loadPatatrack=False)
    return process

## Replace regional pixel tracks with global pixel tracks in NoVtx triggers
from .Run3.customizeMuonHLTForRun3 import customizeMuonHLTForPatatrackNoVtx
def MUO_updateNoVtx(process): 
    process = customizeMuonHLTForPatatrackWithIsoAndTriplets(process, newProcessName = "@currentProcess", loadPatatrack=False)
    return process

############################## BTV ##############################

def fixBtagPrescaler(process):
    els = process.__dict__
    for el in list(els):
        if type(els[el]) == cms.Path and ("ROIForBTag" in el or "DeepJet" in el):
            path = getattr(process,el)
            prescalerName = ""
            i = 0
            while(not("hltPre" in prescalerName)):
                i += 1
                prescalerName = path.directDependencies()[i][1]
            if "ROIForBTag" in el:
                newprescalerName = prescalerName.replace("CSV","CSVROIForBTag")
                setattr(process, newprescalerName, getattr(process,prescalerName).clone())
                path.replace(getattr(process,prescalerName), getattr(process,newprescalerName))
#                print(el,prescalerName,newprescalerName)
            if "DeepJet" in el:
                newprescalerName = prescalerName.replace("DeepCSV","DeepJet")
                setattr(process, newprescalerName, getattr(process,prescalerName).clone())
                path.replace(getattr(process,prescalerName), getattr(process,newprescalerName))
#                print(el,prescalerName,newprescalerName)
    return process

## Calo b-tagging: none
## PF b-tagging: new regional PF b-tagging [new sequence]
from .Run3.customise_TRK_replacement import customiseRun3BTagRegionalTracks_Replacement
def BTV_noCalo_roiPF(process): 
    process = customiseRun3BTagRegionalTracks_Replacement(process)
    process = fixBtagPrescaler(process)
    return process 

## Calo b-tagging: new regional calo b-tagging [new sequence]
## PF b-tagging: new regional PF b-tagging [new sequence]
from .Run3.customizeRun3_BTag_ROICalo_ROIPF import customizeRun3_BTag_ROICalo_ROIPF
def BTV_roiCalo_roiPF_DeepCSV(process): 
    process = customizeRun3_BTag_ROICalo_ROIPF(process, addDeepJetPaths=False)
    process = fixBtagPrescaler(process)
    return process 

## Calo b-tagging: new regional calo b-tagging [new sequence]
## PF b-tagging: new global PF b-tagging
from .Run3.customizeRun3_BTag_ROICalo_GlobalPF import customizeRun3_BTag_ROICalo_GlobalPF
def BTV_roiCalo_globalPF_DeepCSV(process): 
    process = customizeRun3_BTag_ROICalo_GlobalPF(process, addDeepJetPaths=True)
    process = fixBtagPrescaler(process)
    return process 

## Calo b-tagging: new regional calo b-tagging [new sequence]
## PF b-tagging: new regional PF b-tagging [new sequence]
from .Run3.customizeRun3_BTag_ROICalo_ROIPF import customizeRun3_BTag_ROICalo_ROIPF
def BTV_roiCalo_roiPF_DeepJet(process): 
    process = customizeRun3_BTag_ROICalo_ROIPF(process, addDeepJetPaths=True)
    process = fixBtagPrescaler(process)
    return process 

## Calo b-tagging: new regional calo b-tagging [new sequence]
## PF b-tagging: new global PF b-tagging
from .Run3.customizeRun3_BTag_ROICalo_GlobalPF import customizeRun3_BTag_ROICalo_GlobalPF
def BTV_roiCalo_globalPF_DeepJet(process): 
    process = customizeRun3_BTag_ROICalo_GlobalPF(process, addDeepJetPaths=False)
    process = fixBtagPrescaler(process)
    return process 

## Calo b-tagging: new "global" calo b-tagging
## PF b-tagging: new global PF b-tagging
from .Run3.customise_TRK_replacement_globalGlobal_calo import customiseRun3BTagRegionalTracks_Replacement_global_globalCalo
def BTV_globalCalo_globalPF(process): 
    process = customiseRun3BTagRegionalTracks_Replacement_global_globalCalo(process)
    process = fixBtagPrescaler(process)
    return process 

from .Run3.customise_TRK import addDeepJet
from .Run3.customise_TRK_deepjet import customiseRun3BTagRegionalTracks_DeepJet

#customiseRun3BTagRegionalTracks_DeepJet
## Add MC_PFBTagDeepJet
def BTV_addMCDeepJetPath(process):
    process = addDeepJet(process, doPF=True, doPuppi=False, roiReplace=False) 
    process = fixBtagPrescaler(process)
    return process

## Add MC_PFBTagDeepJet
def BTV_addMCDeepJetROIForBTagPath(process):
    process = addDeepJet(process, doPF=True, doPuppi=False, roiReplace=True) 
    process = fixBtagPrescaler(process)
    return process

##Add a DeepJet version to all the paths with PF b-tagging
def BTV_moveToDeepJet(process): 
    process = addDeepJet(process, doPF=True, doPuppi=False, roiReplace=False)
    process = customiseRun3BTagRegionalTracks_DeepJet(process)
    process = fixBtagPrescaler(process)
    return process

##Add a DeepJet version based on ROI PF to all the paths with PF b-tagging
def BTV_moveToDeepJetROI(process): 
    process = addDeepJet(process, doPF=True, doPuppi=False, roiReplace=True)
    process = customiseRun3BTagRegionalTracks_DeepJet(process)
    process = fixBtagPrescaler(process)
    return process


