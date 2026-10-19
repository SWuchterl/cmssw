import FWCore.ParameterSet.Config as cms

ntuplizer_muon = cms.EDAnalyzer('MuonNtuplizer',
                           src = cms.InputTag("muonParTTrainVariables"),
                           srcLeptons = cms.InputTag("linkedObjects","muons"),
                           srcMcTable = cms.InputTag("muonMCTable"),
                           leptonSelection = cms.string("pt > 5 && abs(eta)< 2.4 && passed('CutBasedIdLoose')"),
)


def customize_ntuplizer(process):
    process.ntuplizer_muon = ntuplizer_muon
    process.nanoSequenceMC.insert(process.nanoSequenceMC.index(process.nanoSequenceOnlyFullSim)+1, process.ntuplizer_muon)
    process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string("tree.root"),
                                       closeFileFast = cms.untracked.bool(True)
                                   )

    return process 


# ---------------------------------------------------------------------------
# Training ntuple (Run 3): own feature producer, independent of the inputs of the ONNX models in NanoAOD
# ---------------------------------------------------------------------------
from ParticleNetNtuplizer.ParticleNetNtuplizer.electron_ntuplizer import _cpfVars, _npfVars, _ltVars, _svVars, _trainingMaxLengths, _lean_linked_objects
from ParticleNetNtuplizer.ParticleNetNtuplizer.electron_ntuplizer import _asinh
from PhysicsTools.NanoAOD.muons_cff import muonPOGHighLevelVars

_muPfIso03 = "(pfIsolationR03().sumChargedHadronPt + max(pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - pfIsolationR03().sumPUPt/2,0.0))/pt"

muonParTLLTrainingFeatures = cms.EDProducer(
    "MuonTagInfoCollectionProducer",
    src=cms.InputTag("linkedObjects", "muons"),
    pvSrc=cms.InputTag("offlineSlimmedPrimaryVertices"),
    secondary_vertices=cms.InputTag("slimmedSecondaryVertices"),
    pfCandidates=cms.InputTag("packedPFCandidates"),
    ltCandidates=cms.InputTag("lostTracks"),
    trainingMode=cms.bool(True),
    # v5 branches made in C++ (CPF_dxyRes_asinh, LT_dxyRes_asinh), as in the electron tree
    v5Features=cms.bool(True),
    # full float32 precision as in the CMSSW inference: 12 bits made ParT pair ln m2 noise for close pairs (+27% size)
    reduceMantissaBits=cms.int32(0),
    rhoSrc=cms.InputTag("fixedGridRhoFastjetAll"),
    eventVars=cms.PSet(
        rhoCentral=cms.InputTag("fixedGridRhoFastjetCentral"),
        rhoCentralNeutral=cms.InputTag("fixedGridRhoFastjetCentralNeutral"),
        rhoCentralChargedPileUp=cms.InputTag("fixedGridRhoFastjetCentralChargedPileUp"),
    ),
    leptonVars=cms.PSet(
        # MuonPOG high-level track variables (requested by MuonPOG), same definitions as muonParTTrainVariables
        muonPOGHighLevelVars,
        Lepton_mask=cms.string("1"),
        Lepton_pt=cms.string("pt"),
        Lepton_pt_log=cms.string("log(max(pt,1.e-8))"),
        Lepton_eta=cms.string("eta"),
        Lepton_phi=cms.string("phi"),
        Lepton_px=cms.string("px"),
        Lepton_py=cms.string("py"),
        Lepton_pz=cms.string("pz"),
        Lepton_energy=cms.string("energy"),
        Lepton_energy_log=cms.string("log(max(energy,1.e-8))"),
        Lepton_charge=cms.string("charge"),
        Lepton_jetNDauChargedMVASel=cms.string("?userCand('jetForLepJetVar').isNonnull()?userFloat('jetNDauChargedMVASel'):0"),
        Lepton_miniRelIsoCharged=cms.string("userFloat('miniIsoChg')/pt"),
        Lepton_miniRelIsoCharged_log=cms.string("log(max(userFloat('miniIsoChg')/pt,1.e-8))"),
        Lepton_miniPFRelIso_all=cms.string("userFloat('miniIsoAll')/pt"),
        Lepton_miniRelIsoNeutral=cms.string("(userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt"),
        Lepton_miniRelIsoNeutral_log=cms.string("log(max((userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt,1.e-8))"),
        Lepton_pfRelIso03_all=cms.string(_muPfIso03),
        Lepton_pfRelIso03_all_log=cms.string("log(max(" + _muPfIso03 + ",1.e-8))"),
        Lepton_jetPtRelv2_log=cms.string("?userCand('jetForLepJetVar').isNonnull()?log(max(abs(userFloat('ptRel')),1.e-8)):0.0"),
        # asinh(ptRel / 1 GeV) as in the electron tree; _log above is kept for the old muon models
        Lepton_jetPtRelv2_asinh=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?" + _asinh("userFloat('ptRel')", 1.0) + ":0"),
        Lepton_jetPtRatio=cms.string("?userCand('jetForLepJetVar').isNonnull()?min(userFloat('ptRatio'),1.5):1.0/(1.0+(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt)"),
        Lepton_dxy=cms.string("dB('PV2D')"),
        Lepton_dxy_sig=cms.string("?edB('PV2D')>0?dB('PV2D')/edB('PV2D'):0"),
        Lepton_dxy_asinh=cms.string("log(abs(dB('PV2D')+sqrt(dB('PV2D')*dB('PV2D')+1.0+1.e-8)))"),
        Lepton_dxy_sig_asinh=cms.string("?edB('PV2D')>0?log(abs((dB('PV2D')/edB('PV2D'))+sqrt((dB('PV2D')/edB('PV2D'))*(dB('PV2D')/edB('PV2D')) + 1))+1.e-8):0"),
        Lepton_sip3d=cms.string("dB('PV3D')"),
        Lepton_sip3d_asinh=cms.string("log(abs(dB('PV3D')+sqrt(dB('PV3D')*dB('PV3D')+1.0+1.e-8)))"),
        Lepton_sip3d_sig=cms.string("?edB('PV3D')>0?dB('PV3D')/edB('PV3D'):0"),
        Lepton_sip3d_sig_asinh=cms.string("?edB('PV3D')>0?log(abs((dB('PV3D')/edB('PV3D'))+sqrt((dB('PV3D')/edB('PV3D'))*(dB('PV3D')/edB('PV3D')) + 1))+1.e-8):0"),
        Lepton_dz=cms.string("dB('PVDZ')"),
        Lepton_dz_asinh=cms.string("log(abs(dB('PVDZ')+sqrt(dB('PVDZ')*dB('PVDZ')+1.0+1.e-8)))"),
        Lepton_dz_sig_asinh=cms.string("?edB('PVDZ')>0?log(abs((dB('PVDZ')/edB('PVDZ'))+sqrt((dB('PVDZ')/edB('PVDZ'))*(dB('PVDZ')/edB('PVDZ'))+1.0+1.e-8))):0"),
        # v5: impact parameters in units of the resolution (the *_asinh above are asinh(x / 1 cm), kept), as for electrons
        Lepton_dxyRes_asinh=cms.string(_asinh("dB('PV2D')", 0.005)),
        Lepton_dzRes_asinh=cms.string(_asinh("dB('PVDZ')", 0.02)),
        Lepton_sip3dRes_asinh=cms.string(_asinh("dB('PV3D')", 0.02)),
        # muon specific variables
        Lepton_segmentComp=cms.string("segmentCompatibility"),
        Lepton_global_muon=cms.string("isGlobalMuon"),
        Lepton_validFraction=cms.string("?innerTrack.isNonnull()?innerTrack().validFraction:-1"),
        # -1 when the STA-TK propagation failed: 0, the missing-value rule of the tree (as Lepton_momentumChi2)
        Lepton_local_chi2=cms.string("max(combinedQuality().chi2LocalPosition,0)"),
        Lepton_kink=cms.string("combinedQuality().trkKink"),
        Lepton_n_MatchedStations=cms.string("numberOfMatchedStations()"),
        Lepton_Valid_pixel=cms.string("?innerTrack.isNonnull()?innerTrack().hitPattern().numberOfValidPixelHits():-1"),
        Lepton_tracker_layers=cms.string("?innerTrack.isNonnull()?innerTrack().hitPattern().trackerLayersWithMeasurement():-1"),
        Lepton_mvaId=cms.string("userFloat('mvaIDMuon')"),
        # other IDs and isolations, for comparison only (not model inputs)
        Lepton_ID_looseId=cms.string("passed('CutBasedIdLoose')"),
        Lepton_ID_mediumId=cms.string("passed('CutBasedIdMedium')"),
        Lepton_ID_mediumPromptId=cms.string("passed('CutBasedIdMediumPrompt')"),
        Lepton_ID_tightId=cms.string("passed('CutBasedIdTight')"),
        Lepton_ID_softId=cms.string("passed('SoftCutBasedId')"),
        Lepton_ID_softMvaId=cms.string("passed('SoftMvaId')"),
        Lepton_ID_softMva=cms.string("softMvaValue()"),
        Lepton_ID_softMvaRun3=cms.string("softMvaRun3Value()"),
        Lepton_ID_highPtId=cms.string("?passed('CutBasedIdGlobalHighPt')?2:passed('CutBasedIdTrkHighPt')"),
        Lepton_ID_mvaMuID_WP=cms.string("userFloat('mvaIDMuon_wpMedium') + userFloat('mvaIDMuon_wpTight')"),
        Lepton_ID_pfIsoId=cms.string("passed('PFIsoVeryLoose')+passed('PFIsoLoose')+passed('PFIsoMedium')+passed('PFIsoTight')+passed('PFIsoVeryTight')+passed('PFIsoVeryVeryTight')"),
        Lepton_ID_tkIsoId=cms.string("?passed('TkIsoTight')?2:passed('TkIsoLoose')"),
        Lepton_ID_miniIsoId=cms.string("passed('MiniIsoLoose')+passed('MiniIsoMedium')+passed('MiniIsoTight')+passed('MiniIsoVeryTight')"),
        Lepton_ID_multiIsoId=cms.string("?passed('MultiIsoMedium')?2:passed('MultiIsoLoose')"),
        Lepton_ID_puppiIsoId=cms.string("passed('PuppiIsoLoose')+passed('PuppiIsoMedium')+passed('PuppiIsoTight')"),
        Lepton_ISO_tkRelIso=cms.string("isolationR03().sumPt/pt"),
        Lepton_ISO_pfRelIso03_chg=cms.string("pfIsolationR03().sumChargedHadronPt/pt"),
        Lepton_ISO_pfRelIso04_all=cms.string("(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt"),
    ),
    leptonVarsExt=cms.PSet(
        Lepton_ID_promptMVA=cms.InputTag("muonPROMPTMVA"),
        Lepton_ID_mvaLowPt=cms.InputTag("muonMVALowPt"),
        Lepton_ID_PNet_prompt=cms.InputTag("muonPNetScores:prompt"),
        Lepton_ID_PNet_heavy=cms.InputTag("muonPNetScores:heavy"),
        Lepton_ID_PNet_light=cms.InputTag("muonPNetScores:light"),
        Lepton_ID_PNet_tau=cms.InputTag("muonPNetScores:tau"),
        Lepton_ID_ParTLL_prompt=cms.InputTag("muonParTLLScores:prompt"),
        Lepton_ID_ParTLL_tau=cms.InputTag("muonParTLLScores:tau"),
        Lepton_ID_ParTLL_heavy=cms.InputTag("muonParTLLScores:heavy"),
        Lepton_ID_ParTLL_light=cms.InputTag("muonParTLLScores:light"),
        Lepton_ID_ParTLL_fake=cms.InputTag("muonParTLLScores:fake"),
    ),
    pfVars=cms.PSet(),
    cpfVars=_cpfVars,
    npfVars=_npfVars,
    ltVars=_ltVars,
    svVars=_svVars,
)

ntuplizer_muon_training = ntuplizer_muon.clone(
    src="muonParTLLTrainingFeatures",
    maxLengths=_trainingMaxLengths,
    genMatch=cms.InputTag("muonsMCMatchForTable"),
    prunedGenParticles=cms.InputTag("prunedGenParticles"),
    packedGenParticles=cms.InputTag("packedGenParticles"),
    pileupInfo=cms.InputTag("slimmedAddPileupInfo"),
)


def customize_training_ntuplizer(process):
    process.muonParTLLTrainingFeatures = muonParTLLTrainingFeatures
    process.muonTablesTask.add(process.muonParTLLTrainingFeatures)
    # string features bound once at construction instead of resolved on every call: same values, faster
    for label in ('muonParTLLTrainingFeatures', 'muonParTVariables', 'muonPNetVariables'):
        getattr(process, label).lazyEval = cms.untracked.bool(False)
    process = _lean_linked_objects(process)
    process.ntuplizer_muon = ntuplizer_muon_training
    # features and scores only for the leptons the tree keeps (the others get empty features and score -1)
    for label in ('muonParTLLTrainingFeatures', 'muonParTVariables', 'muonPNetVariables', 'muonParTLLScores', 'muonPNetScores'):
        getattr(process, label).leptonSelection = cms.string(process.ntuplizer_muon.leptonSelection.value())
    process.nanoSequenceMC.insert(process.nanoSequenceMC.index(process.nanoSequenceOnlyFullSim)+1, process.ntuplizer_muon)
    process.TFileService = cms.Service("TFileService",
                                       fileName=cms.string("tree.root"),
                                       closeFileFast=cms.untracked.bool(True)
                                       )
    return process
