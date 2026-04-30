import FWCore.ParameterSet.Config as cms


def customiseForScoutingSecondaryVertices(process, pName):

    process.TransientTrackBuilderESProducer = cms.ESProducer( "TransientTrackBuilderESProducer",
      ComponentName = cms.string( "TransientTrackBuilder" ),
      appendToDataLabel = cms.string( "" )
    )

    from RecoVertex.AdaptiveVertexFinder.inclusiveVertexFinder_cfi import inclusiveVertexFinder

    process.inclusiveVertexFinder = inclusiveVertexFinder.clone(
        beamSpot = cms.InputTag("offlineBeamSpot", "", pName),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName),
        tracks = cms.InputTag("scoutingTracks"),
    )

    from RecoVertex.AdaptiveVertexFinder.vertexMerger_cfi import vertexMerger
    process.vertexMerger = vertexMerger.clone(
        secondaryVertices = cms.InputTag("inclusiveVertexFinder", "", pName),
        )

    from RecoVertex.AdaptiveVertexFinder.trackVertexArbitrator_cfi import trackVertexArbitrator
    process.trackVertexArbitrator = trackVertexArbitrator.clone(
        beamSpot = cms.InputTag("offlineBeamSpot", "", pName),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName),
        tracks = cms.InputTag("scoutingTracks"),
        secondaryVertices = cms.InputTag("vertexMerger", "", pName),
            )

    process.inclusiveSecondaryVertices = vertexMerger.clone(
        secondaryVertices = cms.InputTag("trackVertexArbitrator", "", pName),
        maxFraction = 0.2,
        minSignificance = 10.
    )

    process.slimmedSecondaryVertices = cms.EDProducer("PATSecondaryVertexSlimmer",
        src = cms.InputTag("inclusiveSecondaryVertices", "", "%s"%pName),
        packedPFCandidates = cms.InputTag("packedPFCandidates", "", "%s"%pName),
        lostTracksCandidates = cms.InputTag("lostTracks", "", pName)
    )   


    process.scoutingTransientTrackBuilderTask = cms.Task(process.TransientTrackBuilderESProducer)

    process.scoutingSecondaryVertexTask = cms.Task(process.inclusiveVertexFinder,
                                      process.vertexMerger,
                                      process.trackVertexArbitrator,
                                      process.inclusiveSecondaryVertices,
                                      process.slimmedSecondaryVertices)

    return process


def customiseForScoutingSecondaryCandidateVertices(process, pName):
    process.TransientTrackBuilderESProducer = cms.ESProducer( "TransientTrackBuilderESProducer",
      ComponentName = cms.string( "TransientTrackBuilder" ),
      appendToDataLabel = cms.string( "" )
    )

    from RecoVertex.AdaptiveVertexFinder.inclusiveCandidateVertexFinder_cfi import inclusiveCandidateVertexFinder
    process.inclusiveCandidateVertexFinder = inclusiveCandidateVertexFinder.clone(
        beamSpot = cms.InputTag("offlineBeamSpot", "", "%s"%pName),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", "%s"%pName),
        tracks = cms.InputTag("packedPFCandidates", "recoCands", "%s"%pName),
        minHits = cms.uint32(8), # HLT is 8, offline is 0
    )

    from RecoVertex.AdaptiveVertexFinder.candidateVertexMerger_cfi import candidateVertexMerger
    process.candidateVertexMerger = candidateVertexMerger.clone(
        secondaryVertices = cms.InputTag("inclusiveCandidateVertexFinder", "", "%s"%pName),
    )

    from RecoVertex.AdaptiveVertexFinder.candidateVertexArbitrator_cfi import candidateVertexArbitrator
    process.candidateVertexArbitrator = candidateVertexArbitrator.clone(
        beamSpot = cms.InputTag("offlineBeamSpot", "", "%s"%pName),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", "%s"%pName),
        tracks = cms.InputTag("packedPFCandidates", "recoCands", "%s"%pName),
        secondaryVertices = cms.InputTag("candidateVertexMerger"),
    )

    process.inclusiveCandidateSecondaryVertices = candidateVertexMerger.clone(
        secondaryVertices = cms.InputTag("candidateVertexArbitrator", "", "%s"%pName),
        maxFraction = cms.double(0.2),
        minSignificance = cms.double(10.0)
    )

    process.slimmedCandidateSecondaryVertices = cms.EDProducer("PATSecondaryVertexSlimmer",
        src = cms.InputTag("inclusiveCandidateSecondaryVertices", "", "%s"%pName),
        packedPFCandidates = cms.InputTag("packedPFCandidates", "", "%s"%pName),
        lostTracksCandidates = cms.InputTag("lostTracks", "", pName)
    )   

    process.scoutingTransientTrackBuilderTask = cms.Task(process.TransientTrackBuilderESProducer)

    process.scoutingCandidateSecondaryVertexTask = cms.Task(process.inclusiveCandidateVertexFinder, process.candidateVertexMerger, process.candidateVertexArbitrator, process.inclusiveCandidateSecondaryVertices, process.slimmedCandidateSecondaryVertices)
    #process.scoutingSecondaryVertexTask = cms.Task(process.inclusiveCandidateVertexFinder, process.candidateVertexMerger, process.candidateVertexArbitrator, process.inclusiveCandidateSecondaryVertices)

    #process.scoutingToMiniAODTask.add(process.scoutingTransientTrackBuilderTask, process.scoutingSecondaryVertexTask)

    return process

def customizeForScoutingLostTracks(process, pName):
    #LostTracks

    
    from PhysicsTools.PatAlgos.slimming.packedPFCandidates_cfi import packedPFCandidates
    from CommonTools.RecoAlgos.primaryVertexAssociation_cfi import primaryVertexAssociation

    process.lostTracks = cms.EDProducer("PATLostTracks",
        inputCandidates = cms.InputTag("packedPFCandidates", "recoCands", pName),
        packedPFCandidates	= cms.InputTag("packedPFCandidates", "", pName),
        inputTracks = cms.InputTag("scoutingTracks"),
        secondaryVertices = cms.InputTag("inclusiveSecondaryVertices", "", pName),
        kshorts=cms.InputTag("scoutingV0Candidates","Kshort"),
        lambdas=cms.InputTag("scoutingV0Candidates","Lambda"),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", "%s"%pName),
        originalVertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", "%s"%pName),
        muons = cms.InputTag("slimmedMuons", "", pName),
        minPt = cms.double(0.95),
        minHits = cms.uint32(8),
        minPixelHits = cms.uint32(1),
        covarianceVersion = cms.int32(1), #so far: 0 is Phase0, 1 is Phase1
        covariancePackingSchemas = packedPFCandidates.covariancePackingSchemas,
        qualsToAutoAccept = cms.vstring("highPurity"),
        minPtToStoreProps = cms.double(0.95),
        minPtToStoreLowQualityProps = cms.double(0.0),
        passThroughCut = cms.string("pt>2"),
        pvAssignment = primaryVertexAssociation.assignment,
        useLegacySetup = cms.bool(False), #When True: check only if track used to fit vertex[0] and do not store track detailed info for Pt between 0.5 and minPtToStoreProps GeV
        xiSelection = cms.bool(True),
        xiMassCut = cms.double(1.5)
    )


    #process.lostTracks = cms.EDProducer("Run3ScoutingLostTrackProducer",
    #        src = cms.InputTag("scoutingTracks"),
    #        particles = cms.InputTag("packedPFCandidates", "", "%s"%pName)
    #)
    #Candidates from LostTracks
    process.lostTrackCandidates = cms.EDProducer("ConcreteChargedCandidateProducer",
        src = cms.InputTag("lostTracks", "", pName),
        particleType = cms.string('pi+')
    )

    process.scoutingLostTracksTask = cms.Task(process.lostTracks, process.lostTrackCandidates)
    #process.scoutingLostTracksTask = cms.Task(process.lostTracks)

    return process


def customizeForScoutingV0s(process, pName):
    from RecoVertex.V0Producer.generalV0Candidates_cfi import generalV0Candidates
    process.scoutingV0Candidates = generalV0Candidates.clone(
        beamSpot = cms.InputTag("offlineBeamSpot", "", pName),
        vertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName),
        trackRecoAlgorithm = cms.InputTag("scoutingTracks"),
        innerHitPosCut = cms.double(-1) # disable, default is 4
    )

    from PhysicsTools.PatAlgos.slimming.slimmedSecondaryVertices_cfi import slimmedSecondaryVertices
    process.slimmedKshortVertices=slimmedSecondaryVertices.clone(src=cms.InputTag("scoutingV0Candidates","Kshort"), packedPFCandidates = cms.InputTag("packedPFCandidates", "", "%s"%pName), lostTracksCandidates = cms.InputTag("lostTracks", "", pName)
 )
    process.slimmedLambdaVertices=slimmedSecondaryVertices.clone(src=cms.InputTag("scoutingV0Candidates","Lambda"), packedPFCandidates = cms.InputTag("packedPFCandidates", "", "%s"%pName), lostTracksCandidates = cms.InputTag("lostTracks", "", pName)
)


    process.scoutingV0Task = cms.Task(process.scoutingV0Candidates, process.slimmedKshortVertices, process.slimmedLambdaVertices)    

    return process



def customizeForScoutingAK8ReclusteredJets(process, pName):

    from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets

    process.recoScoutingFatPFJetRecluster = ak4PFJets.clone(
        src = ("packedPFCandidates", "recoCands", pName),
        rParam   = 0.8,
        jetPtMin = 170.0,
    )

    from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import patJetCorrFactors
    process.scoutingFatPFJetReclusterCorrFactors = patJetCorrFactors.clone(
        src = "recoScoutingFatPFJetRecluster",
        levels = cms.vstring(
            "L1FastJet",
            "L2Relative",
            "L3Absolute",
            "L2L3Residual"),
        payload = cms.string("AK8PFHLT"),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName),
    )

    from RecoJets.JetAssociationProducers.ak4JTA_cff import ak4JetTracksAssociatorAtVertex
    process.scoutingFatPFJetReclusterTracksAssociatorAtVertex = ak4JetTracksAssociatorAtVertex.clone(
        jets = cms.InputTag("recoScoutingFatPFJetRecluster"),
        coneSize = cms.double(0.4),
        tracks = cms.InputTag("scoutingTracks"),
        pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName),
    )

    from PhysicsTools.PatAlgos.recoLayer0.jetTracksCharge_cff import patJetCharge
    process.scoutingFatPFJetReclusterCharge = patJetCharge.clone(
        src = cms.InputTag("scoutingFatPFJetReclusterTracksAssociatorAtVertex"),
    )

    process.scoutingFatPFJetReclusterPrimaryVertexAssociation = cms.EDProducer("PFCandidatePrimaryVertexSorter",
        assignment = cms.PSet(
            DzCutForChargedFromPUVtxs = cms.double(0.2),
            EtaMinUseDz = cms.double(-1.0),
            NumOfPUVtxsForCharged = cms.uint32(0),
            OnlyUseFirstDz = cms.bool(False),
            PtMaxCharged = cms.double(-1.0),
            maxDistanceToJetAxis = cms.double(0.07),
            maxDtSigForPrimaryAssignment = cms.double(3.0),
            maxDxyForJetAxisAssigment = cms.double(0.1),
            maxDxyForNotReconstructedPrimary = cms.double(0.01),
            maxDxySigForNotReconstructedPrimary = cms.double(2.0),
            maxDzErrorForPrimaryAssignment = cms.double(0.05),
            maxDzForJetAxisAssigment = cms.double(0.1),
            maxDzForPrimaryAssignment = cms.double(0.1),
            maxDzSigForPrimaryAssignment = cms.double(5.0),
            maxJetDeltaR = cms.double(0.5),
            minJetPt = cms.double(5.0), # lower from 25.0
            preferHighRanked = cms.bool(False),
            useTiming = cms.bool(False),
            useVertexFit = cms.bool(True)
        ),
        jets = cms.InputTag("recoScoutingFatPFJetRecluster"),
        particles = cms.InputTag("packedPFCandidates", "recoCands", pName),
        produceAssociationToOriginalVertices = cms.bool(True),
        produceNoPileUpCollection = cms.bool(False),
        producePileUpCollection = cms.bool(False),
        produceSortedVertices = cms.bool(False),
        qualityForPrimary = cms.int32(2),
        sorting = cms.PSet(

        ),
        usePVMET = cms.bool(True),
        vertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName)
    )

    process.scoutingFatPFJetReclusterHLTParticleNetJetTagsInfosAK8 = cms.EDProducer("DeepBoostedJetTagInfoProducer",
        covariancePackingSchemas = cms.vint32(8, 264, 520, 776, 0),
        covarianceVersion = cms.int32(1),
        dxy_value_map = cms.InputTag(""),
        dxysig_value_map = cms.InputTag(""),
        dz_value_map = cms.InputTag(""),
        dzsig_value_map = cms.InputTag(""),
        flip_ip_sign = cms.bool(False),
        include_neutrals = cms.bool(True),
        jet_radius = cms.double(0.8),
        jets = cms.InputTag("recoScoutingFatPFJetRecluster"),
        lostInnerHits_value_map = cms.InputTag(""),
        max_jet_eta = cms.double(2.5),
        min_jet_pt = cms.double(200.0),
        min_pt_for_pfcandidates = cms.double(0.1),
        min_pt_for_track_properties = cms.double(0.95),
        min_puppi_wgt = cms.double(-1.0),
        normchi2_value_map = cms.InputTag(""),
        pf_candidates = cms.InputTag("packedPFCandidates", "recoCands", pName),
        puppi_value_map = cms.InputTag(""),
        quality_value_map = cms.InputTag(""),
        secondary_vertices = cms.InputTag("inclusiveCandidateSecondaryVertices", "", pName),
        sip3dSigMax = cms.double(-1.0),
        sort_by_sip2dsig = cms.bool(False),
        trkEta_value_map = cms.InputTag(""),
        trkPhi_value_map = cms.InputTag(""),
        trkPt_value_map = cms.InputTag(""),
        unsubjet_map = cms.InputTag(""),
        use_hlt_features = cms.bool(True),
        use_puppiP4 = cms.bool(False),
        use_scouting_features = cms.bool(False),
        vertex_associator = cms.InputTag("scoutingFatPFJetReclusterPrimaryVertexAssociation", "original"),
        vertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName)
    )

    process.scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8 = cms.EDProducer("BoostedJetONNXJetTagsProducer",
        debugMode = cms.untracked.bool(False),
        flav_names = cms.vstring('probHtt', 'probHtm', 'probHte', 'probHbb', 'probHcc', 'probHqq', 'probHgg', 'probQCD2hf', 'probQCD1hf', 'probQCD0hf'),
        jets = cms.InputTag(""),
        model_path = cms.FileInPath('RecoBTag/Combined/data/HLT/ParticleNetAK8/V01/particle-net.onnx'),
        preprocessParams = cms.PSet(

        ),
        preprocess_json = cms.string('RecoBTag/Combined/data/HLT/ParticleNetAK8/V01/preprocess.json'),
        produceValueMap = cms.untracked.bool(False),
        src = cms.InputTag("scoutingFatPFJetReclusterHLTParticleNetJetTagsInfosAK8")
    )

    # convert to PAT
    from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import _patJets
    process.patScoutingFatPFJetRecluster = _patJets.clone(
        jetSource = "recoScoutingFatPFJetRecluster",
        addJetCorrFactors = True,
        jetCorrFactorsSource = [
            "scoutingFatPFJetReclusterCorrFactors",
            ],
        addBTagInfo = True,
        addDiscriminators = True,
        discriminatorSources = [
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probHtt",
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probHtm",
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probHte",
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probHbb",
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probHcc",
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probHqq",
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probHgg",
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probQCD2hf",
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probQCD1hf",
            "scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8:probQCD0hf",
            ],
        addAssociatedTracks = False,
        addJetCharge = True,
        jetChargeSource = "scoutingFatPFJetReclusterCharge",
        addGenPartonMatch = False,
        embedGenPartonMatch = False,
        addGenJetMatch = True,
        embedGenJetMatch = True,
        genJetMatch = cms.InputTag("scoutingFatPFJetReclusterGenJetMatch"),
        getJetMCFlavour = True,
        useLegacyJetMCFlavour = False,
        addJetFlavourInfo = True,
        JetFlavourInfoSource = cms.InputTag("scoutingFatPFJetReclusterFlavourAssociation"),
    )

    process.slimmedJetsAK8 = cms.EDProducer("PATJetSlimmer",
       src = cms.InputTag("patScoutingFatPFJetRecluster"),
       packedPFCandidates = cms.InputTag("packedPFCandidates", "", pName),
       dropJetVars = cms.string("1"),
       dropDaughters = cms.string("0"),
       rekeyDaughters = cms.string("1"),
       dropTrackRefs = cms.string("1"),
       dropSpecific = cms.string("0"),
       dropTagInfos = cms.string("1"),
       modifyJets = cms.bool(True),
       mixedDaughters = cms.bool(False),
       modifierConfig = cms.PSet( modifications = cms.VPSet() )
    )


    from PhysicsTools.PatAlgos.mcMatchLayer0.jetMatch_cfi import patJetGenJetMatch
    process.scoutingFatPFJetReclusterGenJetMatch = patJetGenJetMatch.clone(
        src = cms.InputTag("recoScoutingFatPFJetRecluster"),
        matched = cms.InputTag("slimmedGenJetsAK8"),
        resolveByMatchQuality = cms.bool(True)
    )

    from PhysicsTools.NanoAOD.jetMC_cff import patJetPartonsNano

    from PhysicsTools.PatAlgos.mcMatchLayer0.jetFlavourId_cff import patJetFlavourAssociation
    process.scoutingFatPFJetReclusterFlavourAssociation = patJetFlavourAssociation.clone(
        jets = cms.InputTag("recoScoutingFatPFJetRecluster"),
        rParam = cms.double(0.8),
        bHadrons = cms.InputTag("patJetPartonsNano","bHadrons"),
        cHadrons = cms.InputTag("patJetPartonsNano","cHadrons"),
        partons = cms.InputTag("patJetPartonsNano","physicsPartons"),
        leptons = cms.InputTag("patJetPartonsNano","leptons"),
    )


    process.scoutingFatPFJetRecluster2Task = cms.Task(
            process.recoScoutingFatPFJetRecluster, # jet clustering
            process.scoutingFatPFJetReclusterCorrFactors, # JEC
            process.scoutingFatPFJetReclusterTracksAssociatorAtVertex, process.scoutingFatPFJetReclusterCharge, # jet charge
            process.scoutingFatPFJetReclusterPrimaryVertexAssociation, # pv association
            process.scoutingFatPFJetReclusterHLTParticleNetJetTagsInfosAK8, process.scoutingFatPFJetReclusterHLTParticleNetONNXJetTagsAK8, # HLTPNet tagging
            process.patScoutingFatPFJetRecluster, # pat-ify
            process.slimmedJetsAK8
    )

    process.scoutingFatPFJetRecluster2MCTask = cms.Task(
            process.patJetPartonsNano,
            process.scoutingFatPFJetReclusterGenJetMatch,
            process.scoutingFatPFJetReclusterFlavourAssociation,
    )

    return process


def customizeForScoutingAK4ReclusteredJets(process, pName):

    from RecoJets.JetProducers.ak4PFJets_cfi import ak4PFJets

    process.recoScoutingPFJetRecluster = ak4PFJets.clone(
        src = ("packedPFCandidates", "recoCands", pName),
        jetPtMin = 20,
    )

    from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import patJetCorrFactors
    process.scoutingPFJetReclusterCorrFactors = patJetCorrFactors.clone(
        src = "recoScoutingPFJetRecluster",
        levels = cms.vstring(
            "L1FastJet",
            "L2Relative",
            "L3Absolute",
            "L2L3Residual"),
        payload = cms.string("AK4PFHLT"),
        primaryVertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName),
    )

    from RecoJets.JetAssociationProducers.ak4JTA_cff import ak4JetTracksAssociatorAtVertex
    process.scoutingPFJetReclusterTracksAssociatorAtVertex = ak4JetTracksAssociatorAtVertex.clone(
        jets = cms.InputTag("recoScoutingPFJetRecluster"),
        coneSize = cms.double(0.4),
        tracks = cms.InputTag("scoutingTracks"),
        pvSrc = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName),
    )

    from PhysicsTools.PatAlgos.recoLayer0.jetTracksCharge_cff import patJetCharge
    process.scoutingPFJetReclusterCharge = patJetCharge.clone(
        src = cms.InputTag("scoutingPFJetReclusterTracksAssociatorAtVertex"),
    )

    process.scoutingPFJetReclusterPrimaryVertexAssociation = cms.EDProducer("PFCandidatePrimaryVertexSorter",
        assignment = cms.PSet(
            DzCutForChargedFromPUVtxs = cms.double(0.2),
            EtaMinUseDz = cms.double(-1.0),
            NumOfPUVtxsForCharged = cms.uint32(0),
            OnlyUseFirstDz = cms.bool(False),
            PtMaxCharged = cms.double(-1.0),
            maxDistanceToJetAxis = cms.double(0.07),
            maxDtSigForPrimaryAssignment = cms.double(3.0),
            maxDxyForJetAxisAssigment = cms.double(0.1),
            maxDxyForNotReconstructedPrimary = cms.double(0.01),
            maxDxySigForNotReconstructedPrimary = cms.double(2.0),
            maxDzErrorForPrimaryAssignment = cms.double(0.05),
            maxDzForJetAxisAssigment = cms.double(0.1),
            maxDzForPrimaryAssignment = cms.double(0.1),
            maxDzSigForPrimaryAssignment = cms.double(5.0),
            maxJetDeltaR = cms.double(0.5),
            minJetPt = cms.double(5.0), # lower from 25.0
            preferHighRanked = cms.bool(True),
            useTiming = cms.bool(False),
            useVertexFit = cms.bool(True)
        ),
        jets = cms.InputTag("recoScoutingPFJetRecluster"),
        particles = cms.InputTag("packedPFCandidates", "recoCands", pName),
        produceAssociationToOriginalVertices = cms.bool(True),
        produceNoPileUpCollection = cms.bool(False),
        producePileUpCollection = cms.bool(False),
        produceSortedVertices = cms.bool(False),
        qualityForPrimary = cms.int32(2),
        sorting = cms.PSet(

        ),
        usePVMET = cms.bool(True),
        vertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName)
    )

    process.scoutingPFJetReclusterHLTParticleNetJetTagInfos = cms.EDProducer("DeepBoostedJetTagInfoProducer",
        covariancePackingSchemas = cms.vint32(8, 264, 520, 776, 0),
        covarianceVersion = cms.int32(1),
        dxy_value_map = cms.InputTag(""),
        dxysig_value_map = cms.InputTag(""),
        dz_value_map = cms.InputTag(""),
        dzsig_value_map = cms.InputTag(""),
        flip_ip_sign = cms.bool(False),
        include_neutrals = cms.bool(True),
        jet_radius = cms.double(0.4),
        jets = cms.InputTag("recoScoutingPFJetRecluster"),
        lostInnerHits_value_map = cms.InputTag(""),
        max_jet_eta = cms.double(2.6), # HLT has 2.5
        min_jet_pt = cms.double(5.0), # lower from 30.0
        min_pt_for_pfcandidates = cms.double(0.1),
        min_pt_for_track_properties = cms.double(0.95),
        min_puppi_wgt = cms.double(-1.0),
        normchi2_value_map = cms.InputTag(""),
        #pf_candidates = cms.InputTag("packedPFCandidates", "recoCands", pName),
        pf_candidates = cms.InputTag("packedPFCandidates", "", pName),
        puppi_value_map = cms.InputTag(""),
        quality_value_map = cms.InputTag(""),
        secondary_vertices = cms.InputTag("inclusiveCandidateSecondaryVertices", "", pName),
        sip3dSigMax = cms.double(-1.0),
        sort_by_sip2dsig = cms.bool(False),
        trkEta_value_map = cms.InputTag(""),
        trkPhi_value_map = cms.InputTag(""),
        trkPt_value_map = cms.InputTag(""),
        unsubjet_map = cms.InputTag(""),
        use_hlt_features = cms.bool(True),
        use_puppiP4 = cms.bool(False),
        use_scouting_features = cms.bool(False),
        vertex_associator = cms.InputTag("scoutingPFJetReclusterPrimaryVertexAssociation", "original"),
        vertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName)
    )

    process.scoutingPFJetReclusterHLTParticleNetONNXJetTags = cms.EDProducer("BoostedJetONNXJetTagsProducer",
        debugMode = cms.untracked.bool(False),
        flav_names = cms.vstring('probtauhp', 'probtauhm', 'probb', 'probc', 'probuds', 'probg', 'ptcorr'),
        model_path = cms.FileInPath('RecoBTag/Combined/data/HLT/ParticleNetAK4/V01/particle-net.onnx'),
        preprocessParams = cms.PSet(),
        preprocess_json = cms.string('RecoBTag/Combined/data/HLT/ParticleNetAK4/V01/preprocess.json'),
        produceValueMap = cms.untracked.bool(False), # False in HLT
        src = cms.InputTag("scoutingPFJetReclusterHLTParticleNetJetTagInfos"),
        jets = cms.InputTag("recoScoutingPFJetRecluster")
    )


    process.scoutingPFJetReclusterPFUnifiedParticleTransformerAK4TagInfos = cms.EDProducer('UnifiedParticleTransformerAK4TagInfoProducer',
        jet_radius = cms.double(0.4),
        min_candidate_pt = cms.double(0.1),
        flip = cms.bool(False),
        scouting = cms.bool(True),
        sort_cand_by_pt = cms.bool(False),
        fix_lt_sorting = cms.bool(True),
        vertices = cms.InputTag("offlineSlimmedPrimaryVertices", "", pName),
        losttracks = cms.InputTag("lostTracks", "", pName),
        puppi_value_map = cms.InputTag(''),
        #secondary_vertices = cms.InputTag('inclusiveCandidateSecondaryVertices'),
        secondary_vertices = cms.InputTag('slimmedSecondaryVertices', "", pName),
        jets = cms.InputTag('recoScoutingPFJetRecluster'),
        unsubjet_map = cms.InputTag(''),
        candidates = cms.InputTag("packedPFCandidates", "recoCands", pName),
        #vertex_associator = cms.InputTag("scoutingPFJetReclusterPrimaryVertexAssociation", "original", pName),
        vertex_associator = cms.InputTag("packedPFCandidates", "vtxass", pName),
        quality = cms.InputTag("packedPFCandidates", "quality", pName),
        fallback_puppi_weight = cms.bool(True),
        fallback_vertex_association = cms.bool(True),
        is_weighted_jet = cms.bool(False),
        min_jet_pt = cms.double(0),
        max_jet_eta = cms.double(2.5),
        mightGet = cms.optional.untracked.vstring
      )

    process.scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags = cms.EDProducer('UnifiedParticleTransformerAK4ONNXJetTagsScoutingv2Producer',
        src = cms.InputTag('scoutingPFJetReclusterPFUnifiedParticleTransformerAK4TagInfos'),
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
        model_path = cms.FileInPath('RecoBTag/CombinedScouting/data/model_v2.onnx'),
        output_names = cms.vstring('ID_pred'),
        flav_names = cms.vstring(
        'probb',
        'probbb',
        'probleptonicB',
        'probc',
        'probuds',
        'probg',            
        ),
        mightGet = cms.optional.untracked.vstring
    )


    # convert to PAT
    from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi import _patJets
    process.patScoutingPFJetRecluster = _patJets.clone(
        jetSource = "recoScoutingPFJetRecluster",
        addJetCorrFactors = True,
        jetCorrFactorsSource = [
            "scoutingPFJetReclusterCorrFactors",
            ],
        addBTagInfo = True,
        addDiscriminators = True,
        discriminatorSources = [
            "scoutingPFJetReclusterHLTParticleNetONNXJetTags:probtauhp",
            "scoutingPFJetReclusterHLTParticleNetONNXJetTags:probtauhm",
            "scoutingPFJetReclusterHLTParticleNetONNXJetTags:probb",
            "scoutingPFJetReclusterHLTParticleNetONNXJetTags:probc",
            "scoutingPFJetReclusterHLTParticleNetONNXJetTags:probuds",
            "scoutingPFJetReclusterHLTParticleNetONNXJetTags:probg",
            'scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probb',
            'scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probbb',
            'scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probleptonicB',
            'scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probc',
            'scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probuds',
            'scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probg',            
           
            ],
        addAssociatedTracks = False,
        addJetCharge = True,
        jetChargeSource = "scoutingPFJetReclusterCharge",
        addGenPartonMatch = True,
        embedGenPartonMatch = True,
        genPartonMatch = cms.InputTag("scoutingPFJetReclusterGenPartonMatch"),
        addGenJetMatch = True,
        embedGenJetMatch = True,
        genJetMatch = cms.InputTag("scoutingPFJetReclusterGenJetMatch"),
        getJetMCFlavour = True,
        useLegacyJetMCFlavour = False,
        addJetFlavourInfo = True,
        JetFlavourInfoSource = cms.InputTag("scoutingPFJetReclusterFlavourAssociation"),
    )

    process.slimmedJets = cms.EDProducer("PATJetSlimmer",
       src = cms.InputTag("patScoutingPFJetRecluster"),
       packedPFCandidates = cms.InputTag("packedPFCandidates", "", pName),
       dropJetVars = cms.string("1"),
       dropDaughters = cms.string("0"),
       rekeyDaughters = cms.string("1"),
       dropTrackRefs = cms.string("1"),
       dropSpecific = cms.string("0"),
       dropTagInfos = cms.string("1"),
       modifyJets = cms.bool(True),
       mixedDaughters = cms.bool(False),
       modifierConfig = cms.PSet( modifications = cms.VPSet() )
    )



    from PhysicsTools.PatAlgos.mcMatchLayer0.jetMatch_cfi import patJetGenJetMatch, patJetPartonMatch
    process.scoutingPFJetReclusterGenJetMatch = patJetGenJetMatch.clone(
        src = cms.InputTag("recoScoutingPFJetRecluster"),
        matched = cms.InputTag("slimmedGenJets"),
        resolveByMatchQuality = cms.bool(True)
    )

    process.scoutingPFJetReclusterGenPartonMatch = patJetPartonMatch.clone(
        src = cms.InputTag("recoScoutingPFJetRecluster"),
        matched = cms.InputTag("prunedGenParticles"),
    )


    from PhysicsTools.NanoAOD.jetMC_cff import patJetPartonsNano
    process.patJetPartonsNano = patJetPartonsNano

    from PhysicsTools.PatAlgos.mcMatchLayer0.jetFlavourId_cff import patJetFlavourAssociation
    process.scoutingPFJetReclusterFlavourAssociation = patJetFlavourAssociation.clone(
        jets = cms.InputTag("recoScoutingPFJetRecluster"),
        bHadrons = cms.InputTag("patJetPartonsNano","bHadrons"),
        cHadrons = cms.InputTag("patJetPartonsNano","cHadrons"),
        partons = cms.InputTag("patJetPartonsNano","physicsPartons"),
        leptons = cms.InputTag("patJetPartonsNano","leptons"),
    )

    process.scoutingPFJetRecluster2Task = cms.Task(
            process.recoScoutingPFJetRecluster, # jet clustering
            process.scoutingPFJetReclusterCorrFactors, # JEC
            process.scoutingPFJetReclusterTracksAssociatorAtVertex, process.scoutingPFJetReclusterCharge, # jet charge
            process.scoutingPFJetReclusterPrimaryVertexAssociation, # pv association
            process.scoutingPFJetReclusterHLTParticleNetJetTagInfos, process.scoutingPFJetReclusterHLTParticleNetONNXJetTags, # HLTPNet tagging,
            process.scoutingPFJetReclusterPFUnifiedParticleTransformerAK4TagInfos, process.scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags,
            process.patScoutingPFJetRecluster, # pat-ify
            process.slimmedJets
            )

    process.scoutingPFJetRecluster2MCTask = cms.Task(
            process.patJetPartonsNano,
            process.scoutingPFJetReclusterGenJetMatch,
            process.scoutingPFJetReclusterGenPartonMatch,
            process.scoutingPFJetReclusterFlavourAssociation,
            )
    return process



def customiseScoutingForStandalone(process):

    process.load("PhysicsTools.PatFromScouting.scoutingToMiniAOD_cff")

    """
    Minimal customization for scouting for scouting outside of CMSSW data formats.

    The customization only:
    - Loads particle data table (needed for PackedCandidate producer)
    - Extends output to include scoutingTracks and L1 collections

    The --step USER:...Task handles adding the producers.
    The --eventcontent MINIAOD provides standard MiniAOD output commands.
    """

    # Load particle data table (needed for PackedCandidate producer)
    process.load("SimGeneral.HepPDTESSource.pdt_cfi")

    # Handle missing collections gracefully (not all scouting triggers save all objects)
    # This allows processing datasets where some events don't have egamma, etc.
    if hasattr(process, 'options'):
        if not hasattr(process.options, 'TryToContinue'):
            process.options.TryToContinue = cms.untracked.vstring()
        process.options.TryToContinue.append('ProductNotFound')
    else:
        process.options = cms.untracked.PSet(
            TryToContinue = cms.untracked.vstring('ProductNotFound')
        )

    process.scoutingNanoSequence += process.scoutingToMiniAODSequence

    return process

def customiseForUParTInference(process, pName):

    process = customiseScoutingForStandalone(process)
    process = customizeForScoutingLostTracks(process, pName)
    process = customiseForScoutingSecondaryCandidateVertices(process, pName)

    process = customizeForScoutingAK4ReclusteredJets(process, pName)

    return process



def customiseScoutingNanoDerived(process, pName):

    process = customiseScoutingForStandalone(process)
    process = customizeForScoutingV0s(process, pName)
    process = customizeForScoutingLostTracks(process, pName)
    process = customiseForScoutingSecondaryVertices(process, pName)
    process = customiseForScoutingSecondaryCandidateVertices(process, pName)
    process.scoutingNanoSequence.associate(process.scoutingTransientTrackBuilderTask)
    process.scoutingNanoSequence.associate(process.scoutingSecondaryVertexTask)
    process.scoutingNanoSequence.associate(process.scoutingCandidateSecondaryVertexTask)
    process.scoutingNanoSequence.associate(process.scoutingV0Task)
    process.scoutingNanoSequence.associate(process.scoutingLostTracksTask)

    process = customizeForScoutingAK4ReclusteredJets(process, pName)

    from PhysicsTools.NanoAOD.common_cff import Var, P4Vars
    PFJetVariables = cms.PSet(
        P4Vars,
        area = Var("jetArea()", float, doc="jet catchment area, for JECs",precision=10),
        chHEF = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision=10),
        neHEF = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision=10),
        chEmEF = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision=10),
        neEmEF = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision=10),
        hfHEF = Var("HFHadronEnergyFraction()",float,doc="hadronic Energy Fraction in HF",precision=10),
        hfEmEF = Var("HFEMEnergyFraction()",float,doc="electromagnetic Energy Fraction in HF",precision=10),
        muEF = Var("muonEnergyFraction()", float, doc="muon Energy Fraction", precision=10),
        chHadMultiplicity = Var("chargedHadronMultiplicity()", "int16", doc="number of charged hadrons in the jet"),
        neHadMultiplicity = Var("neutralHadronMultiplicity()", int, doc="number of neutral hadrons in the jet"),
        hfHadMultiplicity = Var("HFHadronMultiplicity()", int, doc="number of HF hadrons in the jet"),
        hfEMMultiplicity = Var("HFEMMultiplicity()", int, doc="number of HF EMs in the jet"),
        muMultiplicity = Var("muonMultiplicity()", int, doc="number of muons in the jet"),
        elMultiplicity = Var("electronMultiplicity()", int, doc="number of electrons in the jet"),
        phMultiplicity = Var("photonMultiplicity()", int, doc="number of photons in the jet"),
        nConstituents = Var("numberOfDaughters()", int, doc="number of particles in the jet"),
    )    

    from PhysicsTools.NanoAOD.simplePATJetFlatTableProducer_cfi import simplePATJetFlatTableProducer
    process.scoutingPFJetRecluster2Table = simplePATJetFlatTableProducer.clone(
        src = cms.InputTag("patScoutingPFJetRecluster"),
        name = cms.string("ScoutingPFJetRecluster2"),
        doc = cms.string(""),
        cut = cms.string(""),
        variables = cms.PSet(
            PFJetVariables,
            rawFactor = Var("1.-jecFactor('Uncorrected')", float, doc="1 - Factor to get back to raw pT", precision=10),
            charge = Var("jetCharge()", float, doc="charge", precision=10),
            hltPNet_probtauhp = Var("?(pt>=5)&&(abs(eta)<=2.6)?bDiscriminator('scoutingPFJetReclusterHLTParticleNetONNXJetTags:probtauhp'):-1", float, doc="HLT PNet tagger tauhp raw score", precision=10),
            hltPNet_probtauhm = Var("?(pt>=5)&&(abs(eta)<=2.6)?bDiscriminator('scoutingPFJetReclusterHLTParticleNetONNXJetTags:probtauhm'):-1", float, doc="HLT PNet tagger tauhm raw score", precision=10),
            hltPNet_probb = Var("?(pt>=5)&&(abs(eta)<=2.6)?bDiscriminator('scoutingPFJetReclusterHLTParticleNetONNXJetTags:probb'):-1", float, doc="HLT PNet tagger b raw score", precision=10),
            hltPNet_probc = Var("?(pt>=5)&&(abs(eta)<=2.6)?bDiscriminator('scoutingPFJetReclusterHLTParticleNetONNXJetTags:probc'):-1", float, doc="HLT PNet tagger c raw score", precision=10),
            hltPNet_probuds = Var("?(pt>=5)&&(abs(eta)<=2.6)?bDiscriminator('scoutingPFJetReclusterHLTParticleNetONNXJetTags:probuds'):-1", float, doc="HLT PNet tagger uds raw score", precision=10),
            hltPNet_probg = Var("?(pt>=5)&&(abs(eta)<=2.6)?bDiscriminator('scoutingPFJetReclusterHLTParticleNetONNXJetTags:probg'):-1", float, doc="HLT PNet tagger g raw score", precision=10),
            scoutUParT_probb = Var("?(pt>=15)&&(abs(eta)<=2.5)?bDiscriminator('scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probb'):-1", float, doc="scouting uParT tagger b raw score", precision=10),
            scoutUParT_probbb = Var("?(pt>=15)&&(abs(eta)<=2.5)?bDiscriminator('scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probbb'):-1", float, doc="scouting uParT tagger bb raw score", precision=10),
            scoutUParT_probleptonicB = Var("?(pt>=15)&&(abs(eta)<=2.5)?bDiscriminator('scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probleptonicB'):-1", float, doc="scouting uParT tagger leptonicB raw score", precision=10),
            scoutUParT_probc = Var("?(pt>=15)&&(abs(eta)<=2.5)?bDiscriminator('scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probc'):-1", float, doc="scouting uParT tagger c raw score", precision=10),
            scoutUParT_probuds = Var("?(pt>=15)&&(abs(eta)<=2.5)?bDiscriminator('scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probuds'):-1", float, doc="scouting uParT tagger uds raw score", precision=10),
            scoutUParT_probg = Var("?(pt>=15)&&(abs(eta)<=2.5)?bDiscriminator('scoutingPFJetReclusterPFUnifiedParticleTransformerAK4Tags:probg'):-1", float, doc="scouting uParT tagger g raw score", precision=10),
        ),
    )

    from PhysicsTools.NanoAOD.jetMC_cff import jetMCTable
    process.scoutingPFJetRecluster2MCTable = jetMCTable.clone(
        src = process.scoutingPFJetRecluster2Table.src,
        name = process.scoutingPFJetRecluster2Table.name,
        cut = process.scoutingPFJetRecluster2Table.cut,
    )

    process.scoutingPFJetRecluster2TableTask = cms.Task( process.scoutingSecondaryVertexTask, process.scoutingCandidateSecondaryVertexTask, process.scoutingV0Task, process.scoutingLostTracksTask, process.scoutingPFJetRecluster2Task, process.scoutingPFJetRecluster2Table)
    process.scoutingNanoSequence.associate(process.scoutingPFJetRecluster2TableTask)

    runOnMC = hasattr(process,"NANOEDMAODSIMoutput") or hasattr(process,"NANOAODSIMoutput")
    if runOnMC:
        process.scoutingPFJetRecluster2MCTableTask = cms.Task(process.scoutingPFJetRecluster2MCTask, process.scoutingPFJetRecluster2MCTable)
        process.scoutingNanoSequence.associate(process.scoutingPFJetRecluster2MCTableTask)

    return process

