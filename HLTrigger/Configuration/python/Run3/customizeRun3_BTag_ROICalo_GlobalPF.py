import FWCore.ParameterSet.Config as cms

def customizeRun3_BTag_ROICalo_GlobalPF(process, addDeepJetPaths = True):

    # delete the old legacy sequences, to be sure
    if hasattr(process, 'HLTDoLocalPixelSequenceRegForBTag'):
    	del process.HLTDoLocalPixelSequenceRegForBTag
    if hasattr(process, 'HLTFastRecopixelvertexingSequence'):
    	del process.HLTFastRecopixelvertexingSequence
    if hasattr(process, 'HLTDoLocalStripSequenceRegForBTag'):
    	del process.HLTDoLocalStripSequenceRegForBTag
    if hasattr(process, 'HLTIterativeTrackingIter02ForBTag'):
    	del process.HLTIterativeTrackingIter02ForBTag
    if hasattr(process, 'HLTIterativeTrackingIteration0ForBTag'):
    	del process.HLTIterativeTrackingIteration0ForBTag
    if hasattr(process, 'HLTIterativeTrackingIteration1ForBTag'):
    	del process.HLTIterativeTrackingIteration1ForBTag
    if hasattr(process, 'HLTIterativeTrackingIteration2ForBTag'):
    	del process.HLTIterativeTrackingIteration2ForBTag
    if hasattr(process, 'HLTIterativeTrackingDoubletRecoveryForBTag'):
    	del process.HLTIterativeTrackingDoubletRecoveryForBTag
    # delete the remaining unneeded paths
    if hasattr(process, 'MC_AK4CaloJetsFromPV_v8'):
    	del process.MC_AK4CaloJetsFromPV_v8
    if hasattr(process, 'hltPreMCAK4CaloJetsFromPV'):
    	del process.hltPreMCAK4CaloJetsFromPV
    if hasattr(process, 'HLTNoPUSequence'):
    	del process.HLTNoPUSequence
    if hasattr(process, 'hltCaloJetFromPVCollection20Filter'):
    	del process.hltCaloJetFromPVCollection20Filter
    if hasattr(process, 'hltHtMhtFromPVForMC'):
    	del process.hltHtMhtFromPVForMC
    if hasattr(process, 'hltCaloHtMhtFromPVOpenFilter'):
    	del process.hltCaloHtMhtFromPVOpenFilter

    #speed up PFPS
    # process.hltParticleFlowClusterECALUnseededROIForBTag = process.hltParticleFlowClusterECALUnseeded.clone(
    #     skipPS = cms.bool(True)
    # )

    #our own tracking region
    process.hltBTaggingRegion = cms.EDProducer("CandidateSeededTrackingRegionsEDProducer",
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        deltaEta = cms.double(0.5),
        deltaPhi = cms.double(0.5),
        input = cms.InputTag("hltSelectorCentralJets20L1FastJeta"),
        maxNRegions = cms.int32(8),
        maxNVertices = cms.int32(2),
        measurementTrackerName = cms.InputTag(""),
        mode = cms.string('VerticesFixed'),
        nSigmaZBeamSpot = cms.double(3.0),
        nSigmaZVertex = cms.double(0.0),
        originRadius = cms.double(0.3),
        precise = cms.bool(True),
        ptMin = cms.double(0.8),
        searchOpt = cms.bool(True),
        vertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
        whereToUseMeasurementTracker = cms.string('Never'),
        zErrorBeamSpot = cms.double(0.5),
        zErrorVetex = cms.double(0.3)
        )
    )

    #select only PV tracks
    process.hltPixelTracksCleanForBTag = cms.EDProducer("TrackWithVertexSelector",
        copyExtras = cms.untracked.bool(False),
        copyTrajectories = cms.untracked.bool(False),
        d0Max = cms.double(999.0),
        dzMax = cms.double(999.0),
        etaMax = cms.double(5.0),
        etaMin = cms.double(0.0),
        nSigmaDtVertex = cms.double(0.0),
        nVertices = cms.uint32(2),
        normalizedChi2 = cms.double(999999.0),
        numberOfLostHits = cms.uint32(999),
        numberOfValidHits = cms.uint32(0),
        numberOfValidPixelHits = cms.uint32(3),
        ptErrorCut = cms.double(5.0),
        ptMax = cms.double(500.0),
        ptMin = cms.double(0.8),
        quality = cms.string('loose'),
        rhoVtx = cms.double(0.2),
        src = cms.InputTag("hltPixelTracks"),
        timeResosTag = cms.InputTag(""),
        timesTag = cms.InputTag(""),
        useVtx = cms.bool(True),
        vertexTag = cms.InputTag("hltTrimmedPixelVertices"),
        vtxFallback = cms.bool(True),
        zetaVtx = cms.double(0.3),
    )

    #select seeds based on our regions
    process.hltPixelTracksForBTag = cms.EDProducer('TrackSelectorByRegion',
          tracks = cms.InputTag('hltPixelTracksCleanForBTag'),
          regions = cms.InputTag('hltBTaggingRegion'),
          produceTrackCollection = cms.bool(True),
          produceMask = cms.bool(True),
          mightGet = cms.optional.untracked.vstring
    )


    # process.hltVerticesPFROIForBTag = process.hltVerticesPF.clone(
    #     TrackLabel = cms.InputTag("hltPFMuonMergingROIForBTag"),
    # )
    #
    # process.hltVerticesPFSelectorROIForBTag = process.hltVerticesPFSelector.clone(
    #     filterParams = cms.PSet(
    #         maxRho = cms.double(2.0),
    #         maxZ = cms.double(24.0),
    #         minNdof = cms.double(4.0),
    #         pvSrc = cms.InputTag("hltVerticesPFROIForBTag")
    #     ),
    #     src = cms.InputTag("hltVerticesPFROIForBTag")
    # )
    #
    # process.hltVerticesPFFilterROIForBTag = process.hltVerticesPFFilter.clone(
    #     src = cms.InputTag("hltVerticesPFSelectorROIForBTag")
    # )
    #
    # process.hltPFJetForBtagSelectorROIForBTag = process.hltPFJetForBtagSelector.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    # )
    #
    # process.hltPFJetForBtagROIForBTag = process.hltPFJetForBtag.clone(
    #     HLTObject = cms.InputTag("hltPFJetForBtagSelectorROIForBTag"),
    # )
    #
    # process.hltDeepBLifetimeTagInfosPFROIForBTag = process.hltDeepBLifetimeTagInfosPF.clone(
    #     candidates = cms.InputTag("hltParticleFlowROIForBTag"),
    #     jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
    #     primaryVertex = cms.InputTag("hltVerticesPFFilterROIForBTag"),
    # )
    #
    #
    # process.hltDeepInclusiveVertexFinderPFROIForBTag = process.hltDeepInclusiveVertexFinderPF.clone(
    #     primaryVertices = cms.InputTag("hltVerticesPFFilterROIForBTag"),
    #     tracks = cms.InputTag("hltParticleFlowROIForBTag"),
    # )
    #
    # process.hltDeepInclusiveSecondaryVerticesPFROIForBTag = process.hltDeepInclusiveSecondaryVerticesPF.clone(
    #     secondaryVertices = cms.InputTag("hltDeepInclusiveVertexFinderPFROIForBTag")
    # )
    #
    # process.hltDeepTrackVertexArbitratorPFROIForBTag = process.hltDeepTrackVertexArbitratorPF.clone(
    #     primaryVertices = cms.InputTag("hltVerticesPFFilterROIForBTag"),
    #     secondaryVertices = cms.InputTag("hltDeepInclusiveSecondaryVerticesPFROIForBTag"),
    #     tracks = cms.InputTag("hltParticleFlowROIForBTag")
    # )
    #
    # process.hltDeepInclusiveMergedVerticesPFROIForBTag = process.hltDeepInclusiveMergedVerticesPF.clone(
    #     secondaryVertices = cms.InputTag("hltDeepTrackVertexArbitratorPFROIForBTag")
    # )
    #
    # process.hltDeepSecondaryVertexTagInfosPFROIForBTag = process.hltDeepSecondaryVertexTagInfosPF.clone(
    #     extSVCollection = cms.InputTag("hltDeepInclusiveMergedVerticesPFROIForBTag"),
    #     trackIPTagInfos = cms.InputTag("hltDeepBLifetimeTagInfosPFROIForBTag"),
    # )
    #
    # process.hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag = process.hltDeepCombinedSecondaryVertexBJetTagsInfos.clone(
    #     svTagInfos = cms.InputTag("hltDeepSecondaryVertexTagInfosPFROIForBTag")
    # )
    #
    # process.hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag = process.hltDeepCombinedSecondaryVertexBJetTagsPF.clone(
    #     NNConfig = cms.FileInPath('RecoBTag/Combined/data/DeepCSV_PhaseI.json'),
    #     src = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag"),
    #     toAdd = cms.PSet(
    #         probbb = cms.string('probb')
    #     )
    # )











    process.hltIter0PFLowPixelSeedsFromPixelTracksROIForBTag = process.hltIter0PFLowPixelSeedsFromPixelTracks.clone(
        InputCollection = cms.InputTag("hltPixelTracksForBTag"),
        InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
    )

    process.hltIter0PFlowCkfTrackCandidatesROIForBTag = process.hltIter0PFlowCkfTrackCandidates.clone(
        src = cms.InputTag("hltIter0PFLowPixelSeedsFromPixelTracksROIForBTag"),
    )

    process.hltIter0PFlowCtfWithMaterialTracksROIForBTag = process.hltIter0PFlowCtfWithMaterialTracks.clone(
        src = cms.InputTag("hltIter0PFlowCkfTrackCandidatesROIForBTag"),
    )

    process.hltIter0PFlowTrackCutClassifierROIForBTag = process.hltIter0PFlowTrackCutClassifier.clone(
        src = cms.InputTag("hltIter0PFlowCtfWithMaterialTracksROIForBTag"),
        vertices = cms.InputTag("hltTrimmedPixelVertices")
    )

    process.hltMergedTracksROIForBTag = process.hltMergedTracks.clone(
        originalMVAVals = cms.InputTag("hltIter0PFlowTrackCutClassifierROIForBTag","MVAValues"),
        originalQualVals = cms.InputTag("hltIter0PFlowTrackCutClassifierROIForBTag","QualityMasks"),
        originalSource = cms.InputTag("hltIter0PFlowCtfWithMaterialTracksROIForBTag")
    )

    # process.hltPFMuonMergingROIForBTag = process.hltPFMuonMerging.clone(
    #     TrackProducers = cms.VInputTag("hltIterL3MuonTracks", "hltMergedTracksROIForBTag"),
    #     selectedTrackQuals = cms.VInputTag("hltIterL3MuonTracks", "hltMergedTracksROIForBTag"),
    # )

    # process.hltMuonLinksROIForBTag = process.hltMuonLinks.clone(
    #     InclusiveTrackerTrackCollection = cms.InputTag("hltPFMuonMergingROIForBTag"),
    # )

    # process.hltMuonsROIForBTag = process.hltMuons.clone(
    #     # TrackExtractorPSet = cms.PSet(
    #     #     BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
    #     #     BeamlineOption = cms.string('BeamSpotFromEvent'),
    #     #     Chi2Ndof_Max = cms.double(1e+64),
    #     #     Chi2Prob_Min = cms.double(-1.0),
    #     #     ComponentName = cms.string('TrackExtractor'),
    #     #     DR_Max = cms.double(1.0),
    #     #     DR_Veto = cms.double(0.01),
    #     #     DepositLabel = cms.untracked.string(''),
    #     #     Diff_r = cms.double(0.1),
    #     #     Diff_z = cms.double(0.2),
    #     #     NHits_Min = cms.uint32(0),
    #     #     Pt_Min = cms.double(-1.0),
    #     #     inputTrackCollection = cms.InputTag("hltPFMuonMergingROIForBTag")
    #     # ),
    #     inputCollectionLabels = cms.VInputTag("hltPFMuonMergingROIForBTag", "hltMuonLinksROIForBTag", "hltL2Muons"),
    # )
    # process.hltMuonsROIForBTag.TrackExtractorPSet.inputTrackCollection = cms.InputTag("hltPFMuonMergingROIForBTag")

    # process.hltLightPFTracksROIForBTag = process.hltLightPFTracks.clone(
    #     TkColList = cms.VInputTag("hltPFMuonMergingROIForBTag"),
    # )


    # process.hltParticleFlowBlockROIForBTag = process.hltParticleFlowBlock.clone(
    #     elementImporters = cms.VPSet(
    #         cms.PSet(
    #             DPtOverPtCuts_byTrackAlgo = cms.vdouble(
    #                 0.5, 0.5, 0.5, 0.5, 0.5,
    #                 0.5
    #             ),
    #             NHitCuts_byTrackAlgo = cms.vuint32(
    #                 3, 3, 3, 3, 3,
    #                 3
    #             ),
    #             cleanBadConvertedBrems = cms.bool(False),
    #             importerName = cms.string('GeneralTracksImporter'),
    #             muonMaxDPtOPt = cms.double(1.0),
    #             muonSrc = cms.InputTag("hltMuonsROIForBTag"),
    #             source = cms.InputTag("hltLightPFTracksROIForBTag"),
    #             trackQuality = cms.string('highPurity'),
    #             useIterativeTracking = cms.bool(False),
    #             vetoEndcap = cms.bool(False)
    #         ),
    #         cms.PSet(
    #             BCtoPFCMap = cms.InputTag(""),
    #             importerName = cms.string('ECALClusterImporter'),
    #             source = cms.InputTag("hltParticleFlowClusterECALUnseededROIForBTag")
    #         ),
    #         cms.PSet(
    #             importerName = cms.string('GenericClusterImporter'),
    #             source = cms.InputTag("hltParticleFlowClusterHCAL")
    #         ),
    #         cms.PSet(
    #             importerName = cms.string('GenericClusterImporter'),
    #             source = cms.InputTag("hltParticleFlowClusterHF")
    #         )
    #     ),
    # )
    #
    # process.hltParticleFlowROIForBTag = process.hltParticleFlow.clone(
    #     blocks = cms.InputTag("hltParticleFlowBlockROIForBTag"),
    #     muons = cms.InputTag("hltMuonsROIForBTag"),
    #     vertexCollection = cms.InputTag("hltPixelVertices"),
    # )
    #
    # process.hltAK4PFJetsROIForBTag = process.hltAK4PFJets.clone(
    #     src = cms.InputTag("hltParticleFlowROIForBTag"),
    #     srcPVs = cms.InputTag("hltPixelVertices"),
    # )
    #
    # process.hltAK4PFJetsLooseIDROIForBTag = process.hltAK4PFJetsLooseID.clone(
    #     jetsInput = cms.InputTag("hltAK4PFJetsROIForBTag"),
    # )
    #
    # process.hltAK4PFJetsTightIDROIForBTag = process.hltAK4PFJetsTightID.clone(
    #     jetsInput = cms.InputTag("hltAK4PFJetsROIForBTag"),
    # )
    #
    # process.hltFixedGridRhoFastjetAllROIForBTag = process.hltFixedGridRhoFastjetAll.clone(
    #     pfCandidatesTag = cms.InputTag("hltParticleFlowROIForBTag")
    # )
    #
    # process.hltAK4PFFastJetCorrectorROIForBTag = process.hltAK4PFFastJetCorrector.clone(
    #     srcRho = cms.InputTag("hltFixedGridRhoFastjetAllROIForBTag")
    # )
    #
    # process.hltAK4PFCorrectorROIForBTag = cms.EDProducer("ChainedJetCorrectorProducer",
    #     correctors = cms.VInputTag("hltAK4PFFastJetCorrectorROIForBTag", "hltAK4PFRelativeCorrector", "hltAK4PFAbsoluteCorrector", "hltAK4PFResidualCorrector")
    # )
    #
    # process.hltAK4PFJetsCorrectedROIForBTag = cms.EDProducer("CorrectedPFJetProducer",
    #     correctors = cms.VInputTag("hltAK4PFCorrectorROIForBTag"),
    #     src = cms.InputTag("hltAK4PFJetsROIForBTag")
    # )
    #
    # process.hltAK4PFJetsLooseIDCorrectedROIForBTag = cms.EDProducer("CorrectedPFJetProducer",
    #     correctors = cms.VInputTag("hltAK4PFCorrectorROIForBTag"),
    #     src = cms.InputTag("hltAK4PFJetsLooseIDROIForBTag")
    # )
    #
    # process.hltAK4PFJetsTightIDCorrectedROIForBTag = cms.EDProducer("CorrectedPFJetProducer",
    #     correctors = cms.VInputTag("hltAK4PFCorrectorROIForBTag"),
    #     src = cms.InputTag("hltAK4PFJetsTightIDROIForBTag")
    # )










    # process.HLTParticleFlowSequenceROIForBTag = cms.Sequence(
    #     process.HLTPreshowerSequence+
    #     process.hltParticleFlowRecHitECALUnseeded+
    #     process.hltParticleFlowRecHitHBHE+
    #     process.hltParticleFlowRecHitHF+
    #     process.hltParticleFlowRecHitPSUnseeded+
    #     process.hltParticleFlowClusterECALUncorrectedUnseeded+
    #     process.hltParticleFlowClusterPSUnseeded+
    #     # process.hltParticleFlowClusterECALUnseeded+
    #     process.hltParticleFlowClusterECALUnseededROIForBTag+
    #     process.hltParticleFlowClusterHBHE+
    #     process.hltParticleFlowClusterHCAL+
    #     process.hltParticleFlowClusterHF+
    #
    #     process.hltLightPFTracksROIForBTag+
    #     process.hltParticleFlowBlockROIForBTag+
    #     process.hltParticleFlowROIForBTag
    # )

    process.HLTIterativeTrackingIteration0ROIForBTag = cms.Sequence(
        process.HLTAK4CaloJetsReconstructionNoIDSequence +
        process.HLTAK4CaloJetsCorrectionNoIDSequence +
        process.hltSelectorJets20L1FastJet +
        process.hltSelectorCentralJets20L1FastJeta +

        process.hltBTaggingRegion +
        process.hltPixelTracksCleanForBTag+
        process.hltPixelTracksForBTag +

        process.hltIter0PFLowPixelSeedsFromPixelTracksROIForBTag+
        process.hltIter0PFlowCkfTrackCandidatesROIForBTag+
        process.hltIter0PFlowCtfWithMaterialTracksROIForBTag+
        process.hltIter0PFlowTrackCutClassifierROIForBTag+
        process.hltMergedTracksROIForBTag
    )
    #
    process.HLTIterativeTrackingIter02ROIForBTag = cms.Sequence(
        process.HLTIterativeTrackingIteration0ROIForBTag
    )
    #
    # process.HLTTrackReconstructionForPFROIForBTag = cms.Sequence(
    #     process.HLTDoLocalPixelSequence+
    #     process.HLTRecopixelvertexingSequence+
    #     process.HLTDoLocalStripSequence+
    #
    #     process.HLTIterativeTrackingIter02ROIForBTag+
    #
    #     process.hltPFMuonMergingROIForBTag+
    #     process.hltMuonLinksROIForBTag+
    #     process.hltMuonsROIForBTag
    #
    # )


    ########################################
    # new CALO and ROI TRK

    process.hltVerticesL3ROIForBTag = process.hltVerticesL3.clone(
        TrackLabel = cms.InputTag("hltMergedTracksROIForBTag"),
    )

    process.hltVerticesL3SelectorROIForBTag = process.hltVerticesPFSelector.clone(
        filterParams = cms.PSet(
            maxRho = cms.double(2.0),
            maxZ = cms.double(24.0),
            minNdof = cms.double(4.0),
            pvSrc = cms.InputTag("hltVerticesL3ROIForBTag")
        ),
        src = cms.InputTag("hltVerticesL3ROIForBTag")
    )

    process.hltVerticesL3FilterROIForBTag = process.hltVerticesPFFilter.clone(
        src = cms.InputTag("hltVerticesL3SelectorROIForBTag")
    )

    process.hltFastPixelBLifetimeL3AssociatorROIForBTag = process.hltFastPixelBLifetimeL3Associator.clone(
        tracks = cms.InputTag("hltMergedTracksROIForBTag"),
    )
    process.hltImpactParameterTagInfosROIForBTag = process.hltImpactParameterTagInfos.clone(
        jetTracks = cms.InputTag("hltFastPixelBLifetimeL3AssociatorROIForBTag"),
        primaryVertex = cms.InputTag("hltVerticesL3FilterROIForBTag"),
    )

    process.hltInclusiveVertexFinderROIForBTag = process.hltInclusiveVertexFinder.clone(
        primaryVertices = cms.InputTag("hltVerticesL3FilterROIForBTag"),
        tracks = cms.InputTag("hltMergedTracksROIForBTag"),
    )

    process.hltInclusiveSecondaryVerticesROIForBTag = process.hltInclusiveSecondaryVertices.clone(
        secondaryVertices = cms.InputTag("hltInclusiveVertexFinderROIForBTag")
    )

    process.hltTrackVertexArbitratorROIForBTag = process.hltTrackVertexArbitrator.clone(
        primaryVertices = cms.InputTag("hltVerticesL3FilterROIForBTag"),
        secondaryVertices = cms.InputTag("hltInclusiveSecondaryVerticesROIForBTag"),
        tracks = cms.InputTag("hltMergedTracksROIForBTag")
    )

    process.hltInclusiveMergedVerticesROIForBTag = process.hltInclusiveMergedVertices.clone(
        secondaryVertices = cms.InputTag("hltTrackVertexArbitratorROIForBTag")
    )

    process.hltInclusiveSecondaryVertexFinderTagInfosROIForBTag = process.hltInclusiveSecondaryVertexFinderTagInfos.clone(
        extSVCollection = cms.InputTag("hltInclusiveMergedVerticesROIForBTag"),
        trackIPTagInfos = cms.InputTag("hltImpactParameterTagInfosROIForBTag"),
    )

    process.hltDeepCombinedSecondaryVertexBJetTagsInfosCaloROIForBTag = process.hltDeepCombinedSecondaryVertexBJetTagsInfosCalo.clone(
        svTagInfos = cms.InputTag("hltInclusiveSecondaryVertexFinderTagInfosROIForBTag")
    )

    process.hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag = process.hltDeepCombinedSecondaryVertexBJetTagsCalo.clone(
        src = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsInfosCaloROIForBTag"),
    )

    process.HLTBtagDeepCSVSequenceL3ROIForBTag = cms.Sequence(
        process.hltSelectorJets30L1FastJet+
        process.hltSelectorCentralJets30L1FastJeta+
        process.hltSelector8CentralJetsL1FastJet+
        process.HLTTrackReconstructionForBTag+
        process.hltVerticesL3ROIForBTag+
        process.hltVerticesL3SelectorROIForBTag+
        process.hltVerticesL3FilterROIForBTag+
        process.hltFastPixelBLifetimeL3AssociatorROIForBTag+
        process.hltImpactParameterTagInfosROIForBTag+
        process.hltInclusiveVertexFinderROIForBTag+
        process.hltInclusiveSecondaryVerticesROIForBTag+
        process.hltTrackVertexArbitratorROIForBTag+
        process.hltInclusiveMergedVerticesROIForBTag+
        process.hltInclusiveSecondaryVertexFinderTagInfosROIForBTag+
        process.hltDeepCombinedSecondaryVertexBJetTagsInfosCaloROIForBTag+
        process.hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag
    )




    process.HLTFastPrimaryVertexSequenceROIForBTag = cms.Sequence(
        process.hltSelectorJets20L1FastJet+
        process.hltSelectorCentralJets20L1FastJeta+
        process.hltSelector4CentralJetsL1FastJet+
        process.HLTDoLocalPixelSequence+
        process.HLTRecopixelvertexingSequence
    )

    process.HLTTrackReconstructionForBTag = cms.Sequence(
        process.HLTDoLocalPixelSequence+
        process.HLTRecopixelvertexingSequence+
        process.HLTDoLocalStripSequence+
        process.HLTIterativeTrackingIter02ROIForBTag
    )

    ########################################



    # process.HLTAK4PFJetsReconstructionSequenceROIForBTag = cms.Sequence(
    #     process.HLTL2muonrecoSequence+
    #     process.HLTL3muonrecoSequence+
    #
    #     process.HLTTrackReconstructionForPFROIForBTag+
    #     process.HLTParticleFlowSequenceROIForBTag+
    #
    #     process.hltAK4PFJetsROIForBTag+
    #     process.hltAK4PFJetsLooseIDROIForBTag+
    #     process.hltAK4PFJetsTightIDROIForBTag
    # )






    # process.HLTAK4PFCorrectorProducersSequenceROIForBTag = cms.Sequence(
    #     process.hltAK4PFFastJetCorrectorROIForBTag+
    #     process.hltAK4PFRelativeCorrector+
    #     process.hltAK4PFAbsoluteCorrector+
    #     process.hltAK4PFResidualCorrector+
    #     process.hltAK4PFCorrectorROIForBTag
    # )
    #
    # process.HLTAK4PFJetsCorrectionSequenceROIForBTag = cms.Sequence(
    #     process.hltFixedGridRhoFastjetAllROIForBTag+
    #     process.HLTAK4PFCorrectorProducersSequenceROIForBTag+
    #     process.hltAK4PFJetsCorrectedROIForBTag+
    #     process.hltAK4PFJetsLooseIDCorrectedROIForBTag+
    #     process.hltAK4PFJetsTightIDCorrectedROIForBTag
    # )
    #
    # process.HLTAK4PFJetsSequenceROIForBTag = cms.Sequence(
    #     process.HLTPreAK4PFJetsRecoSequence+
    #     process.HLTAK4PFJetsReconstructionSequenceROIForBTag+
    #     process.HLTAK4PFJetsCorrectionSequenceROIForBTag
    # )







    # process.HLTBtagDeepCSVSequencePFROIForBTag = cms.Sequence(
    #
    #     process.hltVerticesPFROIForBTag+
    #     process.hltVerticesPFSelectorROIForBTag+
    #     process.hltVerticesPFFilterROIForBTag+
    #
    #     process.hltPFJetForBtagSelectorROIForBTag+
    #     process.hltPFJetForBtagROIForBTag+
    #
    #     process.hltDeepBLifetimeTagInfosPFROIForBTag+
    #     process.hltDeepInclusiveVertexFinderPFROIForBTag+
    #     process.hltDeepInclusiveSecondaryVerticesPFROIForBTag+
    #     process.hltDeepTrackVertexArbitratorPFROIForBTag+
    #     process.hltDeepInclusiveMergedVerticesPFROIForBTag+
    #     process.hltDeepSecondaryVertexTagInfosPFROIForBTag+
    #     process.hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag+
    #     process.hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag
    # )


    # process.MC_CaloBTagDeepCSVROIForBTag_v8 = cms.Path(
    process.MC_CaloBTagDeepCSV_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltPreMCCaloBTagDeepCSV+
        process.HLTAK4CaloJetsSequence+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltCaloJetCollection20Filter+
        process.HLTEndSequence
    )


    ####                    DeepJet?
    if addDeepJetPaths:
        from CommonTools.RecoAlgos.primaryVertexAssociation_cfi import primaryVertexAssociation
        from RecoBTag.FeatureTools.pfDeepFlavourTagInfos_cfi import pfDeepFlavourTagInfos
        from RecoBTag.ONNXRuntime.pfDeepFlavourJetTags_cfi import pfDeepFlavourJetTags

        process.hltDeepJetDiscriminatorsJetTags = cms.EDProducer(
            'BTagProbabilityToDiscriminator',
            discriminators = cms.VPSet(
                cms.PSet(
                    name = cms.string('BvsAll'),
                    numerator = cms.VInputTag(
                        cms.InputTag('hltPFDeepFlavourJetTags', 'probb'),
                        cms.InputTag('hltPFDeepFlavourJetTags', 'probbb'),
                        cms.InputTag('hltPFDeepFlavourJetTags', 'problepb'),
                        ),
                    denominator=cms.VInputTag(
                        cms.InputTag('hltPFDeepFlavourJetTags', 'probb'),
                        cms.InputTag('hltPFDeepFlavourJetTags', 'probbb'),
                        cms.InputTag('hltPFDeepFlavourJetTags', 'problepb'),
                        cms.InputTag('hltPFDeepFlavourJetTags', 'probc'),
                        cms.InputTag('hltPFDeepFlavourJetTags', 'probuds'),
                        cms.InputTag('hltPFDeepFlavourJetTags', 'probg'),
                        ),
                ),
            )
        )

        process.hltPrimaryVertexAssociation = primaryVertexAssociation.clone(
            jets = cms.InputTag("hltPFJetForBtag"),
            particles = cms.InputTag("hltParticleFlow"),
            vertices = cms.InputTag("hltVerticesPFFilter"),
        )

        process.hltPFDeepFlavourTagInfos = pfDeepFlavourTagInfos.clone(
            candidates = cms.InputTag("hltParticleFlow"),
            jets = cms.InputTag("hltPFJetForBtag"),
            fallback_puppi_weight = cms.bool(True),
            puppi_value_map = cms.InputTag(""),
            secondary_vertices = cms.InputTag("hltDeepInclusiveSecondaryVerticesPF"),
            shallow_tag_infos = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsInfos"),
            vertex_associator = cms.InputTag("hltPrimaryVertexAssociation","original"),
            vertices = cms.InputTag("hltVerticesPFFilter")
        )
        process.hltPFDeepFlavourJetTags = pfDeepFlavourJetTags.clone(
            src = cms.InputTag("hltPFDeepFlavourTagInfos")
        )

        process.HLTBtagDeepJetSequencePF = cms.Sequence(
            process.hltVerticesPF+
            process.hltVerticesPFSelector+
            process.hltVerticesPFFilter+
            process.hltPFJetForBtagSelector+
            process.hltPFJetForBtag+
            process.hltDeepBLifetimeTagInfosPF+
            process.hltDeepInclusiveVertexFinderPF+
            process.hltDeepInclusiveSecondaryVerticesPF+
            process.hltDeepTrackVertexArbitratorPF+
            process.hltDeepInclusiveMergedVerticesPF+
            process.hltDeepSecondaryVertexTagInfosPF+
            process.hltDeepCombinedSecondaryVertexBJetTagsInfos+
            process.hltPrimaryVertexAssociation+
            process.hltPFDeepFlavourTagInfos+
            process.hltPFDeepFlavourJetTags+
            process.hltDeepJetDiscriminatorsJetTags
        )

        process.hltPreMCPFBTagDeepJet = process.hltPreMCPFBTagDeepCSV.clone()

        process.hltBTagPFDeepJet4p06Single = process.hltBTagPFDeepCSV4p06Single.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtag"),
            MaxTag = cms.double(999999.0),
            MinJets = cms.int32(1),
            MinTag = cms.double(0.25),
            TriggerType = cms.int32(86),
            saveTags = cms.bool(True)
        )

        ############################################################################
        ####                    MC_PFBTagDeepJet_v1                   ###
        ############################################################################
        process.hltPreMCPFBTagDeepJet = process.hltPreMCPFBTagDeepCSV.clone()

        process.MC_PFBTagDeepJet_v1 = cms.Path(
            process.HLTBeginSequence+
            process.hltPreMCPFBTagDeepJet+
            process.HLTAK4PFJetsSequence+
            process.HLTBtagDeepJetSequencePF+
            process.hltBTagPFDeepJet4p06Single+
            process.HLTEndSequence
        )
    ####         endif           DeepJet?







    ############################################################################
    ####                    MC_PFBTagDeepCSV_v10                   ###
    ############################################################################

    process.hltBTagPFDeepCSV4p06Single = process.hltBTagPFDeepCSV4p06Single.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
        Jets = cms.InputTag("hltPFJetForBtag"),
    )

    process.hltPreMCPFBTagDeepCSV = process.hltPreMCPFBTagDeepCSV.clone()

    process.MC_PFBTagDeepCSV_v10 = cms.Path(
        process.HLTBeginSequence+
        process.hltPreMCPFBTagDeepCSV+

        process.HLTAK4PFJetsSequence+
        process.HLTBtagDeepCSVSequencePF+

        process.hltBTagPFDeepCSV4p06Single+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v3
    ############################################################################

    # process.hltPFCentralJetLooseIDQuad30 = process.hltPFCentralJetLooseIDQuad30.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hlt1PFCentralJetLooseID75 = process.hlt1PFCentralJetLooseID75.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hlt2PFCentralJetLooseID60 = process.hlt2PFCentralJetLooseID60.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hlt3PFCentralJetLooseID45 = process.hlt3PFCentralJetLooseID45.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hlt4PFCentralJetLooseID40 = process.hlt4PFCentralJetLooseID40.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltPFCentralJetLooseIDQuad30forHt = process.hltPFCentralJetLooseIDQuad30forHt.clone(
    #     HLTObject = cms.InputTag("hltPFCentralJetLooseIDQuad30"),
    # )
    #
    # process.hltHtMhtPFCentralJetsLooseIDQuadC30 = process.hltHtMhtPFCentralJetsLooseIDQuadC30.clone(
    #     jetsLabel = cms.InputTag("hltPFCentralJetLooseIDQuad30forHt"),
    #     pfCandidatesLabel = cms.InputTag("hltParticleFlow"),
    # )
    #
    # process.hltPFCentralJetsLooseIDQuad30HT330 = process.hltPFCentralJetsLooseIDQuad30HT330.clone(
    #     htLabels = cms.VInputTag("hltHtMhtPFCentralJetsLooseIDQuadC30"),
    #     mhtLabels = cms.VInputTag("hltHtMhtPFCentralJetsLooseIDQuadC30"),
    # )
    #
    # process.hltBTagPFDeepCSV4p5Triple = process.hltBTagPFDeepCSV4p5Triple.clone(
    #     JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    #     Jets = cms.InputTag("hltPFJetForBtag"),
    #     MinTag = cms.double(0.24),
    # )
    #
    process.hltBTagCaloDeepCSVp17DoubleROIForBTag = process.hltBTagCaloDeepCSVp17Double.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
        MinTag = cms.double(0.17),
    )

    process.HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v3 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sQuadJetC50to60IorHTT280to500IorHTT250to340QuadJet+
        process.hltPrePFHT330PT30QuadPFJet75604540TriplePFBTagDeepCSV4p5+

        process.HLTAK4CaloJetsSequence+
        process.hltQuadCentralJet30+
        process.hltCaloJetsQuad30ForHt+
        process.hltHtMhtCaloJetsQuadC30+
        process.hltCaloQuadJet30HT320+

        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSVp17DoubleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFCentralJetLooseIDQuad30+
        process.hlt1PFCentralJetLooseID75+
        process.hlt2PFCentralJetLooseID60+
        process.hlt3PFCentralJetLooseID45+
        process.hlt4PFCentralJetLooseID40+
        process.hltPFCentralJetLooseIDQuad30forHt+
        process.hltHtMhtPFCentralJetsLooseIDQuadC30+
        process.hltPFCentralJetsLooseIDQuad30HT330+

        process.HLTBtagDeepCSVSequencePF+
        process.hltBTagPFDeepCSV4p5Triple+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet4p5Triple = process.hltBTagPFDeepCSV4p5Triple.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            MinTag = cms.double(0.24),
        )
        process.hltPrePFHT330PT30QuadPFJet75604540TriplePFBTagDeepJet4p5 = process.hltPrePFHT330PT30QuadPFJet75604540TriplePFBTagDeepCSV4p5.clone()
        process.HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepJet_4p5_v3 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sQuadJetC50to60IorHTT280to500IorHTT250to340QuadJet+
            process.hltPrePFHT330PT30QuadPFJet75604540TriplePFBTagDeepJet4p5+

            process.HLTAK4CaloJetsSequence+
            process.hltQuadCentralJet30+
            process.hltCaloJetsQuad30ForHt+
            process.hltHtMhtCaloJetsQuadC30+
            process.hltCaloQuadJet30HT320+

            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSVp17DoubleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFCentralJetLooseIDQuad30+
            process.hlt1PFCentralJetLooseID75+
            process.hlt2PFCentralJetLooseID60+
            process.hlt3PFCentralJetLooseID45+
            process.hlt4PFCentralJetLooseID40+
            process.hltPFCentralJetLooseIDQuad30forHt+
            process.hltHtMhtPFCentralJetsLooseIDQuadC30+
            process.hltPFCentralJetsLooseIDQuad30HT330+

            process.HLTBtagDeepJetSequencePF+
            process.hltBTagPFDeepJet4p5Triple+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5_v8
    ############################################################################

    # process.hltPFJetFilterTwo100er3p0 = process.hltPFJetFilterTwo100er3p0.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    # process.hltPFJetFilterThree60er3p0 = process.hltPFJetFilterThree60er3p0.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    # process.hltPFJetFilterFive30er3p0 = process.hltPFJetFilterFive30er3p0.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltPFJetsFive30ForHt = process.hltPFJetsFive30ForHt.clone(
    #     HLTObject = cms.InputTag("hltPFJetFilterFive30er3p0"),
    # )
    # process.hltHtMhtPFJetsFive30er3p0 = process.hltHtMhtPFJetsFive30er3p0.clone(
    #     jetsLabel = cms.InputTag("hltPFJetsFive30ForHt"),
    #     pfCandidatesLabel = cms.InputTag("hltParticleFlow"),
    # )
    # process.hltPFFiveJet30HT400 = process.hltPFFiveJet30HT400.clone(
    #     htLabels = cms.VInputTag("hltHtMhtPFJetsFive30er3p0"),
    #     mhtLabels = cms.VInputTag("hltHtMhtPFJetsFive30er3p0"),
    # )
    #
    # process.hltBTagPFDeepCSV4p5Double = process.hltBTagPFDeepCSV4p5Double.clone(
    #     JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    #     Jets = cms.InputTag("hltPFJetForBtag"),
    # )

    process.hltBTagCaloDeepCSV10p01SingleROIForBTag = process.hltBTagCaloDeepCSV10p01Single.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
        MinTag = cms.double(0.14),
    )

    process.HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJetTripleJet+
        process.hltPrePFHT400FivePFJet100100603030DoublePFBTagDeepCSV4p5+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterFiveC25+
        process.hltCaloJetsFive25ForHt+
        process.hltHtMhtCaloJetsFiveC25+
        process.hltCaloFiveJet25HT300+

        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV10p01SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFJetFilterTwo100er3p0+
        process.hltPFJetFilterThree60er3p0+
        process.hltPFJetFilterFive30er3p0+
        process.hltPFJetsFive30ForHt+
        process.hltHtMhtPFJetsFive30er3p0+
        process.hltPFFiveJet30HT400+
        process.HLTBtagDeepCSVSequencePF+
        process.hltBTagPFDeepCSV4p5Double+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet4p5Double = process.hltBTagPFDeepCSV4p5Double.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtag"),
        )
        process.hltPrePFHT400FivePFJet100100603030DoublePFBTagDeepJet4p5 = process.hltPrePFHT400FivePFJet100100603030DoublePFBTagDeepCSV4p5.clone()
        process.HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepJet_4p5_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sHTT280to500erIorHTT250to340erQuadJetTripleJet+
            process.hltPrePFHT400FivePFJet100100603030DoublePFBTagDeepJet4p5+
            process.HLTAK4CaloJetsSequence+
            process.hltCaloJetFilterFiveC25+
            process.hltCaloJetsFive25ForHt+
            process.hltHtMhtCaloJetsFiveC25+
            process.hltCaloFiveJet25HT300+

            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV10p01SingleROIForBTag+
            process.HLTAK4PFJetsSequence+

            process.hltPFJetFilterTwo100er3p0+
            process.hltPFJetFilterThree60er3p0+
            process.hltPFJetFilterFive30er3p0+
            process.hltPFJetsFive30ForHt+
            process.hltHtMhtPFJetsFive30er3p0+
            process.hltPFFiveJet30HT400+
            process.HLTBtagDeepJetSequencePF+
            process.hltBTagPFDeepJet4p5Double+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepCSV_4p5_v
    ############################################################################

    # process.hltPFJetFilterTwo120er3p0 = process.hltPFJetFilterTwo120er3p0.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )

    process.HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepCSV_4p5_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJetTripleJet+
        process.hltPrePFHT400FivePFJet120120603030DoublePFBTagDeepCSV4p5+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterFiveC25+
        process.hltCaloJetsFive25ForHt+
        process.hltHtMhtCaloJetsFiveC25+
        process.hltCaloFiveJet25HT300+

        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV10p01SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFJetFilterTwo120er3p0+
        process.hltPFJetFilterThree60er3p0+
        process.hltPFJetFilterFive30er3p0+
        process.hltPFJetsFive30ForHt+
        process.hltHtMhtPFJetsFive30er3p0+
        process.hltPFFiveJet30HT400+
        process.HLTBtagDeepCSVSequencePF+
        process.hltBTagPFDeepCSV4p5Double+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltPrePFHT400FivePFJet120120603030DoublePFBTagDeepJet4p5 = process.hltPrePFHT400FivePFJet120120603030DoublePFBTagDeepCSV4p5.clone()
        process.HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepJet_4p5_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sHTT280to500erIorHTT250to340erQuadJetTripleJet+
            process.hltPrePFHT400FivePFJet120120603030DoublePFBTagDeepJet4p5+
            process.HLTAK4CaloJetsSequence+
            process.hltCaloJetFilterFiveC25+
            process.hltCaloJetsFive25ForHt+
            process.hltHtMhtCaloJetsFiveC25+
            process.hltCaloFiveJet25HT300+

            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV10p01SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFJetFilterTwo120er3p0+
            process.hltPFJetFilterThree60er3p0+
            process.hltPFJetFilterFive30er3p0+
            process.hltPFJetsFive30ForHt+
            process.hltHtMhtPFJetsFive30er3p0+
            process.hltPFFiveJet30HT400+
            process.HLTBtagDeepJetSequencePF+
            process.hltBTagPFDeepJet4p5Double+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94_v
    ############################################################################

    # process.hltPFJetFilterSix30er2p5 = process.hltPFJetFilterSix30er2p5.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltPFJetFilterSix32er2p5 = process.hltPFJetFilterSix32er2p5.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltPFJetsSix30ForHt = cms.EDProducer("HLTPFJetCollectionProducer",
    #     HLTObject = cms.InputTag("hltPFJetFilterSix30er2p5"),
    #     TriggerTypes = cms.vint32(86)
    # )
    #
    # process.hltHtMhtPFJetsSix30er2p5 = process.hltHtMhtPFJetsSix30er2p5.clone(
    #     jetsLabel = cms.InputTag("hltPFJetsSix30ForHt"),
    #     pfCandidatesLabel = cms.InputTag("hltParticleFlow"),
    # )
    #
    # process.hltPFSixJet30HT400 = process.hltPFSixJet30HT400.clone(
    #     htLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5"),
    #     mhtLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5"),
    # )
    #
    # process.hltBTagPFDeepCSV2p94Double = process.hltBTagPFDeepCSV2p94Double.clone(
    #     JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    #     Jets = cms.InputTag("hltPFJetForBtag"),
    # )

    process.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJet+
        process.hltPrePFHT400SixPFJet32DoublePFBTagDeepCSV2p94+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterSixC25+
        process.hltCaloJetsSix25ForHt+
        process.hltHtMhtCaloJetsSixC25+
        process.hltCaloSixJet25HT300+

        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV10p01SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFJetFilterSix30er2p5+
        process.hltPFJetFilterSix32er2p5+
        process.hltPFJetsSix30ForHt+
        process.hltHtMhtPFJetsSix30er2p5+
        process.hltPFSixJet30HT400+
        process.HLTBtagDeepCSVSequencePF+
        process.hltBTagPFDeepCSV2p94Double+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet2p94Double = process.hltBTagPFDeepCSV2p94Double.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtag"),
        )
        process.hltPrePFHT400SixPFJet32DoublePFBTagDeepJet2p94 = process.hltPrePFHT400SixPFJet32DoublePFBTagDeepCSV2p94.clone()
        process.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sHTT280to500erIorHTT250to340erQuadJet+
            process.hltPrePFHT400SixPFJet32DoublePFBTagDeepJet2p94+
            process.HLTAK4CaloJetsSequence+
            process.hltCaloJetFilterSixC25+
            process.hltCaloJetsSix25ForHt+
            process.hltHtMhtCaloJetsSixC25+
            process.hltCaloSixJet25HT300+

            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV10p01SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFJetFilterSix30er2p5+
            process.hltPFJetFilterSix32er2p5+
            process.hltPFJetsSix30ForHt+
            process.hltHtMhtPFJetsSix30er2p5+
            process.hltPFSixJet30HT400+
            process.HLTBtagDeepJetSequencePF+
            process.hltBTagPFDeepJet2p94Double+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_v
    ############################################################################

    # process.hltPFJetFilterSix36er2p5 = process.hltPFJetFilterSix36er2p5.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltPFSixJet30HT450 =process.hltPFSixJet30HT450.clone(
    #     htLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5"),
    #     mhtLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5"),
    # )
    #
    # process.hltBTagPFDeepCSV1p59Single = process.hltBTagPFDeepCSV1p59Single.clone(
    #     JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    #     Jets = cms.InputTag("hltPFJetForBtag"),
    # )

    process.HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_v7 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJet+
        process.hltPrePFHT450SixPFJet36PFBTagDeepCSV1p59+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterSixC30+
        process.hltCaloJetsSix30ForHt+
        process.hltHtMhtCaloJetsSixC30+
        process.hltCaloSixJet30HT350+

        process.HLTAK4PFJetsSequence+
        process.hltPFJetFilterSix30er2p5+
        process.hltPFJetFilterSix36er2p5+
        process.hltPFJetsSix30ForHt+
        process.hltHtMhtPFJetsSix30er2p5+
        process.hltPFSixJet30HT450+
        process.HLTBtagDeepCSVSequencePF+
        process.hltBTagPFDeepCSV1p59Single+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet1p59Single = process.hltBTagPFDeepCSV1p59Single.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtag"),
        )
        process.hltPrePFHT450SixPFJet36PFBTagDeepJet1p59 = process.hltPrePFHT450SixPFJet36PFBTagDeepCSV1p59.clone()
        process.HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59_v7 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sHTT280to500erIorHTT250to340erQuadJet+
            process.hltPrePFHT450SixPFJet36PFBTagDeepJet1p59+
            process.HLTAK4CaloJetsSequence+
            process.hltCaloJetFilterSixC30+
            process.hltCaloJetsSix30ForHt+
            process.hltHtMhtCaloJetsSixC30+
            process.hltCaloSixJet30HT350+

            process.HLTAK4PFJetsSequence+
            process.hltPFJetFilterSix30er2p5+
            process.hltPFJetFilterSix36er2p5+
            process.hltPFJetsSix30ForHt+
            process.hltHtMhtPFJetsSix30er2p5+
            process.hltPFSixJet30HT450+
            process.HLTBtagDeepJetSequencePF+
            process.hltBTagPFDeepJet1p59Single+

            process.HLTEndSequence
        )
    ############################################################################
    #### HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v
    ############################################################################

    # process.hltPFQuadJetLooseID15 = process.hltPFQuadJetLooseID15.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltPFTripleJetLooseID75 = process.hltPFTripleJetLooseID75.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltPFDoubleJetLooseID88 = process.hltPFDoubleJetLooseID88.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltPFSingleJetLooseID103 = process.hltPFSingleJetLooseID103.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltSelector6PFJets = process.hltSelector6PFJets.clone(
    #     src = cms.InputTag("hltAK4PFJetsLooseIDCorrected")
    # )
    #
    # process.hltBTagPFDeepCSV7p68Double6Jets = process.hltBTagPFDeepCSV7p68Double6Jets.clone(
    #     JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    #     Jets = cms.InputTag("hltSelector6PFJets"),
    # )
    #
    # process.hltBTagPFDeepCSV1p28Single6Jets = process.hltBTagPFDeepCSV1p28Single6Jets.clone(
    #     JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    #     Jets = cms.InputTag("hltSelector6PFJets"),
    # )
    #
    # process.hltVBFPFJetCSVSortedMqq200Detaqq1p5 = process.hltVBFPFJetCSVSortedMqq200Detaqq1p5.clone(
    #     inputJetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    #     inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )

    process.hltBTagCaloDeepCSV1p56SingleROIForBTag = process.hltBTagCaloDeepCSV1p56Single.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
        MinTag = cms.double(0.4),
    )

    process.HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJetVBFIorHTTIorSingleJet+
        process.hltPreQuadPFJet103887515DoublePFBTagDeepCSV1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        process.HLTFastPrimaryVertexSequenceROIForBTag+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID75+
        process.hltPFDoubleJetLooseID88+
        process.hltPFSingleJetLooseID103+
        process.HLTBtagDeepCSVSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepCSV7p68Double6Jets+
        process.hltBTagPFDeepCSV1p28Single6Jets+
        process.hltVBFPFJetCSVSortedMqq200Detaqq1p5+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet7p68Double6Jets = process.hltBTagPFDeepCSV7p68Double6Jets.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            Jets = cms.InputTag("hltSelector6PFJets"),
        )

        process.hltBTagPFDeepJet1p28Single6Jets = process.hltBTagPFDeepCSV1p28Single6Jets.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            Jets = cms.InputTag("hltSelector6PFJets"),
        )

        process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5 = process.hltVBFPFJetCSVSortedMqq200Detaqq1p5.clone(
            inputJetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
        )
        process.hltPreQuadPFJet103887515DoublePFBTagDeepJet1p37p7VBF1 = process.hltPreQuadPFJet103887515DoublePFBTagDeepCSV1p37p7VBF1.clone()
        process.HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sTripleJetVBFIorHTTIorSingleJet+
            process.hltPreQuadPFJet103887515DoublePFBTagDeepJet1p37p7VBF1+
            process.HLTAK4CaloJetsSequence+
            process.hltQuadJet15+
            process.hltTripleJet50+
            process.hltDoubleJet65+
            process.hltSingleJet80+
            process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

            process.HLTFastPrimaryVertexSequenceROIForBTag+
            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFQuadJetLooseID15+
            process.hltPFTripleJetLooseID75+
            process.hltPFDoubleJetLooseID88+
            process.hltPFSingleJetLooseID103+
            process.HLTBtagDeepJetSequencePF+
            process.hltSelector6PFJets+
            process.hltBTagPFDeepJet7p68Double6Jets+
            process.hltBTagPFDeepJet1p28Single6Jets+
            process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5+

            process.HLTEndSequence
        )


    ############################################################################
    #### HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2_v
    ############################################################################

    # process.hltVBFPFJetCSVSortedMqq460Detaqq3p5 = process.hltVBFPFJetCSVSortedMqq460Detaqq3p5.clone(
    #     inputJetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    #     inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )

    process.HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJetVBFIorHTTIorSingleJet+
        process.hltPreQuadPFJet103887515PFBTagDeepCSV1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        process.HLTFastPrimaryVertexSequenceROIForBTag+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID75+
        process.hltPFDoubleJetLooseID88+
        process.hltPFSingleJetLooseID103+
        process.HLTBtagDeepCSVSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepCSV1p28Single6Jets+
        process.hltVBFPFJetCSVSortedMqq460Detaqq3p5+
        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5 = process.hltVBFPFJetCSVSortedMqq460Detaqq3p5.clone(
            inputJetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
        )
        process.hltPreQuadPFJet103887515PFBTagDeepJet1p3VBF2 = process.hltPreQuadPFJet103887515PFBTagDeepCSV1p3VBF2.clone()
        process.HLT_QuadPFJet103_88_75_15_PFBTagDeepJet_1p3_VBF2_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sTripleJetVBFIorHTTIorSingleJet+
            process.hltPreQuadPFJet103887515PFBTagDeepJet1p3VBF2+
            process.HLTAK4CaloJetsSequence+
            process.hltQuadJet15+
            process.hltTripleJet50+
            process.hltDoubleJet65+
            process.hltSingleJet80+
            process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

            process.HLTFastPrimaryVertexSequenceROIForBTag+
            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFQuadJetLooseID15+
            process.hltPFTripleJetLooseID75+
            process.hltPFDoubleJetLooseID88+
            process.hltPFSingleJetLooseID103+
            process.HLTBtagDeepJetSequencePF+
            process.hltSelector6PFJets+
            process.hltBTagPFDeepJet1p28Single6Jets+
            process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5+
            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v
    ############################################################################

    # process.hltPFTripleJetLooseID76 = process.hltPFTripleJetLooseID76.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltPFSingleJetLooseID105 = process.hltPFSingleJetLooseID105.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )

    process.HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1008572VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet105887615DoublePFBTagDeepCSV1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        process.HLTFastPrimaryVertexSequenceROIForBTag+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID76+
        process.hltPFDoubleJetLooseID88+
        process.hltPFSingleJetLooseID105+
        process.HLTBtagDeepCSVSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepCSV7p68Double6Jets+
        process.hltBTagPFDeepCSV1p28Single6Jets+
        process.hltVBFPFJetCSVSortedMqq200Detaqq1p5+
        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltPreQuadPFJet105887615DoublePFBTagDeepJet1p37p7VBF1 = process.hltPreQuadPFJet105887615DoublePFBTagDeepCSV1p37p7VBF1.clone()
        process.HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sTripleJet1008572VBFIorHTTIorDoubleJetCIorSingleJet+
            process.hltPreQuadPFJet105887615DoublePFBTagDeepJet1p37p7VBF1+
            process.HLTAK4CaloJetsSequence+
            process.hltQuadJet15+
            process.hltTripleJet50+
            process.hltDoubleJet65+
            process.hltSingleJet80+
            process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

            process.HLTFastPrimaryVertexSequenceROIForBTag+
            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFQuadJetLooseID15+
            process.hltPFTripleJetLooseID76+
            process.hltPFDoubleJetLooseID88+
            process.hltPFSingleJetLooseID105+
            process.HLTBtagDeepJetSequencePF+
            process.hltSelector6PFJets+
            process.hltBTagPFDeepJet7p68Double6Jets+
            process.hltBTagPFDeepJet1p28Single6Jets+
            process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5+
            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_QuadPFJet105_88_76_15_PFBTagDeepCSV_1p3_VBF2_v
    ############################################################################

    process.HLT_QuadPFJet105_88_76_15_PFBTagDeepCSV_1p3_VBF2_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1008572VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet105887615PFBTagDeepCSV1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        process.HLTFastPrimaryVertexSequenceROIForBTag+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID76+
        process.hltPFDoubleJetLooseID88+
        process.hltPFSingleJetLooseID105+
        process.HLTBtagDeepCSVSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepCSV1p28Single6Jets+
        process.hltVBFPFJetCSVSortedMqq460Detaqq3p5+
        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltPreQuadPFJet105887615PFBTagDeepJet1p3VBF2 = process.hltPreQuadPFJet105887615PFBTagDeepCSV1p3VBF2.clone()
        process.HLT_QuadPFJet105_88_76_15_PFBTagDeepJet_1p3_VBF2_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sTripleJet1008572VBFIorHTTIorDoubleJetCIorSingleJet+
            process.hltPreQuadPFJet105887615PFBTagDeepJet1p3VBF2+
            process.HLTAK4CaloJetsSequence+
            process.hltQuadJet15+
            process.hltTripleJet50+
            process.hltDoubleJet65+
            process.hltSingleJet80+
            process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

            process.HLTFastPrimaryVertexSequenceROIForBTag+
            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFQuadJetLooseID15+
            process.hltPFTripleJetLooseID76+
            process.hltPFDoubleJetLooseID88+
            process.hltPFSingleJetLooseID105+
            process.HLTBtagDeepJetSequencePF+
            process.hltSelector6PFJets+
            process.hltBTagPFDeepJet1p28Single6Jets+
            process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5+
            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v
    ############################################################################

    # process.hltPFTripleJetLooseID80 = process.hltPFTripleJetLooseID80.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltPFDoubleJetLooseID90 = process.hltPFDoubleJetLooseID90.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltPFSingleJetLooseID111 = process.hltPFSingleJetLooseID111.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )

    process.HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1058576VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet111908015DoublePFBTagDeepCSV1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        process.HLTFastPrimaryVertexSequenceROIForBTag+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID80+
        process.hltPFDoubleJetLooseID90+
        process.hltPFSingleJetLooseID111+
        process.HLTBtagDeepCSVSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepCSV7p68Double6Jets+
        process.hltBTagPFDeepCSV1p28Single6Jets+
        process.hltVBFPFJetCSVSortedMqq200Detaqq1p5+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltPreQuadPFJet111908015DoublePFBTagDeepJet1p37p7VBF1 = process.hltPreQuadPFJet111908015DoublePFBTagDeepCSV1p37p7VBF1.clone()
        process.HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sTripleJet1058576VBFIorHTTIorDoubleJetCIorSingleJet+
            process.hltPreQuadPFJet111908015DoublePFBTagDeepJet1p37p7VBF1+
            process.HLTAK4CaloJetsSequence+
            process.hltQuadJet15+
            process.hltTripleJet50+
            process.hltDoubleJet65+
            process.hltSingleJet80+
            process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

            process.HLTFastPrimaryVertexSequenceROIForBTag+
            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFQuadJetLooseID15+
            process.hltPFTripleJetLooseID80+
            process.hltPFDoubleJetLooseID90+
            process.hltPFSingleJetLooseID111+
            process.HLTBtagDeepJetSequencePF+
            process.hltSelector6PFJets+
            process.hltBTagPFDeepJet7p68Double6Jets+
            process.hltBTagPFDeepJet1p28Single6Jets+
            process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5+

            process.HLTEndSequence
        )


    ############################################################################
    #### HLT_QuadPFJet111_90_80_15_PFBTagDeepCSV_1p3_VBF2_v
    ############################################################################

    process.HLT_QuadPFJet111_90_80_15_PFBTagDeepCSV_1p3_VBF2_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1058576VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet111908015PFBTagDeepCSV1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        process.HLTFastPrimaryVertexSequenceROIForBTag+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID80+
        process.hltPFDoubleJetLooseID90+
        process.hltPFSingleJetLooseID111+
        process.HLTBtagDeepCSVSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepCSV1p28Single6Jets+
        process.hltVBFPFJetCSVSortedMqq460Detaqq3p5+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltPreQuadPFJet111908015PFBTagDeepJet1p3VBF2 = process.hltPreQuadPFJet111908015PFBTagDeepCSV1p3VBF2.clone()
        process.HLT_QuadPFJet111_90_80_15_PFBTagDeepJet_1p3_VBF2_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sTripleJet1058576VBFIorHTTIorDoubleJetCIorSingleJet+
            process.hltPreQuadPFJet111908015PFBTagDeepJet1p3VBF2+
            process.HLTAK4CaloJetsSequence+
            process.hltQuadJet15+
            process.hltTripleJet50+
            process.hltDoubleJet65+
            process.hltSingleJet80+
            process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

            process.HLTFastPrimaryVertexSequenceROIForBTag+
            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFQuadJetLooseID15+
            process.hltPFTripleJetLooseID80+
            process.hltPFDoubleJetLooseID90+
            process.hltPFSingleJetLooseID111+
            process.HLTBtagDeepJetSequencePF+
            process.hltSelector6PFJets+
            process.hltBTagPFDeepJet1p28Single6Jets+
            process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v
    ############################################################################

    # process.hltPFTripleJetLooseID71 = process.hltPFTripleJetLooseID71.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltPFDoubleJetLooseID83 = process.hltPFDoubleJetLooseID83.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )
    #
    # process.hltPFSingleJetLooseID98 = process.hltPFSingleJetLooseID98.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    # )

    process.HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet927664VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet98837115DoublePFBTagDeepCSV1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        process.HLTFastPrimaryVertexSequenceROIForBTag+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID71+
        process.hltPFDoubleJetLooseID83+
        process.hltPFSingleJetLooseID98+
        process.HLTBtagDeepCSVSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepCSV7p68Double6Jets+
        process.hltBTagPFDeepCSV1p28Single6Jets+
        process.hltVBFPFJetCSVSortedMqq200Detaqq1p5+
        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sTripleJet927664VBFIorHTTIorDoubleJetCIorSingleJet+
            process.hltPreQuadPFJet98837115DoublePFBTagDeepCSV1p37p7VBF1+
            process.HLTAK4CaloJetsSequence+
            process.hltQuadJet15+
            process.hltTripleJet50+
            process.hltDoubleJet65+
            process.hltSingleJet80+
            process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

            process.HLTFastPrimaryVertexSequenceROIForBTag+
            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFQuadJetLooseID15+
            process.hltPFTripleJetLooseID71+
            process.hltPFDoubleJetLooseID83+
            process.hltPFSingleJetLooseID98+
            process.HLTBtagDeepJetSequencePF+
            process.hltSelector6PFJets+
            process.hltBTagPFDeepJet7p68Double6Jets+
            process.hltBTagPFDeepJet1p28Single6Jets+
            process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5+
            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2_v
    ############################################################################

    process.HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet927664VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet98837115PFBTagDeepCSV1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        process.HLTFastPrimaryVertexSequenceROIForBTag+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID71+
        process.hltPFDoubleJetLooseID83+
        process.hltPFSingleJetLooseID98+
        process.HLTBtagDeepCSVSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepCSV1p28Single6Jets+
        process.hltVBFPFJetCSVSortedMqq460Detaqq3p5+
        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.HLT_QuadPFJet98_83_71_15_PFBTagDeepJet_1p3_VBF2_v8 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sTripleJet927664VBFIorHTTIorDoubleJetCIorSingleJet+
            process.hltPreQuadPFJet98837115PFBTagDeepCSV1p3VBF2+
            process.HLTAK4CaloJetsSequence+
            process.hltQuadJet15+
            process.hltTripleJet50+
            process.hltDoubleJet65+
            process.hltSingleJet80+
            process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

            process.HLTFastPrimaryVertexSequenceROIForBTag+
            process.HLTBtagDeepCSVSequenceL3ROIForBTag+
            process.hltBTagCaloDeepCSV1p56SingleROIForBTag+

            process.HLTAK4PFJetsSequence+
            process.hltPFQuadJetLooseID15+
            process.hltPFTripleJetLooseID71+
            process.hltPFDoubleJetLooseID83+
            process.hltPFSingleJetLooseID98+
            process.HLTBtagDeepJetSequencePF+
            process.hltSelector6PFJets+
            process.hltBTagPFDeepJet1p28Single6Jets+
            process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5+
            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepCSV_1p5_v
    ############################################################################

    # process.hltPFJetFilterTwoC30 = process.hltPFJetFilterTwoC30.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltBTagPFDeepCSV1p5Single = process.hltBTagPFDeepCSV1p5Single.clone(
    #     JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
    #     Jets = cms.InputTag("hltPFJetForBtag"),
    # )

    process.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepCSV_1p5_v1 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sMu5EG23IorMu5IsoEG20IorMu7EG23IorMu7IsoEG20IorMuIso7EG23+
        process.hltPreMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZPFDiJet30PFBtagDeepCSV1p5+

        process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegSequence+
        process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegSequence+
        process.hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter+

        process.HLTAK4PFJetsSequence+
        process.hltPFJetFilterTwoC30+
        process.HLTBtagDeepCSVSequencePF+
        process.hltBTagPFDeepCSV1p5Single+
        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet1p5Single = process.hltBTagPFDeepCSV1p5Single.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtag"),
        )
        process.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepJet_1p5_v1 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sMu5EG23IorMu5IsoEG20IorMu7EG23IorMu7IsoEG20IorMuIso7EG23+
            process.hltPreMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZPFDiJet30PFBtagDeepCSV1p5+

            process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegSequence+
            process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegSequence+
            process.hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter+

            process.HLTAK4PFJetsSequence+
            process.hltPFJetFilterTwoC30+
            process.HLTBtagDeepJetSequencePF+
            process.hltBTagPFDeepJet1p5Single+
            process.HLTEndSequence
        )



    ############################################################################
    #### HLT_Ele15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5_v
    ############################################################################

    process.hltBTagCaloDeepCSV4p50SingleROIForBTag = process.hltBTagCaloDeepCSV4p50Single.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
        MinTag = cms.double(0.24),
    )

    # process.hltPFHTJet30 = process.hltPFHTJet30.clone(
    #     jetsLabel = cms.InputTag("hltAK4PFJetsCorrected"),
    #     pfCandidatesLabel = cms.InputTag("hltParticleFlow"),
    # )
    #
    # process.hltPFHT450Jet30 = process.hltPFHT450Jet30.clone(
    #     htLabels = cms.VInputTag("hltPFHTJet30"),
    #     mhtLabels = cms.VInputTag("hltPFHTJet30"),
    # )

    process.HLT_Ele15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT380erIorHTT320er+
        process.hltPreEle15IsoVVVLPFHT450CaloBTagDeepCSV4p5+
        cms.ignore(process.hltL1sSingleEG5ObjectMap)+

        process.HLTAK4CaloJetsSequence+
        process.hltHtMhtJet30+
        process.hltHT200Jet30+
        process.hltSusyPreBtagJetFilter+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV4p50SingleROIForBTag+

        process.HLTEle15VVVLGsfSequence+

        process.HLTAK4PFJetsSequence+
        process.hltPFHTJet30+
        process.hltPFHT450Jet30+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets100_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltBTagCaloDeepCSV0p71Single6Jets80ROIForBTag = process.hltBTagCaloDeepCSV0p71Single6Jets80.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
        MinTag = cms.double(0.52),
    )

    # process.hltDoublePFJets100Eta2p3 = process.hltDoublePFJets100Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )

    process.HLT_DoublePFJets100_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1DoubleJet100er3p0+
        process.hltPreDoublePFJets100CaloBTagDeepCSVp71+

        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets100eta2p3+
        process.hltSelectorJets80L1FastJet+
        process.hltSelectorCentralJets80L1FastJet+
        process.hltSelector6CentralJetsL1FastJet+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single6Jets80ROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltDoublePFJets100Eta2p3+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltBTagCaloDeepCSV0p71Double6Jets80ROIForBTag = process.hltBTagCaloDeepCSV0p71Double6Jets80.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
    )

    # process.hltDoublePFJets116Eta2p3 = process.hltDoublePFJets116Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltDoublePFJets116Eta2p3MaxDeta1p6 = process.hltDoublePFJets116Eta2p3MaxDeta1p6.clone(
    #     inputTag1 = cms.InputTag("hltDoublePFJets116Eta2p3"),
    #     inputTag2 = cms.InputTag("hltDoublePFJets116Eta2p3"),
    #     originTag1 = cms.VInputTag("hltAK4PFJetsCorrected"),
    #     originTag2 = cms.VInputTag("hltAK4PFJetsCorrected"),
    # )

    process.HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1DoubleJet112er2p3dEtaMax1p6+
        process.hltPreDoublePFJets116MaxDeta1p6DoubleCaloBTagDeepCSVp71+

        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets100eta2p3+
        process.hltSelectorJets80L1FastJet+
        process.hltSelectorCentralJets80L1FastJet+
        process.hltSelector6CentralJetsL1FastJet+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Double6Jets80ROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltDoublePFJets116Eta2p3+
        process.hltDoublePFJets116Eta2p3MaxDeta1p6+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    # process.hltDoublePFJets128Eta2p3 = process.hltDoublePFJets128Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltDoublePFJets128Eta2p3MaxDeta1p6 = process.hltDoublePFJets128Eta2p3MaxDeta1p6.clone(
    #     inputTag1 = cms.InputTag("hltDoublePFJets128Eta2p3"),
    #     inputTag2 = cms.InputTag("hltDoublePFJets128Eta2p3"),
    #     originTag1 = cms.VInputTag("hltAK4PFJetsCorrected"),
    #     originTag2 = cms.VInputTag("hltAK4PFJetsCorrected"),
    # )

    process.HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1DoubleJet112er2p3dEtaMax1p6+
        process.hltPreDoublePFJets128MaxDeta1p6DoubleCaloBTagDeepCSVp71+

        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets100eta2p3+
        process.hltSelectorJets80L1FastJet+
        process.hltSelectorCentralJets80L1FastJet+
        process.hltSelector6CentralJetsL1FastJet+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Double6Jets80ROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltDoublePFJets128Eta2p3+
        process.hltDoublePFJets128Eta2p3MaxDeta1p6+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets200_CaloBTagDeepCSV_p71_v
    ############################################################################

    # process.hltDoublePFJets200Eta2p3 = process.hltDoublePFJets200Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )

    process.HLT_DoublePFJets200_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1DoubleJet120er3p0+
        process.hltPreDoublePFJets200CaloBTagDeepCSVp71+

        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets100eta2p3+
        process.hltSelectorJets80L1FastJet+
        process.hltSelectorCentralJets80L1FastJet+
        process.hltSelector6CentralJetsL1FastJet+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single6Jets80ROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltDoublePFJets200Eta2p3+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets350_CaloBTagDeepCSV_p71_v
    ############################################################################

    # process.hltDoublePFJets350Eta2p3 = process.hltDoublePFJets350Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )

    process.HLT_DoublePFJets350_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1DoubleJet120er3p0+
        process.hltPreDoublePFJets350CaloBTagDeepCSVp71+

        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets100eta2p3+
        process.hltSelectorJets80L1FastJet+
        process.hltSelectorCentralJets80L1FastJet+
        process.hltSelector6CentralJetsL1FastJet+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single6Jets80ROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltDoublePFJets350Eta2p3+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_DoublePFJets40_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltBTagCaloDeepCSV0p71Single8Jets30ROIForBTag = process.hltBTagCaloDeepCSV0p71Single8Jets30.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
    )

    # process.hltDoublePFJets40Eta2p3 = process.hltDoublePFJets40Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )

    process.HLT_DoublePFJets40_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1DoubleJet40er3p0+
        process.hltPreDoublePFJets40CaloBTagDeepCSVp71+

        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single8Jets30ROIForBTag+

        process.HLTAK4PFJetsSequence+
        process.hltDoublePFJets40Eta2p3+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets100_CaloBTagDeepCSV_p71_v
    ############################################################################

    # process.hltDoublePFBJets100Eta2p3 = process.hltDoublePFBJets100Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltBSoftMuonGetJetsFromDiJet100PF = process.hltBSoftMuonGetJetsFromDiJet100PF.clone(
    #     HLTObject = cms.InputTag("hltDoublePFBJets100Eta2p3"),
    # )
    #
    # process.hltSelector4JetsDiJet100PF = process.hltSelector4JetsDiJet100PF.clone(
    #     src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet100PF")
    # )
    #
    # process.hltBSoftMuonDiJet100PFMu12L3Jets = process.hltBSoftMuonDiJet100PFMu12L3Jets.clone(
    #     src = cms.InputTag("hltSelector4JetsDiJet100PF")
    # )
    #
    # process.hltBSoftMuonDiJet100PFMu12L3TagInfos = process.hltBSoftMuonDiJet100PFMu12L3TagInfos.clone(
    #     jets = cms.InputTag("hltBSoftMuonDiJet100PFMu12L3Jets"),
    # )
    #
    # process.hltBSoftMuonDiJet100PFMu12L3BJetTagsByDR = process.hltBSoftMuonDiJet100PFMu12L3BJetTagsByDR.clone(
    #     tagInfos = cms.VInputTag("hltBSoftMuonDiJet100PFMu12L3TagInfos")
    # )
    #
    # process.HLTBTagMuDiJet100PFMu12SequenceL3 = cms.Sequence(
    #     process.hltBSoftMuonGetJetsFromDiJet100PF+
    #     process.hltSelector4JetsDiJet100PF+
    #     process.hltBSoftMuonDiJet100PFMu12L3Jets+
    #     process.hltBSoftMuonMu12L3+
    #     process.hltBSoftMuonDiJet100PFMu12L3TagInfos+
    #     process.hltBSoftMuonDiJet100PFMu12L3BJetTagsByDR
    # )
    #
    # process.hltBSoftMuonDiJet100Mu12L3FilterByDR = process.hltBSoftMuonDiJet100Mu12L3FilterByDR.clone(
    #     JetTags = cms.InputTag("hltBSoftMuonDiJet100PFMu12L3BJetTagsByDR"),
    #     Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet100PF"),
    # )

    process.HLT_Mu12_DoublePFJets100_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sMu3JetC60dRMax0p4+
        process.hltPreMu12DoublePFJets100CaloBTagDeepCSVp71+
        process.hltL1fL1sMu3Jet60L1Filtered0+
        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single8Jets30ROIForBTag+

        process.HLTL2muonrecoSequence+
        cms.ignore(process.hltL2fL1sMu3Jet60L1f0L2Filtered8)+
        process.HLTL3muonrecoSequence+
        cms.ignore(process.hltL1fForIterL3L1fL1sMu3Jet60L1Filtered0)+
        process.hltL3fL1sMu3Jet60L1f0L2f8L3Filtered12+

        process.HLTAK4PFJetsSequence+
        process.hltDoublePFBJets100Eta2p3+

        process.HLTBTagMuDiJet100PFMu12SequenceL3+
        process.hltBSoftMuonDiJet100Mu12L3FilterByDR+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets200_CaloBTagDeepCSV_p71_v
    ############################################################################

    # process.hltDoublePFBJets200Eta2p3 = process.hltDoublePFBJets200Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltBSoftMuonGetJetsFromDiJet200PF = process.hltBSoftMuonGetJetsFromDiJet200PF.clone(
    #     HLTObject = cms.InputTag("hltDoublePFBJets200Eta2p3"),
    # )
    #
    # process.hltSelector4JetsDiJet200PF = process.hltSelector4JetsDiJet200PF.clone(
    #     src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet200PF")
    # )
    #
    # process.hltBSoftMuonDiJet200PFMu12L3Jets = process.hltBSoftMuonDiJet200PFMu12L3Jets.clone(
    #     src = cms.InputTag("hltSelector4JetsDiJet200PF")
    # )
    #
    # process.hltBSoftMuonDiJet200PFMu12L3TagInfos = process.hltBSoftMuonDiJet200PFMu12L3TagInfos.clone(
    #     jets = cms.InputTag("hltBSoftMuonDiJet200PFMu12L3Jets"),
    # )
    #
    # process.hltBSoftMuonDiJet200PFMu12L3BJetTagsByDR = process.hltBSoftMuonDiJet200PFMu12L3BJetTagsByDR.clone(
    #     tagInfos = cms.VInputTag("hltBSoftMuonDiJet200PFMu12L3TagInfos")
    # )
    #
    # process.HLTBTagMuDiJet200PFMu12SequenceL3 = cms.Sequence(
    #     process.hltBSoftMuonGetJetsFromDiJet200PF+
    #     process.hltSelector4JetsDiJet200PF+
    #     process.hltBSoftMuonDiJet200PFMu12L3Jets+
    #     process.hltBSoftMuonMu12L3+
    #     process.hltBSoftMuonDiJet200PFMu12L3TagInfos+
    #     process.hltBSoftMuonDiJet200PFMu12L3BJetTagsByDR
    # )
    #
    # process.hltBSoftMuonDiJet200Mu12L3FilterByDR = process.hltBSoftMuonDiJet200Mu12L3FilterByDR.clone(
    #     JetTags = cms.InputTag("hltBSoftMuonDiJet200PFMu12L3BJetTagsByDR"),
    #     Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet200PF"),
    # )

    process.HLT_Mu12_DoublePFJets200_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sMu3JetC120dRMax0p4+
        process.hltPreMu12DoublePFJets200CaloBTagDeepCSVp71+

        process.hltL1fL1sMu3Jet120L1Filtered0+
        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single8Jets30ROIForBTag+
        process.HLTL2muonrecoSequence+
        cms.ignore(process.hltL2fL1sMu3Jet120L1f0L2Filtered8)+
        process.HLTL3muonrecoSequence+
        cms.ignore(process.hltL1fForIterL3L1fL1sMu3Jet120L1Filtered0)+
        process.hltL3fL1sMu3Jet120L1f0L2f8L3Filtered12+

        process.HLTAK4PFJetsSequence+
        process.hltDoublePFBJets200Eta2p3+
        process.HLTBTagMuDiJet200PFMu12SequenceL3+
        process.hltBSoftMuonDiJet200Mu12L3FilterByDR+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets350_CaloBTagDeepCSV_p71_v
    ############################################################################

    # process.hltDoublePFBJets350Eta2p3 = process.hltDoublePFBJets350Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltBSoftMuonGetJetsFromDiJet350PF = process.hltBSoftMuonGetJetsFromDiJet350PF.clone(
    #     HLTObject = cms.InputTag("hltDoublePFBJets350Eta2p3"),
    # )
    #
    # process.hltSelector4JetsDiJet350PF = process.hltSelector4JetsDiJet350PF.clone(
    #     src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet350PF")
    # )
    #
    # process.hltBSoftMuonDiJet350PFMu12L3Jets = process.hltBSoftMuonDiJet350PFMu12L3Jets.clone(
    #     src = cms.InputTag("hltSelector4JetsDiJet350PF")
    # )
    #
    # process.hltBSoftMuonDiJet350PFMu12L3TagInfos = process.hltBSoftMuonDiJet350PFMu12L3TagInfos.clone(
    #     jets = cms.InputTag("hltBSoftMuonDiJet350PFMu12L3Jets"),
    # )
    #
    # process.hltBSoftMuonDiJet350PFMu12L3BJetTagsByDR = process.hltBSoftMuonDiJet350PFMu12L3BJetTagsByDR.clone(
    #     tagInfos = cms.VInputTag("hltBSoftMuonDiJet350PFMu12L3TagInfos")
    # )
    #
    # process.hltBSoftMuonDiJet350Mu12L3FilterByDR = process.hltBSoftMuonDiJet350Mu12L3FilterByDR.clone(
    #     JetTags = cms.InputTag("hltBSoftMuonDiJet350PFMu12L3BJetTagsByDR"),
    #     Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet350PF"),
    # )
    #
    # process.HLTBTagMuDiJet350PFMu12SequenceL3 = cms.Sequence(
    #     process.hltBSoftMuonGetJetsFromDiJet350PF+
    #     process.hltSelector4JetsDiJet350PF+
    #     process.hltBSoftMuonDiJet350PFMu12L3Jets+
    #     process.hltBSoftMuonMu12L3+
    #     process.hltBSoftMuonDiJet350PFMu12L3TagInfos+
    #     process.hltBSoftMuonDiJet350PFMu12L3BJetTagsByDR
    # )

    process.HLT_Mu12_DoublePFJets350_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sMu3JetC120dRMax0p4+
        process.hltPreMu12DoublePFJets350CaloBTagDeepCSVp71+

        process.hltL1fL1sMu3Jet120L1Filtered0+
        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single8Jets30ROIForBTag+

        process.HLTL2muonrecoSequence+
        cms.ignore(process.hltL2fL1sMu3Jet120L1f0L2Filtered8)+
        process.HLTL3muonrecoSequence+
        cms.ignore(process.hltL1fForIterL3L1fL1sMu3Jet120L1Filtered0)+
        process.hltL3fL1sMu3Jet120L1f0L2f8L3Filtered12+
        process.HLTAK4PFJetsSequence+
        process.hltDoublePFBJets350Eta2p3+
        process.HLTBTagMuDiJet350PFMu12SequenceL3+
        process.hltBSoftMuonDiJet350Mu12L3FilterByDR+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltBTagCaloDeepCSV0p71Double8Jets30ROIForBTag = process.hltBTagCaloDeepCSV0p71Double8Jets30.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
    )

    # process.hltDoublePFBJets40Eta2p3 = process.hltDoublePFBJets40Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltDoublePFJets40Eta2p3MaxDeta1p6 = process.hltDoublePFJets40Eta2p3MaxDeta1p6.clone(
    #     inputTag1 = cms.InputTag("hltDoublePFBJets40Eta2p3"),
    #     inputTag2 = cms.InputTag("hltDoublePFBJets40Eta2p3"),
    #     originTag1 = cms.VInputTag("hltAK4PFJetsCorrected"),
    #     originTag2 = cms.VInputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltBSoftMuonGetJetsFromDiJet40PF = process.hltBSoftMuonGetJetsFromDiJet40PF.clone(
    #     HLTObject = cms.InputTag("hltDoublePFBJets40Eta2p3"),
    # )
    #
    # process.hltSelector4JetsDiJet40PF = process.hltSelector4JetsDiJet40PF.clone(
    #     src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet40PF")
    # )
    #
    # process.hltBSoftMuonDiJet40PFMu12L3Jets = process.hltBSoftMuonDiJet40PFMu12L3Jets.clone(
    #     src = cms.InputTag("hltSelector4JetsDiJet40PF")
    # )
    #
    # process.hltBSoftMuonDiJet40PFMu12L3TagInfos = process.hltBSoftMuonDiJet40PFMu12L3TagInfos.clone(
    #     jets = cms.InputTag("hltBSoftMuonDiJet40PFMu12L3Jets"),
    # )
    #
    # process.hltBSoftMuonDiJet40PFMu12L3BJetTagsByDR = process.hltBSoftMuonDiJet40PFMu12L3BJetTagsByDR.clone(
    #     tagInfos = cms.VInputTag("hltBSoftMuonDiJet40PFMu12L3TagInfos")
    # )
    #
    # process.HLTBTagMuDiJet40PFMu12SequenceL3 = cms.Sequence(
    #     process.hltBSoftMuonGetJetsFromDiJet40PF+
    #     process.hltSelector4JetsDiJet40PF+
    #     process.hltBSoftMuonDiJet40PFMu12L3Jets+
    #     process.hltBSoftMuonMu12L3+
    #     process.hltBSoftMuonDiJet40PFMu12L3TagInfos+
    #     process.hltBSoftMuonDiJet40PFMu12L3BJetTagsByDR
    # )
    #
    # process.hltBSoftMuonDiJet40Mu12L3FilterByDR = process.hltBSoftMuonDiJet40Mu12L3FilterByDR.clone(
    #     JetTags = cms.InputTag("hltBSoftMuonDiJet40PFMu12L3BJetTagsByDR"),
    #     Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet40PF"),
    # )

    process.HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6+
        process.hltPreMu12DoublePFJets40MaxDeta1p6DoubleCaloBTagDeepCSVp71+
        process.hltL1fL1sMu12Dijet40L1Filtered0+
        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Double8Jets30ROIForBTag+

        process.HLTL2muonrecoSequence+
        cms.ignore(process.hltL2fL1sMu12Dijet40L1f0L2Filtered8)+
        process.HLTL3muonrecoSequence+
        cms.ignore(process.hltL1fForIterL3L1fL1sMu12Dijet40L1Filtered0)+
        process.hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12+

        process.HLTAK4PFJetsSequence+
        process.hltDoublePFBJets40Eta2p3+
        process.hltDoublePFJets40Eta2p3MaxDeta1p6+
        process.HLTBTagMuDiJet40PFMu12SequenceL3+
        process.hltBSoftMuonDiJet40Mu12L3FilterByDR+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_Mu12_DoublePFJets40_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.HLT_Mu12_DoublePFJets40_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sMu3JetC16dRMax0p4+
        process.hltPreMu12DoublePFJets40CaloBTagDeepCSVp71+
        process.hltL1fL1sMu3Jet16L1Filtered0+
        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single8Jets30ROIForBTag+
        process.HLTL2muonrecoSequence+
        cms.ignore(process.hltL2fL1sMu3Jet16L1f0L2Filtered8)+
        process.HLTL3muonrecoSequence+
        cms.ignore(process.hltL1fForIterL3L1fL1sMu3Jet16L1Filtered0)+
        process.hltL3fL1sMu3Jet16L1f0L2f8L3Filtered12+
        process.HLTAK4PFJetsSequence+
        process.hltDoublePFBJets40Eta2p3+
        process.HLTBTagMuDiJet40PFMu12SequenceL3+
        process.hltBSoftMuonDiJet40Mu12L3FilterByDR+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    # process.hltDoublePFBJets54Eta2p3 = process.hltDoublePFBJets54Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltDoublePFJets54Eta2p3MaxDeta1p6 = process.hltDoublePFJets54Eta2p3MaxDeta1p6.clone(
    #     inputTag1 = cms.InputTag("hltDoublePFBJets54Eta2p3"),
    #     inputTag2 = cms.InputTag("hltDoublePFBJets54Eta2p3"),
    #     originTag1 = cms.VInputTag("hltAK4PFJetsCorrected"),
    #     originTag2 = cms.VInputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltBSoftMuonGetJetsFromDiJet54PF = process.hltBSoftMuonGetJetsFromDiJet54PF.clone(
    #     HLTObject = cms.InputTag("hltDoublePFBJets54Eta2p3"),
    # )
    #
    # process.hltSelector4JetsDiJet54PF = process.hltSelector4JetsDiJet54PF.clone(
    #     src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet54PF")
    # )
    #
    # process.hltBSoftMuonDiJet54PFMu12L3Jets = process.hltBSoftMuonDiJet54PFMu12L3Jets.clone(
    #     src = cms.InputTag("hltSelector4JetsDiJet54PF")
    # )
    #
    # process.hltBSoftMuonDiJet54PFMu12L3TagInfos = process.hltBSoftMuonDiJet54PFMu12L3TagInfos.clone(
    #     jets = cms.InputTag("hltBSoftMuonDiJet54PFMu12L3Jets"),
    # )
    #
    # process.hltBSoftMuonDiJet54PFMu12L3BJetTagsByDR = process.hltBSoftMuonDiJet54PFMu12L3BJetTagsByDR.clone(
    #     tagInfos = cms.VInputTag("hltBSoftMuonDiJet54PFMu12L3TagInfos")
    # )
    #
    # process.HLTBTagMuDiJet54PFMu12SequenceL3 = cms.Sequence(
    #     process.hltBSoftMuonGetJetsFromDiJet54PF+
    #     process.hltSelector4JetsDiJet54PF+
    #     process.hltBSoftMuonDiJet54PFMu12L3Jets+
    #     process.hltBSoftMuonMu12L3+
    #     process.hltBSoftMuonDiJet54PFMu12L3TagInfos+
    #     process.hltBSoftMuonDiJet54PFMu12L3BJetTagsByDR
    # )
    #
    # process.hltBSoftMuonDiJet54Mu12L3FilterByDR = process.hltBSoftMuonDiJet54Mu12L3FilterByDR.clone(
    #     JetTags = cms.InputTag("hltBSoftMuonDiJet54PFMu12L3BJetTagsByDR"),
    #     Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet54PF"),
    # )

    process.HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6+
        process.hltPreMu12DoublePFJets54MaxDeta1p6DoubleCaloBTagDeepCSVp71+
        process.hltL1fL1sMu12Dijet40L1Filtered0+
        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Double8Jets30ROIForBTag+
        process.HLTL2muonrecoSequence+
        cms.ignore(process.hltL2fL1sMu12Dijet40L1f0L2Filtered8)+
        process.HLTL3muonrecoSequence+
        cms.ignore(process.hltL1fForIterL3L1fL1sMu12Dijet40L1Filtered0)+
        process.hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12+
        process.HLTAK4PFJetsSequence+
        process.hltDoublePFBJets54Eta2p3+
        process.hltDoublePFJets54Eta2p3MaxDeta1p6+
        process.HLTBTagMuDiJet54PFMu12SequenceL3+
        process.hltBSoftMuonDiJet54Mu12L3FilterByDR+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    # process.hltDoublePFBJets62Eta2p3 = process.hltDoublePFBJets62Eta2p3.clone(
    #     inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltDoublePFJets62Eta2p3MaxDeta1p6 = process.hltDoublePFJets62Eta2p3MaxDeta1p6.clone(
    #     inputTag1 = cms.InputTag("hltDoublePFBJets62Eta2p3"),
    #     inputTag2 = cms.InputTag("hltDoublePFBJets62Eta2p3"),
    #     originTag1 = cms.VInputTag("hltAK4PFJetsCorrected"),
    #     originTag2 = cms.VInputTag("hltAK4PFJetsCorrected"),
    # )
    #
    # process.hltBSoftMuonGetJetsFromDiJet62PF = process.hltBSoftMuonGetJetsFromDiJet62PF.clone(
    #     HLTObject = cms.InputTag("hltDoublePFBJets62Eta2p3"),
    # )
    #
    # process.hltSelector4JetsDiJet62PF = process.hltSelector4JetsDiJet62PF.clone(
    #     src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet62PF")
    # )
    #
    # process.hltBSoftMuonDiJet62PFMu12L3Jets = process.hltBSoftMuonDiJet62PFMu12L3Jets.clone(
    #     src = cms.InputTag("hltSelector4JetsDiJet62PF")
    # )
    #
    # process.hltBSoftMuonDiJet62PFMu12L3TagInfos = process.hltBSoftMuonDiJet62PFMu12L3TagInfos.clone(
    #     jets = cms.InputTag("hltBSoftMuonDiJet62PFMu12L3Jets"),
    # )
    #
    # process.hltBSoftMuonDiJet62PFMu12L3BJetTagsByDR = process.hltBSoftMuonDiJet62PFMu12L3BJetTagsByDR.clone(
    #     tagInfos = cms.VInputTag("hltBSoftMuonDiJet62PFMu12L3TagInfos")
    # )
    #
    # process.HLTBTagMuDiJet62PFMu12SequenceL3 = cms.Sequence(
    #     process.hltBSoftMuonGetJetsFromDiJet62PF+
    #     process.hltSelector4JetsDiJet62PF+
    #     process.hltBSoftMuonDiJet62PFMu12L3Jets+
    #     process.hltBSoftMuonMu12L3+
    #     process.hltBSoftMuonDiJet62PFMu12L3TagInfos+
    #     process.hltBSoftMuonDiJet62PFMu12L3BJetTagsByDR
    # )
    #
    #
    # process.hltBSoftMuonDiJet62Mu12L3FilterByDR = process.hltBSoftMuonDiJet62Mu12L3FilterByDR.clone(
    #     JetTags = cms.InputTag("hltBSoftMuonDiJet62PFMu12L3BJetTagsByDR"),
    #     Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet62PF"),
    # )

    process.HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1Mu12er2p3Jet40er2p3dRMax0p4DoubleJet40er2p3dEtaMax1p6+
        process.hltPreMu12DoublePFJets62MaxDeta1p6DoubleCaloBTagDeepCSVp71+
        process.hltL1fL1sMu12Dijet40L1Filtered0+
        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Double8Jets30ROIForBTag+
        process.HLTL2muonrecoSequence+
        cms.ignore(process.hltL2fL1sMu12Dijet40L1f0L2Filtered8)+
        process.HLTL3muonrecoSequence+
        cms.ignore(process.hltL1fForIterL3L1fL1sMu12Dijet40L1Filtered0)+
        process.hltL3fL1sMu12Dijet40L1f0L2f8L3Filtered12+
        process.HLTAK4PFJetsSequence+
        process.hltDoublePFBJets62Eta2p3+
        process.hltDoublePFJets62Eta2p3MaxDeta1p6+
        process.HLTBTagMuDiJet62PFMu12SequenceL3+
        process.hltBSoftMuonDiJet62Mu12L3FilterByDR+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_PFMET110_PFMHT110_IDTight_CaloBTagDeepCSV_3p1_v
    ############################################################################

    process.hltBTagCaloDeepCSV3p07SingleROIForBTag = process.hltBTagCaloDeepCSV3p07Single.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
    )

    process.HLT_PFMET110_PFMHT110_IDTight_CaloBTagDeepCSV_3p1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sAllETMHFSeeds+
        process.hltPrePFMET110PFMHT110IDTightCaloBTagDeepCSV3p1+
        process.HLTRecoMETSequence+
        process.hltMET80+
        process.HLTAK4CaloJetsSequence+
        process.hltMht+
        process.hltMHT80+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV3p07SingleROIForBTag+
        process.HLTAK4PFJetsSequence+
        process.hltPFMHTTightID+
        process.hltPFMHTTightID110+
        process.hltPFMETProducer+
        process.hltPFMET110+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_PFMET120_PFMHT120_IDTight_CaloBTagDeepCSV_3p1_v
    ############################################################################

    process.HLT_PFMET120_PFMHT120_IDTight_CaloBTagDeepCSV_3p1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sAllETMHFSeeds+
        process.hltPrePFMET120PFMHT120IDTightCaloBTagDeepCSV3p1+
        process.HLTRecoMETSequence+
        process.hltMET90+
        process.HLTAK4CaloJetsSequence+
        process.hltMht+
        process.hltMHT90+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV3p07SingleROIForBTag+
        process.HLTAK4PFJetsSequence+
        process.hltPFMHTTightID+
        process.hltPFMHTTightID120+
        process.hltPFMETProducer+
        process.hltPFMET120+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_PFMET130_PFMHT130_IDTight_CaloBTagDeepCSV_3p1_v
    ############################################################################

    process.HLT_PFMET130_PFMHT130_IDTight_CaloBTagDeepCSV_3p1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sAllETMHFSeeds+
        process.hltPrePFMET130PFMHT130IDTightCaloBTagDeepCSV3p1+
        process.HLTRecoMETSequence+
        process.hltMET100+
        process.HLTAK4CaloJetsSequence+
        process.hltMht+
        process.hltMHT100+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV3p07SingleROIForBTag+
        process.HLTAK4PFJetsSequence+
        process.hltPFMHTTightID+
        process.hltPFMHTTightID130+
        process.hltPFMETProducer+
        process.hltPFMET130+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1_v
    ############################################################################

    process.HLT_PFMET100_PFMHT100_IDTight_CaloBTagDeepCSV_3p1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sAllETMHFSeeds+
        process.hltPrePFMET100PFMHT100IDTightCaloBTagDeepCSV3p1+
        process.HLTRecoMETSequence+
        process.hltMET70+
        process.HLTAK4CaloJetsSequence+
        process.hltMht+
        process.hltMHT70+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV3p07SingleROIForBTag+
        process.HLTAK4PFJetsSequence+
        process.hltPFMHTTightID+
        process.hltPFMHTTightID100+
        process.hltPFMETProducer+
        process.hltPFMET100+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_PFMET140_PFMHT140_IDTight_CaloBTagDeepCSV_3p1_v
    ############################################################################

    process.HLT_PFMET140_PFMHT140_IDTight_CaloBTagDeepCSV_3p1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sAllETMHFSeeds+
        process.hltPrePFMET140PFMHT140IDTightCaloBTagDeepCSV3p1+
        process.HLTRecoMETSequence+
        process.hltMET110+
        process.HLTAK4CaloJetsSequence+
        process.hltMht+
        process.hltMHT110+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV3p07SingleROIForBTag+
        process.HLTAK4PFJetsSequence+
        process.hltPFMHTTightID+
        process.hltPFMHTTightID140+
        process.hltPFMETProducer+
        process.hltPFMET140+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_CaloDiJet30_CaloBtagDeepCSV_1p5_v
    ############################################################################

    process.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_CaloDiJet30_CaloBtagDeepCSV_1p5_v1 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sMu5EG23IorMu5IsoEG20IorMu7EG23IorMu7IsoEG20IorMuIso7EG23+
        process.hltPreMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZCaloDiJet30CaloBtagDeepCSV1p5+
        process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegSequence+
        process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegSequence+
        process.hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterTwoC30+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV1p56SingleROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5_v
    ############################################################################

    process.HLT_Mu15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT380erIorHTT320er+
        process.hltPreMu15IsoVVVLPFHT450CaloBTagDeepCSV4p5+
        cms.ignore(process.hltL1sSingleMuOpenObjectMap)+
        process.HLTAK4CaloJetsSequence+
        process.hltHtMhtJet30+
        process.hltHT200Jet30+
        process.hltSusyPreBtagJetFilter+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV4p50SingleROIForBTag+
        process.hltL1fL1sSingleMuOpenCandidateL1Filtered0+
        process.HLTL2muonrecoSequence+
        cms.ignore(process.hltL2fL1sSingleMuOpenCandidateL1f0L2Filtered0Q)+
        process.HLTL3muonrecoSequence+
        cms.ignore(process.hltL1fForIterL3L1fL1sSingleMuOpenCandidateL1Filtered0)+
        process.hltL3fL1sSingleMuOpenCandidateL1f0L2f3QL3Filtered15Q+
        process.HLTMuVVVLCombinedIsolationR02Sequence+
        process.hltL3MuVVVLIsoFIlter+
        process.HLTAK4PFJetsSequence+
        process.hltPFHTJet30+
        process.hltPFHT450Jet30+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets40_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.HLT_DoublePFJets40_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1DoubleJet40er3p0+
        process.hltPreDoublePFJets40CaloBTagDeepCSVp71+
        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single8Jets30ROIForBTag+
        process.HLTAK4PFJetsSequence+
        process.hltDoublePFJets40Eta2p3+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Ele15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5_v
    ############################################################################

    process.HLT_Ele15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT380erIorHTT320er+
        process.hltPreEle15IsoVVVLPFHT450CaloBTagDeepCSV4p5+
        cms.ignore(process.hltL1sSingleEG5ObjectMap)+
        process.HLTAK4CaloJetsSequence+
        process.hltHtMhtJet30+
        process.hltHT200Jet30+
        process.hltSusyPreBtagJetFilter+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV4p50SingleROIForBTag+
        process.HLTEle15VVVLGsfSequence+
        process.HLTAK4PFJetsSequence+
        process.hltPFHTJet30+
        process.hltPFHT450Jet30+
        process.HLTEndSequence
    )


    return process
