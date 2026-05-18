import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask, addToProcessAndTask
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection, setupPuppiForPackedPF
from PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi import selectedPatJets
from PhysicsTools.PatAlgos.tools.coreTools import removeMCMatching

from RecoJets.JetProducers.ak8PFJets_cfi import ak8PFJetsPuppi, ak8PFJetsPuppiSoftDrop
from RecoJets.JetProducers.ak8GenJets_cfi import ak8GenJets, ak8GenJetsSoftDrop
from RecoJets.JetProducers.nJettinessAdder_cfi import Njettiness


def addCustomJets(process, rParam=1.5, jetAlgo='ak15', minPt=150, runOnMC=True, postfix=""):

    task = getPatAlgosToolsTask(process)

    def add_module(label, module, no_opt=False):
        if not no_opt:
            addToProcessAndTask(label, module, process, task)
        return label

    pfCands = 'packedPFCandidates'
    puppiWeights = setupPuppiForPackedPF(process)[0]
    genParticlesLabel = 'prunedGenParticles'
    pvLabel = 'offlineSlimmedPrimaryVertices'
    svLabel = 'slimmedSecondaryVertices'
    muLabel = 'slimmedMuons'
    elLabel = 'slimmedElectrons'

    # ===== RECO jets ======
    pfJets = add_module(
        jetAlgo + 'PFJetsPuppi' + postfix,
        ak8PFJetsPuppi.clone(
            rParam=rParam,
            jetPtMin=100,
            src=pfCands,
            applyWeight=True,
            srcWeights=puppiWeights,
        )
    )
    pfJetsConstituents = add_module(
        jetAlgo + 'PFJetsPuppiConstituents' + postfix,
        cms.EDProducer(
            "MiniAODJetConstituentSelector",
            src=cms.InputTag(pfJets),
            cut=cms.string('pt > 100')
        )
    )
    pfJetsSoftDrop = add_module(
        jetAlgo + 'PFJetsPuppiSoftDrop' + postfix,
        ak8PFJetsPuppiSoftDrop.clone(
            src=pfJetsConstituents + ':constituents',
            applyWeight=True,
            srcWeights=puppiWeights,
            R0=cms.double(rParam),
            rParam=cms.double(rParam),
            jetPtMin=100,
        )
    )

    # ===== GEN jets ======
    genParticlesNoNu = add_module(
        'packedGenParticlesForJetsNoNu',
        cms.EDFilter("CandPtrSelector",
                     src=cms.InputTag("packedGenParticles"),
                     cut=cms.string("abs(pdgId) != 12 && abs(pdgId) != 14 && abs(pdgId) != 16"),
                     ),
        no_opt=(not runOnMC)
    )
    genJets = add_module(
        jetAlgo + 'GenJetsNoNu' + postfix,
        ak8GenJets.clone(
            src=genParticlesNoNu,
            rParam=rParam,
            jetPtMin=50,
        ),
        no_opt=(not runOnMC)
    )
    # TODO: fix JetConstituentSelector.cc
    # genJetsConstituents = add_module(
    #     jetAlgo + 'GenJetsNoNuConstituents' + postfix,
    #     cms.EDProducer(
    #         "GenJetPackedConstituentSelector",
    #         src=cms.InputTag(genJets),
    #         cut=cms.string('pt > 50')
    #     ),
    #     no_opt=(not runOnMC)
    # )
    genJetsSoftDrop = add_module(
        jetAlgo + 'GenJetsNoNuSoftDrop' + postfix,
        ak8GenJetsSoftDrop.clone(
            # src=genJetsConstituents + ':constituents',
            src=genParticlesNoNu,
            R0=cms.double(rParam),
            rParam=cms.double(rParam),
            jetPtMin=cms.double(50),
        ),
        no_opt=(not runOnMC)
    )

    patJetsLabel = jetAlgo.upper() + 'PFPuppi' + postfix
    addJetCollection(
        process,
        labelName=patJetsLabel,
        jetSource=cms.InputTag(pfJets),
        postfix=postfix,
        rParam=rParam,
        jetCorrections=('AK8PFPuppi', ['L2Relative', 'L3Absolute', 'L2L3Residual'], 'None'),
        genJetCollection=cms.InputTag(genJets),
        pfCandidates=cms.InputTag(pfCands),
        pvSource=cms.InputTag(pvLabel),
        svSource=cms.InputTag(svLabel),
        muSource=cms.InputTag(muLabel),
        elSource=cms.InputTag(elLabel),
        btagDiscriminators=['None'],
        getJetMCFlavour=runOnMC,
        genParticles=cms.InputTag(genParticlesLabel),
    )
    patJets = 'patJets' + patJetsLabel
    selPatJets = add_module(
        'selectedPatJets' + patJetsLabel,
        selectedPatJets.clone(
            src=patJets,
            cut=f'pt > {minPt} && abs(eta()) < 2.5',
        )
    )
    if hasattr(process, 'patJetFlavourAssociation' + patJetsLabel):
        getattr(process, 'patJetFlavourAssociation' + patJetsLabel).weights = cms.InputTag(puppiWeights)

    patJetsSoftDropLabel = jetAlgo.upper() + 'PFPuppiSoftDrop' + postfix
    addJetCollection(
        process,
        labelName=patJetsSoftDropLabel,
        jetSource=cms.InputTag(pfJetsSoftDrop),
        rParam=rParam,
        jetCorrections=('AK8PFPuppi', ['L2Relative', 'L3Absolute', 'L2L3Residual'], 'None'),
        pvSource=cms.InputTag(pvLabel),
        btagDiscriminators=['None'],
        genJetCollection=cms.InputTag(genJets),
        getJetMCFlavour=False,  # jet flavor should always be disabled for groomed jets
        genParticles=cms.InputTag(genParticlesLabel),
    )
    patJetsSoftDrop = 'patJets' + patJetsSoftDropLabel
    selPatJetsSoftDrop = add_module(
        'selectedPatJets' + patJetsSoftDropLabel,
        selectedPatJets.clone(
            src=patJetsSoftDrop,
            cut=f'pt > {minPt} && abs(eta()) < 2.5',
        )
    )

    patJetsSoftDropSubjetsLabel = jetAlgo.upper() + 'PFPuppiSoftDropSubjets' + postfix
    addJetCollection(
        process,
        labelName=patJetsSoftDropSubjetsLabel,
        jetSource=cms.InputTag(pfJetsSoftDrop, 'SubJets'),
        rParam=rParam,
        jetCorrections=('AK4PFPuppi', ['L2Relative', 'L3Absolute', 'L2L3Residual'], 'None'),
        genJetCollection=cms.InputTag(genJetsSoftDrop, 'SubJets'),
        pfCandidates=cms.InputTag(pfCands),
        pvSource=cms.InputTag(pvLabel),
        svSource=cms.InputTag(svLabel),
        muSource=cms.InputTag(muLabel),
        elSource=cms.InputTag(elLabel),
        btagDiscriminators=['None'],
        getJetMCFlavour=runOnMC,
        genParticles=cms.InputTag(genParticlesLabel),
        fatJets=cms.InputTag(pfJets),
        groomedFatJets=cms.InputTag(pfJetsSoftDrop),
    )
    patJetsSoftDropSubjets = 'patJets' + patJetsSoftDropSubjetsLabel
    selPatJetsSoftDropSubjets = add_module(
        'selectedPatJets' + patJetsSoftDropSubjetsLabel,
        selectedPatJets.clone(
            src=patJetsSoftDropSubjets,
            cut='',
        )
    )
    if hasattr(process, 'patJetFlavourAssociation' + patJetsSoftDropSubjetsLabel):
        getattr(process, 'patJetFlavourAssociation' + patJetsSoftDropSubjetsLabel).weights = cms.InputTag(puppiWeights)

    selPatJetsSoftDropPacked = add_module(
        selPatJetsSoftDrop + 'Packed',
        cms.EDProducer("BoostedJetMerger",
                       jetSrc=cms.InputTag(selPatJetsSoftDrop),
                       subjetSrc=cms.InputTag(selPatJetsSoftDropSubjets)
                       )

    )

    packedPatJetsSoftDrop = add_module(
        'packedPatJets' + patJetsSoftDropLabel,
        cms.EDProducer("JetSubstructurePacker",
                       jetSrc=cms.InputTag(selPatJets),
                       distMax=cms.double(rParam),
                       fixDaughters=cms.bool(False),
                       algoTags=cms.VInputTag(
                           cms.InputTag(selPatJetsSoftDropPacked)
                       ),
                       algoLabels=cms.vstring('SoftDrop'),
                       )
    )

    njettiness = add_module(
        'Njettiness' + jetAlgo.upper() + 'Puppi' + postfix,
        Njettiness.clone(
            src=cms.InputTag(pfJets),
            Njets=cms.vuint32(1, 2, 3),
            R0=cms.double(rParam),
            srcWeights=puppiWeights,
        )
    )
    for tau in (1, 2, 3):
        getattr(process, patJets).userData.userFloats.src += [f'{njettiness}:tau{tau}']

    if not runOnMC:
        removeMCMatching(process, names=['Jets'], postfix=postfix, outputModules=[])
