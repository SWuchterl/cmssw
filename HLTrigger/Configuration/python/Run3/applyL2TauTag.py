import FWCore.ParameterSet.Config as cms
from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets
from RecoTauTag.HLTProducers.l2TauNNProducer_cfi import *
from RecoTauTag.HLTProducers.l2TauTagFilter_cfi import *

def insertL2TauSequence(process, path, ref_module, L2TauNNfilter):
    ref_idx = path.index(ref_module)
    path.insert(ref_idx + 1, process.hltL2TauTagNNSequence)
    path.insert(ref_idx + 2, L2TauNNfilter)
    path.insert(ref_idx + 3, process.HLTGlobalPFTauHPSSequence)


def update(process):
    thWp = {
            'Tight': 0.180858813224404,
            'Medium': 0.12267940863785043,
            'Loose': 0.08411243185219064,
    }

    working_point = "Tight"
    graphPath = 'RecoTauTag/TrainingFiles/data/L2TauNNTag/L2TauTag_Run3v1.pb'

    normalizationDict = 'RecoTauTag/TrainingFiles/data/L2TauNNTag/NormalizationDict.json'


    if 'statusOnGPU' not in process. __dict__:
        process = customizeHLTforPatatrackTriplets(process)
    process.hltL2TauTagNNProducer = l2TauNNProducer.clone(
        debugLevel = 0,
        L1Taus= cms.VPSet(
            cms.PSet(
                L1CollectionName = cms.string('DoubleTau'),
                L1TauTrigger =cms.InputTag('hltL1sDoubleTauBigOR'),
            ),
            cms.PSet(
                L1CollectionName = cms.string('IsoTau'),
                L1TauTrigger =cms.InputTag('hltL1sIsoTau40erETMHF90To120'),
            ),
            cms.PSet(
                L1CollectionName = cms.string('SingleTau'),
                L1TauTrigger =cms.InputTag('hltL1sSingleTau'),
            ),
        ),
        hbheInput = cms.InputTag("hltHbhereco"),
        hoInput = cms.InputTag("hltHoreco"),
        ebInput =cms.InputTag("hltEcalRecHit:EcalRecHitsEB"),
        eeInput =cms.InputTag("hltEcalRecHit:EcalRecHitsEE"),
        pataVertices = cms.InputTag("hltPixelVerticesSoA"),
        pataTracks = cms.InputTag("hltPixelTracksSoA"),
        BeamSpot = cms.InputTag("hltOnlineBeamSpot"),
        graphPath = cms.string(graphPath),
        normalizationDict = cms.string(normalizationDict)
    )
    
    process.hltL2DoubleTauTagNNFilter = l2TauTagFilter.clone(
        nExpected = 2,
        L1TauSrc = cms.InputTag('hltL1sDoubleTauBigOR'),
        L2Outcomes = ('hltL2TauTagNNProducer', 'DoubleTau'),
        DiscrWP = cms.double(thWp[working_point])
    )
    process.hltL2IsoTauTagNNFilter = l2TauTagFilter.clone(
        nExpected = 1,
        L1TauSrc = cms.InputTag('hltL1sIsoTau40erETMHF90To120'),
        L2Outcomes = ('hltL2TauTagNNProducer', 'IsoTau'),
        DiscrWP = cms.double(thWp[working_point])
    )
    process.hltL2SingleTauTagNNFilter = l2TauTagFilter.clone(
        nExpected = 1,
        L1TauSrc = cms.InputTag('hltL1sSingleTau'),
        L2Outcomes = ('hltL2TauTagNNProducer', 'SingleTau'),
        DiscrWP = cms.double(thWp[working_point])
    )
    # L2 updated Sequence
    process.hltL2TauTagNNSequence = cms.Sequence(process.HLTDoCaloSequence + cms.ignore(process.hltL1sDoubleTauBigOR) + cms.ignore(process.hltL1sIsoTau40erETMHF90To120) + cms.ignore(process.hltL1sSingleTau) + process.hltL2TauTagNNProducer)


    # Regional -> Global customization
    process.hltHpsPFTauTrackPt1DiscriminatorReg.PFTauProducer = cms.InputTag("hltHpsPFTauProducer")
    process.hltHpsDoublePFTau35Reg.inputTag = cms.InputTag( "hltHpsPFTauProducer")
    process.hltHpsSelectedPFTausTrackPt1Reg.src = cms.InputTag( "hltHpsPFTauProducer")
    process.hltHpsPFTauMediumAbsoluteChargedIsolationDiscriminatorReg.PFTauProducer = cms.InputTag( "hltHpsPFTauProducer" )
    process.hltHpsPFTauMediumAbsoluteChargedIsolationDiscriminatorReg.particleFlowSrc = cms.InputTag( "hltParticleFlow" )
    process.hltHpsPFTauMediumRelativeChargedIsolationDiscriminatorReg.PFTauProducer = cms.InputTag( "hltHpsPFTauProducer" )
    process.hltHpsPFTauMediumRelativeChargedIsolationDiscriminatorReg.particleFlowSrc = cms.InputTag( "hltParticleFlow" )
    process.hltHpsPFTauMediumAbsOrRelChargedIsolationDiscriminatorReg.PFTauProducer = cms.InputTag( "hltHpsPFTauProducer" )
    process.hltHpsSelectedPFTausTrackPt1MediumChargedIsolationReg.src = cms.InputTag( "hltHpsPFTauProducer" )

    # Remove old modules in di-tau path
    process.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v4.remove(process.HLTL2TauJetsL1TauSeededSequence)
    process.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v4.remove(process.hltDoubleL2Tau26eta2p2)
    process.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v4.remove(process.HLTL2p5IsoTauL1TauSeededSequence)
    process.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v4.remove(process.hltDoubleL2IsoTau26eta2p2 )
    process.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v4.remove(process.HLTRegionalPFTauHPSSequence )

    # Remove old modules in tau+MET path
    process.HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET100_v12.remove(process.HLTL2TauJetsSequence)
    process.HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET100_v12.remove(process.hltSingleL2Tau35eta2p2)
    process.HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET100_v12.remove(process.HLTGlobalPFTauConeSequence)

    # Remove old modules in high-pt path
    process.HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v12.remove(process.HLTL2TauJetsSequence)
    process.HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v12.remove(process.hltSingleL2Tau80eta2p2)
    process.HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v12.remove(process.HLTGlobalPFTauConeSequence)

    # Add L2 sequence
    insertL2TauSequence(process, process.HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v4, process.hltPreDoubleMediumChargedIsoPFTauHPS35Trk1eta2p1Reg, process.hltL2DoubleTauTagNNFilter)
    insertL2TauSequence(process, process.HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET100_v12, process.hltPreMediumChargedIsoPFTau50Trk30eta2p11prMET100, process.hltL2IsoTauTagNNFilter)
    insertL2TauSequence(process, process.HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v12, process.hltPreMediumChargedIsoPFTau180HighPtRelaxedIsoTrk50eta2p1, process.hltL2SingleTauTagNNFilter)

    old_diTau_paths = ['HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1_v1', 'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_CrossL1_v1','HLT_IsoMu24_eta2p1_TightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_CrossL1_v1','HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_CrossL1_v4','HLT_IsoMu24_eta2p1_MediumChargedIsoPFTauHPS30_Trk1_eta2p1_Reg_CrossL1_v1','HLT_DoubleMediumChargedIsoPFTauHPS30_L1MaxMass_Trk1_eta2p1_Reg_v1','HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v1','HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_v1','HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_v1','HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_eta2p1_Reg_v1','HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg_v1','HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg_v1','HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg_v1']
    for i in old_diTau_paths:
        if i in process.__dict__:
            process.HLTSchedule.remove(getattr(process, i))

    return process
