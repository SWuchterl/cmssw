import FWCore.ParameterSet.Config as cms

def customizeRun3_BTag_ROICalo_ROIPF(process, addDeepJetPaths = True):

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
    process.hltParticleFlowClusterECALUnseededROIForBTag = process.hltParticleFlowClusterECALUnseeded.clone(
        skipPS = cms.bool(True)
    )

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


    process.hltVerticesPFROIForBTag = process.hltVerticesPF.clone(
        TrackLabel = cms.InputTag("hltPFMuonMergingROIForBTag"),
    )

    process.hltVerticesPFSelectorROIForBTag = process.hltVerticesPFSelector.clone(
        filterParams = cms.PSet(
            maxRho = cms.double(2.0),
            maxZ = cms.double(24.0),
            minNdof = cms.double(4.0),
            pvSrc = cms.InputTag("hltVerticesPFROIForBTag")
        ),
        src = cms.InputTag("hltVerticesPFROIForBTag")
    )

    process.hltVerticesPFFilterROIForBTag = process.hltVerticesPFFilter.clone(
        src = cms.InputTag("hltVerticesPFSelectorROIForBTag")
    )

    process.hltPFJetForBtagSelectorROIForBTag = process.hltPFJetForBtagSelector.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltPFJetForBtagROIForBTag = process.hltPFJetForBtag.clone(
        HLTObject = cms.InputTag("hltPFJetForBtagSelectorROIForBTag"),
    )

    process.hltDeepBLifetimeTagInfosPFROIForBTag = process.hltDeepBLifetimeTagInfosPF.clone(
        candidates = cms.InputTag("hltParticleFlowROIForBTag"),
        jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
        primaryVertex = cms.InputTag("hltVerticesPFFilterROIForBTag"),
    )


    process.hltDeepInclusiveVertexFinderPFROIForBTag = process.hltDeepInclusiveVertexFinderPF.clone(
        primaryVertices = cms.InputTag("hltVerticesPFFilterROIForBTag"),
        tracks = cms.InputTag("hltParticleFlowROIForBTag"),
    )

    process.hltDeepInclusiveSecondaryVerticesPFROIForBTag = process.hltDeepInclusiveSecondaryVerticesPF.clone(
        secondaryVertices = cms.InputTag("hltDeepInclusiveVertexFinderPFROIForBTag")
    )

    process.hltDeepTrackVertexArbitratorPFROIForBTag = process.hltDeepTrackVertexArbitratorPF.clone(
        primaryVertices = cms.InputTag("hltVerticesPFFilterROIForBTag"),
        secondaryVertices = cms.InputTag("hltDeepInclusiveSecondaryVerticesPFROIForBTag"),
        tracks = cms.InputTag("hltParticleFlowROIForBTag")
    )

    process.hltDeepInclusiveMergedVerticesPFROIForBTag = process.hltDeepInclusiveMergedVerticesPF.clone(
        secondaryVertices = cms.InputTag("hltDeepTrackVertexArbitratorPFROIForBTag")
    )

    process.hltDeepSecondaryVertexTagInfosPFROIForBTag = process.hltDeepSecondaryVertexTagInfosPF.clone(
        extSVCollection = cms.InputTag("hltDeepInclusiveMergedVerticesPFROIForBTag"),
        trackIPTagInfos = cms.InputTag("hltDeepBLifetimeTagInfosPFROIForBTag"),
    )

    process.hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag = process.hltDeepCombinedSecondaryVertexBJetTagsInfos.clone(
        svTagInfos = cms.InputTag("hltDeepSecondaryVertexTagInfosPFROIForBTag")
    )

    process.hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag = process.hltDeepCombinedSecondaryVertexBJetTagsPF.clone(
        NNConfig = cms.FileInPath('RecoBTag/Combined/data/DeepCSV_PhaseI.json'),
        src = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag"),
        toAdd = cms.PSet(
            probbb = cms.string('probb')
        )
    )











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

    process.hltPFMuonMergingROIForBTag = process.hltPFMuonMerging.clone(
        TrackProducers = cms.VInputTag("hltIterL3MuonTracks", "hltMergedTracksROIForBTag"),
        selectedTrackQuals = cms.VInputTag("hltIterL3MuonTracks", "hltMergedTracksROIForBTag"),
    )

    process.hltMuonLinksROIForBTag = process.hltMuonLinks.clone(
        InclusiveTrackerTrackCollection = cms.InputTag("hltPFMuonMergingROIForBTag"),
    )

    process.hltMuonsROIForBTag = process.hltMuons.clone(
        # TrackExtractorPSet = cms.PSet(
        #     BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
        #     BeamlineOption = cms.string('BeamSpotFromEvent'),
        #     Chi2Ndof_Max = cms.double(1e+64),
        #     Chi2Prob_Min = cms.double(-1.0),
        #     ComponentName = cms.string('TrackExtractor'),
        #     DR_Max = cms.double(1.0),
        #     DR_Veto = cms.double(0.01),
        #     DepositLabel = cms.untracked.string(''),
        #     Diff_r = cms.double(0.1),
        #     Diff_z = cms.double(0.2),
        #     NHits_Min = cms.uint32(0),
        #     Pt_Min = cms.double(-1.0),
        #     inputTrackCollection = cms.InputTag("hltPFMuonMergingROIForBTag")
        # ),
        inputCollectionLabels = cms.VInputTag("hltPFMuonMergingROIForBTag", "hltMuonLinksROIForBTag", "hltL2Muons"),
    )
    process.hltMuonsROIForBTag.TrackExtractorPSet.inputTrackCollection = cms.InputTag("hltPFMuonMergingROIForBTag")

    process.hltLightPFTracksROIForBTag = process.hltLightPFTracks.clone(
        TkColList = cms.VInputTag("hltPFMuonMergingROIForBTag"),
    )


    process.hltParticleFlowBlockROIForBTag = process.hltParticleFlowBlock.clone(
        elementImporters = cms.VPSet(
            cms.PSet(
                DPtOverPtCuts_byTrackAlgo = cms.vdouble(
                    0.5, 0.5, 0.5, 0.5, 0.5,
                    0.5
                ),
                NHitCuts_byTrackAlgo = cms.vuint32(
                    3, 3, 3, 3, 3,
                    3
                ),
                cleanBadConvertedBrems = cms.bool(False),
                importerName = cms.string('GeneralTracksImporter'),
                muonMaxDPtOPt = cms.double(1.0),
                muonSrc = cms.InputTag("hltMuonsROIForBTag"),
                source = cms.InputTag("hltLightPFTracksROIForBTag"),
                trackQuality = cms.string('highPurity'),
                useIterativeTracking = cms.bool(False),
                vetoEndcap = cms.bool(False)
            ),
            cms.PSet(
                BCtoPFCMap = cms.InputTag(""),
                importerName = cms.string('ECALClusterImporter'),
                source = cms.InputTag("hltParticleFlowClusterECALUnseededROIForBTag")
            ),
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("hltParticleFlowClusterHCAL")
            ),
            cms.PSet(
                importerName = cms.string('GenericClusterImporter'),
                source = cms.InputTag("hltParticleFlowClusterHF")
            )
        ),
    )

    process.hltParticleFlowROIForBTag = process.hltParticleFlow.clone(
        blocks = cms.InputTag("hltParticleFlowBlockROIForBTag"),
        muons = cms.InputTag("hltMuonsROIForBTag"),
        vertexCollection = cms.InputTag("hltPixelVertices"),
    )

    process.hltAK4PFJetsROIForBTag = process.hltAK4PFJets.clone(
        src = cms.InputTag("hltParticleFlowROIForBTag"),
        srcPVs = cms.InputTag("hltPixelVertices"),
    )

    process.hltAK4PFJetsLooseIDROIForBTag = process.hltAK4PFJetsLooseID.clone(
        jetsInput = cms.InputTag("hltAK4PFJetsROIForBTag"),
    )

    process.hltAK4PFJetsTightIDROIForBTag = process.hltAK4PFJetsTightID.clone(
        jetsInput = cms.InputTag("hltAK4PFJetsROIForBTag"),
    )

    process.hltFixedGridRhoFastjetAllROIForBTag = process.hltFixedGridRhoFastjetAll.clone(
        pfCandidatesTag = cms.InputTag("hltParticleFlowROIForBTag")
    )

    process.hltAK4PFFastJetCorrectorROIForBTag = process.hltAK4PFFastJetCorrector.clone(
        srcRho = cms.InputTag("hltFixedGridRhoFastjetAllROIForBTag")
    )

    process.hltAK4PFCorrectorROIForBTag = cms.EDProducer("ChainedJetCorrectorProducer",
        correctors = cms.VInputTag("hltAK4PFFastJetCorrectorROIForBTag", "hltAK4PFRelativeCorrector", "hltAK4PFAbsoluteCorrector", "hltAK4PFResidualCorrector")
    )

    process.hltAK4PFJetsCorrectedROIForBTag = cms.EDProducer("CorrectedPFJetProducer",
        correctors = cms.VInputTag("hltAK4PFCorrectorROIForBTag"),
        src = cms.InputTag("hltAK4PFJetsROIForBTag")
    )

    process.hltAK4PFJetsLooseIDCorrectedROIForBTag = cms.EDProducer("CorrectedPFJetProducer",
        correctors = cms.VInputTag("hltAK4PFCorrectorROIForBTag"),
        src = cms.InputTag("hltAK4PFJetsLooseIDROIForBTag")
    )

    process.hltAK4PFJetsTightIDCorrectedROIForBTag = cms.EDProducer("CorrectedPFJetProducer",
        correctors = cms.VInputTag("hltAK4PFCorrectorROIForBTag"),
        src = cms.InputTag("hltAK4PFJetsTightIDROIForBTag")
    )










    process.HLTParticleFlowSequenceROIForBTag = cms.Sequence(
        process.HLTPreshowerSequence+
        process.hltParticleFlowRecHitECALUnseeded+
        process.hltParticleFlowRecHitHBHE+
        process.hltParticleFlowRecHitHF+
        process.hltParticleFlowRecHitPSUnseeded+
        process.hltParticleFlowClusterECALUncorrectedUnseeded+
        process.hltParticleFlowClusterPSUnseeded+
        # process.hltParticleFlowClusterECALUnseeded+
        process.hltParticleFlowClusterECALUnseededROIForBTag+
        process.hltParticleFlowClusterHBHE+
        process.hltParticleFlowClusterHCAL+
        process.hltParticleFlowClusterHF+

        process.hltLightPFTracksROIForBTag+
        process.hltParticleFlowBlockROIForBTag+
        process.hltParticleFlowROIForBTag
    )

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

    process.HLTIterativeTrackingIter02ROIForBTag = cms.Sequence(
        process.HLTIterativeTrackingIteration0ROIForBTag
    )

    process.HLTTrackReconstructionForPFROIForBTag = cms.Sequence(
        process.HLTDoLocalPixelSequence+
        process.HLTRecopixelvertexingSequence+
        process.HLTDoLocalStripSequence+

        process.HLTIterativeTrackingIter02ROIForBTag+

        process.hltPFMuonMergingROIForBTag+
        process.hltMuonLinksROIForBTag+
        process.hltMuonsROIForBTag

    )


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



    process.HLTAK4PFJetsReconstructionSequenceROIForBTag = cms.Sequence(
        process.HLTL2muonrecoSequence+
        process.HLTL3muonrecoSequence+

        process.HLTTrackReconstructionForPFROIForBTag+
        process.HLTParticleFlowSequenceROIForBTag+

        process.hltAK4PFJetsROIForBTag+
        process.hltAK4PFJetsLooseIDROIForBTag+
        process.hltAK4PFJetsTightIDROIForBTag
    )






    process.HLTAK4PFCorrectorProducersSequenceROIForBTag = cms.Sequence(
        process.hltAK4PFFastJetCorrectorROIForBTag+
        process.hltAK4PFRelativeCorrector+
        process.hltAK4PFAbsoluteCorrector+
        process.hltAK4PFResidualCorrector+
        process.hltAK4PFCorrectorROIForBTag
    )

    process.HLTAK4PFJetsCorrectionSequenceROIForBTag = cms.Sequence(
        process.hltFixedGridRhoFastjetAllROIForBTag+
        process.HLTAK4PFCorrectorProducersSequenceROIForBTag+
        process.hltAK4PFJetsCorrectedROIForBTag+
        process.hltAK4PFJetsLooseIDCorrectedROIForBTag+
        process.hltAK4PFJetsTightIDCorrectedROIForBTag
    )

    process.HLTAK4PFJetsSequenceROIForBTag = cms.Sequence(
        process.HLTPreAK4PFJetsRecoSequence+
        process.HLTAK4PFJetsReconstructionSequenceROIForBTag+
        process.HLTAK4PFJetsCorrectionSequenceROIForBTag
    )







    process.HLTBtagDeepCSVSequencePFROIForBTag = cms.Sequence(

        process.hltVerticesPFROIForBTag+
        process.hltVerticesPFSelectorROIForBTag+
        process.hltVerticesPFFilterROIForBTag+

        process.hltPFJetForBtagSelectorROIForBTag+
        process.hltPFJetForBtagROIForBTag+

        process.hltDeepBLifetimeTagInfosPFROIForBTag+
        process.hltDeepInclusiveVertexFinderPFROIForBTag+
        process.hltDeepInclusiveSecondaryVerticesPFROIForBTag+
        process.hltDeepTrackVertexArbitratorPFROIForBTag+
        process.hltDeepInclusiveMergedVerticesPFROIForBTag+
        process.hltDeepSecondaryVertexTagInfosPFROIForBTag+
        process.hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag+
        process.hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag
    )


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

        process.hltDeepJetDiscriminatorsJetTagsROIForBTag = cms.EDProducer(
            'BTagProbabilityToDiscriminator',
            discriminators = cms.VPSet(
                cms.PSet(
                    name = cms.string('BvsAll'),
                    numerator = cms.VInputTag(
                        cms.InputTag('hltPFDeepFlavourJetTagsROIForBTag', 'probb'),
                        cms.InputTag('hltPFDeepFlavourJetTagsROIForBTag', 'probbb'),
                        cms.InputTag('hltPFDeepFlavourJetTagsROIForBTag', 'problepb'),
                        ),
                    denominator=cms.VInputTag(
                        cms.InputTag('hltPFDeepFlavourJetTagsROIForBTag', 'probb'),
                        cms.InputTag('hltPFDeepFlavourJetTagsROIForBTag', 'probbb'),
                        cms.InputTag('hltPFDeepFlavourJetTagsROIForBTag', 'problepb'),
                        cms.InputTag('hltPFDeepFlavourJetTagsROIForBTag', 'probc'),
                        cms.InputTag('hltPFDeepFlavourJetTagsROIForBTag', 'probuds'),
                        cms.InputTag('hltPFDeepFlavourJetTagsROIForBTag', 'probg'),
                        ),
                ),
            )
        )

        process.hltPrimaryVertexAssociationROIForBTag = primaryVertexAssociation.clone(
            jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
            particles = cms.InputTag("hltParticleFlowROIForBTag"),
            vertices = cms.InputTag("hltVerticesPFFilterROIForBTag"),
        )

        process.hltPFDeepFlavourTagInfosROIForBTag = pfDeepFlavourTagInfos.clone(
            candidates = cms.InputTag("hltParticleFlowROIForBTag"),
            jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
            fallback_puppi_weight = cms.bool(True),
            puppi_value_map = cms.InputTag(""),
            secondary_vertices = cms.InputTag("hltDeepInclusiveSecondaryVerticesPFROIForBTag"),
            shallow_tag_infos = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag"),
            vertex_associator = cms.InputTag("hltPrimaryVertexAssociationROIForBTag","original"),
            vertices = cms.InputTag("hltVerticesPFFilterROIForBTag")
        )
        process.hltPFDeepFlavourJetTagsROIForBTag = pfDeepFlavourJetTags.clone(
            src = cms.InputTag("hltPFDeepFlavourTagInfosROIForBTag")
        )

        process.HLTBtagDeepJetSequencePFROIForBTag = cms.Sequence(
            process.hltVerticesPFROIForBTag+
            process.hltVerticesPFSelectorROIForBTag+
            process.hltVerticesPFFilterROIForBTag+
            process.hltPFJetForBtagSelectorROIForBTag+
            process.hltPFJetForBtagROIForBTag+
            process.hltDeepBLifetimeTagInfosPFROIForBTag+
            process.hltDeepInclusiveVertexFinderPFROIForBTag+
            process.hltDeepInclusiveSecondaryVerticesPFROIForBTag+
            process.hltDeepTrackVertexArbitratorPFROIForBTag+
            process.hltDeepInclusiveMergedVerticesPFROIForBTag+
            process.hltDeepSecondaryVertexTagInfosPFROIForBTag+
            process.hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag+
            process.hltPrimaryVertexAssociationROIForBTag+
            process.hltPFDeepFlavourTagInfosROIForBTag+
            process.hltPFDeepFlavourJetTagsROIForBTag+
            process.hltDeepJetDiscriminatorsJetTagsROIForBTag
        )

        process.hltPreMCPFBTagDeepJet = process.hltPreMCPFBTagDeepCSV.clone()

        process.hltBTagPFDeepJet4p06SingleROIForBTag = process.hltBTagPFDeepCSV4p06Single.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
            MaxTag = cms.double(999999.0),
            MinJets = cms.int32(1),
            MinTag = cms.double(0.25),
            TriggerType = cms.int32(86),
            saveTags = cms.bool(True)
        )

        ############################################################################
        ####                    MC_PFBTagDeepJet_v1                   ###
        ############################################################################
        process.hltPreMCPFBTagDeepJetROIForBTag = process.hltPreMCPFBTagDeepCSV.clone()

        process.MC_PFBTagDeepJet_v1 = cms.Path(
            process.HLTBeginSequence+
            process.hltPreMCPFBTagDeepJetROIForBTag+
            process.HLTAK4PFJetsSequenceROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltBTagPFDeepJet4p06SingleROIForBTag+
            process.HLTEndSequence
        )
    ####         endif           DeepJet?







    ############################################################################
    ####                    MC_PFBTagDeepCSV_v10                   ###
    ############################################################################

    process.hltBTagPFDeepCSV4p06SingleROIForBTag = process.hltBTagPFDeepCSV4p06Single.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
    )

    process.hltPreMCPFBTagDeepCSVROIForBTag = process.hltPreMCPFBTagDeepCSV.clone()

    process.MC_PFBTagDeepCSV_v10 = cms.Path(
        process.HLTBeginSequence+
        process.hltPreMCPFBTagDeepCSVROIForBTag+

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+

        process.hltBTagPFDeepCSV4p06SingleROIForBTag+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v3
    ############################################################################

    process.hltPFCentralJetLooseIDQuad30ROIForBTag = process.hltPFCentralJetLooseIDQuad30.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hlt1PFCentralJetLooseID75ROIForBTag = process.hlt1PFCentralJetLooseID75.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hlt2PFCentralJetLooseID60ROIForBTag = process.hlt2PFCentralJetLooseID60.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hlt3PFCentralJetLooseID45ROIForBTag = process.hlt3PFCentralJetLooseID45.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hlt4PFCentralJetLooseID40ROIForBTag = process.hlt4PFCentralJetLooseID40.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltPFCentralJetLooseIDQuad30forHtROIForBTag = process.hltPFCentralJetLooseIDQuad30forHt.clone(
        HLTObject = cms.InputTag("hltPFCentralJetLooseIDQuad30ROIForBTag"),
    )

    process.hltHtMhtPFCentralJetsLooseIDQuadC30ROIForBTag = process.hltHtMhtPFCentralJetsLooseIDQuadC30.clone(
        jetsLabel = cms.InputTag("hltPFCentralJetLooseIDQuad30forHtROIForBTag"),
        pfCandidatesLabel = cms.InputTag("hltParticleFlowROIForBTag"),
    )

    process.hltPFCentralJetsLooseIDQuad30HT330ROIForBTag = process.hltPFCentralJetsLooseIDQuad30HT330.clone(
        htLabels = cms.VInputTag("hltHtMhtPFCentralJetsLooseIDQuadC30ROIForBTag"),
        mhtLabels = cms.VInputTag("hltHtMhtPFCentralJetsLooseIDQuadC30ROIForBTag"),
    )

    process.hltBTagPFDeepCSV4p5TripleROIForBTag = process.hltBTagPFDeepCSV4p5Triple.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
        MinTag = cms.double(0.24),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFCentralJetLooseIDQuad30ROIForBTag+
        process.hlt1PFCentralJetLooseID75ROIForBTag+
        process.hlt2PFCentralJetLooseID60ROIForBTag+
        process.hlt3PFCentralJetLooseID45ROIForBTag+
        process.hlt4PFCentralJetLooseID40ROIForBTag+
        process.hltPFCentralJetLooseIDQuad30forHtROIForBTag+
        process.hltHtMhtPFCentralJetsLooseIDQuadC30ROIForBTag+
        process.hltPFCentralJetsLooseIDQuad30HT330ROIForBTag+

        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltBTagPFDeepCSV4p5TripleROIForBTag+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet4p5TripleROIForBTag = process.hltBTagPFDeepCSV4p5Triple.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFCentralJetLooseIDQuad30ROIForBTag+
            process.hlt1PFCentralJetLooseID75ROIForBTag+
            process.hlt2PFCentralJetLooseID60ROIForBTag+
            process.hlt3PFCentralJetLooseID45ROIForBTag+
            process.hlt4PFCentralJetLooseID40ROIForBTag+
            process.hltPFCentralJetLooseIDQuad30forHtROIForBTag+
            process.hltHtMhtPFCentralJetsLooseIDQuadC30ROIForBTag+
            process.hltPFCentralJetsLooseIDQuad30HT330ROIForBTag+

            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltBTagPFDeepJet4p5TripleROIForBTag+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5_v8
    ############################################################################

    process.hltPFJetFilterTwo100er3p0ROIForBTag = process.hltPFJetFilterTwo100er3p0.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )
    process.hltPFJetFilterThree60er3p0ROIForBTag = process.hltPFJetFilterThree60er3p0.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )
    process.hltPFJetFilterFive30er3p0ROIForBTag = process.hltPFJetFilterFive30er3p0.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltPFJetsFive30ForHtROIForBTag = process.hltPFJetsFive30ForHt.clone(
        HLTObject = cms.InputTag("hltPFJetFilterFive30er3p0ROIForBTag"),
    )
    process.hltHtMhtPFJetsFive30er3p0ROIForBTag = process.hltHtMhtPFJetsFive30er3p0.clone(
        jetsLabel = cms.InputTag("hltPFJetsFive30ForHtROIForBTag"),
        pfCandidatesLabel = cms.InputTag("hltParticleFlowROIForBTag"),
    )
    process.hltPFFiveJet30HT400ROIForBTag = process.hltPFFiveJet30HT400.clone(
        htLabels = cms.VInputTag("hltHtMhtPFJetsFive30er3p0ROIForBTag"),
        mhtLabels = cms.VInputTag("hltHtMhtPFJetsFive30er3p0ROIForBTag"),
    )

    process.hltBTagPFDeepCSV4p5DoubleROIForBTag = process.hltBTagPFDeepCSV4p5Double.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
    )

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
        process.HLTAK4PFJetsSequenceROIForBTag+

        process.hltPFJetFilterTwo100er3p0ROIForBTag+
        process.hltPFJetFilterThree60er3p0ROIForBTag+
        process.hltPFJetFilterFive30er3p0ROIForBTag+
        process.hltPFJetsFive30ForHtROIForBTag+
        process.hltHtMhtPFJetsFive30er3p0ROIForBTag+
        process.hltPFFiveJet30HT400ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltBTagPFDeepCSV4p5DoubleROIForBTag+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet4p5DoubleROIForBTag = process.hltBTagPFDeepCSV4p5Double.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
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
            process.HLTAK4PFJetsSequenceROIForBTag+

            process.hltPFJetFilterTwo100er3p0ROIForBTag+
            process.hltPFJetFilterThree60er3p0ROIForBTag+
            process.hltPFJetFilterFive30er3p0ROIForBTag+
            process.hltPFJetsFive30ForHtROIForBTag+
            process.hltHtMhtPFJetsFive30er3p0ROIForBTag+
            process.hltPFFiveJet30HT400ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltBTagPFDeepJet4p5DoubleROIForBTag+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepCSV_4p5_v
    ############################################################################

    process.hltPFJetFilterTwo120er3p0ROIForBTag = process.hltPFJetFilterTwo120er3p0.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFJetFilterTwo120er3p0ROIForBTag+
        process.hltPFJetFilterThree60er3p0ROIForBTag+
        process.hltPFJetFilterFive30er3p0ROIForBTag+
        process.hltPFJetsFive30ForHtROIForBTag+
        process.hltHtMhtPFJetsFive30er3p0ROIForBTag+
        process.hltPFFiveJet30HT400ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltBTagPFDeepCSV4p5DoubleROIForBTag+

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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFJetFilterTwo120er3p0ROIForBTag+
            process.hltPFJetFilterThree60er3p0ROIForBTag+
            process.hltPFJetFilterFive30er3p0ROIForBTag+
            process.hltPFJetsFive30ForHtROIForBTag+
            process.hltHtMhtPFJetsFive30er3p0ROIForBTag+
            process.hltPFFiveJet30HT400ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltBTagPFDeepJet4p5DoubleROIForBTag+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94_v
    ############################################################################

    process.hltPFJetFilterSix30er2p5ROIForBTag = process.hltPFJetFilterSix30er2p5.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltPFJetFilterSix32er2p5ROIForBTag = process.hltPFJetFilterSix32er2p5.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltPFJetsSix30ForHtROIForBTag = cms.EDProducer("HLTPFJetCollectionProducer",
        HLTObject = cms.InputTag("hltPFJetFilterSix30er2p5ROIForBTag"),
        TriggerTypes = cms.vint32(86)
    )

    process.hltHtMhtPFJetsSix30er2p5ROIForBTag = process.hltHtMhtPFJetsSix30er2p5.clone(
        jetsLabel = cms.InputTag("hltPFJetsSix30ForHtROIForBTag"),
        pfCandidatesLabel = cms.InputTag("hltParticleFlowROIForBTag"),
    )

    process.hltPFSixJet30HT400ROIForBTag = process.hltPFSixJet30HT400.clone(
        htLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5ROIForBTag"),
        mhtLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5ROIForBTag"),
    )

    process.hltBTagPFDeepCSV2p94DoubleROIForBTag = process.hltBTagPFDeepCSV2p94Double.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFJetFilterSix30er2p5ROIForBTag+
        process.hltPFJetFilterSix32er2p5ROIForBTag+
        process.hltPFJetsSix30ForHtROIForBTag+
        process.hltHtMhtPFJetsSix30er2p5ROIForBTag+
        process.hltPFSixJet30HT400ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltBTagPFDeepCSV2p94DoubleROIForBTag+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet2p94DoubleROIForBTag = process.hltBTagPFDeepCSV2p94Double.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFJetFilterSix30er2p5ROIForBTag+
            process.hltPFJetFilterSix32er2p5ROIForBTag+
            process.hltPFJetsSix30ForHtROIForBTag+
            process.hltHtMhtPFJetsSix30er2p5ROIForBTag+
            process.hltPFSixJet30HT400ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltBTagPFDeepJet2p94DoubleROIForBTag+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_v
    ############################################################################

    process.hltPFJetFilterSix36er2p5ROIForBTag = process.hltPFJetFilterSix36er2p5.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltPFSixJet30HT450ROIForBTag =process.hltPFSixJet30HT450.clone(
        htLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5ROIForBTag"),
        mhtLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5ROIForBTag"),
    )

    process.hltBTagPFDeepCSV1p59SingleROIForBTag = process.hltBTagPFDeepCSV1p59Single.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
    )

    process.HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_v7 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJet+
        process.hltPrePFHT450SixPFJet36PFBTagDeepCSV1p59+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterSixC30+
        process.hltCaloJetsSix30ForHt+
        process.hltHtMhtCaloJetsSixC30+
        process.hltCaloSixJet30HT350+

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFJetFilterSix30er2p5ROIForBTag+
        process.hltPFJetFilterSix36er2p5ROIForBTag+
        process.hltPFJetsSix30ForHtROIForBTag+
        process.hltHtMhtPFJetsSix30er2p5ROIForBTag+
        process.hltPFSixJet30HT450ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltBTagPFDeepCSV1p59SingleROIForBTag+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet1p59SingleROIForBTag = process.hltBTagPFDeepCSV1p59Single.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFJetFilterSix30er2p5ROIForBTag+
            process.hltPFJetFilterSix36er2p5ROIForBTag+
            process.hltPFJetsSix30ForHtROIForBTag+
            process.hltHtMhtPFJetsSix30er2p5ROIForBTag+
            process.hltPFSixJet30HT450ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltBTagPFDeepJet1p59SingleROIForBTag+

            process.HLTEndSequence
        )
    ############################################################################
    #### HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v
    ############################################################################

    process.hltPFQuadJetLooseID15ROIForBTag = process.hltPFQuadJetLooseID15.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltPFTripleJetLooseID75ROIForBTag = process.hltPFTripleJetLooseID75.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltPFDoubleJetLooseID88ROIForBTag = process.hltPFDoubleJetLooseID88.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPFSingleJetLooseID103ROIForBTag = process.hltPFSingleJetLooseID103.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltSelector6PFJetsROIForBTag = process.hltSelector6PFJets.clone(
        src = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag")
    )

    process.hltBTagPFDeepCSV7p68Double6JetsROIForBTag = process.hltBTagPFDeepCSV7p68Double6Jets.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltSelector6PFJetsROIForBTag"),
    )

    process.hltBTagPFDeepCSV1p28Single6JetsROIForBTag = process.hltBTagPFDeepCSV1p28Single6Jets.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltSelector6PFJetsROIForBTag"),
    )

    process.hltVBFPFJetCSVSortedMqq200Detaqq1p5ROIForBTag = process.hltVBFPFJetCSVSortedMqq200Detaqq1p5.clone(
        inputJetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFQuadJetLooseID15ROIForBTag+
        process.hltPFTripleJetLooseID75ROIForBTag+
        process.hltPFDoubleJetLooseID88ROIForBTag+
        process.hltPFSingleJetLooseID103ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltSelector6PFJetsROIForBTag+
        process.hltBTagPFDeepCSV7p68Double6JetsROIForBTag+
        process.hltBTagPFDeepCSV1p28Single6JetsROIForBTag+
        process.hltVBFPFJetCSVSortedMqq200Detaqq1p5ROIForBTag+

        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet7p68Double6JetsROIForBTag = process.hltBTagPFDeepCSV7p68Double6Jets.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
            Jets = cms.InputTag("hltSelector6PFJetsROIForBTag"),
        )

        process.hltBTagPFDeepJet1p28Single6JetsROIForBTag = process.hltBTagPFDeepCSV1p28Single6Jets.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
            Jets = cms.InputTag("hltSelector6PFJetsROIForBTag"),
        )

        process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5ROIForBTag = process.hltVBFPFJetCSVSortedMqq200Detaqq1p5.clone(
            inputJetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
            inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFQuadJetLooseID15ROIForBTag+
            process.hltPFTripleJetLooseID75ROIForBTag+
            process.hltPFDoubleJetLooseID88ROIForBTag+
            process.hltPFSingleJetLooseID103ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltSelector6PFJetsROIForBTag+
            process.hltBTagPFDeepJet7p68Double6JetsROIForBTag+
            process.hltBTagPFDeepJet1p28Single6JetsROIForBTag+
            process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5ROIForBTag+

            process.HLTEndSequence
        )


    ############################################################################
    #### HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2_v
    ############################################################################

    process.hltVBFPFJetCSVSortedMqq460Detaqq3p5ROIForBTag = process.hltVBFPFJetCSVSortedMqq460Detaqq3p5.clone(
        inputJetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFQuadJetLooseID15ROIForBTag+
        process.hltPFTripleJetLooseID75ROIForBTag+
        process.hltPFDoubleJetLooseID88ROIForBTag+
        process.hltPFSingleJetLooseID103ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltSelector6PFJetsROIForBTag+
        process.hltBTagPFDeepCSV1p28Single6JetsROIForBTag+
        process.hltVBFPFJetCSVSortedMqq460Detaqq3p5ROIForBTag+
        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5ROIForBTag = process.hltVBFPFJetCSVSortedMqq460Detaqq3p5.clone(
            inputJetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
            inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFQuadJetLooseID15ROIForBTag+
            process.hltPFTripleJetLooseID75ROIForBTag+
            process.hltPFDoubleJetLooseID88ROIForBTag+
            process.hltPFSingleJetLooseID103ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltSelector6PFJetsROIForBTag+
            process.hltBTagPFDeepJet1p28Single6JetsROIForBTag+
            process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5ROIForBTag+
            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v
    ############################################################################

    process.hltPFTripleJetLooseID76ROIForBTag = process.hltPFTripleJetLooseID76.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltPFSingleJetLooseID105ROIForBTag = process.hltPFSingleJetLooseID105.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFQuadJetLooseID15ROIForBTag+
        process.hltPFTripleJetLooseID76ROIForBTag+
        process.hltPFDoubleJetLooseID88ROIForBTag+
        process.hltPFSingleJetLooseID105ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltSelector6PFJetsROIForBTag+
        process.hltBTagPFDeepCSV7p68Double6JetsROIForBTag+
        process.hltBTagPFDeepCSV1p28Single6JetsROIForBTag+
        process.hltVBFPFJetCSVSortedMqq200Detaqq1p5ROIForBTag+
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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFQuadJetLooseID15ROIForBTag+
            process.hltPFTripleJetLooseID76ROIForBTag+
            process.hltPFDoubleJetLooseID88ROIForBTag+
            process.hltPFSingleJetLooseID105ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltSelector6PFJetsROIForBTag+
            process.hltBTagPFDeepJet7p68Double6JetsROIForBTag+
            process.hltBTagPFDeepJet1p28Single6JetsROIForBTag+
            process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5ROIForBTag+
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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFQuadJetLooseID15ROIForBTag+
        process.hltPFTripleJetLooseID76ROIForBTag+
        process.hltPFDoubleJetLooseID88ROIForBTag+
        process.hltPFSingleJetLooseID105ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltSelector6PFJetsROIForBTag+
        process.hltBTagPFDeepCSV1p28Single6JetsROIForBTag+
        process.hltVBFPFJetCSVSortedMqq460Detaqq3p5ROIForBTag+
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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFQuadJetLooseID15ROIForBTag+
            process.hltPFTripleJetLooseID76ROIForBTag+
            process.hltPFDoubleJetLooseID88ROIForBTag+
            process.hltPFSingleJetLooseID105ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltSelector6PFJetsROIForBTag+
            process.hltBTagPFDeepJet1p28Single6JetsROIForBTag+
            process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5ROIForBTag+
            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v
    ############################################################################

    process.hltPFTripleJetLooseID80ROIForBTag = process.hltPFTripleJetLooseID80.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltPFDoubleJetLooseID90ROIForBTag = process.hltPFDoubleJetLooseID90.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltPFSingleJetLooseID111ROIForBTag = process.hltPFSingleJetLooseID111.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFQuadJetLooseID15ROIForBTag+
        process.hltPFTripleJetLooseID80ROIForBTag+
        process.hltPFDoubleJetLooseID90ROIForBTag+
        process.hltPFSingleJetLooseID111ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltSelector6PFJetsROIForBTag+
        process.hltBTagPFDeepCSV7p68Double6JetsROIForBTag+
        process.hltBTagPFDeepCSV1p28Single6JetsROIForBTag+
        process.hltVBFPFJetCSVSortedMqq200Detaqq1p5ROIForBTag+

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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFQuadJetLooseID15ROIForBTag+
            process.hltPFTripleJetLooseID80ROIForBTag+
            process.hltPFDoubleJetLooseID90ROIForBTag+
            process.hltPFSingleJetLooseID111ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltSelector6PFJetsROIForBTag+
            process.hltBTagPFDeepJet7p68Double6JetsROIForBTag+
            process.hltBTagPFDeepJet1p28Single6JetsROIForBTag+
            process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5ROIForBTag+

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFQuadJetLooseID15ROIForBTag+
        process.hltPFTripleJetLooseID80ROIForBTag+
        process.hltPFDoubleJetLooseID90ROIForBTag+
        process.hltPFSingleJetLooseID111ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltSelector6PFJetsROIForBTag+
        process.hltBTagPFDeepCSV1p28Single6JetsROIForBTag+
        process.hltVBFPFJetCSVSortedMqq460Detaqq3p5ROIForBTag+

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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFQuadJetLooseID15ROIForBTag+
            process.hltPFTripleJetLooseID80ROIForBTag+
            process.hltPFDoubleJetLooseID90ROIForBTag+
            process.hltPFSingleJetLooseID111ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltSelector6PFJetsROIForBTag+
            process.hltBTagPFDeepJet1p28Single6JetsROIForBTag+
            process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5ROIForBTag+

            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v
    ############################################################################

    process.hltPFTripleJetLooseID71ROIForBTag = process.hltPFTripleJetLooseID71.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltPFDoubleJetLooseID83ROIForBTag = process.hltPFDoubleJetLooseID83.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltPFSingleJetLooseID98ROIForBTag = process.hltPFSingleJetLooseID98.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFQuadJetLooseID15ROIForBTag+
        process.hltPFTripleJetLooseID71ROIForBTag+
        process.hltPFDoubleJetLooseID83ROIForBTag+
        process.hltPFSingleJetLooseID98ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltSelector6PFJetsROIForBTag+
        process.hltBTagPFDeepCSV7p68Double6JetsROIForBTag+
        process.hltBTagPFDeepCSV1p28Single6JetsROIForBTag+
        process.hltVBFPFJetCSVSortedMqq200Detaqq1p5ROIForBTag+
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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFQuadJetLooseID15ROIForBTag+
            process.hltPFTripleJetLooseID71ROIForBTag+
            process.hltPFDoubleJetLooseID83ROIForBTag+
            process.hltPFSingleJetLooseID98ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltSelector6PFJetsROIForBTag+
            process.hltBTagPFDeepJet7p68Double6JetsROIForBTag+
            process.hltBTagPFDeepJet1p28Single6JetsROIForBTag+
            process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5ROIForBTag+
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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFQuadJetLooseID15ROIForBTag+
        process.hltPFTripleJetLooseID71ROIForBTag+
        process.hltPFDoubleJetLooseID83ROIForBTag+
        process.hltPFSingleJetLooseID98ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltSelector6PFJetsROIForBTag+
        process.hltBTagPFDeepCSV1p28Single6JetsROIForBTag+
        process.hltVBFPFJetCSVSortedMqq460Detaqq3p5ROIForBTag+
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

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFQuadJetLooseID15ROIForBTag+
            process.hltPFTripleJetLooseID71ROIForBTag+
            process.hltPFDoubleJetLooseID83ROIForBTag+
            process.hltPFSingleJetLooseID98ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltSelector6PFJetsROIForBTag+
            process.hltBTagPFDeepJet1p28Single6JetsROIForBTag+
            process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5ROIForBTag+
            process.HLTEndSequence
        )

    ############################################################################
    #### HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepCSV_1p5_v
    ############################################################################

    process.hltPFJetFilterTwoC30ROIForBTag = process.hltPFJetFilterTwoC30.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltBTagPFDeepCSV1p5SingleROIForBTag = process.hltBTagPFDeepCSV1p5Single.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
    )

    process.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepCSV_1p5_v1 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sMu5EG23IorMu5IsoEG20IorMu7EG23IorMu7IsoEG20IorMuIso7EG23+
        process.hltPreMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZPFDiJet30PFBtagDeepCSV1p5+

        process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegSequence+
        process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegSequence+
        process.hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter+

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFJetFilterTwoC30ROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+
        process.hltBTagPFDeepCSV1p5SingleROIForBTag+
        process.HLTEndSequence
    )
    if addDeepJetPaths:
        process.hltBTagPFDeepJet1p5SingleROIForBTag = process.hltBTagPFDeepCSV1p5Single.clone(
            JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTagsROIForBTag","BvsAll"),
            Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
        )
        process.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepJet_1p5_v1 = cms.Path(
            process.HLTBeginSequence+
            process.hltL1sMu5EG23IorMu5IsoEG20IorMu7EG23IorMu7IsoEG20IorMuIso7EG23+
            process.hltPreMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZPFDiJet30PFBtagDeepCSV1p5+

            process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegSequence+
            process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegSequence+
            process.hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter+

            process.HLTAK4PFJetsSequenceROIForBTag+
            process.hltPFJetFilterTwoC30ROIForBTag+
            process.HLTBtagDeepJetSequencePFROIForBTag+
            process.hltBTagPFDeepJet1p5SingleROIForBTag+
            process.HLTEndSequence
        )



    ############################################################################
    #### HLT_Ele15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5_v
    ############################################################################

    process.hltBTagCaloDeepCSV4p50SingleROIForBTag = process.hltBTagCaloDeepCSV4p50Single.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
        MinTag = cms.double(0.24),
    )

    process.hltPFHTJet30ROIForBTag = process.hltPFHTJet30.clone(
        jetsLabel = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
        pfCandidatesLabel = cms.InputTag("hltParticleFlowROIForBTag"),
    )

    process.hltPFHT450Jet30ROIForBTag = process.hltPFHT450Jet30.clone(
        htLabels = cms.VInputTag("hltPFHTJet30ROIForBTag"),
        mhtLabels = cms.VInputTag("hltPFHTJet30ROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFHTJet30ROIForBTag+
        process.hltPFHT450Jet30ROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets100_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltBTagCaloDeepCSV0p71Single6Jets80ROIForBTag = process.hltBTagCaloDeepCSV0p71Single6Jets80.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
        MinTag = cms.double(0.52),
    )

    process.hltDoublePFJets100Eta2p3ROIForBTag = process.hltDoublePFJets100Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFJets100Eta2p3ROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltBTagCaloDeepCSV0p71Double6Jets80ROIForBTag = process.hltBTagCaloDeepCSV0p71Double6Jets80.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
    )

    process.hltDoublePFJets116Eta2p3ROIForBTag = process.hltDoublePFJets116Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )

    process.hltDoublePFJets116Eta2p3MaxDeta1p6ROIForBTag = process.hltDoublePFJets116Eta2p3MaxDeta1p6.clone(
        inputTag1 = cms.InputTag("hltDoublePFJets116Eta2p3ROIForBTag"),
        inputTag2 = cms.InputTag("hltDoublePFJets116Eta2p3ROIForBTag"),
        originTag1 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
        originTag2 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFJets116Eta2p3ROIForBTag+
        process.hltDoublePFJets116Eta2p3MaxDeta1p6ROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltDoublePFJets128Eta2p3ROIForBTag = process.hltDoublePFJets128Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltDoublePFJets128Eta2p3MaxDeta1p6ROIForBTag = process.hltDoublePFJets128Eta2p3MaxDeta1p6.clone(
        inputTag1 = cms.InputTag("hltDoublePFJets128Eta2p3ROIForBTag"),
        inputTag2 = cms.InputTag("hltDoublePFJets128Eta2p3ROIForBTag"),
        originTag1 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
        originTag2 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFJets128Eta2p3ROIForBTag+
        process.hltDoublePFJets128Eta2p3MaxDeta1p6ROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets200_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltDoublePFJets200Eta2p3ROIForBTag = process.hltDoublePFJets200Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFJets200Eta2p3ROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_DoublePFJets350_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltDoublePFJets350Eta2p3ROIForBTag = process.hltDoublePFJets350Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFJets350Eta2p3ROIForBTag+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_DoublePFJets40_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltBTagCaloDeepCSV0p71Single8Jets30ROIForBTag = process.hltBTagCaloDeepCSV0p71Single8Jets30.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
    )

    process.hltDoublePFJets40Eta2p3ROIForBTag = process.hltDoublePFJets40Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.HLT_DoublePFJets40_CaloBTagDeepCSV_p71_v2 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1DoubleJet40er3p0+
        process.hltPreDoublePFJets40CaloBTagDeepCSVp71+

        process.HLTAK4CaloJetsSequence+
        process.hltDoubleCaloBJets30eta2p3+
        process.HLTBtagDeepCSVSequenceL3ROIForBTag+
        process.hltBTagCaloDeepCSV0p71Single8Jets30ROIForBTag+

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFJets40Eta2p3ROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets100_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltDoublePFBJets100Eta2p3ROIForBTag = process.hltDoublePFBJets100Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltBSoftMuonGetJetsFromDiJet100PFROIForBTag = process.hltBSoftMuonGetJetsFromDiJet100PF.clone(
        HLTObject = cms.InputTag("hltDoublePFBJets100Eta2p3ROIForBTag"),
    )

    process.hltSelector4JetsDiJet100PFROIForBTag = process.hltSelector4JetsDiJet100PF.clone(
        src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet100PFROIForBTag")
    )

    process.hltBSoftMuonDiJet100PFMu12L3JetsROIForBTag = process.hltBSoftMuonDiJet100PFMu12L3Jets.clone(
        src = cms.InputTag("hltSelector4JetsDiJet100PFROIForBTag")
    )

    process.hltBSoftMuonDiJet100PFMu12L3TagInfosROIForBTag = process.hltBSoftMuonDiJet100PFMu12L3TagInfos.clone(
        jets = cms.InputTag("hltBSoftMuonDiJet100PFMu12L3JetsROIForBTag"),
    )

    process.hltBSoftMuonDiJet100PFMu12L3BJetTagsByDRROIForBTag = process.hltBSoftMuonDiJet100PFMu12L3BJetTagsByDR.clone(
        tagInfos = cms.VInputTag("hltBSoftMuonDiJet100PFMu12L3TagInfosROIForBTag")
    )

    process.HLTBTagMuDiJet100PFMu12SequenceL3ROIForBTag = cms.Sequence(
        process.hltBSoftMuonGetJetsFromDiJet100PFROIForBTag+
        process.hltSelector4JetsDiJet100PFROIForBTag+
        process.hltBSoftMuonDiJet100PFMu12L3JetsROIForBTag+
        process.hltBSoftMuonMu12L3+
        process.hltBSoftMuonDiJet100PFMu12L3TagInfosROIForBTag+
        process.hltBSoftMuonDiJet100PFMu12L3BJetTagsByDRROIForBTag
    )

    process.hltBSoftMuonDiJet100Mu12L3FilterByDRROIForBTag = process.hltBSoftMuonDiJet100Mu12L3FilterByDR.clone(
        JetTags = cms.InputTag("hltBSoftMuonDiJet100PFMu12L3BJetTagsByDRROIForBTag"),
        Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet100PFROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFBJets100Eta2p3ROIForBTag+

        process.HLTBTagMuDiJet100PFMu12SequenceL3ROIForBTag+
        process.hltBSoftMuonDiJet100Mu12L3FilterByDRROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets200_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltDoublePFBJets200Eta2p3ROIForBTag = process.hltDoublePFBJets200Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltBSoftMuonGetJetsFromDiJet200PFROIForBTag = process.hltBSoftMuonGetJetsFromDiJet200PF.clone(
        HLTObject = cms.InputTag("hltDoublePFBJets200Eta2p3ROIForBTag"),
    )

    process.hltSelector4JetsDiJet200PFROIForBTag = process.hltSelector4JetsDiJet200PF.clone(
        src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet200PFROIForBTag")
    )

    process.hltBSoftMuonDiJet200PFMu12L3JetsROIForBTag = process.hltBSoftMuonDiJet200PFMu12L3Jets.clone(
        src = cms.InputTag("hltSelector4JetsDiJet200PFROIForBTag")
    )

    process.hltBSoftMuonDiJet200PFMu12L3TagInfosROIForBTag = process.hltBSoftMuonDiJet200PFMu12L3TagInfos.clone(
        jets = cms.InputTag("hltBSoftMuonDiJet200PFMu12L3JetsROIForBTag"),
    )

    process.hltBSoftMuonDiJet200PFMu12L3BJetTagsByDRROIForBTag = process.hltBSoftMuonDiJet200PFMu12L3BJetTagsByDR.clone(
        tagInfos = cms.VInputTag("hltBSoftMuonDiJet200PFMu12L3TagInfosROIForBTag")
    )

    process.HLTBTagMuDiJet200PFMu12SequenceL3ROIForBTag = cms.Sequence(
        process.hltBSoftMuonGetJetsFromDiJet200PFROIForBTag+
        process.hltSelector4JetsDiJet200PFROIForBTag+
        process.hltBSoftMuonDiJet200PFMu12L3JetsROIForBTag+
        process.hltBSoftMuonMu12L3+
        process.hltBSoftMuonDiJet200PFMu12L3TagInfosROIForBTag+
        process.hltBSoftMuonDiJet200PFMu12L3BJetTagsByDRROIForBTag
    )

    process.hltBSoftMuonDiJet200Mu12L3FilterByDRROIForBTag = process.hltBSoftMuonDiJet200Mu12L3FilterByDR.clone(
        JetTags = cms.InputTag("hltBSoftMuonDiJet200PFMu12L3BJetTagsByDRROIForBTag"),
        Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet200PFROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFBJets200Eta2p3ROIForBTag+
        process.HLTBTagMuDiJet200PFMu12SequenceL3ROIForBTag+
        process.hltBSoftMuonDiJet200Mu12L3FilterByDRROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets350_CaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltDoublePFBJets350Eta2p3ROIForBTag = process.hltDoublePFBJets350Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltBSoftMuonGetJetsFromDiJet350PFROIForBTag = process.hltBSoftMuonGetJetsFromDiJet350PF.clone(
        HLTObject = cms.InputTag("hltDoublePFBJets350Eta2p3ROIForBTag"),
    )

    process.hltSelector4JetsDiJet350PFROIForBTag = process.hltSelector4JetsDiJet350PF.clone(
        src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet350PFROIForBTag")
    )

    process.hltBSoftMuonDiJet350PFMu12L3JetsROIForBTag = process.hltBSoftMuonDiJet350PFMu12L3Jets.clone(
        src = cms.InputTag("hltSelector4JetsDiJet350PFROIForBTag")
    )

    process.hltBSoftMuonDiJet350PFMu12L3TagInfosROIForBTag = process.hltBSoftMuonDiJet350PFMu12L3TagInfos.clone(
        jets = cms.InputTag("hltBSoftMuonDiJet350PFMu12L3JetsROIForBTag"),
    )

    process.hltBSoftMuonDiJet350PFMu12L3BJetTagsByDRROIForBTag = process.hltBSoftMuonDiJet350PFMu12L3BJetTagsByDR.clone(
        tagInfos = cms.VInputTag("hltBSoftMuonDiJet350PFMu12L3TagInfosROIForBTag")
    )

    process.hltBSoftMuonDiJet350Mu12L3FilterByDRROIForBTag = process.hltBSoftMuonDiJet350Mu12L3FilterByDR.clone(
        JetTags = cms.InputTag("hltBSoftMuonDiJet350PFMu12L3BJetTagsByDRROIForBTag"),
        Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet350PFROIForBTag"),
    )

    process.HLTBTagMuDiJet350PFMu12SequenceL3ROIForBTag = cms.Sequence(
        process.hltBSoftMuonGetJetsFromDiJet350PFROIForBTag+
        process.hltSelector4JetsDiJet350PFROIForBTag+
        process.hltBSoftMuonDiJet350PFMu12L3JetsROIForBTag+
        process.hltBSoftMuonMu12L3+
        process.hltBSoftMuonDiJet350PFMu12L3TagInfosROIForBTag+
        process.hltBSoftMuonDiJet350PFMu12L3BJetTagsByDRROIForBTag
    )

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
        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFBJets350Eta2p3ROIForBTag+
        process.HLTBTagMuDiJet350PFMu12SequenceL3ROIForBTag+
        process.hltBSoftMuonDiJet350Mu12L3FilterByDRROIForBTag+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltBTagCaloDeepCSV0p71Double8Jets30ROIForBTag = process.hltBTagCaloDeepCSV0p71Double8Jets30.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsCaloROIForBTag","probb"),
    )

    process.hltDoublePFBJets40Eta2p3ROIForBTag = process.hltDoublePFBJets40Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltDoublePFJets40Eta2p3MaxDeta1p6ROIForBTag = process.hltDoublePFJets40Eta2p3MaxDeta1p6.clone(
        inputTag1 = cms.InputTag("hltDoublePFBJets40Eta2p3ROIForBTag"),
        inputTag2 = cms.InputTag("hltDoublePFBJets40Eta2p3ROIForBTag"),
        originTag1 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
        originTag2 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltBSoftMuonGetJetsFromDiJet40PFROIForBTag = process.hltBSoftMuonGetJetsFromDiJet40PF.clone(
        HLTObject = cms.InputTag("hltDoublePFBJets40Eta2p3ROIForBTag"),
    )

    process.hltSelector4JetsDiJet40PFROIForBTag = process.hltSelector4JetsDiJet40PF.clone(
        src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet40PFROIForBTag")
    )

    process.hltBSoftMuonDiJet40PFMu12L3JetsROIForBTag = process.hltBSoftMuonDiJet40PFMu12L3Jets.clone(
        src = cms.InputTag("hltSelector4JetsDiJet40PFROIForBTag")
    )

    process.hltBSoftMuonDiJet40PFMu12L3TagInfosROIForBTag = process.hltBSoftMuonDiJet40PFMu12L3TagInfos.clone(
        jets = cms.InputTag("hltBSoftMuonDiJet40PFMu12L3JetsROIForBTag"),
    )

    process.hltBSoftMuonDiJet40PFMu12L3BJetTagsByDRROIForBTag = process.hltBSoftMuonDiJet40PFMu12L3BJetTagsByDR.clone(
        tagInfos = cms.VInputTag("hltBSoftMuonDiJet40PFMu12L3TagInfosROIForBTag")
    )

    process.HLTBTagMuDiJet40PFMu12SequenceL3ROIForBTag = cms.Sequence(
        process.hltBSoftMuonGetJetsFromDiJet40PFROIForBTag+
        process.hltSelector4JetsDiJet40PFROIForBTag+
        process.hltBSoftMuonDiJet40PFMu12L3JetsROIForBTag+
        process.hltBSoftMuonMu12L3+
        process.hltBSoftMuonDiJet40PFMu12L3TagInfosROIForBTag+
        process.hltBSoftMuonDiJet40PFMu12L3BJetTagsByDRROIForBTag
    )

    process.hltBSoftMuonDiJet40Mu12L3FilterByDRROIForBTag = process.hltBSoftMuonDiJet40Mu12L3FilterByDR.clone(
        JetTags = cms.InputTag("hltBSoftMuonDiJet40PFMu12L3BJetTagsByDRROIForBTag"),
        Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet40PFROIForBTag"),
    )

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

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFBJets40Eta2p3ROIForBTag+
        process.hltDoublePFJets40Eta2p3MaxDeta1p6ROIForBTag+
        process.HLTBTagMuDiJet40PFMu12SequenceL3ROIForBTag+
        process.hltBSoftMuonDiJet40Mu12L3FilterByDRROIForBTag+
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
        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFBJets40Eta2p3ROIForBTag+
        process.HLTBTagMuDiJet40PFMu12SequenceL3ROIForBTag+
        process.hltBSoftMuonDiJet40Mu12L3FilterByDRROIForBTag+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltDoublePFBJets54Eta2p3ROIForBTag = process.hltDoublePFBJets54Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltDoublePFJets54Eta2p3MaxDeta1p6ROIForBTag = process.hltDoublePFJets54Eta2p3MaxDeta1p6.clone(
        inputTag1 = cms.InputTag("hltDoublePFBJets54Eta2p3ROIForBTag"),
        inputTag2 = cms.InputTag("hltDoublePFBJets54Eta2p3ROIForBTag"),
        originTag1 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
        originTag2 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltBSoftMuonGetJetsFromDiJet54PFROIForBTag = process.hltBSoftMuonGetJetsFromDiJet54PF.clone(
        HLTObject = cms.InputTag("hltDoublePFBJets54Eta2p3"),
    )

    process.hltSelector4JetsDiJet54PFROIForBTag = process.hltSelector4JetsDiJet54PF.clone(
        src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet54PFROIForBTag")
    )

    process.hltBSoftMuonDiJet54PFMu12L3JetsROIForBTag = process.hltBSoftMuonDiJet54PFMu12L3Jets.clone(
        src = cms.InputTag("hltSelector4JetsDiJet54PFROIForBTag")
    )

    process.hltBSoftMuonDiJet54PFMu12L3TagInfosROIForBTag = process.hltBSoftMuonDiJet54PFMu12L3TagInfos.clone(
        jets = cms.InputTag("hltBSoftMuonDiJet54PFMu12L3JetsROIForBTag"),
    )

    process.hltBSoftMuonDiJet54PFMu12L3BJetTagsByDRROIForBTag = process.hltBSoftMuonDiJet54PFMu12L3BJetTagsByDR.clone(
        tagInfos = cms.VInputTag("hltBSoftMuonDiJet54PFMu12L3TagInfosROIForBTag")
    )

    process.HLTBTagMuDiJet54PFMu12SequenceL3ROIForBTag = cms.Sequence(
        process.hltBSoftMuonGetJetsFromDiJet54PFROIForBTag+
        process.hltSelector4JetsDiJet54PFROIForBTag+
        process.hltBSoftMuonDiJet54PFMu12L3JetsROIForBTag+
        process.hltBSoftMuonMu12L3+
        process.hltBSoftMuonDiJet54PFMu12L3TagInfosROIForBTag+
        process.hltBSoftMuonDiJet54PFMu12L3BJetTagsByDRROIForBTag
    )

    process.hltBSoftMuonDiJet54Mu12L3FilterByDRROIForBTag = process.hltBSoftMuonDiJet54Mu12L3FilterByDR.clone(
        JetTags = cms.InputTag("hltBSoftMuonDiJet54PFMu12L3BJetTagsByDRROIForBTag"),
        Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet54PFROIForBTag"),
    )

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
        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFBJets54Eta2p3ROIForBTag+
        process.hltDoublePFJets54Eta2p3MaxDeta1p6ROIForBTag+
        process.HLTBTagMuDiJet54PFMu12SequenceL3ROIForBTag+
        process.hltBSoftMuonDiJet54Mu12L3FilterByDR+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v
    ############################################################################

    process.hltDoublePFBJets62Eta2p3ROIForBTag = process.hltDoublePFBJets62Eta2p3.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )

    process.hltDoublePFJets62Eta2p3MaxDeta1p6ROIForBTag = process.hltDoublePFJets62Eta2p3MaxDeta1p6.clone(
        inputTag1 = cms.InputTag("hltDoublePFBJets62Eta2p3ROIForBTag"),
        inputTag2 = cms.InputTag("hltDoublePFBJets62Eta2p3ROIForBTag"),
        originTag1 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
        originTag2 = cms.VInputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.hltBSoftMuonGetJetsFromDiJet62PFROIForBTag = process.hltBSoftMuonGetJetsFromDiJet62PF.clone(
        HLTObject = cms.InputTag("hltDoublePFBJets62Eta2p3ROIForBTag"),
    )

    process.hltSelector4JetsDiJet62PFROIForBTag = process.hltSelector4JetsDiJet62PF.clone(
        src = cms.InputTag("hltBSoftMuonGetJetsFromDiJet62PFROIForBTag")
    )

    process.hltBSoftMuonDiJet62PFMu12L3JetsROIForBTag = process.hltBSoftMuonDiJet62PFMu12L3Jets.clone(
        src = cms.InputTag("hltSelector4JetsDiJet62PFROIForBTag")
    )

    process.hltBSoftMuonDiJet62PFMu12L3TagInfosROIForBTag = process.hltBSoftMuonDiJet62PFMu12L3TagInfos.clone(
        jets = cms.InputTag("hltBSoftMuonDiJet62PFMu12L3JetsROIForBTag"),
    )

    process.hltBSoftMuonDiJet62PFMu12L3BJetTagsByDRROIForBTag = process.hltBSoftMuonDiJet62PFMu12L3BJetTagsByDR.clone(
        tagInfos = cms.VInputTag("hltBSoftMuonDiJet62PFMu12L3TagInfosROIForBTag")
    )

    process.HLTBTagMuDiJet62PFMu12SequenceL3ROIForBTag = cms.Sequence(
        process.hltBSoftMuonGetJetsFromDiJet62PFROIForBTag+
        process.hltSelector4JetsDiJet62PFROIForBTag+
        process.hltBSoftMuonDiJet62PFMu12L3JetsROIForBTag+
        process.hltBSoftMuonMu12L3+
        process.hltBSoftMuonDiJet62PFMu12L3TagInfosROIForBTag+
        process.hltBSoftMuonDiJet62PFMu12L3BJetTagsByDR
    )


    process.hltBSoftMuonDiJet62Mu12L3FilterByDRROIForBTag = process.hltBSoftMuonDiJet62Mu12L3FilterByDR.clone(
        JetTags = cms.InputTag("hltBSoftMuonDiJet62PFMu12L3BJetTagsByDRROIForBTag"),
        Jets = cms.InputTag("hltBSoftMuonGetJetsFromDiJet62PFROIForBTag"),
    )

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
        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFBJets62Eta2p3ROIForBTag+
        process.hltDoublePFJets62Eta2p3MaxDeta1p6ROIForBTag+
        process.HLTBTagMuDiJet62PFMu12SequenceL3ROIForBTag+
        process.hltBSoftMuonDiJet62Mu12L3FilterByDRROIForBTag+
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
        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFHTJet30ROIForBTag+
        process.hltPFHT450Jet30ROIForBTag+
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
        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltDoublePFJets40Eta2p3ROIForBTag+
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
        process.HLTAK4PFJetsSequenceROIForBTag+
        process.hltPFHTJet30ROIForBTag+
        process.hltPFHT450Jet30ROIForBTag+
        process.HLTEndSequence
    )


    return process
