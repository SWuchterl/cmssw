import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *
from PhysicsTools.NanoAOD.simpleGenJetFlatTableProducer_cfi import simpleGenJetFlatTableProducer
from PhysicsTools.NanoAOD.simplePATJetFlatTableProducer_cfi import simplePATJetFlatTableProducer
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
from RecoBTag.ONNXRuntime.pfParticleNet_cff import _pfMassDecorrelatedParticleNetJetTagsProbs, _pfParticleNetMassRegressionOutputs

#from PhysicsTools.NanoTuples.jetUtils import addCustomJets
from NanoTuples.NanoTuples.jetUtils import addCustomJets


def setupAK15(process, runOnMC=False, path=None, runParticleNetMD=True, customAK15Taggers=[]):
    # cluster AK15Puppi jets
    addCustomJets(process, rParam=1.5, jetAlgo='ak15', minPt=150, runOnMC=runOnMC)

    bTagDiscriminators = []
    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']
    if runParticleNetMD:
        bTagDiscriminators += _pfMassDecorrelatedParticleNetJetTagsProbs + _pfParticleNetMassRegressionOutputs
    if len(customAK15Taggers) > 0:
        branchInfo = []
        for name in customAK15Taggers:
            disc, bchinfo = getCustomTaggerDiscriminatorsAK15(name)
            bTagDiscriminators += disc
            branchInfo += bchinfo

    updateJetCollection(
        process,
        jetSource=cms.InputTag('packedPatJetsAK15PFPuppiSoftDrop'),
        rParam=1.5,
        jetCorrections=('AK8PFPuppi', cms.vstring(JETCorrLevels), 'None'),
        btagDiscriminators=bTagDiscriminators,
        postfix='AK15ParticleNet',
    )

    if runParticleNetMD:
        process.pfParticleNetTagInfosAK15ParticleNet.jet_radius = 1.5
        process.pfMassDecorrelatedParticleNetJetTagsAK15ParticleNet.preprocess_json = 'RecoBTag/Combined/data/ParticleNet-MD/ak15/V02d/preprocess.json'
        process.pfMassDecorrelatedParticleNetJetTagsAK15ParticleNet.model_path = 'RecoBTag/Combined/data/ParticleNet-MD/ak15/V02d/particle-net.onnx'
        process.pfParticleNetMassRegressionJetTagsAK15ParticleNet.preprocess_json = 'RecoBTag/Combined/data/MassRegression/ak15/V01c/preprocess.json'
        process.pfParticleNetMassRegressionJetTagsAK15ParticleNet.model_path = 'RecoBTag/Combined/data/MassRegression/ak15/V01c/particle_net_regression.onnx'

    if len(customAK15Taggers) > 0:
        process.pfParticleTransformerAK15TagInfosAK15ParticleNet.jet_radius = 1.5
        process.pfParticleTransformerAK15JetTagsAK15ParticleNet.preprocess_json = 'RecoBTag/Combined/data/InclParticleTransformer-MD/ak15/V02/preprocess_corr.json'
        process.pfParticleTransformerAK15JetTagsAK15ParticleNet.model_path = 'RecoBTag/Combined/data/InclParticleTransformer-MD/ak15/V02/model.onnx'
        process.pfParticleTransformerAK15JetTagsAK15ParticleNet.preprocess_json = 'RecoBTag/Combined/data/OfflineGlobalParticleTransformerAK15/preprocess.json'
        process.pfParticleTransformerAK15JetTagsAK15ParticleNet.model_path = 'RecoBTag/Combined/data/OfflineGlobalParticleTransformerAK15/model_ak15.onnx'

    # src
    srcJets = cms.InputTag('selectedUpdatedPatJetsAK15ParticleNet')

    # jetID
    process.tightJetIdAK15Puppi = cms.EDProducer("PatJetIDValueMapProducer",
        filterParams=cms.PSet(
            version=cms.string('RUN2ULPUPPI'),
            quality=cms.string('TIGHT'),
        ),
        src=srcJets
    )

    process.tightJetIdLepVetoAK15Puppi = cms.EDProducer("PatJetIDValueMapProducer",
        filterParams=cms.PSet(
            version=cms.string('RUN2ULPUPPI'),
            quality=cms.string('TIGHTLEPVETO'),
        ),
        src=srcJets
    )

    process.ak15WithUserData = cms.EDProducer("PATJetUserDataEmbedder",
        src=srcJets,
        userFloats=cms.PSet(),
        userInts=cms.PSet(
            tightId=cms.InputTag("tightJetIdAK15Puppi"),
            tightIdLepVeto=cms.InputTag("tightJetIdLepVetoAK15Puppi"),
        ),
    )

    process.ak15Table = simplePATJetFlatTableProducer.clone(
        src=cms.InputTag("ak15WithUserData"),
        name=cms.string("AK15Puppi"),
        cut=cms.string(""),
        doc=cms.string("ak15 puppi jets"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the main table for the jets
        variables=cms.PSet(P4Vars,
            jetId=Var("userInt('tightId')*2+4*userInt('tightIdLepVeto')", int, doc="Jet ID flags bit1 is loose (always false in 2017 since it does not exist), bit2 is tight, bit3 is tightLepVeto"),
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            # nPFConstituents=Var("numberOfDaughters()", int, doc="Number of PF candidate constituents"),
            tau1=Var("userFloat('NjettinessAK15Puppi:tau1')", float, doc="Nsubjettiness (1 axis)", precision=10),
            tau2=Var("userFloat('NjettinessAK15Puppi:tau2')", float, doc="Nsubjettiness (2 axis)", precision=10),
            tau3=Var("userFloat('NjettinessAK15Puppi:tau3')", float, doc="Nsubjettiness (3 axis)", precision=10),
            msoftdrop=Var("groomedMass()", float, doc="Corrected soft drop mass with PUPPI", precision=10),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
            subJetIdx1=Var("?nSubjetCollections()>0 && subjets().size()>0?subjets()[0].key():-1", int,
                 doc="index of first subjet"),
            subJetIdx2=Var("?nSubjetCollections()>0 && subjets().size()>1?subjets()[1].key():-1", int,
                 doc="index of second subjet"),
        )
    )
    process.ak15Table.variables.pt.precision = 10

    if runParticleNetMD:
        for prob in _pfMassDecorrelatedParticleNetJetTagsProbs + _pfParticleNetMassRegressionOutputs:
            name = 'ParticleNetMD_' + prob.split(':')[1]
            setattr(process.ak15Table.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))

    # add other AK15 custom taggers
    if len(customAK15Taggers) > 0:
        for name, var_info in branchInfo:
            setattr(process.ak15Table.variables, name, var_info)

    process.ak15SubJetTable = simplePATJetFlatTableProducer.clone(
        src=cms.InputTag("selectedPatJetsAK15PFPuppiSoftDropPacked", "SubJets"),
        cut=cms.string(""),
        name=cms.string("AK15PuppiSubJet"),
        doc=cms.string("ak15 puppi subjets"),
        singleton=cms.bool(False),  # the number of entries is variable
        extension=cms.bool(False),  # this is the main table for the jets
        variables=cms.PSet(P4Vars,
            area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
            rawFactor=Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=6),
            nBHadrons=Var("jetFlavourInfo().getbHadrons().size()", int, doc="number of b-hadrons"),
            nCHadrons=Var("jetFlavourInfo().getcHadrons().size()", int, doc="number of c-hadrons"),
        )
    )
    process.ak15SubJetTable.variables.pt.precision = 10

    process.ak15Task = cms.Task(
        process.tightJetIdAK15Puppi,
        process.tightJetIdLepVetoAK15Puppi,
        process.ak15WithUserData,
        process.ak15Table,
        process.ak15SubJetTable,
    )

    if runOnMC:
        # process.slimmedGenJetsAK15 = cms.EDProducer("PATGenJetSlimmer",
        #     src = cms.InputTag("ak15GenJetsNoNu"),
        #     packedGenParticles = cms.InputTag("packedGenParticles"),
        #     cut = cms.string("pt > 80"),
        #     cutLoose = cms.string("pt > 10."),
        #     nLoose = cms.uint32(3),
        #     clearDaughters = cms.bool(False), #False means rekeying
        #     dropSpecific = cms.bool(False),
        # )

        process.genJetAK15Table = simpleGenJetFlatTableProducer.clone(
            src=cms.InputTag("ak15GenJetsNoNu"),
            cut=cms.string("pt > 100."),
            name=cms.string("GenJetAK15"),
            doc=cms.string("AK15 GenJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.genJetAK15Table.variables.pt.precision = 10

        process.genSubJetAK15Table = simpleGenJetFlatTableProducer.clone(
            src=cms.InputTag("ak15GenJetsNoNuSoftDrop", "SubJets"),
            cut=cms.string(""),
            name=cms.string("GenSubJetAK15"),
            doc=cms.string("AK15 Gen-SubJets made with visible genparticles"),
            singleton=cms.bool(False),  # the number of entries is variable
            extension=cms.bool(False),  # this is the main table for the genjets
            variables=cms.PSet(P4Vars,
            )
        )
        process.genSubJetAK15Table.variables.pt.precision = 10

        # process.ak15Task.add(process.slimmedGenJetsAK15)
        process.ak15Task.add(process.genJetAK15Table)
        process.ak15Task.add(process.genSubJetAK15Table)
        ###############################################

    if path is None:
        process.schedule.associate(process.ak15Task)
    else:
        getattr(process, path).associate(process.ak15Task)


def getCustomTaggerDiscriminatorsAK15(name):
    customTaggersAvailableDict = {
        # 'InclParticleTransformerV2': {
        #     'cff_path': 'RecoBTag.ONNXRuntime.pfParticleTransformerAK15_cff',
        #     'disc_name': '_pfParticleTransformerAK15JetTagsAll',
        #     'nano_branch_name': 'ParT',
        # },
        'GlobalParticleTransformerV3': {
            'cff_path': 'RecoBTag.ONNXRuntime.pfParticleTransformerAK15_cff',
            'disc_name': '_pfParticleTransformerAK15JetTagsAll',
            'nano_branch_name': 'ParTv3',
        },
    }

    cfg = customTaggersAvailableDict[name]
    mod = __import__(cfg['cff_path'], globals(), locals(), [cfg['disc_name']])
    btagDiscriminators = getattr(mod, cfg['disc_name'])

    # variables to store in NanoAOD FatJet table
    branchInfo = []
    for prob in btagDiscriminators:
        if 'probHW' in prob or 'probHZ' in prob:
            continue
        name = cfg['nano_branch_name'] + '_' + prob.split(':')[1]
        branchInfo.append([name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1)])

    return btagDiscriminators, branchInfo
