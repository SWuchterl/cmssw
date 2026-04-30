import FWCore.ParameterSet.Config as cms

ntuplizer_muon = cms.EDAnalyzer('MuonNtuplizer',
                           src = cms.InputTag("muonParTTrainVariables"),
                           srcLeptons = cms.InputTag("linkedObjects","muons"),
                           srcMcTable = cms.InputTag("muonMCTable"),
                           leptonSelection = cms.string("pt > 5 && abs(eta)< 2.4 && passed('CutBasedIdLoose') && (userFloat('miniIsoAll')/pt < 0.4) && (abs(dB('PV3D')/edB('PV3D')) < 8) && (abs(dB('PV2D')) < 0.05) && (abs(dB('PVDZ')) < 0.1)"),
)


def customize_ntuplizer(process):
    process.ntuplizer_muon = ntuplizer_muon
    process.nanoSequenceMC.insert(process.nanoSequenceMC.index(process.nanoSequenceOnlyFullSim)+1, process.ntuplizer_muon)
    process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string("tree.root"),
                                       closeFileFast = cms.untracked.bool(True)
                                   )

    return process 
