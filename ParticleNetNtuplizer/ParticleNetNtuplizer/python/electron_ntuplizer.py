import FWCore.ParameterSet.Config as cms

ntuplizer_electron = cms.EDAnalyzer('ElectronNtuplizer',
                           src = cms.InputTag("electronParTTrainVariables"),
                           srcLeptons = cms.InputTag("linkedObjects","electrons"),
                           srcMcTable = cms.InputTag("electronMCTable"),
                           leptonSelection = cms.string("pt > 5 && abs(eta)< 2.4 && (userFloat('miniIsoAll')/pt < 0.4) && (abs(dB('PV3D')/edB('PV3D')) < 8) && (abs(dB('PV2D')) < 0.05) && (abs(dB('PVDZ')) < 0.1)"),
)


def customize_ntuplizer(process):
    process.ntuplizer_electron = ntuplizer_electron
    process.nanoSequenceMC.insert(process.nanoSequenceMC.index(process.nanoSequenceOnlyFullSim)+1, process.ntuplizer_electron)
    process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string("tree.root"),
                                       closeFileFast = cms.untracked.bool(True)
                                   )

    return process 
