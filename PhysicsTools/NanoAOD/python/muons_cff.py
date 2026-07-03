from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *
from PhysicsTools.PatAlgos.muonPNetTags_cfi import muonPNetTags as _muonPNetTags
from PhysicsTools.PatAlgos.muonParTTags_cfi import muonParTTags as _muonParTTags
from PhysicsTools.PatAlgos.muonTagInfos_cfi import muonTagInfos as _muonTagInfos
import FWCore.ParameterSet.Config as cms

from PhysicsTools.NanoAOD.nano_eras_cff import *
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.simplePATMuonFlatTableProducer_cfi import simplePATMuonFlatTableProducer

import PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi

# this below is used only in some eras
slimmedMuonsUpdated = cms.EDProducer("PATMuonUpdater",
                                     src=cms.InputTag("slimmedMuons"),
                                     vertices=cms.InputTag(
                                         "offlineSlimmedPrimaryVertices"),
                                     computeMiniIso=cms.bool(False),
                                     fixDxySign=cms.bool(True),
                                     pfCandsForMiniIso=cms.InputTag(
                                         "packedPFCandidates"),
                                     # so they're in sync
                                     miniIsoParams=PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi.patMuons.miniIsoParams,
                                     recomputeMuonBasicSelectors=cms.bool(
                                         False),
                                     )

isoForMu = cms.EDProducer("MuonIsoValueMapProducer",
                          src=cms.InputTag("slimmedMuonsUpdated"),
                          relative=cms.bool(False),
                          rho_MiniIso=cms.InputTag("fixedGridRhoFastjetAll"),
                          EAFile_MiniIso=cms.FileInPath(
                              "PhysicsTools/NanoAOD/data/effAreaMuons_cone03_pfNeuHadronsAndPhotons_94X.txt"),
                          )

ptRatioRelForMu = cms.EDProducer("MuonJetVarProducer",
                                 srcJet=cms.InputTag("updatedJetsPuppi"),
                                 srcLep=cms.InputTag("slimmedMuonsUpdated"),
                                 srcVtx=cms.InputTag(
                                     "offlineSlimmedPrimaryVertices"),
                                 )

muonMVAID = cms.EDProducer("EvaluateMuonMVAID",
                           src=cms.InputTag("slimmedMuonsUpdated"),
                           weightFile=cms.FileInPath(
                               "RecoMuon/MuonIdentification/data/mvaID.onnx"),
                           backend=cms.string('ONNX'),
                           name=cms.string("muonMVAID"),
                           outputTensorName=cms.string("probabilities"),
                           inputTensorName=cms.string("float_input"),
                           outputNames=cms.vstring(
                               ["probGOOD", "wpMedium", "wpTight"]),
                           batch_eval=cms.bool(True),
                           outputFormulas=cms.vstring(
                               ["at(1)", "? at(1) > 0.08 ? 1 : 0", "? at(1) > 0.20 ? 1 : 0"]),
                           variables=cms.VPSet(
                               cms.PSet(name=cms.string("LepGood_global_muon"),
                                        expr=cms.string("isGlobalMuon")),
                               cms.PSet(name=cms.string("LepGood_validFraction"), expr=cms.string(
                                   "?innerTrack.isNonnull?innerTrack().validFraction:-99")),
                               cms.PSet(name=cms.string(
                                   "Muon_norm_chi2_extended")),
                               cms.PSet(name=cms.string("LepGood_local_chi2"),
                                        expr=cms.string("combinedQuality().chi2LocalPosition")),
                               cms.PSet(name=cms.string("LepGood_kink"),
                                        expr=cms.string("combinedQuality().trkKink")),
                               cms.PSet(name=cms.string("LepGood_segmentComp"),
                                        expr=cms.string("segmentCompatibility")),
                               cms.PSet(name=cms.string(
                                   "Muon_n_Valid_hits_extended")),
                               cms.PSet(name=cms.string("LepGood_n_MatchedStations"),
                                        expr=cms.string("numberOfMatchedStations()")),
                               cms.PSet(name=cms.string("LepGood_Valid_pixel"), expr=cms.string(
                                   "?innerTrack.isNonnull()?innerTrack().hitPattern().numberOfValidPixelHits():-99")),
                               cms.PSet(name=cms.string("LepGood_tracker_layers"), expr=cms.string(
                                   "?innerTrack.isNonnull()?innerTrack().hitPattern().trackerLayersWithMeasurement():-99")),
                               cms.PSet(name=cms.string("LepGood_pt"),
                                        expr=cms.string("pt")),
                               cms.PSet(name=cms.string("LepGood_eta"),
                                        expr=cms.string("eta")),
                           )
                           )


slimmedMuonsWithUserData = cms.EDProducer("PATMuonUserDataEmbedder",
                                          src=cms.InputTag(
                                              "slimmedMuonsUpdated"),
                                          userFloats=cms.PSet(
                                              miniIsoChg=cms.InputTag(
                                                  "isoForMu:miniIsoChg"),
                                              miniIsoAll=cms.InputTag(
                                                  "isoForMu:miniIsoAll"),
                                              ptRatio=cms.InputTag(
                                                  "ptRatioRelForMu:ptRatio"),
                                              ptRel=cms.InputTag(
                                                  "ptRatioRelForMu:ptRel"),
                                              jetNDauChargedMVASel=cms.InputTag(
                                                  "ptRatioRelForMu:jetNDauChargedMVASel"),
                                              mvaIDMuon_wpMedium=cms.InputTag(
                                                  "muonMVAID:wpMedium"),
                                              mvaIDMuon_wpTight=cms.InputTag(
                                                  "muonMVAID:wpTight"),
                                              mvaIDMuon=cms.InputTag(
                                                  "muonMVAID:probGOOD")
                                          ),
                                          userCands=cms.PSet(
                                              # warning: Ptr is null if no match is found
                                              jetForLepJetVar=cms.InputTag(
                                                  "ptRatioRelForMu:jetForLepJetVar")
                                          ),
                                          )


finalMuons = cms.EDFilter("PATMuonRefSelector",
                          src=cms.InputTag("slimmedMuonsWithUserData"),
                          cut=cms.string(
                              "pt > 15 || (pt > 3 && (passed('CutBasedIdLoose') || passed('SoftCutBasedId') || passed('SoftMvaId') || passed('CutBasedIdGlobalHighPt') || passed('CutBasedIdTrkHighPt')))")
                          )

finalLooseMuons = cms.EDFilter("PATMuonRefSelector",  # for isotrack cleaning
                               src=cms.InputTag("slimmedMuonsWithUserData"),
                               cut=cms.string(
                                   "pt > 3 && track.isNonnull && isLooseMuon")
                               )

muonPROMPTMVA = cms.EDProducer("MuonBaseMVAValueMapProducer",
                               src=cms.InputTag("linkedObjects", "muons"),
                               weightFile=cms.FileInPath(
                                   "PhysicsTools/NanoAOD/data/mu_BDTG_2022.weights.xml"),
                               backend=cms.string("TMVA"),
                               name=cms.string("muonPROMPTMVA"),
                               isClassifier=cms.bool(True),
                               variables=cms.VPSet(
                                   cms.PSet(name=cms.string(
                                       "LepGood_pt"), expr=cms.string("pt")),
                                   cms.PSet(name=cms.string(
                                       "LepGood_eta"), expr=cms.string("eta")),
                                   cms.PSet(name=cms.string("LepGood_pfRelIso03_all"), expr=cms.string(
                                       "(pfIsolationR03().sumChargedHadronPt + max(pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - pfIsolationR03().sumPUPt/2,0.0))/pt")),
                                   cms.PSet(name=cms.string("LepGood_miniRelIsoCharged"),
                                            expr=cms.string("userFloat('miniIsoChg')/pt")),
                                   cms.PSet(name=cms.string("LepGood_miniRelIsoNeutral"), expr=cms.string(
                                       "(userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt")),
                                   cms.PSet(name=cms.string("LepGood_jetNDauChargedMVASel"), expr=cms.string(
                                       "?userCand('jetForLepJetVar').isNonnull()?userFloat('jetNDauChargedMVASel'):0")),
                                   cms.PSet(name=cms.string("LepGood_jetPtRelv2"), expr=cms.string(
                                       "?userCand('jetForLepJetVar').isNonnull()?userFloat('ptRel'):0")),
                                   cms.PSet(name=cms.string("LepGood_jetDF"), expr=cms.string(
                                       "?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:probbb')+userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:probb')+userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:problepb'),0.0):0.0")),
                                   cms.PSet(name=cms.string("LepGood_jetPtRatio"), expr=cms.string(
                                       "?userCand('jetForLepJetVar').isNonnull()?min(userFloat('ptRatio'),1.5):1.0/(1.0+(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt)")),
                                   cms.PSet(name=cms.string("LepGood_sip3d"),
                                            expr=cms.string("abs(dB('PV3D')/edB('PV3D'))")),
                                   cms.PSet(name=cms.string("LepGood_dxy"),
                                            expr=cms.string("log(abs(dB('PV2D')))")),
                                   cms.PSet(name=cms.string("LepGood_dz"),
                                            expr=cms.string("log(abs(dB('PVDZ')))")),
                                   cms.PSet(name=cms.string("LepGood_segmentComp"),
                                            expr=cms.string("segmentCompatibility")),
                               )
                               )

_legacy_muon_BDT_variable = cms.VPSet(
    cms.PSet(name=cms.string("LepGood_pt"), expr=cms.string("pt")),
    cms.PSet(name=cms.string("LepGood_eta"), expr=cms.string("eta")),
    cms.PSet(name=cms.string("LepGood_jetNDauChargedMVASel"), expr=cms.string(
        "?userCand('jetForLepJetVar').isNonnull()?userFloat('jetNDauChargedMVASel'):0")),
    cms.PSet(name=cms.string("LepGood_miniRelIsoCharged"),
             expr=cms.string("userFloat('miniIsoChg')/pt")),
    cms.PSet(name=cms.string("LepGood_miniRelIsoNeutral"), expr=cms.string(
        "(userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt")),
    cms.PSet(name=cms.string("LepGood_jetPtRelv2"), expr=cms.string(
        "?userCand('jetForLepJetVar').isNonnull()?userFloat('ptRel'):0")),
    cms.PSet(name=cms.string("LepGood_jetDF"), expr=cms.string(
        "?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:probbb')+userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:probb')+userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:problepb'),0.0):0.0")),
    cms.PSet(name=cms.string("LepGood_jetPtRatio"), expr=cms.string(
        "?userCand('jetForLepJetVar').isNonnull()?min(userFloat('ptRatio'),1.5):1.0/(1.0+(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt)")),
    cms.PSet(name=cms.string("LepGood_dxy"),
             expr=cms.string("log(abs(dB('PV2D')))")),
    cms.PSet(name=cms.string("LepGood_sip3d"),
             expr=cms.string("abs(dB('PV3D')/edB('PV3D'))")),
    cms.PSet(name=cms.string("LepGood_dz"),
             expr=cms.string("log(abs(dB('PVDZ')))")),
    cms.PSet(name=cms.string("LepGood_segmentComp"),
             expr=cms.string("segmentCompatibility")),
)

muonMVALowPt = muonPROMPTMVA.clone(
    weightFile=cms.FileInPath(
        "PhysicsTools/NanoAOD/data/mu_BDTG_lowpt.weights.xml"),
    name=cms.string("muonMVALowPt"),
    variables=_legacy_muon_BDT_variable
)

run2_muon_2016.toModify(
    muonPROMPTMVA,
    weightFile="PhysicsTools/NanoAOD/data/mu_BDTG_2016.weights.xml",
    variables=_legacy_muon_BDT_variable
)

(run2_muon_2017 | run2_muon_2018).toModify(
    muonPROMPTMVA,
    weightFile=cms.FileInPath(
        "PhysicsTools/NanoAOD/data/mu_BDTG_2017.weights.xml"),
    variables=_legacy_muon_BDT_variable
)

muonPNetVariables = _muonTagInfos.clone(
    src=cms.InputTag("linkedObjects", "muons"),
    leptonVars=cms.PSet(
        MuonSelected_LepGood_pt=cms.string("pt"),
        MuonSelected_LepGood_eta=cms.string("eta"),
        MuonSelected_LepGood_jetNDauChargedMVASel=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?userFloat('jetNDauChargedMVASel'):0"),
        # for ntuplizer studies
        MuonSelected_LepGood_pfRelIso03_all=cms.string(
            "((pfIsolationR03().sumChargedHadronPt + max(pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - pfIsolationR03().sumPUPt/2,0.0))/pt)"),
        MuonSelected_LepGood_miniRelIsoCharged=cms.string(
            "userFloat('miniIsoChg')/pt"),
        MuonSelected_LepGood_miniRelIsoNeutral=cms.string(
            "(userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt"),
        MuonSelected_LepGood_jetPtRelv2=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?userFloat('ptRel'):0"),
        MuonSelected_LepGood_jetDF=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:probbb')+userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:probb')+userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:problepb'),0.0):0.0"),
        # for ntuplizer studies
        MuonSelected_LepGood_jetPNet=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:BvsAll'),0.0):0.0"),
        MuonSelected_LepGood_jetPtRatio=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?min(userFloat('ptRatio'),1.5):1.0/(1.0+(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt)"),
        MuonSelected_dxy=cms.string("log(abs(dB('PV2D')))"),
        MuonSelected_sip3d=cms.string("abs(dB('PV3D')/edB('PV3D'))"),
        MuonSelected_dz=cms.string("log(abs(dB('PVDZ')))"),
        MuonSelected_LepGood_dz=cms.string("log(abs(dB('PVDZ')))"),
        MuonSelected_segmentComp=cms.string("segmentCompatibility"),
        MuonSelected_global_muon=cms.string("isGlobalMuon"),
        MuonSelected_validFraction=cms.string(
            "?innerTrack.isNonnull?innerTrack().validFraction:-99"),
        MuonSelected_local_chi2=cms.string(
            "combinedQuality().chi2LocalPosition"),
        MuonSelected_kink=cms.string("combinedQuality().trkKink"),
        MuonSelected_n_MatchedStations=cms.string("numberOfMatchedStations()"),
        MuonSelected_Valid_pixel=cms.string(
            "?innerTrack.isNonnull()?innerTrack().hitPattern().numberOfValidPixelHits():-99"),
        MuonSelected_tracker_layers=cms.string(
            "?innerTrack.isNonnull()?innerTrack().hitPattern().trackerLayersWithMeasurement():-99"),
        MuonSelected_mvaId=cms.string("userFloat('mvaIDMuon')"),
    ),
    leptonVarsExt=cms.PSet(
        MuonSelected_mvaTTH=cms.InputTag("muonPROMPTMVA"),
    ),
    pfVars=cms.PSet(
        PF_pt=cms.string("pt"),
        PF_charge=cms.string("charge"),
        PF_isElectron=cms.string("?abs(pdgId)==11?1:0"),
        PF_isMuon=cms.string("?abs(pdgId)==13?1:0"),
        PF_isNeutralHadron=cms.string("?abs(pdgId)==130?1:0"),
        PF_isPhoton=cms.string("?abs(pdgId)==22?1:0"),
        PF_isChargedHadron=cms.string("?abs(pdgId)==211?1:0"),
        PF_puppiWeightNoLep=cms.string("puppiWeightNoLep"),
        PF_fromPV=cms.string("fromPV"),
        PF_numberOfPixelHits=cms.string("numberOfPixelHits"),
        PF_dzSig=cms.string("?hasTrackDetails?dz/max(dzError,1.e-6):0"),
        PF_dxySig=cms.string("?hasTrackDetails?dxy/max(dxyError,1.e-6):0"),
        PF_hcalFraction=cms.string("hcalFraction"),
        PF_trackerLayersWithMeasurement=cms.string(
            "?hasTrackDetails?bestTrack().hitPattern().trackerLayersWithMeasurement:0"),
        PF_mask=cms.string("1"),
    ),
    svVars=cms.PSet(
        SV_eta=cms.string("eta"),
        SV_phi=cms.string("phi"),
        SV_pt=cms.string("pt"),
        SV_ndof=cms.string("vertexNdof"),
        SV_chi2=cms.string("vertexChi2"),
        SV_nTracks=cms.string("numberOfDaughters"),
        SV_mass=cms.string("mass"),
        SV_mask=cms.string("1"),
    ),
)

muonPNetScores = _muonPNetTags.clone(
    src=cms.InputTag("muonPNetVariables"),
    srcLeps=cms.InputTag("linkedObjects", "muons"),
    model_path='PhysicsTools/NanoAOD/data/PNetMuonId/model.onnx',
    preprocess_json='PhysicsTools/NanoAOD/data/PNetMuonId/preprocess.json',
    flav_names=cms.vstring(["light", "prompt", "tau", "heavy"]),
)

muonParTVariables = cms.EDProducer(
    "MuonTagInfoCollectionProducer",
    pvSrc=cms.InputTag("offlineSlimmedPrimaryVertices"),
    secondary_vertices=cms.InputTag("slimmedSecondaryVertices"),
    src=cms.InputTag("linkedObjects", "muons"),
    pfCandidates=cms.InputTag("packedPFCandidates"),
    leptonVars=cms.PSet(
        Lepton_pt=cms.string("pt"),
        Lepton_pt_log=cms.string("log(pt+1.e-8)"),
        Lepton_eta=cms.string("eta"),
        Lepton_jetNDauChargedMVASel=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?userFloat('jetNDauChargedMVASel'):0"),
        Lepton_miniRelIsoCharged_log=cms.string(
            "log((userFloat('miniIsoChg')/pt)+1.e-8)"),
        Lepton_miniRelIsoNeutral_log=cms.string(
            "log(((userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt)+1.e-8)"),
        Lepton_pfRelIso03_all_log=cms.string(
            "log(((pfIsolationR03().sumChargedHadronPt + max(pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - pfIsolationR03().sumPUPt/2,0.0))/pt)+1.e-8)"),
        Lepton_jetPtRelv2_log=cms.string(
            "log((?userCand('jetForLepJetVar').isNonnull()?userFloat('ptRel'):0)+1.e-8)"),
        Lepton_jetPNet=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:BvsAll'),0.0):0.0"),
        Lepton_jetPtRatio=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?min(userFloat('ptRatio'),1.5):1.0/(1.0+(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt)"),
        Lepton_dxy=cms.string(
            "log(abs(dB('PV2D')))"),
        Lepton_sip3d=cms.string(
            "abs(dB('PV3D')/edB('PV3D'))"),
        Lepton_dz=cms.string(
            "log(abs(dB('PVDZ')))"),
        Lepton_segmentComp=cms.string(
            "segmentCompatibility"),
        Lepton_global_muon=cms.string(
            "isGlobalMuon"),
        Lepton_validFraction=cms.string(
            "?innerTrack.isNonnull?innerTrack().validFraction:-99"),
        Lepton_local_chi2=cms.string(
            "combinedQuality().chi2LocalPosition"),
        Lepton_kink=cms.string(
            "combinedQuality().trkKink"),
        Lepton_n_MatchedStations=cms.string(
            "numberOfMatchedStations()"),
        Lepton_Valid_pixel=cms.string(
            "?innerTrack.isNonnull()?innerTrack().hitPattern().numberOfValidPixelHits():-99"),
        Lepton_tracker_layers=cms.string(
            "?innerTrack.isNonnull()?innerTrack().hitPattern().trackerLayersWithMeasurement():-99"),
        Lepton_mvaId=cms.string(
            "userFloat('mvaIDMuon')"),
    ),
    pfVars=cms.PSet(
        PF_pt=cms.string("pt"),
        PF_pt_log=cms.string("log(pt+1.e-8)"),
        PF_charge=cms.string("charge"),
        PF_isElectron=cms.string(
            "?abs(pdgId)==11?1:0"),
        PF_isMuon=cms.string(
            "?abs(pdgId)==13?1:0"),
        PF_isNeutralHadron=cms.string(
            "?abs(pdgId)==130?1:0"),
        PF_isPhoton=cms.string(
            "?abs(pdgId)==22?1:0"),
        PF_isChargedHadron=cms.string(
            "?abs(pdgId)==211?1:0"),
        PF_puppiWeightNoLep=cms.string(
            "puppiWeightNoLep"),
        PF_fromPV=cms.string("fromPV"),
        PF_numberOfPixelHits=cms.string(
            "numberOfPixelHits"),
        PF_hcalFraction=cms.string(
            "hcalFraction"),
        PF_trackerLayersWithMeasurement=cms.string(
            "?hasTrackDetails?bestTrack().hitPattern().trackerLayersWithMeasurement:0"),
        PF_mask=cms.string("1"),
    ),
    svVars=cms.PSet(
        SV_pt_log=cms.string("log(pt+1.e-8)"),
        SV_eta=cms.string("eta"),
        SV_phi=cms.string("phi"),
        SV_ndof=cms.string("vertexNdof"),
        SV_chi2=cms.string("vertexChi2"),
        SV_nTracks=cms.string(
            "numberOfDaughters"),
        SV_mass=cms.string("mass"),
        SV_mass_log=cms.string("log(mass+1.e-8)"),
        SV_mask=cms.string("1"),
    ),
)

from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *
muonBSConstrain = cms.EDProducer("MuonBeamspotConstraintValueMapProducer",
    src = cms.InputTag("linkedObjects","muons"),
)

muonParTTrainVariables = cms.EDProducer(
    "MuonTagInfoCollectionProducer",
    src=cms.InputTag("linkedObjects", "muons"),
    pvSrc=cms.InputTag("offlineSlimmedPrimaryVertices"),
    secondary_vertices=cms.InputTag("slimmedSecondaryVertices"),
    pfCandidates=cms.InputTag("packedPFCandidates"),
    ltCandidates=cms.InputTag("lostTracks"),
    leptonVars=cms.PSet(
        Lepton_mask=cms.string("1"),
        Lepton_pt=cms.string("pt"),
        Lepton_pt_log=cms.string("log(pt+1.e-8)"),
        Lepton_eta=cms.string("eta"),
        Lepton_phi=cms.string("phi"),
        Lepton_px=cms.string("px"),
        Lepton_py=cms.string("py"),
        Lepton_pz=cms.string("pz"),
        Lepton_energy=cms.string("energy"),
        Lepton_energy_log=cms.string("log(energy+1.e-8)"),
        Lepton_jetNDauChargedMVASel=cms.string("?userCand('jetForLepJetVar').isNonnull()?userFloat('jetNDauChargedMVASel'):0"),
        Lepton_miniRelIsoCharged=cms.string("(userFloat('miniIsoChg')/pt)"),
        Lepton_miniRelIsoCharged_log=cms.string("log((userFloat('miniIsoChg')/pt)+1.e-8)"),
        Lepton_miniPFRelIso_all=cms.string("userFloat('miniIsoAll')/pt"),
        Lepton_miniRelIsoNeutral=cms.string("((userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt)"),
        Lepton_miniRelIsoNeutral_log=cms.string("log(((userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt)+1.e-8)"),
        Lepton_pfRelIso03_all_log=cms.string("log(((pfIsolationR03().sumChargedHadronPt + max(pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - pfIsolationR03().sumPUPt/2,0.0))/pt)+1.e-8)"),
        Lepton_pfRelIso03_all=cms.string("((pfIsolationR03().sumChargedHadronPt + max(pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - pfIsolationR03().sumPUPt/2,0.0))/pt)"),
        Lepton_jetPtRelv2_log=cms.string("?userCand('jetForLepJetVar').isNonnull()?log(abs(userFloat('ptRel'))+1.e-8):0.0"),
        # Lepton_jetPNet=cms.string("?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:BvsAll'),0.0):0.0"),
        # Lepton_jetPNet_TauVsJet=cms.string("?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:TauVsJet'),0.0):0.0"),
        # Lepton_jetPNet_CvsL=cms.string("?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsL'),0.0):0.0"),
        # Lepton_jetPNet_CvsB=cms.string("?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:CvsB'),0.0):0.0"),
        # Lepton_jetPNet_QvsG=cms.string("?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfParticleNetFromMiniAODAK4PuppiCentralDiscriminatorsJetTags:QvsG'),0.0):0.0"),
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
        # muon specific variables
        Lepton_segmentComp=cms.string("segmentCompatibility"),
        Lepton_global_muon=cms.string("isGlobalMuon"),
        Lepton_validFraction=cms.string("?innerTrack.isNonnull()?innerTrack().validFraction:-1"),
        Lepton_local_chi2=cms.string("combinedQuality().chi2LocalPosition"),
        Lepton_kink=cms.string("combinedQuality().trkKink"),
        Lepton_n_MatchedStations=cms.string("numberOfMatchedStations()"),
        Lepton_Valid_pixel=cms.string("?innerTrack.isNonnull()?innerTrack().hitPattern().numberOfValidPixelHits():-1"),
        Lepton_tracker_layers=cms.string("?innerTrack.isNonnull()?innerTrack().hitPattern().trackerLayersWithMeasurement():-1"),
        Lepton_mvaId=cms.string("userFloat('mvaIDMuon')"),
        # let's also add the classic mva and cutbased IDs for comparison
        # Lepton_ID_cutBasedLoose=cms.string("passed('CutBasedIdLoose')"),
        # Lepton_ID_cutBasedMedium=cms.string("passed('CutBasedIdMedium')"),
        # Lepton_ID_cutBasedMediumPrompt=cms.string("passed('CutBasedIdMediumPrompt')"),
        # Lepton_ID_cutBasedTight=cms.string("passed('CutBasedIdTight')"),
        # Lepton_ID_mva=cms.string("userFloat('mvaIDMuon')"),
    ),
    leptonVarsExt=cms.PSet(
        # Lepton_ID_promptMVA=cms.InputTag("muonPROMPTMVA"),
        # Lepton_ID_PNET_prompt=cms.InputTag("muonPNetScores:prompt"),
        # Lepton_ID_PNET_heavy=cms.InputTag("muonPNetScores:heavy"),
        # Lepton_ID_PNET_light=cms.InputTag("muonPNetScores:light"),
        # Lepton_ID_PNET_tau=cms.InputTag("muonPNetScores:tau"),
        # Lepton_ID_ParT_prompt=cms.InputTag("muonParTScores:prompt"),
        # Lepton_ID_ParT_heavy=cms.InputTag("muonParTScores:heavy"),
        # Lepton_ID_ParT_light=cms.InputTag("muonParTScores:light"),
        # Lepton_ID_ParT_tau=cms.InputTag("muonParTScores:tau"),
        # Lepton_ID_ParT_fake=cms.InputTag("muonParTScores:fake"),
        # it's own outputs for testing
        # Lepton_ID_ParT_prompt=cms.InputTag("muonParTLLScores:prompt"),
        # Lepton_ID_ParT_heavy=cms.InputTag("muonParTLLScores:heavy"),
        # Lepton_ID_ParT_light=cms.InputTag("muonParTLLScores:light"),
        # Lepton_ID_ParT_tau=cms.InputTag("muonParTLLScores:tau"),
        # Lepton_ID_ParT_fake=cms.InputTag("muonParTLLScores:fake"),
    ),
    pfVars=cms.PSet(
        PF_pt=cms.string("pt"),
        PF_pt_log=cms.string("log(pt+1.e-8)"),
        PF_px_glob=cms.string("px"),
        PF_py_glob=cms.string("py"),
        PF_pz_glob=cms.string("pz"),
        PF_energy_glob=cms.string("energy"),
        PF_energy_glob_log=cms.string("log(energy+1.e-8)"),
        PF_charge=cms.string("charge"),
        PF_isElectron=cms.string("?abs(pdgId)==11?1:0"),
        PF_isMuon=cms.string("?abs(pdgId)==13?1:0"),
        PF_isNeutralHadron=cms.string("?abs(pdgId)==130?1:0"),
        PF_isPhoton=cms.string("?abs(pdgId)==22?1:0"),
        PF_isChargedHadron=cms.string("?abs(pdgId)==211?1:0"),
        PF_puppiWeightNoLep=cms.string("puppiWeightNoLep"),
        PF_fromPV=cms.string("fromPV"),
        PF_numberOfPixelHits=cms.string("numberOfPixelHits"),
        PF_hcalFraction=cms.string("hcalFraction"),
        PF_trackerLayersWithMeasurement=cms.string(
            "?hasTrackDetails?bestTrack().hitPattern().trackerLayersWithMeasurement():0"),
        PF_mask=cms.string("1"),
        # new stuff
        PF_qoverp=cms.string("?hasTrackDetails?charge()/pt():0"),
        PF_qdotp=cms.string("?hasTrackDetails?charge()*pt():0"),
        PF_ass=cms.string("?hasTrackDetails?pvAssociationQuality():0"),
        PF_chi2=cms.string("?hasTrackDetails?bestTrack().chi2():0"),
        PF_caloFraction=cms.string("caloFraction"),
        PF_lostInnerHits=cms.string("?hasTrackDetails?lostInnerHits():0"),
    ),
    ltVars=cms.PSet(
        LT_pt=cms.string("pt"),
        LT_pt_log=cms.string("log(pt+1.e-8)"),
        LT_px_glob=cms.string("px"),
        LT_py_glob=cms.string("py"),
        LT_pz_glob=cms.string("pz"),
        LT_energy_glob=cms.string("energy"),
        LT_energy_glob_log=cms.string("log(energy+1.e-8)"),
        LT_charge=cms.string("charge"),
        LT_isElectron=cms.string(
            "?abs(pdgId)==11?1:0"),
        LT_isMuon=cms.string(
            "?abs(pdgId)==13?1:0"),
        LT_isNeutralHadron=cms.string(
            "?abs(pdgId)==130?1:0"),
        LT_isPhoton=cms.string(
            "?abs(pdgId)==22?1:0"),
        LT_isChargedHadron=cms.string(
            "?abs(pdgId)==211?1:0"),
        LT_puppiWeightNoLep=cms.string(
            "puppiWeightNoLep"),
        LT_fromPV=cms.string("fromPV"),
        LT_numberOfPixelHits=cms.string(
            "numberOfPixelHits"),
        LT_hcalFraction=cms.string(
            "hcalFraction"),
        LT_trackerLayersWithMeasurement=cms.string(
            "?hasTrackDetails?bestTrack().hitPattern().trackerLayersWithMeasurement():0"),
        LT_mask=cms.string("1"),
        # new stuff
        LT_qoverp=cms.string("?hasTrackDetails?charge()/pt():0"),
        LT_qdotp=cms.string("?hasTrackDetails?charge()*pt():0"),
        LT_ass=cms.string("?hasTrackDetails?pvAssociationQuality():0"),
        LT_chi2=cms.string("?hasTrackDetails?bestTrack().chi2():0"),
        LT_caloFraction=cms.string("caloFraction"),
        LT_lostInnerHits=cms.string("?hasTrackDetails?lostInnerHits():0"),
    ),
    svVars=cms.PSet(
        SV_eta=cms.string("eta"),
        SV_phi=cms.string("phi"),
        SV_pt=cms.string("pt"),
        SV_px_glob=cms.string("px"),
        SV_py_glob=cms.string("py"),
        SV_pz_glob=cms.string("pz"),
        SV_energy_glob=cms.string("energy"),
        SV_energy_glob_log=cms.string("log(energy+1.e-8)"),
        SV_pt_log=cms.string("log(pt+1.e-8)"),
        SV_ndof=cms.string("vertexNdof"),
        SV_chi2=cms.string("vertexChi2"),
        SV_chi2norm=cms.string("vertexChi2/vertexNdof"),
        SV_nTracks=cms.string("numberOfDaughters"),
        SV_mass=cms.string("mass"),
        SV_mass_log=cms.string("log(mass+1.e-8)"),
        SV_mask=cms.string("1"),
    ),
)


from PhysicsTools.PatAlgos.muonParTTags_cfi import muonParTTags as _muonParTTags
# muonParTScores = _muonParTTags.clone(
#     src=cms.InputTag("muonParTVariables"),
#     srcLeps=cms.InputTag("linkedObjects", "muons"),
#     model_path='PhysicsTools/NanoAOD/data/ParTMuonId/model.onnx',
#     preprocess_json='PhysicsTools/NanoAOD/data/ParTMuonId/preprocess.json',
#     flav_names=cms.vstring(["prompt", "tau", "heavy", "light", "fake"]),
# )

muonParTLLScores = _muonParTTags.clone(
    src=cms.InputTag("muonParTTrainVariables"),
    srcLeps=cms.InputTag("linkedObjects", "muons"),
    model_path='PhysicsTools/NanoAOD/data/ParTMuonId/v2/muon_ParT_2024.onnx',
    preprocess_json='PhysicsTools/NanoAOD/data/ParTMuonId/v2/preprocess.json',
    # [fake, prompt, tau, heavy, light]
    flav_names=cms.vstring(["fake", "prompt", "tau", "heavy", "light"]),
    # debugMode=cms.untracked.bool(True),
)

muonBSConstrain = cms.EDProducer("MuonBeamspotConstraintValueMapProducer",
                                 src=cms.InputTag("linkedObjects", "muons"),
                                 )

muonTable = simplePATMuonFlatTableProducer.clone(
    src = cms.InputTag("linkedObjects","muons"),
    name = cms.string("Muon"),
    doc  = cms.string("slimmedMuons after basic selection (" + finalMuons.cut.value()+")"),
    variables = cms.PSet(CandVars,
        ptErr   = Var("bestTrack().ptError()", float, doc = "ptError of the muon track", precision=6),
        tunepRelPt = Var("tunePMuonBestTrack().pt/pt",float,doc="TuneP relative pt, tunePpt/pt",precision=6),
        tuneP_pterr = Var("tunePMuonBestTrack().ptError()", float, doc = "pTerr from tunePMuonBestTrack", precision=6),
        tuneP_charge = Var("? tunePMuonBestTrack().isNonnull() && tunePMuonBestTrack().isAvailable() ? tunePMuonBestTrack().charge(): -99", float, doc="tunePMuonBestTrack() charge",precision=6),
        dz = Var("dB('PVDZ')",float,doc="dz (with sign) wrt first PV, in cm",precision=10),
        dzErr = Var("abs(edB('PVDZ'))",float,doc="dz uncertainty, in cm",precision=6),
        dxybs = Var("dB('BS2D')",float,doc="dxy (with sign) wrt the beam spot, in cm",precision=10),
        dxybsErr = Var("edB('BS2D')",float,doc="dxy uncertainty wrt the beam spot, in cm", precision=6),
        dxy = Var("dB('PV2D')",float,doc="dxy (with sign) wrt first PV, in cm",precision=10),
        dxyErr = Var("edB('PV2D')",float,doc="dxy uncertainty, in cm",precision=6),
        ip3d = Var("abs(dB('PV3D'))",float,doc="3D impact parameter wrt first PV, in cm",precision=10),
        sip3d = Var("abs(dB('PV3D')/edB('PV3D'))",float,doc="3D impact parameter significance wrt first PV",precision=10),
        segmentComp   = Var("segmentCompatibility()", float, doc = "muon segment compatibility", precision=14), # keep higher precision since people have cuts with 3 digits on this
        nStations = Var("numberOfMatchedStations", "uint8", doc = "number of matched stations with default arbitration (segment & track)"),
        nTrackerLayers = Var("?track.isNonnull?innerTrack().hitPattern().trackerLayersWithMeasurement():0", "uint8", doc = "number of layers in the tracker"),
        bestTrackType = Var("muonBestTrackType()", "uint8", doc = "Type of track used (1=inner, 2=STA, 3=global, 4=TPFMS, 5=Picky, 6=DYT)"),
        highPurity = Var("?track.isNonnull?innerTrack().quality('highPurity'):0", bool, doc = "inner track is high purity"),
        jetIdx = Var("?hasUserCand('jet')?userCand('jet').key():-1", "int16", doc="index of the associated jet (-1 if none)"),
        svIdx = Var("?hasUserCand('vertex')?userCand('vertex').key():-1", "int16", doc="index of matching secondary vertex"),
        tkRelIso = Var("isolationR03().sumPt/pt",float,doc="Tracker-based relative isolation dR=0.3 for highPt, trkIso/pt",precision=6),
        miniPFRelIso_chg = Var("userFloat('miniIsoChg')/pt",float,doc="mini PF relative isolation, charged component"),
        miniPFRelIso_all = Var("userFloat('miniIsoAll')/pt",float,doc="mini PF relative isolation, total (with scaled rho*EA PU corrections)"),
        pfRelIso03_chg = Var("pfIsolationR03().sumChargedHadronPt/pt",float,doc="PF relative isolation dR=0.3, charged component"),
        pfRelIso03_all = Var("(pfIsolationR03().sumChargedHadronPt + max(pfIsolationR03().sumNeutralHadronEt + pfIsolationR03().sumPhotonEt - pfIsolationR03().sumPUPt/2,0.0))/pt",float,doc="PF relative isolation dR=0.3, total (deltaBeta corrections)"),
        pfRelIso04_all = Var("(pfIsolationR04().sumChargedHadronPt + max(pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - pfIsolationR04().sumPUPt/2,0.0))/pt",float,doc="PF relative isolation dR=0.4, total (deltaBeta corrections)"),
        jetRelIso = Var("?userCand('jetForLepJetVar').isNonnull()?(1./userFloat('ptRatio'))-1.:-1.",float,doc="Relative isolation in matched jet (1/ptRatio-1), -1 if none",precision=8),
        jetPtRelv2 = Var("?userCand('jetForLepJetVar').isNonnull()?userFloat('ptRel'):0",float,doc="Relative momentum of the lepton with respect to the closest jet after subtracting the lepton",precision=8),
        jetDF = Var("?userCand('jetForLepJetVar').isNonnull()?max(userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:probbb')+userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:probb')+userCand('jetForLepJetVar').bDiscriminator('pfDeepFlavourJetTags:problepb'),0.0):0.0",float,doc="value of the DEEPJET b tagging algorithm discriminator of the associated jet (0 if none)",precision=8,lazyEval=True),
        tightCharge = Var("?(muonBestTrack().ptError()/muonBestTrack().pt() < 0.2)?2:0", "uint8", doc="Tight charge criterion using pterr/pt of muonBestTrack (0:fail, 2:pass)"),
        looseId  = Var("passed('CutBasedIdLoose')",bool, doc="muon is loose muon"),
        isPFcand = Var("isPFMuon",bool,doc="muon is PF candidate"),
        isGlobal = Var("isGlobalMuon",bool,doc="muon is global muon"),
        isTracker = Var("isTrackerMuon",bool,doc="muon is tracker muon"),
        isStandalone = Var("isStandAloneMuon",bool,doc="muon is a standalone muon"),
        mediumId = Var("passed('CutBasedIdMedium')",bool,doc="cut-based ID, medium WP"),
        mediumPromptId = Var("passed('CutBasedIdMediumPrompt')",bool,doc="cut-based ID, medium prompt WP"),
        tightId = Var("passed('CutBasedIdTight')",bool,doc="cut-based ID, tight WP"),
        softId = Var("passed('SoftCutBasedId')",bool,doc="soft cut-based ID"),
        softMvaId = Var("passed('SoftMvaId')",bool,doc="soft MVA ID"),
        softMva = Var("softMvaValue()",float,doc="soft MVA ID score",precision=6),
        softMvaRun3 = Var("softMvaRun3Value()",float,doc="soft MVA Run3 ID score",precision=6),
        highPtId = Var("?passed('CutBasedIdGlobalHighPt')?2:passed('CutBasedIdTrkHighPt')","uint8",doc="high-pT cut-based ID (1 = tracker high pT, 2 = global high pT, which includes tracker high pT)"),
        pfIsoId = Var("passed('PFIsoVeryLoose')+passed('PFIsoLoose')+passed('PFIsoMedium')+passed('PFIsoTight')+passed('PFIsoVeryTight')+passed('PFIsoVeryVeryTight')","uint8",doc="PFIso ID from miniAOD selector (1=PFIsoVeryLoose, 2=PFIsoLoose, 3=PFIsoMedium, 4=PFIsoTight, 5=PFIsoVeryTight, 6=PFIsoVeryVeryTight)"),
        tkIsoId = Var("?passed('TkIsoTight')?2:passed('TkIsoLoose')","uint8",doc="TkIso ID (1=TkIsoLoose, 2=TkIsoTight)"),
        miniIsoId = Var("passed('MiniIsoLoose')+passed('MiniIsoMedium')+passed('MiniIsoTight')+passed('MiniIsoVeryTight')","uint8",doc="MiniIso ID from miniAOD selector (1=MiniIsoLoose, 2=MiniIsoMedium, 3=MiniIsoTight, 4=MiniIsoVeryTight)"),
        mvaMuID = Var("userFloat('mvaIDMuon')", float, doc="MVA-based ID score",precision=6),
        mvaMuID_WP = Var("userFloat('mvaIDMuon_wpMedium') + userFloat('mvaIDMuon_wpTight')","uint8",doc="MVA-based ID selector WPs (1=MVAIDwpMedium,2=MVAIDwpTight)"),
        multiIsoId = Var("?passed('MultiIsoMedium')?2:passed('MultiIsoLoose')","uint8",doc="MultiIsoId from miniAOD selector (1=MultiIsoLoose, 2=MultiIsoMedium)"),
        puppiIsoId = Var("passed('PuppiIsoLoose')+passed('PuppiIsoMedium')+passed('PuppiIsoTight')", "uint8", doc="PuppiIsoId from miniAOD selector (1=Loose, 2=Medium, 3=Tight)"),
        triggerIdLoose = Var("passed('TriggerIdLoose')",bool,doc="TriggerIdLoose ID"),
        inTimeMuon = Var("passed('InTimeMuon')",bool,doc="inTimeMuon ID"),
        jetNDauCharged = Var("?userCand('jetForLepJetVar').isNonnull()?userFloat('jetNDauChargedMVASel'):0", "uint8", doc="number of charged daughters of the closest jet"),
        VXBS_Cov00 = Var("? tunePMuonBestTrack().isNonnull() && tunePMuonBestTrack().isAvailable() ? tunePMuonBestTrack().covariance(0,0) : -999",float,doc="0, 0 element of the VXBS Covariance matrix", precision=16),
        VXBS_Cov03 = Var("? tunePMuonBestTrack().isNonnull() && tunePMuonBestTrack().isAvailable() ? tunePMuonBestTrack().covariance(0,3) : -999",float,doc="0, 3 element of the VXBS Covariance matrix", precision=16),
        VXBS_Cov33 = Var("? tunePMuonBestTrack().isNonnull() && tunePMuonBestTrack().isAvailable() ? tunePMuonBestTrack().covariance(3,3) : -999",float,doc="3, 3 element of the VXBS Covariance matrix", precision=16),
        ),
    externalVariables = cms.PSet(
        promptMVA = ExtVar(cms.InputTag("muonPROMPTMVA"),float, doc="Prompt MVA lepton ID score. Corresponds to the previous mvaTTH",precision=14),
        mvaLowPt = ExtVar(cms.InputTag("muonMVALowPt"),float, doc="Low pt muon ID score",precision=14),
        pnScore_prompt = ExtVar(cms.InputTag("muonPNetScores:prompt"),float, doc="PNet muon ID score for lepton from W/Z/H bosons", precision=14),
        pnScore_heavy = ExtVar(cms.InputTag("muonPNetScores:heavy"),float, doc="PNet muon ID score for lepton from B or D hadrons", precision=14),
        pnScore_light = ExtVar(cms.InputTag("muonPNetScores:light"),float, doc="PNet muon ID score for lepton from hadrons w/o b or c quarks OR w/o generator matching", precision=14),
        pnScore_tau = ExtVar(cms.InputTag("muonPNetScores:tau"),float, doc="PNet muon ID score for decay of tau to light leptons (mu)", precision=14),
        # parTScore_prompt=ExtVar(cms.InputTag("muonParTScores:prompt"), float, doc="ParT muon ID score for lepton from W/Z/H bosons", precision=14),
        # parTScore_heavy=ExtVar(cms.InputTag("muonParTScores:heavy"), float, doc="ParT muon ID score for lepton from B or D hadrons", precision=14),
        # parTScore_light=ExtVar(cms.InputTag("muonParTScores:light"), float, doc="ParT muon ID score for lepton from hadrons w/o b or c quarks OR w/o generator matching", precision=14),
        # parTScore_tau=ExtVar(cms.InputTag("muonParTScores:tau"), float, doc="ParT muon ID score for decay of tau to light leptons (mu)", precision=14),
        # parTScore_fake=ExtVar(cms.InputTag("muonParTScores:fake"), float, doc="ParT muon ID score for fake leptons", precision=14),
        parTScore_prompt=ExtVar(cms.InputTag("muonParTLLScores:prompt"), float, doc="ParTLL muon ID score for lepton from W/Z/H bosons", precision=14),
        parTScore_heavy=ExtVar(cms.InputTag("muonParTLLScores:heavy"), float, doc="ParTLL muon ID score for lepton from B or D hadrons", precision=14),
        parTScore_light=ExtVar(cms.InputTag("muonParTLLScores:light"), float, doc="ParTLL muon ID score for lepton from hadrons w/o b or c quarks OR w/o generator matching", precision=14),
        parTScore_tau=ExtVar(cms.InputTag("muonParTLLScores:tau"), float, doc="ParTLL muon ID score for decay of tau to light leptons (mu)", precision=14),
        parTScore_fake=ExtVar(cms.InputTag("muonParTLLScores:fake"), float, doc="ParTLL muon ID score for fake leptons", precision=14),
        fsrPhotonIdx = ExtVar(cms.InputTag("leptonFSRphotons:muFsrIndex"), "int16", doc="Index of the lowest-dR/ET2 among associated FSR photons"),
        bsConstrainedPt = ExtVar(cms.InputTag("muonBSConstrain:muonBSConstrainedPt"),float, doc="pT with beamspot constraint",precision=-1),
        bsConstrainedPtErr = ExtVar(cms.InputTag("muonBSConstrain:muonBSConstrainedPtErr"),float, doc="pT error with beamspot constraint ",precision=6),
        bsConstrainedChi2 = ExtVar(cms.InputTag("muonBSConstrain:muonBSConstrainedChi2"),float, doc="chi2 of beamspot constraint",precision=6),
    ),
)

# Increase precision of eta and phi
muonTable.variables.eta.precision = 16
muonTable.variables.phi.precision = 16


# Revert back to AK4 CHS jets for Run 2
run2_nanoAOD_ANY.toModify(
    ptRatioRelForMu, srcJet="updatedJets"
)


muonsMCMatchForTable = cms.EDProducer("MCMatcher",       # cut on deltaR, deltaPt/Pt; pick best by deltaR
                                      src=muonTable.src,                         # final reco collection
                                      # final mc-truth particle collection
                                      matched=cms.InputTag(
                                          "finalGenParticles"),
                                      # one or more PDG ID (13 = mu); absolute values (see below)
                                      mcPdgId=cms.vint32(13),
                                      # True = require RECO and MC objects to have the same charge
                                      checkCharge=cms.bool(False),
                                      # PYTHIA status code (1 = stable, 2 = shower, 3 = hard scattering)
                                      mcStatus=cms.vint32(1),
                                      # Minimum deltaR for the match
                                      maxDeltaR=cms.double(0.3),
                                      # Minimum deltaPt/Pt for the match
                                      maxDPtRel=cms.double(0.5),
                                      # Forbid two RECO objects to match to the same GEN object
                                      resolveAmbiguities=cms.bool(True),
                                      # False = just match input in order; True = pick lowest deltaR pair first
                                      resolveByMatchQuality=cms.bool(True),
                                      )

muonMCTable = cms.EDProducer("CandMCMatchTableProducer",
                             src=muonTable.src,
                             mcMap=cms.InputTag("muonsMCMatchForTable"),
                             objName=muonTable.name,
                             objType=muonTable.name,  # cms.string("Muon"),
                             branchName=cms.string("genPart"),
                             docString=cms.string(
                                 "MC matching to status==1 muons"),
                             )

muonTask = cms.Task(slimmedMuonsUpdated,isoForMu,ptRatioRelForMu,slimmedMuonsWithUserData,finalMuons,finalLooseMuons)
muonMCTask = cms.Task(muonsMCMatchForTable,muonMCTable)
# muonTablesTask = cms.Task(muonPROMPTMVA,muonMVALowPt,muonBSConstrain,muonTable,muonMVAID,muonPNetVariables,muonPNetScores, muonParTVariables, muonParTTrainVariables, muonParTScores, muonParTLLScores)
muonTablesTask = cms.Task(muonPROMPTMVA,muonMVALowPt,muonBSConstrain,muonTable,muonMVAID,muonPNetVariables,muonPNetScores, muonParTTrainVariables, muonParTLLScores)
