import FWCore.ParameterSet.Config as cms

from RecoBTag.FeatureTools.pfUnifiedParticleTransformerAK4TagInfos_cfi import pfUnifiedParticleTransformerAK4TagInfos as pfNoPIDParticleTransformerAK4TagInfos

from RecoBTag.ONNXRuntime.pfUnifiedParticleTransformerAK4JetTags_cfi import pfUnifiedParticleTransformerAK4JetTags
from RecoBTag.ONNXRuntime.pfNoPIDParticleTransformerAK4DiscriminatorsJetTags_cfi import pfNoPIDParticleTransformerAK4DiscriminatorsJetTags
from CommonTools.PileupAlgos.Puppi_cff import puppi
from CommonTools.RecoAlgos.primaryVertexAssociation_cfi import primaryVertexAssociation

# modify the TagInfos
# pfNoPIDParticleTransformerAK4TagInfos.is_weighted_jet = cms.bool(False)

# modify the JetTags
pfNoPIDParticleTransformerAK4JetTags = pfUnifiedParticleTransformerAK4JetTags.clone(
    src = 'pfNoPIDParticleTransformerAK4TagInfos',
    flav_names = cms.vstring(
        'probb',
        'probbb',
        'probc',
        'probcc',
        'probud',
        'probs',
        'probg',
        'probpu',
    ),
    # input_names = cms.vstring(
    #         'cpf_feats',
    #         'lt_feats',
    #         'npf_feats',
    #         'sv_feats',
    #         'cpf_4v',
    #         'lt_4v',
    #         'npf_4v',
    #         'sv_4v',
    # ),
    input_names = cms.vstring(
            'input_1',
            'input_2',
            'input_3',
            'input_4',
            'input_5',
            'input_6',
            'input_7',
            'input_8',
    ),
    model_path = cms.FileInPath('RecoBTag/Combined/data/UParTAK4/PUPPI/V02NoPID/UParTAK4_v2.onnx'),
    output_names = cms.vstring('softmax_8'),
    usePID = cms.bool(False),
    verbose = cms.bool(False),
    testMode = cms.string("off"), # "off", "testOnnx", "testCpu", "print"
    # testN = cms.uint32(3),
    # testM = cms.uint32(2),
)

# declare all the discriminators
# probs
_pfNoPIDParticleTransformerAK4JetTagsProbs = ['pfNoPIDParticleTransformerAK4JetTags:' + flav_name
                                 for flav_name in pfNoPIDParticleTransformerAK4JetTags.flav_names]
# meta-taggers
_pfNoPIDParticleTransformerAK4JetTagsMetaDiscrs = ['pfNoPIDParticleTransformerAK4DiscriminatorsJetTags:' + disc.name.value()
                                      for disc in pfNoPIDParticleTransformerAK4DiscriminatorsJetTags.discriminators]
_pfNoPIDParticleTransformerAK4JetTagsAll = _pfNoPIDParticleTransformerAK4JetTagsProbs + _pfNoPIDParticleTransformerAK4JetTagsMetaDiscrs



# ==
# # This task is not used, useful only if we run it from RECO jets (RECO/AOD)
pfNoPIDParticleTransformerAK4Task = cms.Task(puppi, primaryVertexAssociation,
                             pfNoPIDParticleTransformerAK4TagInfos, pfNoPIDParticleTransformerAK4JetTags,
                             pfNoPIDParticleTransformerAK4DiscriminatorsJetTags)
# # run from MiniAOD instead
pfNoPIDParticleTransformerAK4FromMiniAODTask = cms.Task(pfNoPIDParticleTransformerAK4TagInfos,
                             pfNoPIDParticleTransformerAK4JetTags,
                             pfNoPIDParticleTransformerAK4DiscriminatorsJetTags)
