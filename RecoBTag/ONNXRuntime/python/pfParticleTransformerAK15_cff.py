import FWCore.ParameterSet.Config as cms

from RecoBTag.FeatureTools.pfGlobalParticleTransformerAK8TagInfos_cfi import pfGlobalParticleTransformerAK8TagInfos as _pfGlobalParticleTransformerAK8TagInfos
from RecoBTag.ONNXRuntime.boostedJetONNXJetTagsProducer_cfi import boostedJetONNXJetTagsProducer

pfParticleTransformerAK15TagInfos = _pfGlobalParticleTransformerAK8TagInfos.clone(
    jet_radius = 1.5
)

pfParticleTransformerAK15JetTags = boostedJetONNXJetTagsProducer.clone(
    src='pfParticleTransformerAK15TagInfos',
    preprocess_json='scoutnanotuples/data/OfflineGlobalParticleTransformerAK15/preprocess.json',
    model_path='scoutnanotuples/data/OfflineGlobalParticleTransformerAK15/model_ak15.onnx',
    flav_names=[
        # Classification nodes  
        'probXbb', # probHbb
        'probXcc', # probHcc
        'probXcs', #'probHpcs + probHmcs', 
        'probXqq', #'probHss + probHqq*2', 
        'probXtauhtaue', # probHtauhtaue
        'probXtauhtaum', # probHtauhtaum
        'probXtauhtauh', # probHtauhtauh
        'probXWW4q', #'probHWWcscs + probHWWcsqq + probHWWqqqq',
        'probXWW3q', #'probHWWcsc + probHWWcss + probHWWcsq + probHWWqqc + probHWWqqs + probHWWqqq',
        'probXWWqqev', #'probHWWcsev + probHWWqqev',
        'probXWWqqmv', #'probHWWcsmv + probHWWqqmv',
        'probTopbWqq', #'probTopbWpcs + probTopbWpqq + probTopbWmcs + probTopbWmqq',
        'probTopbWq', #'probTopbWpc + probTopbWps + probTopbWpq + probTopbWmc + probTopbWms + probTopbWmq',
        'probTopbWev', #'probTopbWpev + probTopbWmev',
        'probTopbWmv', #'probTopbWpmv + probTopbWmmv',
        'probTopbWtauhv', #'probTopbWptauhv + probTopbWmtauhv',
        'probQCD', #'probQCDbb + probQCDcc + probQCDb + probQCDc + probQCDothers', # QCD
        # Regression nodes
        'massCorrX2p', #'massCorrGeneric + (massCorrHbb*probHbb + massCorrHcc*probHcc + massCorrHss*probHss + 2*massCorrHqq*probHqq + massCorrHpcs*probHpcs + massCorrHmcs*probHmcs) / (probHbb + probHcc + probHss + 2*probHqq + probHpcs + probHmcs).clamp(min=1e-10)', # 
        'massCorrGeneric', # massCorrGeneric
        'massCorrResonance' # massCorrResonance
    ]
)

from CommonTools.PileupAlgos.Puppi_cff import puppi
from CommonTools.RecoAlgos.primaryVertexAssociation_cfi import primaryVertexAssociation

# This task is not used, useful only if we run it from RECO jets (RECO/AOD)
pfParticleTransformerAK15Task = cms.Task(puppi, primaryVertexAssociation, pfParticleTransformerAK15TagInfos,
                                        pfParticleTransformerAK15JetTags)

# declare all the discriminators

# mass-decorrelated: probs
_pfParticleTransformerAK15JetTagsProbs = ['pfParticleTransformerAK15JetTags:' + flav_name
                                           for flav_name in pfParticleTransformerAK15JetTags.flav_names]
# mass-decorrelated: meta-taggers
_pfParticleTransformerAK15JetTagsMetaDiscrs = []

_pfParticleTransformerAK15JetTagsAll = _pfParticleTransformerAK15JetTagsProbs + _pfParticleTransformerAK15JetTagsMetaDiscrs
