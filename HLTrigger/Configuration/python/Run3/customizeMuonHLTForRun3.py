import FWCore.ParameterSet.Config as cms

from HLTrigger.Configuration.common import *

def customizeMuonHLTForDoubletRemoval(process, newProcessName = "MYHLT"):

    # -- Remove Iter3 (doublet)
    process.HLTIterativeTrackingIter023ForIterL3Muon = cms.Sequence(
        process.HLTIterativeTrackingIteration0ForIterL3Muon + 
        process.HLTIterativeTrackingIteration2ForIterL3Muon + 
        process.hltIter2IterL3MuonMerged
        # process.HLTIterativeTrackingIteration3ForIterL3Muon + 
        # process.hltIter3IterL3MuonMerged
    )

    process.HLTIterativeTrackingIter023ForIterL3FromL1Muon = cms.Sequence(
        process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon + 
        process.HLTIterativeTrackingIteration2ForIterL3FromL1Muon + 
        process.hltIter2IterL3FromL1MuonMerged
        # process.HLTIterativeTrackingIteration3ForIterL3FromL1Muon + 
        # process.hltIter3IterL3FromL1MuonMerged
    )

    # process.hltL3MuonsIterL3IO
    for mod in producers_by_type(process, 'L3MuonProducer'):
        if hasattr(mod, 'L3TrajBuilderParameters'):
            if hasattr(mod.L3TrajBuilderParameters, 'tkTrajLabel'):
                if mod.L3TrajBuilderParameters.tkTrajLabel == cms.InputTag( "hltIter3IterL3MuonMerged" ):
                    mod.L3TrajBuilderParameters.tkTrajLabel = cms.InputTag( "hltIter2IterL3MuonMerged" )

    # process.hltIterL3MuonMerged and process.hltIterL3MuonAndMuonFromL1Merged
    for mod in producers_by_type(process, 'TrackListMerger'):
        if hasattr(mod, 'selectedTrackQuals'):
            _vinputtag = mod.selectedTrackQuals.value()
            for index in range(0, len(_vinputtag)):
                if mod.selectedTrackQuals.value()[index] == "hltIter3IterL3MuonMerged":
                    _vinputtag[index] = "hltIter2IterL3MuonMerged"
                if mod.selectedTrackQuals.value()[index] == "hltIter3IterL3FromL1MuonMerged":
                    _vinputtag[index] = "hltIter2IterL3FromL1MuonMerged"
            mod.selectedTrackQuals = cms.VInputTag( *_vinputtag )

        if hasattr(mod, 'TrackProducers'):
            _vinputtag = mod.TrackProducers.value()
            for index in range(0, len(_vinputtag)):
                if mod.TrackProducers.value()[index] == "hltIter3IterL3MuonMerged":
                    _vinputtag[index] = "hltIter2IterL3MuonMerged"
                if mod.TrackProducers.value()[index] == "hltIter3IterL3FromL1MuonMerged":
                    _vinputtag[index] = "hltIter2IterL3FromL1MuonMerged"
            mod.TrackProducers = cms.VInputTag( *_vinputtag )

    # process.hltIterL3MuonsNoID
    for mod in producers_by_type(process, 'MuonIdProducer'):
        if hasattr(mod, 'TrackExtractorPSet'):
            if hasattr(mod.TrackExtractorPSet, 'inputTrackCollection'):
                if mod.TrackExtractorPSet.inputTrackCollection == cms.InputTag( "hltIter3IterL3FromL1MuonMerged" ):
                    mod.TrackExtractorPSet.inputTrackCollection = cms.InputTag( "hltIter2IterL3FromL1MuonMerged" )

    return process


def customizeMuonHLTForCscSegment(process, newProcessName = "MYHLT"):

    # -- CSC segment builder
    process.hltCscSegments = cms.EDProducer( "CSCSegmentProducer",
        inputObjects = cms.InputTag( "hltCsc2DRecHits" ),
        algo_psets = cms.VPSet( 
          cms.PSet(  parameters_per_chamber_type = cms.vint32( 1, 2, 3, 4, 5, 6, 5, 6, 5, 6),
            algo_psets = cms.VPSet( 
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        chi2Max = cms.double(100.0),
                        dPhiIntMax = cms.double(0.005),
                        dPhiMax = cms.double(0.006),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        chi2Max = cms.double(100.0),
                        dPhiIntMax = cms.double(0.004),
                        dPhiMax = cms.double(0.005),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        chi2Max = cms.double(100.0),
                        dPhiIntMax = cms.double(0.003),
                        dPhiMax = cms.double(0.004),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(20),
                        chi2_str = cms.double(30.0),
                        chi2Max = cms.double(60.0),
                        dPhiIntMax = cms.double(0.002),
                        dPhiMax = cms.double(0.003),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(60),
                        chi2_str = cms.double(80.0),
                        chi2Max = cms.double(180.0),
                        dPhiIntMax = cms.double(0.005),
                        dPhiMax = cms.double(0.007),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        ),
              cms.PSet(
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        chi2Max = cms.double(100.0),
                        dPhiIntMax = cms.double(0.004),
                        dPhiMax = cms.double(0.006),
                        wideSeg = cms.double(3.0),
                        minLayersApart = cms.int32(1),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5)
                        )
              ),
            algo_name = cms.string( "CSCSegAlgoRU" ),
            chamber_types = cms.vstring( 'ME1/a',
              'ME1/b',
              'ME1/2',
              'ME1/3',
              'ME2/1',
              'ME2/2',
              'ME3/1',
              'ME3/2',
              'ME4/1',
              'ME4/2' )
          )
        ),
        algo_type = cms.int32( 1 )
    )

    return process


def customizeMuonHLTForGEM(process, newProcessName = "MYHLT"):
	process.load('Geometry.GEMGeometryBuilder.gemGeometryDB_cfi')

	# GEM local reco (from offline)
	from Configuration.StandardSequences.RawToDigi_cff import muonGEMDigis
	from Configuration.StandardSequences.Reconstruction_cff import gemRecHits, gemSegments

	process.hltMuonGEMDigis = muonGEMDigis.clone()

	process.hltGemRecHits = gemRecHits.clone(
		gemDigiLabel = cms.InputTag("hltMuonGEMDigis"),
	)

	process.hltGemSegments = gemSegments.clone(
		gemRecHitLabel = cms.InputTag("hltGemRecHits")
	)

	process.HLTMuonLocalRecoSequence = cms.Sequence(
		process.hltMuonDTDigis +
		process.hltDt1DRecHits +
		process.hltDt4DSegments +
		process.hltMuonCSCDigis +
		process.hltCsc2DRecHits +
		process.hltCscSegments +
		process.hltMuonRPCDigis +
		process.hltRpcRecHits +
		process.hltMuonGEMDigis +
		process.hltGemRecHits +
		process.hltGemSegments
	)

	# L2 reconstruction
	process.hltL2Muons.L2TrajBuilderParameters.FilterParameters.EnableGEMMeasurement = cms.bool(True)
	process.hltL2Muons.L2TrajBuilderParameters.FilterParameters.GEMRecSegmentLabel = cms.InputTag("hltGemRecHits")
	process.hltL2Muons.L2TrajBuilderParameters.BWFilterParameters.EnableGEMMeasurement = cms.bool(True)
	process.hltL2Muons.L2TrajBuilderParameters.BWFilterParameters.GEMRecSegmentLabel = cms.InputTag("hltGemRecHits")

	# L3 reconstruction
	process.hltL3MuonsIterL3OI.L3TrajBuilderParameters.GlbRefitterParameters.GEMRecHitLabel = cms.InputTag( "hltGemRecHits" )
	process.hltL3MuonsIterL3OI.L3TrajBuilderParameters.GlbRefitterParameters.Chi2CutGEM = cms.double(1.0)

	process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.GlbRefitterParameters.GEMRecHitLabel = cms.InputTag( "hltGemRecHits" )
	process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.GlbRefitterParameters.Chi2CutGEM = cms.double(1.0)

	process.hltIterL3GlbMuon.L3TrajBuilderParameters.GlbRefitterParameters.GEMRecHitLabel = cms.InputTag( "hltGemRecHits" )
	process.hltIterL3GlbMuon.L3TrajBuilderParameters.GlbRefitterParameters.Chi2CutGEM = cms.double(1.0)

	process.hltIterL3MuonsNoID.TrackAssociatorParameters.useGEM = cms.bool(True)
	process.hltIterL3MuonsNoID.TrackAssociatorParameters.GEMSegmentCollectionLabel = cms.InputTag("hltGemSegments")

	return process


def customizeMuonHLTForPatatrackWithIsoAndTriplets(process, loadPatatrack=True, newProcessName = "MYHLT"):


	if loadPatatrack:
    	# -- modify process to create patatrack pixel tracks and vertices
		from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets


		process.HLTRecoPixelTracksSequence = cms.Sequence()
		process.HLTRecopixelvertexingSequence = cms.Sequence()
		process.hltPixelTracksTrackingRegions = cms.EDProducer( "GlobalTrackingRegionFromBeamSpotEDProducer",
		    RegionPSet = cms.PSet( 
		      nSigmaZ = cms.double( 4.0 ),
		      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
		      ptMin = cms.double( 0.8 ),
		      originRadius = cms.double( 0.02 ),
		      precise = cms.bool( True )
		    )
		)
		process.hltTrimmedPixelVertices = cms.EDProducer( "PixelVertexCollectionTrimmer",
		    src = cms.InputTag( "hltPixelVertices" ),
		    fractionSumPt2 = cms.double( 0.3 ),
		    minSumPt2 = cms.double( 0.0 ),
		    PVcomparer = cms.PSet(  refToPSet_ = cms.string( "HLTPSetPvClusterComparerForIT" ) ),
		    maxVtx = cms.uint32( 100 )
		)
		process.hltPixelTracksFitter = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
		    scaleErrorsForBPix1 = cms.bool( False ),
		    scaleFactor = cms.double( 0.65 )
		)
		process.hltPixelTracksFilter = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
		    nSigmaTipMaxTolerance = cms.double( 0.0 ),
		    chi2 = cms.double( 1000.0 ),
		    nSigmaInvPtTolerance = cms.double( 0.0 ),
		    ptMin = cms.double( 0.1 ),
		    tipMax = cms.double( 1.0 )
		)
	 
		process = customizeHLTforPatatrackTriplets(process)    


	process.hltPixelTracksInRegionL2 = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegions")

	)

	process.hltIterL3MuonPixelTracksTrackingRegions.Pt_min = cms.double( 0.0 )
	process.hltIterL3MuonPixelTracksTrackingRegions.maxRegions = cms.int32( 5 )


	process.HLTIterL3MuonRecopixelvertexingSequence = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3MuonPixelTracksTrackingRegions + process.hltPixelTracksInRegionL2 )

	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputCollection = cms.InputTag("hltPixelTracksInRegionL2")
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.includeFourthHit = cms.bool(True)
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag("hltTrimmedPixelVertices")
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag("")


	process.HLTIterativeTrackingIteration0ForIterL3Muon = cms.Sequence( process.hltIter0IterL3MuonPixelSeedsFromPixelTracks + process.hltIter0IterL3MuonCkfTrackCandidates + process.hltIter0IterL3MuonCtfWithMaterialTracks + process.hltIter0IterL3MuonTrackCutClassifier + process.hltIter0IterL3MuonTrackSelectionHighPurity)

	process.hltL3MuonsIterL3IO.L3TrajBuilderParameters.tkTrajLabel = cms.InputTag("hltIter0IterL3MuonTrackSelectionHighPurity")

	process.HLTIterL3IOmuonTkCandidateSequence = cms.Sequence( process.HLTIterL3MuonRecopixelvertexingSequence + process.HLTIterativeTrackingIteration0ForIterL3Muon + process.hltL3MuonsIterL3IO )

	process.hltIter0IterL3MuonTrackCutClassifier.vertices = cms.InputTag("hltTrimmedPixelVertices")
	process.hltIter0IterL3MuonTrackCutClassifier.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3MuonTrackCutClassifier.mva.min3DLayers = cms.vint32( 0, 0, 0 )


	process.hltPixelTracksInRegionL1 = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegions")

	)

	process.hltIterL3FromL1MuonPixelTracksTrackingRegions.RegionPSet.ptMin = cms.double( 0.0 )
	process.hltIterL3FromL1MuonPixelTracksTrackingRegions.RegionPSet.maxNRegions = cms.int32( 5 )

	process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3FromL1MuonPixelTracksTrackingRegions + process.hltPixelTracksInRegionL1 )

	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.InputCollection = cms.InputTag("hltPixelTracksInRegionL1")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag("")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks.includeFourthHit = cms.bool(True)


	process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon = cms.Sequence( process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks + process.hltIter0IterL3FromL1MuonCkfTrackCandidates + process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks + process.hltIter0IterL3FromL1MuonTrackCutClassifier + process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity )

	process.HLTIterL3IOmuonFromL1TkCandidateSequence = cms.Sequence( process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon + process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon )

	process.hltIter0IterL3FromL1MuonTrackCutClassifier.vertices = cms.InputTag("hltTrimmedPixelVertices")
	process.hltIter0IterL3FromL1MuonTrackCutClassifier.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3FromL1MuonTrackCutClassifier.mva.min3DLayers = cms.vint32( 0, 0, 0 )


	process.hltIterL3MuonMerged.selectedTrackQuals = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurity','hltIter0IterL3MuonTrackSelectionHighPurity' )
	process.hltIterL3MuonMerged.TrackProducers = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurity','hltIter0IterL3MuonTrackSelectionHighPurity' )

	process.hltIterL3MuonAndMuonFromL1Merged.selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonMerged','hltIter0IterL3FromL1MuonTrackSelectionHighPurity' )
	process.hltIterL3MuonAndMuonFromL1Merged.TrackProducers = cms.VInputTag( 'hltIterL3MuonMerged','hltIter0IterL3FromL1MuonTrackSelectionHighPurity' )

	process.hltIterL3MuonsNoID.inputTrackCollection = cms.InputTag( "hltIter0IterL3FromL1MuonTrackSelectionHighPurity")


	process.hltPixelTracksTrackingRegionsForSeedsL3Muon.RegionPSet.ptMin = cms.double( 0.3 )
	process.hltPixelTracksTrackingRegionsForSeedsL3Muon.RegionPSet.vertexCollection = cms.InputTag( "hltPixelVertices" )


	process.hltPixelTracksInRegionIter0L3Muon = cms.EDProducer("TrackSelectorByRegion",
          produceTrackCollection = cms.bool(True),
          produceMask = cms.bool(False),
          tracks = cms.InputTag("hltPixelTracks"),
          regions = cms.InputTag("hltPixelTracksTrackingRegionsForSeedsL3Muon")

        )
	process.hltIter0L3MuonPixelSeedsFromPixelTracks.InputCollection = cms.InputTag("hltPixelTracksInRegionIter0L3Muon")
	process.hltIter0L3MuonPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag( "hltPixelVertices" )
	process.hltIter0L3MuonTrackCutClassifier.vertices = cms.InputTag( "hltPixelVertices" )
	process.hltMuonTkRelIsolationCut0p07Map.TrkExtractorPSet.inputTrackCollection = cms.InputTag("hltIter0L3MuonTrackSelectionHighPurity")

	process.HLTIterativeTrackingL3MuonIteration0 = cms.Sequence( process.hltPixelTracksTrackingRegionsForSeedsL3Muon + process.hltPixelTracksInRegionIter0L3Muon + process.hltIter0L3MuonPixelSeedsFromPixelTracks + process.hltIter0L3MuonCkfTrackCandidates + process.hltIter0L3MuonCtfWithMaterialTracks + process.hltIter0L3MuonTrackCutClassifier + process.hltIter0L3MuonTrackSelectionHighPurity )


	process.HLTTrackReconstructionForIsoL3MuonIter02 = cms.Sequence( process.HLTDoLocalPixelSequence + process.HLTDoLocalStripSequence + process.HLTIterativeTrackingL3MuonIteration0 )

	return process

def customizeMuonHLTForPatatrackTkMu(process, loadPatatrack=True, newProcessName = "MYHLT"):


	if loadPatatrack:
    	# -- modify process to create patatrack pixel tracks and vertices
		from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets


		process.HLTRecoPixelTracksSequence = cms.Sequence()
		process.HLTRecopixelvertexingSequence = cms.Sequence()
		process.hltPixelTracksTrackingRegions = cms.EDProducer( "GlobalTrackingRegionFromBeamSpotEDProducer",
		    RegionPSet = cms.PSet( 
		      nSigmaZ = cms.double( 4.0 ),
		      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
		      ptMin = cms.double( 0.8 ),
		      originRadius = cms.double( 0.02 ),
		      precise = cms.bool( True )
		    )
		)
		process.hltTrimmedPixelVertices = cms.EDProducer( "PixelVertexCollectionTrimmer",
		    src = cms.InputTag( "hltPixelVertices" ),
		    fractionSumPt2 = cms.double( 0.3 ),
		    minSumPt2 = cms.double( 0.0 ),
		    PVcomparer = cms.PSet(  refToPSet_ = cms.string( "HLTPSetPvClusterComparerForIT" ) ),
		    maxVtx = cms.uint32( 100 )
		)
		process.hltPixelTracksFitter = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
		    scaleErrorsForBPix1 = cms.bool( False ),
		    scaleFactor = cms.double( 0.65 )
		)
		process.hltPixelTracksFilter = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
		    nSigmaTipMaxTolerance = cms.double( 0.0 ),
		    chi2 = cms.double( 1000.0 ),
		    nSigmaInvPtTolerance = cms.double( 0.0 ),
		    ptMin = cms.double( 0.1 ),
		    tipMax = cms.double( 1.0 )
		)
	 
		process = customizeHLTforPatatrackTriplets(process)    



	process.hltPixelTracksInRegionTkMu = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIter0HighPtTkMuPixelTracksTrackingRegions")

	)

	process.hltIter0HighPtTkMuPixelTracksTrackingRegions.RegionPSet.ptMin = cms.double( 10.0 )
	process.hltIter0HighPtTkMuPixelTracksTrackingRegions.RegionPSet.maxNRegions = cms.int32( 5 )


	process.hltIter0HighPtTkMuPixelSeedsFromPixelTracks.InputCollection = cms.InputTag("hltPixelTracksInRegionTkMu")
	process.hltIter0HighPtTkMuPixelSeedsFromPixelTracks.includeFourthHit = cms.bool(True)

	process.HLTIterativeTrackingHighPtTkMuIteration0 = cms.Sequence(process.hltIter0HighPtTkMuPixelTracksTrackingRegions + process.hltPixelTracksInRegionTkMu + process.hltIter0HighPtTkMuPixelSeedsFromPixelTracks + process.hltIter0HighPtTkMuCkfTrackCandidates + process.hltIter0HighPtTkMuCtfWithMaterialTracks + process.hltIter0HighPtTkMuTrackSelectionHighPurity )


	process.HLTIterativeTrackingHighPtTkMu = cms.Sequence(process.HLTIterativeTrackingHighPtTkMuIteration0)
	process.hltHighPtTkMu50TkFilt.src = cms.InputTag("hltIter0HighPtTkMuTrackSelectionHighPurity")
	process.hltHighPtTkMuons.inputCollectionLabels = cms.VInputTag( 'hltIter0HighPtTkMuTrackSelectionHighPurity' )



	process.HLTTrackerMuonSequenceLowPtIter0and1 = cms.Sequence( process.HLTDoLocalPixelSequence + process.HLTRecopixelvertexingSequence + process.HLTDoLocalStripSequence + process.HLTIterativeTrackingIteration0 + process.HLTL3muonrecoNocandSequence + process.hltDiMuonMergingIter01TkMu + process.hltDiMuonLinksIter01TkMuMerge + process.hltGlbTrkMuonsLowPtIter01Merge + process.hltGlbTrkMuonLowPtIter01MergeCands )
	process.hltDiMuonMergingIter01TkMu.TrackProducers = cms.VInputTag( 'hltIterL3MuonAndMuonFromL1Merged','hltIter0PFlowTrackSelectionHighPurity' )
	process.hltDiMuonMergingIter01TkMu.selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonAndMuonFromL1Merged','hltIter0PFlowTrackSelectionHighPurity' )

	return process



	
def customizeMuonHLTForPatatrackNoVtx(process, loadPatatrack=True, newProcessName = "MYHLT"):


	if loadPatatrack:
    	# -- modify process to create patatrack pixel tracks and vertices
		from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets


		process.HLTRecoPixelTracksSequence = cms.Sequence()
		process.HLTRecopixelvertexingSequence = cms.Sequence()
		process.hltPixelTracksTrackingRegions = cms.EDProducer( "GlobalTrackingRegionFromBeamSpotEDProducer",
		    RegionPSet = cms.PSet( 
		      nSigmaZ = cms.double( 4.0 ),
		      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
		      ptMin = cms.double( 0.8 ),
		      originRadius = cms.double( 0.02 ),
		      precise = cms.bool( True )
		    )
		)
		process.hltTrimmedPixelVertices = cms.EDProducer( "PixelVertexCollectionTrimmer",
		    src = cms.InputTag( "hltPixelVertices" ),
		    fractionSumPt2 = cms.double( 0.3 ),
		    minSumPt2 = cms.double( 0.0 ),
		    PVcomparer = cms.PSet(  refToPSet_ = cms.string( "HLTPSetPvClusterComparerForIT" ) ),
		    maxVtx = cms.uint32( 100 )
		)
		process.hltPixelTracksFitter = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
		    scaleErrorsForBPix1 = cms.bool( False ),
		    scaleFactor = cms.double( 0.65 )
		)
		process.hltPixelTracksFilter = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
		    nSigmaTipMaxTolerance = cms.double( 0.0 ),
		    chi2 = cms.double( 1000.0 ),
		    nSigmaInvPtTolerance = cms.double( 0.0 ),
		    ptMin = cms.double( 0.1 ),
		    tipMax = cms.double( 1.0 )
		)
	 
		process = customizeHLTforPatatrackTriplets(process)    


	process.hltPixelTracksInRegionL2NoVtx = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegionsNoVtx")

	)

	process.hltIterL3MuonPixelTracksTrackingRegionsNoVtx.Pt_min = cms.double( 0.0 )


	process.HLTIterL3MuonRecoPixelTracksSequenceNoVtx = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3MuonPixelTracksTrackingRegionsNoVtx + process.hltPixelTracksInRegionL2NoVtx )
	process.HLTIterL3MuonRecopixelvertexingSequenceNoVtx = cms.Sequence( process.HLTIterL3MuonRecoPixelTracksSequenceNoVtx )
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksNoVtx.InputCollection = cms.InputTag("hltPixelTracksInRegionL2NoVtx")
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksNoVtx.includeFourthHit = cms.bool(True)
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksNoVtx.InputVertexCollection = cms.InputTag("")


	process.HLTIterL3IOmuonTkCandidateSequenceNoVtx = cms.Sequence( process.HLTIterL3MuonRecopixelvertexingSequenceNoVtx + process.HLTIterativeTrackingIteration0ForIterL3MuonNoVtx + process.hltL3MuonsIterL3IONoVtx )

	process.hltIter0IterL3MuonTrackCutClassifierNoVtx.vertices = cms.InputTag("hltTrimmedPixelVertices")
	process.hltIter0IterL3MuonTrackCutClassifierNoVtx.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3MuonTrackCutClassifierNoVtx.mva.min3DLayers = cms.vint32( 0, 0, 0 )


	process.hltL3MuonsIterL3IONoVtx.L3TrajBuilderParameters.tkTrajLabel = cms.InputTag("hltIter0IterL3MuonTrackSelectionHighPurityNoVtx")
	process.hltL3MuonsIterL3IONoVtx.L3TrajBuilderParameters.tkTrajVertex = cms.InputTag("hltTrimmedPixelVertices")
	process.hltL3MuonsIterL3LinksNoVtx.InclusiveTrackerTrackCollection = cms.InputTag( "hltIter0IterL3MuonTrackSelectionHighPurityNoVtx" )

	process.hltPixelTracksInRegionL1NoVtx = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx")

	)

	process.hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx.RegionPSet.ptMin = cms.double( 0.0 )
	process.hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx.RegionPSet.maxNRegions = cms.int32( 5 )

	process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonNoVtx = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3FromL1MuonPixelTracksTrackingRegionsNoVtx + process.hltPixelTracksInRegionL1NoVtx )

	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksNoVtx.InputCollection = cms.InputTag("hltPixelTracksInRegionL1NoVtx")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksNoVtx.InputVertexCollection = cms.InputTag("")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksNoVtx.includeFourthHit = cms.bool(True)

	process.HLTIterL3IOmuonFromL1TkCandidateSequenceNoVtx = cms.Sequence( process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonNoVtx + process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonNoVtx )

	process.hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx.vertices = cms.InputTag("hltTrimmedPixelVertices")
	process.hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3FromL1MuonTrackCutClassifierNoVtx.mva.min3DLayers = cms.vint32( 0, 0, 0 )


	process.hltIterL3MuonMergedNoVtx.selectedTrackQuals = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurityNoVtx','hltIter0IterL3MuonTrackSelectionHighPurityNoVtx' )
	process.hltIterL3MuonMergedNoVtx.TrackProducers = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurityNoVtx','hltIter0IterL3MuonTrackSelectionHighPurityNoVtx' )

	process.hltIterL3MuonAndMuonFromL1MergedNoVtx.selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonMergedNoVtx','hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx' )
	process.hltIterL3MuonAndMuonFromL1MergedNoVtx.TrackProducers = cms.VInputTag( 'hltIterL3MuonMergedNoVtx','hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx' )

	process.hltIterL3MuonsNoVtx.TrackExtractorPSet.inputTrackCollection = cms.InputTag( "hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx")
	process.hltIterL3MuonsNoVtx.inputCollectionLabels = cms.VInputTag( 'hltIter0IterL3FromL1MuonTrackSelectionHighPurityNoVtx','hltL3MuonsIterL3LinksNoVtx' )

	return process



	
def customizeMuonHLTForPatatrackOpenMu(process, loadPatatrack=True, newProcessName = "MYHLT"):


	if loadPatatrack:
    	# -- modify process to create patatrack pixel tracks and vertices
		from HLTrigger.Configuration.customizeHLTforPatatrack import customizeHLTforPatatrackTriplets


		process.HLTRecoPixelTracksSequence = cms.Sequence()
		process.HLTRecopixelvertexingSequence = cms.Sequence()
		process.hltPixelTracksTrackingRegions = cms.EDProducer( "GlobalTrackingRegionFromBeamSpotEDProducer",
		    RegionPSet = cms.PSet( 
		      nSigmaZ = cms.double( 4.0 ),
		      beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
		      ptMin = cms.double( 0.8 ),
		      originRadius = cms.double( 0.02 ),
		      precise = cms.bool( True )
		    )
		)
		process.hltTrimmedPixelVertices = cms.EDProducer( "PixelVertexCollectionTrimmer",
		    src = cms.InputTag( "hltPixelVertices" ),
		    fractionSumPt2 = cms.double( 0.3 ),
		    minSumPt2 = cms.double( 0.0 ),
		    PVcomparer = cms.PSet(  refToPSet_ = cms.string( "HLTPSetPvClusterComparerForIT" ) ),
		    maxVtx = cms.uint32( 100 )
		)
		process.hltPixelTracksFitter = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
		    scaleErrorsForBPix1 = cms.bool( False ),
		    scaleFactor = cms.double( 0.65 )
		)
		process.hltPixelTracksFilter = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
		    nSigmaTipMaxTolerance = cms.double( 0.0 ),
		    chi2 = cms.double( 1000.0 ),
		    nSigmaInvPtTolerance = cms.double( 0.0 ),
		    ptMin = cms.double( 0.1 ),
		    tipMax = cms.double( 1.0 )
		)
	 
		process = customizeHLTforPatatrackTriplets(process)    

	process.hltPixelTracksInRegionL2OpenMu = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegionsOpenMu")

	)

	process.hltIterL3MuonPixelTracksTrackingRegionsOpenMu.Pt_min = cms.double( 0.0 )


	process.HLTIterL3MuonRecoPixelTracksOpenMuSequence = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3MuonPixelTracksTrackingRegionsOpenMu + process.hltPixelTracksInRegionL2OpenMu )

	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksOpenMu.InputCollection = cms.InputTag("hltPixelTracksInRegionL2OpenMu")
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksOpenMu.includeFourthHit = cms.bool(True)
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksOpenMu.InputVertexCollection = cms.InputTag("")

	process.hltIter0IterL3MuonTrackWithVertexSelectorOpenMu = cms.EDProducer("TrackWithVertexSelector",
	    # -- module configuration --
	    src = cms.InputTag('hltIter0IterL3MuonTrackSelectionHighPurityOpenMu'),
	    quality = cms.string("highPurity"),
	    useVtx = cms.bool(True),
	    vertexTag = cms.InputTag('hltTrimmedPixelVertices'),
	    nVertices = cms.uint32(5),
	    zetaVtxSig = cms.double(0.3),
	    rhoVtxSig = cms.double(0.1), ## tags used by b-tagging folks
	    zetaVtx = cms.double(0.3),
	    rhoVtx = cms.double(0.1), ## tags used by b-tagging folks
	    zetaVtxScale = cms.double(1.0),
	    rhoVtxScale = cms.double(1.0), ## tags used by b-tagging folks
	    vtxFallback = cms.bool(False),
	    copyExtras = cms.untracked.bool(True),
	    copyTrajectories = cms.untracked.bool(False),
	    # --------------------------
	    # -- these are the vertex compatibility cuts --
	    # ---------------------------------------------
	    # -- dummy selection on tracks --
	    etaMin = cms.double(0.0),
	    etaMax = cms.double(5.0),
	    ptMin = cms.double(0.00001),
	    ptMax = cms.double(999999.),
	    d0Max = cms.double(999999.),
	    dzMax = cms.double(999999.),
	    normalizedChi2 = cms.double(999999.),
	    numberOfValidHits = cms.uint32(0),
	    numberOfLostHits = cms.uint32(999),
	    numberOfValidPixelHits = cms.uint32(0),
	    numberOfValidPixelHitsForGood = cms.uint32(0),
	    numberOfValidHitsForGood = cms.uint32(0),
	    timesTag = cms.InputTag(""),
	    timeResosTag = cms.InputTag(""),
	    ptErrorCut = cms.double(999999.),
	    nSigmaDtVertex = cms.double(0)
	    # ------------------------------                                       
	)

	process.hltL3MuonsIterL3IOOpenMu.L3TrajBuilderParameters.tkTrajLabel = cms.InputTag("hltIter0IterL3MuonTrackWithVertexSelectorOpenMu")

	process.HLTIterativeTrackingIteration0ForIterL3MuonOpenMu = cms.Sequence( process.hltIter0IterL3MuonPixelSeedsFromPixelTracksOpenMu + process.hltIter0IterL3MuonCkfTrackCandidatesOpenMu + process.hltIter0IterL3MuonCtfWithMaterialTracksOpenMu + process.hltIter0IterL3MuonTrackCutClassifierOpenMu + process.hltIter0IterL3MuonTrackSelectionHighPurityOpenMu + process.hltIter0IterL3MuonTrackWithVertexSelectorOpenMu)

	process.HLTIterL3IOmuonTkCandidateOpenMuSequence = cms.Sequence( process.HLTIterL3MuonRecoPixelTracksOpenMuSequence + process.HLTIterativeTrackingIteration0ForIterL3MuonOpenMu + process.hltL3MuonsIterL3IOOpenMu )

	process.hltIter0IterL3MuonTrackCutClassifierOpenMu.vertices = cms.InputTag("hltTrimmedPixelVertices")
	process.hltIter0IterL3MuonTrackCutClassifierOpenMu.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3MuonTrackCutClassifierOpenMu.mva.min3DLayers = cms.vint32( 0, 0, 0 )


	process.hltPixelTracksInRegionL1OpenMu = cms.EDProducer("TrackSelectorByRegion",
	  produceTrackCollection = cms.bool(True),
	  produceMask = cms.bool(False),
	  tracks = cms.InputTag("hltPixelTracks"),
	  regions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegionsOpenMu")

	)

	process.hltIterL3FromL1MuonPixelTracksTrackingRegionsOpenMu.RegionPSet.ptMin = cms.double( 0.0 )
	process.hltIterL3FromL1MuonPixelTracksTrackingRegionsOpenMu.RegionPSet.maxNRegions = cms.int32( 5 )

	process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonOpenMu = cms.Sequence( process.HLTRecopixelvertexingSequence + process.hltIterL3FromL1MuonPixelTracksTrackingRegionsOpenMu + process.hltPixelTracksInRegionL1OpenMu )

	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksOpenMu.InputCollection = cms.InputTag("hltPixelTracksInRegionL1OpenMu")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksOpenMu.InputVertexCollection = cms.InputTag("")
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksOpenMu.includeFourthHit = cms.bool(True)

	process.hltIter0IterL3FromL1MuonTrackWithVertexSelectorOpenMu = cms.EDProducer("TrackWithVertexSelector",
	    # -- module configuration --
	    src = cms.InputTag('hltIter0IterL3FromL1MuonTrackSelectionHighPurityOpenMu'),
	    quality = cms.string("highPurity"),
	    useVtx = cms.bool(True),
	    vertexTag = cms.InputTag('hltTrimmedPixelVertices'),
	    nVertices = cms.uint32(5),
	    vtxFallback = cms.bool(False),
	    zetaVtx = cms.double(0.3),
	    zetaVtxScale = cms.double(1.0),
	    rhoVtxScale = cms.double(1.0), ## tags used by b-tagging folks
	    rhoVtx = cms.double(0.1), ## tags used by b-tagging folks
	    rhoVtxSig = cms.double(0.1), ## tags used by b-tagging folks
	    zetaVtxSig = cms.double(0.3),
	    copyExtras = cms.untracked.bool(True),
	    copyTrajectories = cms.untracked.bool(False),
	    # --------------------------
	    # -- these are the vertex compatibility cuts --
	    # ---------------------------------------------
	    # -- dummy selection on tracks --
	    etaMin = cms.double(0.0),
	    etaMax = cms.double(5.0),
	    ptMin = cms.double(0.00001),
	    ptMax = cms.double(999999.),
	    d0Max = cms.double(999999.),
	    dzMax = cms.double(999999.),
	    normalizedChi2 = cms.double(999999.),
	    numberOfValidHits = cms.uint32(0),
	    numberOfLostHits = cms.uint32(999),
	    numberOfValidPixelHits = cms.uint32(0),
	    numberOfValidPixelHitsForGood = cms.uint32(0),
	    numberOfValidHitsForGood = cms.uint32(0),
	    timesTag = cms.InputTag(""),
	    timeResosTag = cms.InputTag(""),
	    ptErrorCut = cms.double(999999.),
	    nSigmaDtVertex = cms.double(0),
	    # ------------------------------                                       
	)
	process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonOpenMu = cms.Sequence( process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksOpenMu + process.hltIter0IterL3FromL1MuonCkfTrackCandidatesOpenMu + process.hltIter0IterL3FromL1MuonCtfWithMaterialTracksOpenMu + process.hltIter0IterL3FromL1MuonTrackCutClassifierOpenMu + process.hltIter0IterL3FromL1MuonTrackSelectionHighPurityOpenMu + process.hltIter0IterL3FromL1MuonTrackWithVertexSelectorOpenMu )

	process.HLTIterL3IOmuonFromL1TkCandidateSequenceOpenMu = cms.Sequence( process.HLTRecopixelvertexingSequenceForIterL3FromL1MuonOpenMu + process.HLTIterativeTrackingIteration0ForIterL3FromL1MuonOpenMu )

	process.hltIter0IterL3FromL1MuonTrackCutClassifierOpenMu.vertices = cms.InputTag("hltTrimmedPixelVertices")
	process.hltIter0IterL3FromL1MuonTrackCutClassifierOpenMu.mva.minPixelHits = cms.vint32( 0, 0, 0 )
	process.hltIter0IterL3FromL1MuonTrackCutClassifierOpenMu.mva.min3DLayers = cms.vint32( 0, 0, 0 )


	process.hltIterL3MuonMergedOpenMu.selectedTrackQuals = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurityOpenMu','hltIter0IterL3MuonTrackWithVertexSelectorOpenMu' )
	process.hltIterL3MuonMergedOpenMu.TrackProducers = cms.VInputTag( 'hltIterL3OIMuonTrackSelectionHighPurityOpenMu','hltIter0IterL3MuonTrackWithVertexSelectorOpenMu' )

	process.hltIterL3MuonAndMuonFromL1MergedOpenMu.selectedTrackQuals = cms.VInputTag( 'hltIterL3MuonMergedOpenMu','hltIter0IterL3FromL1MuonTrackWithVertexSelectorOpenMu' )
	process.hltIterL3MuonAndMuonFromL1MergedOpenMu.TrackProducers = cms.VInputTag( 'hltIterL3MuonMergedOpenMu','hltIter0IterL3FromL1MuonTrackWithVertexSelectorOpenMu' )

	process.hltIterL3MuonsOpenMu.inputTrackCollection = cms.InputTag( "hltIter0IterL3FromL1MuonTrackWithVertexSelectorOpenMu")

	return process




def customizerFuncForMuonHLTSeeding(
    process, newProcessName = "MYHLT",
    doSort = False,
    nSeedsMaxBs = (99999, 99999), nSeedsMaxEs = (99999, 99999),
    mvaCutBs = (0.01, 0.01), mvaCutEs = (0.01, 0.01)):

    from . import mvaScale as _mvaScale

    # print "\nCustomizing Seed MVA Classifier:"
    # print "\tdoSort:      ", doSort
    # print "\tnSeedsMaxBs: ", nSeedsMaxBs
    # print "\tnSeedsMaxEs: ", nSeedsMaxEs
    # print "\tmvaCutBs:    ", mvaCutBs
    # print "\tmvaCutEs:    ", mvaCutEs

    # -- Seed MVA Classifiers
    process.hltIter2IterL3MuonPixelSeedsFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
        rejectAll = cms.bool(False),
        isFromL1 = cms.bool(False),

        src    = cms.InputTag("hltIter2IterL3MuonPixelSeeds", "", newProcessName),
        L1Muon = cms.InputTag("hltGtStage2Digis", "Muon", newProcessName),
        L2Muon = cms.InputTag("hltL2MuonCandidates", "", newProcessName),

        mvaFileBL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v7Fast_Barrel_hltIter2.xml"),
        mvaFileEL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v7Fast_Endcap_hltIter2.xml"),

        mvaScaleMeanBL2 = cms.vdouble( getattr(_mvaScale, "v7Fast_Barrel_hltIter2_ScaleMean") ),
        mvaScaleStdBL2  = cms.vdouble( getattr(_mvaScale, "v7Fast_Barrel_hltIter2_ScaleStd") ),
        mvaScaleMeanEL2 = cms.vdouble( getattr(_mvaScale, "v7Fast_Endcap_hltIter2_ScaleMean") ),
        mvaScaleStdEL2  = cms.vdouble( getattr(_mvaScale, "v7Fast_Endcap_hltIter2_ScaleStd") ),

        doSort = cms.bool(doSort),
        nSeedsMaxB = cms.int32(nSeedsMaxBs[0]),
        nSeedsMaxE = cms.int32(nSeedsMaxEs[0]),

        mvaCutB = cms.double(mvaCutBs[0]),
        mvaCutE = cms.double(mvaCutEs[0])
    )
    process.hltIter2IterL3FromL1MuonPixelSeedsFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
        rejectAll = cms.bool(False),
        isFromL1 = cms.bool(True),

        src    = cms.InputTag("hltIter2IterL3FromL1MuonPixelSeeds", "", newProcessName),
        L1Muon = cms.InputTag("hltGtStage2Digis", "Muon", newProcessName),
        L2Muon = cms.InputTag("hltL2MuonCandidates", "", newProcessName),

        mvaFileBL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v7Fast_Barrel_hltIter2FromL1.xml"),
        mvaFileEL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v7Fast_Endcap_hltIter2FromL1.xml"),

        mvaScaleMeanBL1 = cms.vdouble( getattr(_mvaScale, "v7Fast_Barrel_hltIter2FromL1_ScaleMean") ),
        mvaScaleStdBL1  = cms.vdouble( getattr(_mvaScale, "v7Fast_Barrel_hltIter2FromL1_ScaleStd") ),
        mvaScaleMeanEL1 = cms.vdouble( getattr(_mvaScale, "v7Fast_Endcap_hltIter2FromL1_ScaleMean") ),
        mvaScaleStdEL1  = cms.vdouble( getattr(_mvaScale, "v7Fast_Endcap_hltIter2FromL1_ScaleStd") ),

        doSort = cms.bool(doSort),
        nSeedsMaxB = cms.int32(nSeedsMaxBs[1]),
        nSeedsMaxE = cms.int32(nSeedsMaxEs[1]),

        mvaCutB = cms.double(mvaCutBs[1]),
        mvaCutE = cms.double(mvaCutEs[1])
    )

    # -- Track Candidates
    process.hltIter2IterL3MuonCkfTrackCandidates.src       = cms.InputTag("hltIter2IterL3MuonPixelSeedsFiltered", "", newProcessName)
    process.hltIter2IterL3FromL1MuonCkfTrackCandidates.src = cms.InputTag("hltIter2IterL3FromL1MuonPixelSeedsFiltered", "", newProcessName)

    # -- Sequences
    process.HLTIterativeTrackingIteration2ForIterL3Muon = cms.Sequence(
        process.hltIter2IterL3MuonClustersRefRemoval+
        process.hltIter2IterL3MuonMaskedMeasurementTrackerEvent+
        process.hltIter2IterL3MuonPixelLayerTriplets+
        process.hltIter2IterL3MuonPixelClusterCheck+
        process.hltIter2IterL3MuonPixelHitDoublets+
        process.hltIter2IterL3MuonPixelHitTriplets+
        process.hltIter2IterL3MuonPixelSeeds+
        process.hltIter2IterL3MuonPixelSeedsFiltered+
        process.hltIter2IterL3MuonCkfTrackCandidates+
        process.hltIter2IterL3MuonCtfWithMaterialTracks+
        process.hltIter2IterL3MuonTrackCutClassifier+
        process.hltIter2IterL3MuonTrackSelectionHighPurity
    )
    process.HLTIterativeTrackingIteration2ForIterL3FromL1Muon = cms.Sequence(
        process.hltIter2IterL3FromL1MuonClustersRefRemoval+
        process.hltIter2IterL3FromL1MuonMaskedMeasurementTrackerEvent+
        process.hltIter2IterL3FromL1MuonPixelLayerTriplets+
        process.hltIter2IterL3FromL1MuonPixelClusterCheck+
        process.hltIter2IterL3FromL1MuonPixelHitDoublets+
        process.hltIter2IterL3FromL1MuonPixelHitTriplets+
        process.hltIter2IterL3FromL1MuonPixelSeeds+
        process.hltIter2IterL3FromL1MuonPixelSeedsFiltered+
        process.hltIter2IterL3FromL1MuonCkfTrackCandidates+
        process.hltIter2IterL3FromL1MuonCtfWithMaterialTracks+
        process.hltIter2IterL3FromL1MuonTrackCutClassifier+
        process.hltIter2IterL3FromL1MuonTrackSelectionHighPurity
    )

    return process

def customizeIOSeedingPatatrack(
	process, newProcessName = "MYHLT",
	doSort = False,
	nSeedsMaxBs = (99999, 99999), nSeedsMaxEs = (99999, 99999),
	mvaCutBs = (0.01, 0.01), mvaCutEs = (0.01, 0.01)):

	from . import mvaScale as _mvaScale

	# -- Seed MVA Classifiers
	process.hltIter0IterL3MuonPixelSeedsFromPixelTracksFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
		rejectAll = cms.bool(False),
		isFromL1 = cms.bool(False),

		src    = cms.InputTag("hltIter0IterL3MuonPixelSeedsFromPixelTracks", "", newProcessName),
		L1Muon = cms.InputTag("hltGtStage2Digis", "Muon", newProcessName),
		L2Muon = cms.InputTag("hltL2MuonCandidates", "", newProcessName),

		mvaFileBL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v8Pre_Barrel_hltIter2.xml"),
		mvaFileEL2 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v8Pre_Endcap_hltIter2.xml"),

		mvaScaleMeanBL2 = cms.vdouble( getattr(_mvaScale, "v8Pre_Barrel_hltIter2_ScaleMean") ),
		mvaScaleStdBL2  = cms.vdouble( getattr(_mvaScale, "v8Pre_Barrel_hltIter2_ScaleStd") ),
		mvaScaleMeanEL2 = cms.vdouble( getattr(_mvaScale, "v8Pre_Endcap_hltIter2_ScaleMean") ),
		mvaScaleStdEL2  = cms.vdouble( getattr(_mvaScale, "v8Pre_Endcap_hltIter2_ScaleStd") ),

		doSort = cms.bool(doSort),
		nSeedsMaxB = cms.int32(nSeedsMaxBs[0]),
		nSeedsMaxE = cms.int32(nSeedsMaxEs[0]),

		mvaCutB = cms.double(mvaCutBs[0]),
		mvaCutE = cms.double(mvaCutEs[0])
	)
	process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered = cms.EDProducer("MuonHLTSeedMVAClassifier",
		rejectAll = cms.bool(False),
		isFromL1 = cms.bool(True),

		src    = cms.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks", "", newProcessName),
		L1Muon = cms.InputTag("hltGtStage2Digis", "Muon", newProcessName),
		L2Muon = cms.InputTag("hltL2MuonCandidates", "", newProcessName),

		mvaFileBL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v8Pre_Barrel_hltIter2FromL1.xml"),
		mvaFileEL1 = cms.FileInPath("RecoMuon/TrackerSeedGenerator/data/v8Pre_Endcap_hltIter2FromL1.xml"),

		mvaScaleMeanBL1 = cms.vdouble( getattr(_mvaScale, "v8Pre_Barrel_hltIter2FromL1_ScaleMean") ),
		mvaScaleStdBL1  = cms.vdouble( getattr(_mvaScale, "v8Pre_Barrel_hltIter2FromL1_ScaleStd") ),
		mvaScaleMeanEL1 = cms.vdouble( getattr(_mvaScale, "v8Pre_Endcap_hltIter2FromL1_ScaleMean") ),
		mvaScaleStdEL1  = cms.vdouble( getattr(_mvaScale, "v8Pre_Endcap_hltIter2FromL1_ScaleStd") ),

		doSort = cms.bool(doSort),
		nSeedsMaxB = cms.int32(nSeedsMaxBs[1]),
		nSeedsMaxE = cms.int32(nSeedsMaxEs[1]),

		mvaCutB = cms.double(mvaCutBs[1]),
		mvaCutE = cms.double(mvaCutEs[1])
	)

	# -- Track Candidates
	process.hltIter0IterL3MuonCkfTrackCandidates.src       = cms.InputTag("hltIter0IterL3MuonPixelSeedsFromPixelTracksFiltered", "", newProcessName)
	process.hltIter0IterL3FromL1MuonCkfTrackCandidates.src = cms.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered", "", newProcessName)

	# -- Sequences
	process.HLTIterativeTrackingIteration0ForIterL3Muon = cms.Sequence(
		process.hltIter0IterL3MuonPixelSeedsFromPixelTracks +
		process.hltIter0IterL3MuonPixelSeedsFromPixelTracksFiltered +
		process.hltIter0IterL3MuonCkfTrackCandidates +
		process.hltIter0IterL3MuonCtfWithMaterialTracks +
		process.hltIter0IterL3MuonTrackCutClassifier +
		process.hltIter0IterL3MuonTrackSelectionHighPurity
	)
	process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon = cms.Sequence(
		process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks +
		process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracksFiltered +
		process.hltIter0IterL3FromL1MuonCkfTrackCandidates +
		process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks +
		process.hltIter0IterL3FromL1MuonTrackCutClassifier +
		process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity 
	)

	return process


def customizeDoubleMuIsoFix(process, newProcessName = "MYHLT"):
	if hasattr(process, "hltL3MuonRelTrkIsolationVVL"):
		process.hltL3MuonRelTrkIsolationVVL.TrkExtractorPSet.inputTrackCollection = cms.InputTag('hltIter2L3MuonMerged', '', newProcessName)

	return process


def customizeMuonHLTForAll(process, newProcessName = "MYHLT",
                           doDoubletRemoval = True,
                           doGEM = True,
                           doPatatrack = True,
                           doOISeeding = True,
                           doIOSeeding = True):

	process = customizeMuonHLTForCscSegment(process, newProcessName = newProcessName)
	process = customizeDoubleMuIsoFix(process, newProcessName = newProcessName)

	if doDoubletRemoval:
		process = customizeMuonHLTForDoubletRemoval(process, newProcessName = newProcessName)

	if doGEM:
		process = customizeMuonHLTForGEM(process, newProcessName = newProcessName)

	if doPatatrack:
		process = customizeMuonHLTForPatatrackWithIsoAndTriplets(process, newProcessName = newProcessName)

	if doOISeeding:
		from RecoMuon.TrackerSeedGenerator.customizeOIseeding import customizeOIseeding
		process = customizeOIseeding(process)

	if doIOSeeding:
		process = customizeIOSeedingPatatrack(process, newProcessName = newProcessName)

	return process
