import FWCore.ParameterSet.Config as cms

def customiseRun3BTagRegionalTracks_Replacement(process):




    # process.hltParticleFlowClusterECALForMuonsMF.skipPS = cms.bool(True)
    # process.hltParticleFlowClusterECALForMuonsMFScoutingNoVtx.skipPS = cms.bool(True)
    # process.hltParticleFlowClusterECALL1Seeded.skipPS = cms.bool(True)
    # process.hltParticleFlowClusterECALUnseeded.skipPS = cms.bool(True)



    process.hltBTaggingRegion = cms.EDProducer("CandidateSeededTrackingRegionsEDProducer",
    RegionPSet = cms.PSet(
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        deltaEta = cms.double(0.5),
        deltaPhi = cms.double(0.5),
        input = cms.InputTag("hltSelectorCentralJets20L1FastJeta"),
        # maxNRegions = cms.int32(100),
        maxNRegions = cms.int32(8),
        # maxNRegions = cms.int32(6),
        maxNVertices = cms.int32(2),
        measurementTrackerName = cms.InputTag(""),
        mode = cms.string('VerticesFixed'),
        nSigmaZBeamSpot = cms.double(3.0),
        nSigmaZVertex = cms.double(0.0),
        originRadius = cms.double(0.3),
        precise = cms.bool(True),
        ptMin = cms.double(0.3),
        searchOpt = cms.bool(True),
        vertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
        whereToUseMeasurementTracker = cms.string('Never'),
        zErrorBeamSpot = cms.double(0.5),
        zErrorVetex = cms.double(0.3)
        )
    )

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
        ptMin = cms.double(0.3),
        # ptMin = cms.double(0.8),
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

    process.hltPixelTracksForBTag = cms.EDProducer('TrackSelectorByRegion',
          # tracks = cms.InputTag('hltPixelTracks'),
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

    process.hltPFJetForBtagSelectorROIForBTag = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.6),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(1),
        MinPt = cms.double(30.0),
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(86)
    )
    process.hltPFJetForBtagROIForBTag = cms.EDProducer("HLTPFJetCollectionProducer",
        HLTObject = cms.InputTag("hltPFJetForBtagSelectorROIForBTag"),
        TriggerTypes = cms.vint32(86)
    )

    process.hltDeepBLifetimeTagInfosPFROIForBTag = cms.EDProducer("CandIPProducer",
        candidates = cms.InputTag("hltParticleFlowROIForBTag"),
        computeGhostTrack = cms.bool(True),
        computeProbabilities = cms.bool(True),
        ghostTrackPriorDeltaR = cms.double(0.03),
        jetDirectionUsingGhostTrack = cms.bool(False),
        jetDirectionUsingTracks = cms.bool(False),
        # jets = cms.InputTag("hltPFJetForBtag"),
        jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
        maxDeltaR = cms.double(0.4),
        maximumChiSquared = cms.double(5.0),
        maximumLongitudinalImpactParameter = cms.double(17.0),
        maximumTransverseImpactParameter = cms.double(0.2),
        minimumNumberOfHits = cms.int32(3),
        minimumNumberOfPixelHits = cms.int32(2),
        minimumTransverseMomentum = cms.double(1.0),
        primaryVertex = cms.InputTag("hltVerticesPFFilterROIForBTag"),
        useTrackQuality = cms.bool(False)
    )


    process.hltDeepInclusiveVertexFinderPFROIForBTag = cms.EDProducer("InclusiveCandidateVertexFinder",
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        clusterizer = cms.PSet(
            clusterMaxDistance = cms.double(0.05),
            clusterMaxSignificance = cms.double(4.5),
            clusterMinAngleCosine = cms.double(0.5),
            distanceRatio = cms.double(20.0),
            seedMax3DIPSignificance = cms.double(9999.0),
            seedMax3DIPValue = cms.double(9999.0),
            seedMin3DIPSignificance = cms.double(1.2),
            seedMin3DIPValue = cms.double(0.005)
        ),
        fitterRatio = cms.double(0.25),
        fitterSigmacut = cms.double(3.0),
        fitterTini = cms.double(256.0),
        maxNTracks = cms.uint32(30),
        maximumLongitudinalImpactParameter = cms.double(0.3),
        maximumTimeSignificance = cms.double(3.0),
        minHits = cms.uint32(8),
        minPt = cms.double(0.8),
        primaryVertices = cms.InputTag("hltVerticesPFFilterROIForBTag"),
        tracks = cms.InputTag("hltParticleFlowROIForBTag"),
        useDirectVertexFitter = cms.bool(True),
        useVertexReco = cms.bool(True),
        vertexMinAngleCosine = cms.double(0.95),
        vertexMinDLen2DSig = cms.double(2.5),
        vertexMinDLenSig = cms.double(0.5),
        vertexReco = cms.PSet(
            finder = cms.string('avr'),
            primcut = cms.double(1.0),
            seccut = cms.double(3.0),
            smoothing = cms.bool(True)
        )
    )

    process.hltDeepInclusiveSecondaryVerticesPFROIForBTag = cms.EDProducer("CandidateVertexMerger",
        maxFraction = cms.double(0.7),
        minSignificance = cms.double(2.0),
        secondaryVertices = cms.InputTag("hltDeepInclusiveVertexFinderPFROIForBTag")
    )


    process.hltDeepTrackVertexArbitratorPFROIForBTag = cms.EDProducer("CandidateVertexArbitrator",
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        dLenFraction = cms.double(0.333),
        dRCut = cms.double(0.4),
        distCut = cms.double(0.04),
        fitterRatio = cms.double(0.25),
        fitterSigmacut = cms.double(3.0),
        fitterTini = cms.double(256.0),
        maxTimeSignificance = cms.double(3.5),
        primaryVertices = cms.InputTag("hltVerticesPFFilterROIForBTag"),
        secondaryVertices = cms.InputTag("hltDeepInclusiveSecondaryVerticesPFROIForBTag"),
        sigCut = cms.double(5.0),
        trackMinLayers = cms.int32(4),
        trackMinPixels = cms.int32(1),
        trackMinPt = cms.double(0.4),
        tracks = cms.InputTag("hltParticleFlowROIForBTag")
    )

    process.hltDeepInclusiveMergedVerticesPFROIForBTag = cms.EDProducer("CandidateVertexMerger",
        maxFraction = cms.double(0.2),
        minSignificance = cms.double(10.0),
        secondaryVertices = cms.InputTag("hltDeepTrackVertexArbitratorPFROIForBTag")
    )

    process.hltDeepSecondaryVertexTagInfosPFROIForBTag = cms.EDProducer("CandSecondaryVertexProducer",
        beamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
        constraint = cms.string('BeamSpot'),
        extSVCollection = cms.InputTag("hltDeepInclusiveMergedVerticesPFROIForBTag"),
        extSVDeltaRToJet = cms.double(0.3),
        minimumTrackWeight = cms.double(0.5),
        trackIPTagInfos = cms.InputTag("hltDeepBLifetimeTagInfosPFROIForBTag"),
        trackSelection = cms.PSet(
            a_dR = cms.double(-0.001053),
            a_pT = cms.double(0.005263),
            b_dR = cms.double(0.6263),
            b_pT = cms.double(0.3684),
            jetDeltaRMax = cms.double(0.3),
            maxDecayLen = cms.double(99999.9),
            maxDistToAxis = cms.double(0.2),
            max_pT = cms.double(500.0),
            max_pT_dRcut = cms.double(0.1),
            max_pT_trackPTcut = cms.double(3.0),
            min_pT = cms.double(120.0),
            min_pT_dRcut = cms.double(0.5),
            normChi2Max = cms.double(99999.9),
            pixelHitsMin = cms.uint32(2),
            ptMin = cms.double(1.0),
            qualityClass = cms.string('any'),
            sip2dSigMax = cms.double(99999.9),
            sip2dSigMin = cms.double(-99999.9),
            sip2dValMax = cms.double(99999.9),
            sip2dValMin = cms.double(-99999.9),
            sip3dSigMax = cms.double(99999.9),
            sip3dSigMin = cms.double(-99999.9),
            sip3dValMax = cms.double(99999.9),
            sip3dValMin = cms.double(-99999.9),
            totalHitsMin = cms.uint32(3),
            useVariableJTA = cms.bool(False)
        ),
        trackSort = cms.string('sip3dSig'),
        useExternalSV = cms.bool(True),
        usePVError = cms.bool(True),
        vertexCuts = cms.PSet(
            distSig2dMax = cms.double(99999.9),
            distSig2dMin = cms.double(2.0),
            distSig3dMax = cms.double(99999.9),
            distSig3dMin = cms.double(-99999.9),
            distVal2dMax = cms.double(2.5),
            distVal2dMin = cms.double(0.01),
            distVal3dMax = cms.double(99999.9),
            distVal3dMin = cms.double(-99999.9),
            fracPV = cms.double(0.79),
            massMax = cms.double(6.5),
            maxDeltaRToJetAxis = cms.double(0.4),
            minimumTrackWeight = cms.double(0.5),
            multiplicityMin = cms.uint32(2),
            useTrackWeights = cms.bool(True),
            v0Filter = cms.PSet(
                k0sMassWindow = cms.double(0.05)
            )
        ),
        vertexReco = cms.PSet(
            finder = cms.string('avr'),
            minweight = cms.double(0.5),
            primcut = cms.double(1.8),
            seccut = cms.double(6.0),
            smoothing = cms.bool(False),
            weightthreshold = cms.double(0.001)
        ),
        vertexSelection = cms.PSet(
            sortCriterium = cms.string('dist3dError')
        )
    )



    process.hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag = cms.EDProducer("DeepNNTagInfoProducer",
        computer = cms.PSet(
            SoftLeptonFlip = cms.bool(False),
            charmCut = cms.double(1.5),
            correctVertexMass = cms.bool(True),
            minimumTrackWeight = cms.double(0.5),
            pseudoMultiplicityMin = cms.uint32(2),
            pseudoVertexV0Filter = cms.PSet(
                k0sMassWindow = cms.double(0.05)
            ),
            trackFlip = cms.bool(False),
            trackMultiplicityMin = cms.uint32(2),
            trackPairV0Filter = cms.PSet(
                k0sMassWindow = cms.double(0.03)
            ),
            trackPseudoSelection = cms.PSet(
                a_dR = cms.double(-0.001053),
                a_pT = cms.double(0.005263),
                b_dR = cms.double(0.6263),
                b_pT = cms.double(0.3684),
                jetDeltaRMax = cms.double(0.3),
                maxDecayLen = cms.double(5.0),
                maxDistToAxis = cms.double(0.07),
                max_pT = cms.double(500.0),
                max_pT_dRcut = cms.double(0.1),
                max_pT_trackPTcut = cms.double(3.0),
                min_pT = cms.double(120.0),
                min_pT_dRcut = cms.double(0.5),
                normChi2Max = cms.double(99999.9),
                pixelHitsMin = cms.uint32(0),
                ptMin = cms.double(0.0),
                qualityClass = cms.string('any'),
                sip2dSigMax = cms.double(99999.9),
                sip2dSigMin = cms.double(2.0),
                sip2dValMax = cms.double(99999.9),
                sip2dValMin = cms.double(-99999.9),
                sip3dSigMax = cms.double(99999.9),
                sip3dSigMin = cms.double(-99999.9),
                sip3dValMax = cms.double(99999.9),
                sip3dValMin = cms.double(-99999.9),
                totalHitsMin = cms.uint32(3),
                useVariableJTA = cms.bool(False)
            ),
            trackSelection = cms.PSet(
                a_dR = cms.double(-0.001053),
                a_pT = cms.double(0.005263),
                b_dR = cms.double(0.6263),
                b_pT = cms.double(0.3684),
                jetDeltaRMax = cms.double(0.3),
                maxDecayLen = cms.double(5.0),
                maxDistToAxis = cms.double(0.07),
                max_pT = cms.double(500.0),
                max_pT_dRcut = cms.double(0.1),
                max_pT_trackPTcut = cms.double(3.0),
                min_pT = cms.double(120.0),
                min_pT_dRcut = cms.double(0.5),
                normChi2Max = cms.double(99999.9),
                pixelHitsMin = cms.uint32(2),
                ptMin = cms.double(0.0),
                qualityClass = cms.string('any'),
                sip2dSigMax = cms.double(99999.9),
                sip2dSigMin = cms.double(-99999.9),
                sip2dValMax = cms.double(99999.9),
                sip2dValMin = cms.double(-99999.9),
                sip3dSigMax = cms.double(99999.9),
                sip3dSigMin = cms.double(-99999.9),
                sip3dValMax = cms.double(99999.9),
                sip3dValMin = cms.double(-99999.9),
                totalHitsMin = cms.uint32(3),
                useVariableJTA = cms.bool(False)
            ),
            trackSort = cms.string('sip2dSig'),
            useTrackWeights = cms.bool(True),
            vertexFlip = cms.bool(False)
        ),
        svTagInfos = cms.InputTag("hltDeepSecondaryVertexTagInfosPFROIForBTag")
    )

    # process.hltDeepCombinedSecondaryVertexBJetTagsPF = cms.EDProducer("DeepFlavourJetTagsProducer",
    process.hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag = cms.EDProducer("DeepFlavourJetTagsProducer",
        NNConfig = cms.FileInPath('RecoBTag/Combined/data/DeepCSV_PhaseI.json'),
        checkSVForDefaults = cms.bool(True),
        meanPadding = cms.bool(True),
        # src = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsInfos"),
        src = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag"),
        toAdd = cms.PSet(
            probbb = cms.string('probb')
        )
    )











    process.hltIter0PFLowPixelSeedsFromPixelTracksROIForBTag = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
        InputCollection = cms.InputTag("hltPixelTracksForBTag"),
        InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices"),
        SeedCreatorPSet = cms.PSet(
            refToPSet_ = cms.string('HLTSeedFromProtoTracks')
        ),
        TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
        includeFourthHit = cms.bool(True),
        originHalfLength = cms.double(0.3),
        originRadius = cms.double(0.1),
        useEventsWithNoVertex = cms.bool(True),
        usePV = cms.bool(False),
        useProtoTrackKinematics = cms.bool(False)
    )

    process.hltIter0PFlowCkfTrackCandidatesROIForBTag = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TrajectoryBuilder = cms.string(''),
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('HLTIter0GroupedCkfTrajectoryBuilderIT')
        ),
        TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(4),
            propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
        ),
        cleanTrajectoryAfterInOut = cms.bool(False),
        doSeedingRegionRebuilding = cms.bool(False),
        maxNSeeds = cms.uint32(100000),
        maxSeedsBeforeCleaning = cms.uint32(1000),
        reverseTrajectories = cms.bool(False),
        src = cms.InputTag("hltIter0PFLowPixelSeedsFromPixelTracksROIForBTag"),
        useHitsSplitting = cms.bool(False)
    )

    process.hltIter0PFlowCtfWithMaterialTracksROIForBTag = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('hltIter0'),
        Fitter = cms.string('hltESPFittingSmootherIT'),
        GeometricInnerState = cms.bool(True),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
        NavigationSchool = cms.string(''),
        Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TTRHBuilder = cms.string('hltESPTTRHBWithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("hltIter0PFlowCkfTrackCandidatesROIForBTag"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(True)
    )

    process.hltIter0PFlowTrackCutClassifierROIForBTag = cms.EDProducer("TrackCutClassifier",
        beamspot = cms.InputTag("hltOnlineBeamSpot"),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 0.003),
                d0err_par = cms.vdouble(0.001, 0.001, 0.001),
                dr_exp = cms.vint32(4, 4, 4),
                dr_par1 = cms.vdouble(3.40282346639e+38, 0.8, 0.8),
                dr_par2 = cms.vdouble(3.40282346639e+38, 0.6, 0.6)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 4),
                dz_par1 = cms.vdouble(3.40282346639e+38, 0.75, 0.75),
                dz_par2 = cms.vdouble(3.40282346639e+38, 0.5, 0.5)
            ),
            maxChi2 = cms.vdouble(9999.0, 25.0, 16.0),
            maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
            maxLostLayers = cms.vint32(1, 1, 1),
            min3DLayers = cms.vint32(0, 0, 0),
            minLayers = cms.vint32(3, 3, 3),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 0, 0)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag("hltIter0PFlowCtfWithMaterialTracksROIForBTag"),
        vertices = cms.InputTag("hltTrimmedPixelVertices")
    )

    process.hltMergedTracksROIForBTag = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("hltIter0PFlowTrackCutClassifierROIForBTag","MVAValues"),
        originalQualVals = cms.InputTag("hltIter0PFlowTrackCutClassifierROIForBTag","QualityMasks"),
        originalSource = cms.InputTag("hltIter0PFlowCtfWithMaterialTracksROIForBTag")
    )


    process.hltPFMuonMergingROIForBTag = cms.EDProducer("TrackListMerger",
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(20.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.05),
        ShareFrac = cms.double(0.19),
        TrackProducers = cms.VInputTag("hltIterL3MuonTracks", "hltMergedTracksROIForBTag"),
        allowFirstHitShare = cms.bool(True),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False),
        hasSelector = cms.vint32(0, 0),
        indivShareFrac = cms.vdouble(1.0, 1.0),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag("hltIterL3MuonTracks", "hltMergedTracksROIForBTag"),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(False),
            tLists = cms.vint32(0, 1)
        )),
        trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )


    process.hltMuonLinksROIForBTag = cms.EDProducer("MuonLinksProducerForHLT",
        InclusiveTrackerTrackCollection = cms.InputTag("hltPFMuonMergingROIForBTag"),
        LinkCollection = cms.InputTag("hltL3MuonsIterL3Links"),
        pMin = cms.double(2.5),
        ptMin = cms.double(2.5),
        shareHitFraction = cms.double(0.8)
    )


    process.hltMuonsROIForBTag = cms.EDProducer("MuonIdProducer",
        CaloExtractorPSet = cms.PSet(
            CenterConeOnCalIntersection = cms.bool(False),
            ComponentName = cms.string('CaloExtractorByAssociator'),
            DR_Max = cms.double(1.0),
            DR_Veto_E = cms.double(0.07),
            DR_Veto_H = cms.double(0.1),
            DR_Veto_HO = cms.double(0.1),
            DepositInstanceLabels = cms.vstring(
                'ecal',
                'hcal',
                'ho'
            ),
            DepositLabel = cms.untracked.string('Cal'),
            NoiseTow_EB = cms.double(0.04),
            NoiseTow_EE = cms.double(0.15),
            Noise_EB = cms.double(0.025),
            Noise_EE = cms.double(0.1),
            Noise_HB = cms.double(0.2),
            Noise_HE = cms.double(0.2),
            Noise_HO = cms.double(0.2),
            PrintTimeReport = cms.untracked.bool(False),
            PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(False),
                UseMuonNavigation = cms.untracked.bool(False)
            ),
            Threshold_E = cms.double(0.2),
            Threshold_H = cms.double(0.5),
            Threshold_HO = cms.double(0.5),
            TrackAssociatorParameters = cms.PSet(
                CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
                CaloTowerCollectionLabel = cms.InputTag("hltTowerMakerForAll"),
                DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
                EBRecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
                EERecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
                HBHERecHitCollectionLabel = cms.InputTag("hltHbhereco"),
                HORecHitCollectionLabel = cms.InputTag("hltHoreco"),
                accountForTrajectoryChangeCalo = cms.bool(False),
                dREcal = cms.double(1.0),
                dREcalPreselection = cms.double(1.0),
                dRHcal = cms.double(1.0),
                dRHcalPreselection = cms.double(1.0),
                dRMuon = cms.double(9999.0),
                dRMuonPreselection = cms.double(0.2),
                dRPreshowerPreselection = cms.double(0.2),
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                propagateAllDirections = cms.bool(True),
                trajectoryUncertaintyTolerance = cms.double(-1.0),
                truthMatch = cms.bool(False),
                useCalo = cms.bool(True),
                useEcal = cms.bool(False),
                useHO = cms.bool(False),
                useHcal = cms.bool(False),
                useMuon = cms.bool(False),
                usePreshower = cms.bool(False)
            ),
            UseRecHitsFlag = cms.bool(False)
        ),
        JetExtractorPSet = cms.PSet(
            ComponentName = cms.string('JetExtractor'),
            DR_Max = cms.double(1.0),
            DR_Veto = cms.double(0.1),
            ExcludeMuonVeto = cms.bool(True),
            JetCollectionLabel = cms.InputTag("hltAK4CaloJetsPFEt5"),
            PrintTimeReport = cms.untracked.bool(False),
            PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(False),
                UseMuonNavigation = cms.untracked.bool(False)
            ),
            Threshold = cms.double(5.0),
            TrackAssociatorParameters = cms.PSet(
                CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
                CaloTowerCollectionLabel = cms.InputTag("hltTowerMakerForAll"),
                DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
                EBRecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
                EERecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
                HBHERecHitCollectionLabel = cms.InputTag("hltHbhereco"),
                HORecHitCollectionLabel = cms.InputTag("hltHoreco"),
                accountForTrajectoryChangeCalo = cms.bool(False),
                dREcal = cms.double(0.5),
                dREcalPreselection = cms.double(0.5),
                dRHcal = cms.double(0.5),
                dRHcalPreselection = cms.double(0.5),
                dRMuon = cms.double(9999.0),
                dRMuonPreselection = cms.double(0.2),
                dRPreshowerPreselection = cms.double(0.2),
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                propagateAllDirections = cms.bool(True),
                trajectoryUncertaintyTolerance = cms.double(-1.0),
                truthMatch = cms.bool(False),
                useCalo = cms.bool(True),
                useEcal = cms.bool(False),
                useHO = cms.bool(False),
                useHcal = cms.bool(False),
                useMuon = cms.bool(False),
                usePreshower = cms.bool(False)
            )
        ),
        MuonCaloCompatibility = cms.PSet(
            MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_lowPt_3_1_norm.root'),
            PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_lowPt_3_1_norm.root'),
            allSiPMHO = cms.bool(False),
            delta_eta = cms.double(0.02),
            delta_phi = cms.double(0.02)
        ),
        ShowerDigiFillerParameters = cms.PSet(
            cscDigiCollectionLabel = cms.InputTag("muonCSCDigis","MuonCSCStripDigi"),
            digiMaxDistanceX = cms.double(25.0),
            dtDigiCollectionLabel = cms.InputTag("muonDTDigis")
        ),
        TimingFillerParameters = cms.PSet(
            CSCTimingParameters = cms.PSet(
                CSCStripError = cms.double(7.0),
                CSCStripTimeOffset = cms.double(0.0),
                CSCTimeOffset = cms.double(0.0),
                CSCWireError = cms.double(8.6),
                CSCWireTimeOffset = cms.double(0.0),
                CSCsegments = cms.InputTag("hltCscSegments"),
                MatchParameters = cms.PSet(
                    CSCsegments = cms.InputTag("hltCscSegments"),
                    DTradius = cms.double(0.01),
                    DTsegments = cms.InputTag("hltDt4DSegments"),
                    TightMatchCSC = cms.bool(True),
                    TightMatchDT = cms.bool(False)
                ),
                PruneCut = cms.double(100.0),
                ServiceParameters = cms.PSet(
                    Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                    RPCLayers = cms.bool(True)
                ),
                UseStripTime = cms.bool(True),
                UseWireTime = cms.bool(True),
                debug = cms.bool(False)
            ),
            DTTimingParameters = cms.PSet(
                DTTimeOffset = cms.double(2.7),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                DoWireCorr = cms.bool(False),
                DropTheta = cms.bool(True),
                HitError = cms.double(6.0),
                HitsMin = cms.int32(5),
                MatchParameters = cms.PSet(
                    CSCsegments = cms.InputTag("hltCscSegments"),
                    DTradius = cms.double(0.01),
                    DTsegments = cms.InputTag("hltDt4DSegments"),
                    TightMatchCSC = cms.bool(True),
                    TightMatchDT = cms.bool(False)
                ),
                PruneCut = cms.double(10000.0),
                RequireBothProjections = cms.bool(False),
                ServiceParameters = cms.PSet(
                    Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                    RPCLayers = cms.bool(True)
                ),
                UseSegmentT0 = cms.bool(False),
                debug = cms.bool(False)
            ),
            EcalEnergyCut = cms.double(0.4),
            ErrorCSC = cms.double(7.4),
            ErrorDT = cms.double(6.0),
            ErrorEB = cms.double(2.085),
            ErrorEE = cms.double(6.95),
            UseCSC = cms.bool(True),
            UseDT = cms.bool(True),
            UseECAL = cms.bool(True)
        ),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("hltTowerMakerForAll"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
            EERecHitCollectionLabel = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
            HBHERecHitCollectionLabel = cms.InputTag("hltHbhereco"),
            HORecHitCollectionLabel = cms.InputTag("hltHoreco"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(9999.0),
            dREcalPreselection = cms.double(0.05),
            dRHcal = cms.double(9999.0),
            dRHcalPreselection = cms.double(0.2),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(False),
            useEcal = cms.bool(True),
            useHO = cms.bool(True),
            useHcal = cms.bool(True),
            useMuon = cms.bool(True),
            usePreshower = cms.bool(False)
        ),
        TrackExtractorPSet = cms.PSet(
            BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
            BeamlineOption = cms.string('BeamSpotFromEvent'),
            Chi2Ndof_Max = cms.double(1e+64),
            Chi2Prob_Min = cms.double(-1.0),
            ComponentName = cms.string('TrackExtractor'),
            DR_Max = cms.double(1.0),
            DR_Veto = cms.double(0.01),
            DepositLabel = cms.untracked.string(''),
            Diff_r = cms.double(0.1),
            Diff_z = cms.double(0.2),
            NHits_Min = cms.uint32(0),
            Pt_Min = cms.double(-1.0),
            inputTrackCollection = cms.InputTag("hltPFMuonMergingROIForBTag")
        ),
        TrackerKinkFinderParameters = cms.PSet(
            diagonalOnly = cms.bool(False),
            usePosition = cms.bool(False)
        ),
        addExtraSoftMuons = cms.bool(False),
        arbitrateTrackerMuons = cms.bool(False),
        arbitrationCleanerOptions = cms.PSet(
            ClusterDPhi = cms.double(0.6),
            ClusterDTheta = cms.double(0.02),
            Clustering = cms.bool(True),
            ME1a = cms.bool(True),
            Overlap = cms.bool(True),
            OverlapDPhi = cms.double(0.0786),
            OverlapDTheta = cms.double(0.02)
        ),
        debugWithTruthMatching = cms.bool(False),
        ecalDepositName = cms.string('ecal'),
        fillCaloCompatibility = cms.bool(True),
        fillEnergy = cms.bool(True),
        fillGlobalTrackQuality = cms.bool(False),
        fillGlobalTrackRefits = cms.bool(False),
        fillIsolation = cms.bool(True),
        fillMatching = cms.bool(True),
        fillShowerDigis = cms.bool(False),
        fillTrackerKink = cms.bool(False),
        globalTrackQualityInputTag = cms.InputTag("glbTrackQual"),
        hcalDepositName = cms.string('hcal'),
        hoDepositName = cms.string('ho'),
        inputCollectionLabels = cms.VInputTag("hltPFMuonMergingROIForBTag", "hltMuonLinksROIForBTag", "hltL2Muons"),
        inputCollectionTypes = cms.vstring(
            'inner tracks',
            'links',
            'outer tracks'
        ),
        jetDepositName = cms.string('jets'),
        maxAbsDx = cms.double(3.0),
        maxAbsDy = cms.double(9999.0),
        maxAbsEta = cms.double(3.0),
        maxAbsPullX = cms.double(4.0),
        maxAbsPullY = cms.double(9999.0),
        minCaloCompatibility = cms.double(0.6),
        minNumberOfMatches = cms.int32(1),
        minP = cms.double(10.0),
        minPCaloMuon = cms.double(1000000000.0),
        minPt = cms.double(10.0),
        ptThresholdToFillCandidateP4WithGlobalFit = cms.double(200.0),
        runArbitrationCleaner = cms.bool(False),
        sigmaThresholdToFillCandidateP4WithGlobalFit = cms.double(2.0),
        storeCrossedHcalRecHits = cms.bool(False),
        trackDepositName = cms.string('tracker'),
        writeIsoDeposits = cms.bool(False)
    )


    process.hltLightPFTracksROIForBTag = cms.EDProducer("LightPFTrackProducer",
        TkColList = cms.VInputTag("hltPFMuonMergingROIForBTag"),
        TrackQuality = cms.string('none'),
        UseQuality = cms.bool(False)
    )


    process.hltParticleFlowBlockROIForBTag = cms.EDProducer("PFBlockProducer",
        debug = cms.untracked.bool(False),
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
                source = cms.InputTag("hltParticleFlowClusterECALUnseeded")
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
        linkDefinitions = cms.VPSet(
            cms.PSet(
                linkType = cms.string('TRACK:ECAL'),
                linkerName = cms.string('TrackAndECALLinker'),
                useKDTree = cms.bool(True)
            ),
            cms.PSet(
                linkType = cms.string('TRACK:HCAL'),
                linkerName = cms.string('TrackAndHCALLinker'),
                nMaxHcalLinksPerTrack = cms.int32(1),
                trajectoryLayerEntrance = cms.string('HCALEntrance'),
                trajectoryLayerExit = cms.string('HCALExit'),
                useKDTree = cms.bool(True)
            ),
            cms.PSet(
                linkType = cms.string('ECAL:HCAL'),
                linkerName = cms.string('ECALAndHCALLinker'),
                minAbsEtaEcal = cms.double(2.5),
                useKDTree = cms.bool(False)
            ),
            cms.PSet(
                linkType = cms.string('HFEM:HFHAD'),
                linkerName = cms.string('HFEMAndHFHADLinker'),
                useKDTree = cms.bool(False)
            )
        ),
        verbose = cms.untracked.bool(False)
    )


    process.hltParticleFlowROIForBTag = cms.EDProducer("PFProducer",
        GedElectronValueMap = cms.InputTag("gedGsfElectronsTmp"),
        GedPhotonValueMap = cms.InputTag("tmpGedPhotons","valMapPFEgammaCandToPhoton"),
        PFEGammaCandidates = cms.InputTag("particleFlowEGamma"),
        PFEGammaFiltersParameters = cms.PSet(
            electron_ecalDrivenHademPreselCut = cms.double(0.15),
            electron_iso_combIso_barrel = cms.double(10.0),
            electron_iso_combIso_endcap = cms.double(10.0),
            electron_iso_mva_barrel = cms.double(-0.1875),
            electron_iso_mva_endcap = cms.double(-0.1075),
            electron_iso_pt = cms.double(10.0),
            electron_maxElePtForOnlyMVAPresel = cms.double(50.0),
            electron_missinghits = cms.uint32(1),
            electron_noniso_mvaCut = cms.double(-0.1),
            electron_protectionsForBadHcal = cms.PSet(
                dEta = cms.vdouble(0.0064, 0.01264),
                dPhi = cms.vdouble(0.0547, 0.0394),
                eInvPInv = cms.vdouble(0.184, 0.0721),
                enableProtections = cms.bool(False),
                full5x5_sigmaIetaIeta = cms.vdouble(0.0106, 0.0387)
            ),
            electron_protectionsForJetMET = cms.PSet(
                maxDPhiIN = cms.double(0.1),
                maxE = cms.double(50.0),
                maxEcalEOverPRes = cms.double(0.2),
                maxEcalEOverP_1 = cms.double(0.5),
                maxEcalEOverP_2 = cms.double(0.2),
                maxEeleOverPout = cms.double(0.2),
                maxEeleOverPoutRes = cms.double(0.5),
                maxEleHcalEOverEcalE = cms.double(0.1),
                maxHcalE = cms.double(10.0),
                maxHcalEOverEcalE = cms.double(0.1),
                maxHcalEOverP = cms.double(1.0),
                maxNtracks = cms.double(3.0),
                maxTrackPOverEele = cms.double(1.0)
            ),
            photon_HoE = cms.double(0.05),
            photon_MinEt = cms.double(10.0),
            photon_SigmaiEtaiEta_barrel = cms.double(0.0125),
            photon_SigmaiEtaiEta_endcap = cms.double(0.034),
            photon_combIso = cms.double(10.0),
            photon_protectionsForBadHcal = cms.PSet(
                enableProtections = cms.bool(False),
                solidConeTrkIsoOffset = cms.double(10.0),
                solidConeTrkIsoSlope = cms.double(0.3)
            ),
            photon_protectionsForJetMET = cms.PSet(
                sumPtTrackIso = cms.double(4.0),
                sumPtTrackIsoSlope = cms.double(0.001)
            )
        ),
        PFHFCleaningParameters = cms.PSet(
            maxDeltaPhiPt = cms.double(7.0),
            maxSignificance = cms.double(2.5),
            minDeltaMet = cms.double(0.4),
            minHFCleaningPt = cms.double(5.0),
            minSignificance = cms.double(2.5),
            minSignificanceReduction = cms.double(1.4)
        ),
        PFMuonAlgoParameters = cms.PSet(

        ),
        blocks = cms.InputTag("hltParticleFlowBlockROIForBTag"),
        calibHF_a_EMHAD = cms.vdouble(
            1.42215, 1.00496, 0.68961, 0.81656, 0.98504,
            0.98504, 1.00802, 1.0593, 1.4576, 1.4576
        ),
        calibHF_a_EMonly = cms.vdouble(
            0.96945, 0.96701, 0.76309, 0.82268, 0.87583,
            0.89718, 0.98674, 1.4681, 1.458, 1.458
        ),
        calibHF_b_EMHAD = cms.vdouble(
            1.27541, 0.85361, 0.86333, 0.89091, 0.94348,
            0.94348, 0.9437, 1.0034, 1.0444, 1.0444
        ),
        calibHF_b_HADonly = cms.vdouble(
            1.27541, 0.85361, 0.86333, 0.89091, 0.94348,
            0.94348, 0.9437, 1.0034, 1.0444, 1.0444
        ),
        calibHF_eta_step = cms.vdouble(
            0.0, 2.9, 3.0, 3.2, 4.2,
            4.4, 4.6, 4.8, 5.2, 5.4
        ),
        calibHF_use = cms.bool(False),
        calibrationsLabel = cms.string('HLT'),
        cleanedHF = cms.VInputTag("hltParticleFlowRecHitHF:Cleaned", "hltParticleFlowClusterHF:Cleaned"),
        debug = cms.untracked.bool(False),
        dptRel_DispVtx = cms.double(10.0),
        egammaElectrons = cms.InputTag(""),
        factors_45 = cms.vdouble(10.0, 100.0),
        goodPixelTrackDeadHcal_chi2n = cms.double(2.0),
        goodPixelTrackDeadHcal_dxy = cms.double(0.02),
        goodPixelTrackDeadHcal_dz = cms.double(0.05),
        goodPixelTrackDeadHcal_maxLost3Hit = cms.int32(0),
        goodPixelTrackDeadHcal_maxLost4Hit = cms.int32(1),
        goodPixelTrackDeadHcal_maxPt = cms.double(50.0),
        goodPixelTrackDeadHcal_minEta = cms.double(2.3),
        goodPixelTrackDeadHcal_ptErrRel = cms.double(1.0),
        goodTrackDeadHcal_chi2n = cms.double(5.0),
        goodTrackDeadHcal_dxy = cms.double(0.5),
        goodTrackDeadHcal_layers = cms.uint32(4),
        goodTrackDeadHcal_ptErrRel = cms.double(0.2),
        goodTrackDeadHcal_validFr = cms.double(0.5),
        iCfgCandConnector = cms.PSet(
            bCalibPrimary = cms.bool(False),
            bCorrect = cms.bool(False),
            nuclCalibFactors = cms.vdouble(0.8, 0.15, 0.5, 0.5, 0.05)
        ),
        muon_ECAL = cms.vdouble(0.5, 0.5),
        muon_HCAL = cms.vdouble(3.0, 3.0),
        muon_HO = cms.vdouble(0.9, 0.9),
        muons = cms.InputTag("hltMuonsROIForBTag"),
        nsigma_TRACK = cms.double(1.0),
        pf_nsigma_ECAL = cms.double(0.0),
        pf_nsigma_HCAL = cms.double(1.0),
        pf_nsigma_HFEM = cms.double(1.0),
        pf_nsigma_HFHAD = cms.double(1.0),
        postHFCleaning = cms.bool(False),
        postMuonCleaning = cms.bool(True),
        pt_Error = cms.double(1.0),
        rejectTracks_Bad = cms.bool(False),
        rejectTracks_Step45 = cms.bool(False),
        resolHF_square = cms.vdouble(7.834401, 0.012996, 0.0),
        useCalibrationsFromDB = cms.bool(True),
        useEGammaElectrons = cms.bool(False),
        useEGammaFilters = cms.bool(False),
        useHO = cms.bool(False),
        usePFConversions = cms.bool(False),
        usePFDecays = cms.bool(False),
        usePFNuclearInteractions = cms.bool(False),
        useProtectionsForJetMET = cms.bool(True),
        useVerticesForNeutral = cms.bool(True),
        verbose = cms.untracked.bool(False),
        vertexCollection = cms.InputTag("hltPixelVertices"),
        vetoEndcap = cms.bool(False)
    )


    process.hltAK4PFJetsROIForBTag = cms.EDProducer("FastjetJetProducer",
        Active_Area_Repeats = cms.int32(5),
        DxyTrVtxMax = cms.double(0.0),
        DzTrVtxMax = cms.double(0.0),
        GhostArea = cms.double(0.01),
        Ghost_EtaMax = cms.double(6.0),
        MaxVtxZ = cms.double(15.0),
        MinVtxNdof = cms.int32(0),
        R0 = cms.double(-1.0),
        Rho_EtaMax = cms.double(4.4),
        UseOnlyOnePV = cms.bool(False),
        UseOnlyVertexTracks = cms.bool(False),
        applyWeight = cms.bool(False),
        beta = cms.double(-1.0),
        correctShape = cms.bool(False),
        csRParam = cms.double(-1.0),
        csRho_EtaMax = cms.double(-1.0),
        dRMax = cms.double(-1.0),
        dRMin = cms.double(-1.0),
        doAreaDiskApprox = cms.bool(True),
        doAreaFastjet = cms.bool(False),
        doFastJetNonUniform = cms.bool(False),
        doPUOffsetCorr = cms.bool(False),
        doPVCorrection = cms.bool(False),
        doRhoFastjet = cms.bool(False),
        gridMaxRapidity = cms.double(-1.0),
        gridSpacing = cms.double(-1.0),
        inputEMin = cms.double(0.0),
        inputEtMin = cms.double(0.0),
        jetAlgorithm = cms.string('AntiKt'),
        jetCollInstanceName = cms.string(''),
        jetPtMin = cms.double(0.0),
        jetType = cms.string('PFJet'),
        maxBadEcalCells = cms.uint32(9999999),
        maxBadHcalCells = cms.uint32(9999999),
        maxDepth = cms.int32(-1),
        maxInputs = cms.uint32(1),
        maxProblematicEcalCells = cms.uint32(9999999),
        maxProblematicHcalCells = cms.uint32(9999999),
        maxRecoveredEcalCells = cms.uint32(9999999),
        maxRecoveredHcalCells = cms.uint32(9999999),
        minSeed = cms.uint32(0),
        minimumTowersFraction = cms.double(0.0),
        muCut = cms.double(-1.0),
        muMax = cms.double(-1.0),
        muMin = cms.double(-1.0),
        nExclude = cms.uint32(0),
        nFilt = cms.int32(-1),
        nSigmaPU = cms.double(1.0),
        puCenters = cms.vdouble(),
        puPtMin = cms.double(10.0),
        puWidth = cms.double(0.0),
        rFilt = cms.double(-1.0),
        rFiltFactor = cms.double(-1.0),
        rParam = cms.double(0.4),
        radiusPU = cms.double(0.4),
        rcut_factor = cms.double(-1.0),
        restrictInputs = cms.bool(False),
        src = cms.InputTag("hltParticleFlowROIForBTag"),
        srcPVs = cms.InputTag("hltPixelVertices"),
        srcWeights = cms.InputTag(""),
        subjetPtMin = cms.double(-1.0),
        subtractorName = cms.string(''),
        sumRecHits = cms.bool(False),
        trimPtFracMin = cms.double(-1.0),
        useCMSBoostedTauSeedingAlgorithm = cms.bool(False),
        useConstituentSubtraction = cms.bool(False),
        useDeterministicSeed = cms.bool(True),
        useDynamicFiltering = cms.bool(False),
        useExplicitGhosts = cms.bool(False),
        useFiltering = cms.bool(False),
        useKtPruning = cms.bool(False),
        useMassDropTagger = cms.bool(False),
        usePruning = cms.bool(False),
        useSoftDrop = cms.bool(False),
        useTrimming = cms.bool(False),
        verbosity = cms.int32(0),
        voronoiRfact = cms.double(-9.0),
        writeCompound = cms.bool(False),
        writeJetsWithConst = cms.bool(False),
        yCut = cms.double(-1.0),
        yMax = cms.double(-1.0),
        yMin = cms.double(-1.0),
        zcut = cms.double(-1.0)
    )


    process.hltAK4PFJetsLooseIDROIForBTag = cms.EDProducer("HLTPFJetIDProducer",
        CEF = cms.double(0.99),
        CHF = cms.double(0.0),
        NCH = cms.int32(0),
        NEF = cms.double(0.99),
        NHF = cms.double(0.99),
        NTOT = cms.int32(1),
        jetsInput = cms.InputTag("hltAK4PFJetsROIForBTag"),
        maxCF = cms.double(99.0),
        maxEta = cms.double(1e+99),
        minPt = cms.double(20.0)
    )

    process.hltAK4PFJetsTightIDROIForBTag = cms.EDProducer("HLTPFJetIDProducer",
        CEF = cms.double(0.99),
        CHF = cms.double(0.0),
        NCH = cms.int32(0),
        NEF = cms.double(0.99),
        NHF = cms.double(0.9),
        NTOT = cms.int32(1),
        jetsInput = cms.InputTag("hltAK4PFJetsROIForBTag"),
        maxCF = cms.double(99.0),
        maxEta = cms.double(1e+99),
        minPt = cms.double(20.0)
    )

    process.hltFixedGridRhoFastjetAllROIForBTag = cms.EDProducer("FixedGridRhoProducerFastjet",
        gridSpacing = cms.double(0.55),
        maxRapidity = cms.double(5.0),
        pfCandidatesTag = cms.InputTag("hltParticleFlowROIForBTag")
    )


    process.hltAK4PFFastJetCorrectorROIForBTag = cms.EDProducer("L1FastjetCorrectorProducer",
        algorithm = cms.string('AK4PFHLT'),
        level = cms.string('L1FastJet'),
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
        process.hltParticleFlowClusterECALUnseeded+
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
        process.hltPixelTracksCleanForBTag +
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




    #  process.HLTAK4CaloJetsSequence = cms.Sequence(
        #  process.HLTAK4CaloJetsReconstructionSequence+
        #  process.HLTAK4CaloJetsCorrectionSequence
    #  )

    #  process.HLTAK4CaloJetsReconstructionSequence = cms.Sequence(
        #  process.HLTDoCaloSequence+
        #  process.hltAK4CaloJets+
        #  process.hltAK4CaloJetsIDPassed
    #  )

    #  process.HLTAK4CaloJetsCorrectionSequence = cms.Sequence(
        #  process.hltFixedGridRhoFastjetAllCalo+
        #  process.HLTAK4CaloCorrectorProducersSequence+
        #  process.hltAK4CaloJetsCorrected+
        #  process.hltAK4CaloJetsCorrectedIDPassed
    #  )



















    process.HLTBtagDeepCSVSequencePFROIForBTag = cms.Sequence(

        process.hltVerticesPFROIForBTag+
        process.hltVerticesPFSelectorROIForBTag+
        process.hltVerticesPFFilterROIForBTag+

        process.hltPFJetForBtagSelectorROIForBTag+
        process.hltPFJetForBtagROIForBTag+

        # process.hltDeepBLifetimeTagInfosPF+
        # process.hltDeepInclusiveVertexFinderPF+
        # process.hltDeepInclusiveSecondaryVerticesPF+
        # process.hltDeepTrackVertexArbitratorPF+
        # process.hltDeepInclusiveMergedVerticesPF+
        # process.hltDeepSecondaryVertexTagInfosPF+
        # process.hltDeepCombinedSecondaryVertexBJetTagsInfos+
        # process.hltDeepCombinedSecondaryVertexBJetTagsPF

        process.hltDeepBLifetimeTagInfosPFROIForBTag+
        process.hltDeepInclusiveVertexFinderPFROIForBTag+
        process.hltDeepInclusiveSecondaryVerticesPFROIForBTag+
        process.hltDeepTrackVertexArbitratorPFROIForBTag+
        process.hltDeepInclusiveMergedVerticesPFROIForBTag+
        process.hltDeepSecondaryVertexTagInfosPFROIForBTag+
        process.hltDeepCombinedSecondaryVertexBJetTagsInfosROIForBTag+
        process.hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag
    )


    ############################################################################
    ####                    MC_PFBTagDeepCSV_v10ROIForBTag                   ###
    ############################################################################


    process.hltBTagPFDeepCSV4p06SingleROIForBTag = cms.EDFilter("HLTPFJetTag",
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
        MaxTag = cms.double(999999.0),
        MinJets = cms.int32(1),
        MinTag = cms.double(0.25),
        TriggerType = cms.int32(86),
        saveTags = cms.bool(True)
    )

    process.hltPreMCPFBTagDeepCSVROIForBTag = cms.EDFilter("HLTPrescaler",
        L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
        offset = cms.uint32(0)
    )

    process.MC_PFBTagDeepCSVROIForBTag_v10 = cms.Path(
        process.HLTBeginSequence+
        process.hltPreMCPFBTagDeepCSVROIForBTag+

        process.HLTAK4PFJetsSequenceROIForBTag+
        process.HLTBtagDeepCSVSequencePFROIForBTag+

        process.hltBTagPFDeepCSV4p06SingleROIForBTag+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v3ROIForBTag
    ############################################################################


    process.hltPFCentralJetLooseIDQuad30ROIForBTag = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(4),
        MinPt = cms.double(30.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(86)
    )

    process.hlt1PFCentralJetLooseID75ROIForBTag = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(1),
        MinPt = cms.double(75.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(0)
    )

    process.hlt2PFCentralJetLooseID60ROIForBTag = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(2),
        MinPt = cms.double(60.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(0)
    )

    process.hlt3PFCentralJetLooseID45ROIForBTag = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(3),
        MinPt = cms.double(45.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(0)
    )

    process.hlt4PFCentralJetLooseID40ROIForBTag = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(4),
        MinPt = cms.double(40.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(0)
    )

    process.hltPFCentralJetLooseIDQuad30forHtROIForBTag = cms.EDProducer("HLTPFJetCollectionProducer",
        HLTObject = cms.InputTag("hltPFCentralJetLooseIDQuad30ROIForBTag"),
        TriggerTypes = cms.vint32(86)
    )

    process.hltHtMhtPFCentralJetsLooseIDQuadC30ROIForBTag = cms.EDProducer("HLTHtMhtProducer",
        excludePFMuons = cms.bool(False),
        jetsLabel = cms.InputTag("hltPFCentralJetLooseIDQuad30forHtROIForBTag"),
        maxEtaJetHt = cms.double(2.5),
        maxEtaJetMht = cms.double(999.0),
        minNJetHt = cms.int32(4),
        minNJetMht = cms.int32(0),
        minPtJetHt = cms.double(30.0),
        minPtJetMht = cms.double(0.0),
        pfCandidatesLabel = cms.InputTag("hltParticleFlowROIForBTag"),
        usePt = cms.bool(True)
    )


    process.hltPFCentralJetsLooseIDQuad30HT330ROIForBTag = cms.EDFilter("HLTHtMhtFilter",
        htLabels = cms.VInputTag("hltHtMhtPFCentralJetsLooseIDQuadC30ROIForBTag"),
        meffSlope = cms.vdouble(1.0),
        mhtLabels = cms.VInputTag("hltHtMhtPFCentralJetsLooseIDQuadC30ROIForBTag"),
        minHt = cms.vdouble(330.0),
        minMeff = cms.vdouble(0.0),
        minMht = cms.vdouble(0.0),
        saveTags = cms.bool(True)
    )



    process.hltBTagPFDeepCSV4p5TripleROIForBTag = cms.EDFilter("HLTPFJetTag",
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        Jets = cms.InputTag("hltPFJetForBtagROIForBTag"),
        MaxTag = cms.double(999999.0),
        MinJets = cms.int32(3),
        MinTag = cms.double(0.24),
        TriggerType = cms.int32(86),
        saveTags = cms.bool(True)
    )



    process.HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5ROIForBTag_v3 = cms.Path(
        process.HLTBeginSequence+

        process.hltL1sQuadJetC50to60IorHTT280to500IorHTT250to340QuadJet+
        process.hltPrePFHT330PT30QuadPFJet75604540TriplePFBTagDeepCSV4p5+

        process.HLTAK4CaloJetsSequence+

        process.hltQuadCentralJet30+
        process.hltCaloJetsQuad30ForHt+
        process.hltHtMhtCaloJetsQuadC30+
        process.hltCaloQuadJet30HT320+

        #  process.HLTBtagDeepCSVSequenceL3+
        #  process.hltBTagCaloDeepCSVp17Double+

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


    ############################################################################
    #### HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5_v8ROIForBTag
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

    process.HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJetTripleJet+
        process.hltPrePFHT400FivePFJet100100603030DoublePFBTagDeepCSV4p5+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterFiveC25+
        process.hltCaloJetsFive25ForHt+
        process.hltHtMhtCaloJetsFiveC25+
        process.hltCaloFiveJet25HT300+

        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV10p01Single+
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


    ############################################################################
    #### HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepCSV_4p5_v
    ############################################################################

    process.hltPFJetFilterTwo120er3p0ROIForBTag = process.hltPFJetFilterTwo120er3p0.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrectedROIForBTag"),
    )

    process.HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepCSV_4p5ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJetTripleJet+
        process.hltPrePFHT400FivePFJet120120603030DoublePFBTagDeepCSV4p5+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterFiveC25+
        process.hltCaloJetsFive25ForHt+
        process.hltHtMhtCaloJetsFiveC25+
        process.hltCaloFiveJet25HT300+

        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV10p01Single+

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

    process.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJet+
        process.hltPrePFHT400SixPFJet32DoublePFBTagDeepCSV2p94+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterSixC25+
        process.hltCaloJetsSix25ForHt+
        process.hltHtMhtCaloJetsSixC25+
        process.hltCaloSixJet25HT300+

        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV10p01Single+

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

    process.HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59ROIForBTag_v7 = cms.Path(
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

    process.HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJetVBFIorHTTIorSingleJet+
        process.hltPreQuadPFJet103887515DoublePFBTagDeepCSV1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

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


    ############################################################################
    #### HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2_v
    ############################################################################

    process.hltVBFPFJetCSVSortedMqq460Detaqq3p5ROIForBTag = process.hltVBFPFJetCSVSortedMqq460Detaqq3p5.clone(
        inputJetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPFROIForBTag","probb"),
        inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJetVBFIorHTTIorSingleJet+
        process.hltPreQuadPFJet103887515PFBTagDeepCSV1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

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

    ############################################################################
    #### HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v
    ############################################################################

    process.hltPFTripleJetLooseID76ROIForBTag = process.hltPFTripleJetLooseID76.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.hltPFSingleJetLooseID105ROIForBTag = process.hltPFSingleJetLooseID105.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrectedROIForBTag"),
    )

    process.HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1008572VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet105887615DoublePFBTagDeepCSV1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

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

    ############################################################################
    #### HLT_QuadPFJet105_88_76_15_PFBTagDeepCSV_1p3_VBF2_v
    ############################################################################



    process.HLT_QuadPFJet105_88_76_15_PFBTagDeepCSV_1p3_VBF2ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1008572VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet105887615PFBTagDeepCSV1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

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

    process.HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1058576VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet111908015DoublePFBTagDeepCSV1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

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


    ############################################################################
    #### HLT_QuadPFJet111_90_80_15_PFBTagDeepCSV_1p3_VBF2_v
    ############################################################################

    process.HLT_QuadPFJet111_90_80_15_PFBTagDeepCSV_1p3_VBF2ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1058576VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet111908015PFBTagDeepCSV1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

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

    process.HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet927664VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet98837115DoublePFBTagDeepCSV1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

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

    ############################################################################
    #### HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2_v
    ############################################################################

    process.HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2ROIForBTag_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet927664VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet98837115PFBTagDeepCSV1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

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

    process.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepCSV_1p5ROIForBTag_v1 = cms.Path(
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

    return process
