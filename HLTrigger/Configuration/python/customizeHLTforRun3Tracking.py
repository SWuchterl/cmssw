import copy
import FWCore.ParameterSet.Config as cms
from HLTrigger.Configuration.common import *
from HLTrigger.Configuration.customizeHLTforPatatrack import *
from Configuration.ProcessModifiers.pixelNtupletFit_cff import pixelNtupletFit
from Configuration.ProcessModifiers.gpu_cff import gpu

### Default
def customizeHLTforRun3Tracking(process):
    
    process.extend(pixelNtupletFit)
    process.extend(gpu)

    for producer in producers_by_type(process, "TrackWithVertexSelector"):
        if not hasattr(producer,'numberOfValidHitsForGood'):
            producer.numberOfValidHitsForGood = cms.uint32(999)
        if not hasattr(producer,'numberOfValidPixelHitsForGood'):
            producer.numberOfValidPixelHitsForGood = cms.uint32(999)
        if not hasattr(producer,'zetaVtxScale'):
            producer.zetaVtxScale = cms.double(1.0)
        if not hasattr(producer,'rhoVtxScale'):
            producer.rhoVtxScale = cms.double(1.0)
        if not hasattr(producer,'zetaVtxSig'):
            producer.zetaVtxSig = cms.double(999.0)
        if not hasattr(producer,'rhoVtxSig'):
            producer.rhoVtxSig = cms.double(999.0)
            
    process = customizeHLTforPatatrack(process)    
    if hasattr(process,'hltPixelTracksCUDA'):
        process.hltPixelTracksCUDA.includeJumpingForwardDoublets = cms.bool(True)
        process.hltPixelTracksCUDA.minHitsPerNtuplet             = cms.uint32(3)
        process.hltPixelTracksCUDA.idealConditions               = cms.bool(False)
        process.hltPixelTracksCUDA.fillStatistics                = cms.bool(True)
        process.hltPixelTracksCUDA.useSimpleTripletCleaner       = cms.bool(False)
    if hasattr(process,'hltPixelTracksSoA'):
        process.hltPixelTracksSoA.cpu.includeJumpingForwardDoublets = cms.bool(True)
        process.hltPixelTracksSoA.cpu.minHitsPerNtuplet             = cms.uint32(3)
        process.hltPixelTracksSoA.cpu.idealConditions               = cms.bool(False)
        process.hltPixelTracksSoA.cpu.fillStatistics                = cms.bool(True)
        process.hltPixelTracksSoA.cpu.useSimpleTripletCleaner       = cms.bool(False)

    if hasattr(process,'hltPixelTracks'):
        process.hltPixelTracks.minNumberOfHits = cms.int32(0)
        process.hltPixelTracks.minQuality = cms.string('loose')

    if hasattr(process,'HLTIter0PSetTrajectoryFilterIT'):
        process.HLTIter0PSetTrajectoryFilterIT.minHitsMinPt        = cms.int32(3)
        process.HLTIter0PSetTrajectoryFilterIT.minimumNumberOfHits = cms.int32(3)

    if hasattr(process,'hltSiStripRawToClustersFacility'):
        process.hltSiStripRawToClustersFacility.onDemand = cms.bool( False )

    if hasattr(process,'hltIter0PFLowPixelSeedsFromPixelTracks'):
        process.hltIter0PFLowPixelSeedsFromPixelTracks.includeFourthHit = cms.bool(True)

    if hasattr(process,'hltIter0PFlowTrackCutClassifier'):
        #delattr(process,'hltIter0PFlowTrackCutClassifier')
        process.hltIter0PFlowTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
            src = cms.InputTag("hltIter0PFlowCtfWithMaterialTracks"),
            beamspot = cms.InputTag("hltOnlineBeamSpot"),
            vertices = cms.InputTag("hltTrimmedPixelVertices"),
            qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
            mva = cms.PSet(
                minPixelHits = cms.vint32(0, 0, 0),
                maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
                dr_par = cms.PSet(
                    d0err = cms.vdouble(0.003, 0.003, 0.003),
                    dr_par2 = cms.vdouble(3.40282346639e+38, 0.6, 0.6),
                    dr_par1 = cms.vdouble(3.40282346639e+38, 0.8, 0.8),
                    dr_exp = cms.vint32(4, 4, 4),
                    d0err_par = cms.vdouble(0.001, 0.001, 0.001)
                ),
                maxLostLayers = cms.vint32(1, 1, 1),
                min3DLayers = cms.vint32(0, 0, 0),
                dz_par = cms.PSet(
                    dz_par1 = cms.vdouble(3.40282346639e+38, 0.75, 0.75),
                    dz_par2 = cms.vdouble(3.40282346639e+38, 0.5, 0.5),
                    dz_exp = cms.vint32(4, 4, 4)
                ),
                minNVtxTrk = cms.int32(3),
                maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
                minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
                maxChi2 = cms.vdouble(9999.0, 25.0, 16.0),
                maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
                maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
                minLayers = cms.vint32(3, 3, 3)
            ),
            ignoreVertices = cms.bool(False)
        )
    
    if hasattr(process,'hltMergedTracks'):
        #delattr(process,'hltMergedTracks')
        process.hltMergedTracks = process.hltIter0PFlowTrackSelectionHighPurity.clone()

    process.HLTIterativeTrackingIteration0Task = cms.Task(
        process.hltIter0PFLowPixelSeedsFromPixelTracks,
        process.hltIter0PFlowCkfTrackCandidates,
        process.hltIter0PFlowCtfWithMaterialTracks,
        process.hltIter0PFlowTrackCutClassifier,
        process.hltMergedTracks
    )
    if hasattr(process,'HLTIterativeTrackingIteration0'):
        #delattr(process,'HLTIterativeTrackingIteration0')
        process.HLTIterativeTrackingIteration0 = cms.Sequence( process.HLTIterativeTrackingIteration0Task )
    
    if hasattr(process,'HLTIterativeTrackingIter02'):
        #delattr(process,'HLTIterativeTrackingIter02')
        process.HLTIterativeTrackingIter02 = cms.Sequence( process.HLTIterativeTrackingIteration0 )
    
    if hasattr(process,'MC_ReducedIterativeTracking_v12'):
        #delattr(process,'MC_ReducedIterativeTracking_v12')
        process.MC_ReducedIterativeTracking_v12 = cms.Path( 
            process.HLTBeginSequence +
            process.hltPreMCReducedIterativeTracking +
            process.HLTDoLocalPixelSequence +
            process.HLTRecopixelvertexingSequence +
            process.HLTDoLocalStripSequence +
            process.HLTIterativeTrackingIter02 +
            process.HLTEndSequence
        )

    return process


### Using quadruplet pixel tracks from any pixel vertex
def customizeHLTforRun3TrackingAllPixelVertices(process):

    process.extend(pixelNtupletFit)
    process.extend(gpu)

    for producer in producers_by_type(process, "TrackWithVertexSelector"):
        if not hasattr(producer,'numberOfValidHitsForGood'):
            producer.numberOfValidHitsForGood = cms.uint32(999)
        if not hasattr(producer,'numberOfValidPixelHitsForGood'):
            producer.numberOfValidPixelHitsForGood = cms.uint32(999)
        if not hasattr(producer,'zetaVtxScale'):
            producer.zetaVtxScale = cms.double(1.0)
        if not hasattr(producer,'rhoVtxScale'):
            producer.rhoVtxScale = cms.double(1.0)
        if not hasattr(producer,'zetaVtxSig'):
            producer.zetaVtxSig = cms.double(999.0)
        if not hasattr(producer,'rhoVtxSig'):
            producer.rhoVtxSig = cms.double(999.0)
    
    process = customizeHLTforPatatrack(process)    
    if hasattr(process,'hltPixelTracksCUDA'):
        process.hltPixelTracksCUDA.includeJumpingForwardDoublets = cms.bool(True)
        process.hltPixelTracksCUDA.minHitsPerNtuplet             = cms.uint32(3)
        process.hltPixelTracksCUDA.idealConditions               = cms.bool(False)
        process.hltPixelTracksCUDA.fillStatistics                = cms.bool(True)
    if hasattr(process,'hltPixelTracksSoA'):
        process.hltPixelTracksSoA.cpu.includeJumpingForwardDoublets = cms.bool(True)
        process.hltPixelTracksSoA.cpu.minHitsPerNtuplet             = cms.uint32(3)
        process.hltPixelTracksSoA.cpu.idealConditions               = cms.bool(False)
        process.hltPixelTracksSoA.cpu.fillStatistics                = cms.bool(True)

    if hasattr(process,'hltPixelTracks'):
        process.hltPixelTracks.minNumberOfHits = cms.int32(0)
        process.hltPixelTracks.minQuality = cms.string('loose')

    if hasattr(process,'HLTIter0PSetTrajectoryFilterIT'):
        process.HLTIter0PSetTrajectoryFilterIT.minHitsMinPt        = cms.int32(3)
        process.HLTIter0PSetTrajectoryFilterIT.minimumNumberOfHits = cms.int32(3)

    if hasattr(process,'hltSiStripRawToClustersFacility'):
        process.hltSiStripRawToClustersFacility.onDemand = cms.bool( False )

    process.hltPixelTracksClean = cms.EDProducer("TrackWithVertexSelector",
        src = cms.InputTag('hltPixelTracks'),
        etaMin = cms.double(0.0),
        etaMax = cms.double(5.0),
        ptMin = cms.double(0.0),
        ptMax = cms.double(999999.),
        d0Max = cms.double(999.),
        dzMax = cms.double(999.),
        normalizedChi2 = cms.double(999999.),
        numberOfValidHits = cms.uint32(0),
        numberOfValidPixelHits = cms.uint32(0),
        numberOfValidHitsForGood = cms.uint32(4),
        numberOfValidPixelHitsForGood = cms.uint32(4),
        numberOfLostHits = cms.uint32(999),
        ptErrorCut = cms.double(999999.),
        quality = cms.string("loose"),
        useVtx = cms.bool(True),
        vertexTag = cms.InputTag('hltPixelVertices'),
        timesTag = cms.InputTag(''),
        timeResosTag = cms.InputTag(''),
        nVertices = cms.uint32(100),
        vtxFallback = cms.bool(True),
        zetaVtx = cms.double(0.3),
        rhoVtx = cms.double(0.1),
        zetaVtxScale = cms.double(5.0),
        rhoVtxScale = cms.double(2.5), 
        zetaVtxSig = cms.double(2.0),
        rhoVtxSig = cms.double(2.0),
        nSigmaDtVertex = cms.double(0),
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False)
    )

    if hasattr(process,'hltIter0PFLowPixelSeedsFromPixelTracks'):
        process.hltIter0PFLowPixelSeedsFromPixelTracks.includeFourthHit = cms.bool(True)
        process.hltIter0PFLowPixelSeedsFromPixelTracks.InputVertexCollection = cms.InputTag( "hltPixelVertices" )
        process.hltIter0PFLowPixelSeedsFromPixelTracks.InputCollection = cms.InputTag("hltPixelTracksClean")
    
    if hasattr(process,'hltIter0PFlowTrackCutClassifier'):
        #delattr(process,'hltIter0PFlowTrackCutClassifier')
        process.hltIter0PFlowTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
            src = cms.InputTag("hltIter0PFlowCtfWithMaterialTracks"),
            beamspot = cms.InputTag("hltOnlineBeamSpot"),
            vertices = cms.InputTag("hltTrimmedPixelVertices"),
            qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
            mva = cms.PSet(
                minPixelHits = cms.vint32(0, 0, 0),
                maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 15.0),
                dr_par = cms.PSet(
                    d0err = cms.vdouble(0.003, 0.003, 0.003),
                    dr_par2 = cms.vdouble(3.40282346639e+38, 0.6, 0.6),
                    dr_par1 = cms.vdouble(3.40282346639e+38, 0.8, 0.8),
                    dr_exp = cms.vint32(4, 4, 4),
                    d0err_par = cms.vdouble(0.001, 0.001, 0.001)
                ),
                maxLostLayers = cms.vint32(1, 1, 1),
                min3DLayers = cms.vint32(0, 0, 0),
                dz_par = cms.PSet(
                    dz_par1 = cms.vdouble(3.40282346639e+38, 0.75, 0.75),
                    dz_par2 = cms.vdouble(3.40282346639e+38, 0.5, 0.5),
                    dz_exp = cms.vint32(4, 4, 4)
                ),
                minNVtxTrk = cms.int32(3),
                maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
                minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
                maxChi2 = cms.vdouble(9999.0, 25.0, 16.0),
                maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
                maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
                minLayers = cms.vint32(3, 3, 3)
            ),
            ignoreVertices = cms.bool(False)
        )
    
    if hasattr(process,'hltMergedTracks'):
        #delattr(process,'hltMergedTracks')
        process.hltMergedTracks = process.hltIter0PFlowTrackSelectionHighPurity.clone()

    process.HLTIterativeTrackingIteration0Task = cms.Task(
        process.hltPixelTracksClean,
        process.hltIter0PFLowPixelSeedsFromPixelTracks,
        process.hltIter0PFlowCkfTrackCandidates,
        process.hltIter0PFlowCtfWithMaterialTracks,
        process.hltIter0PFlowTrackCutClassifier,
        process.hltMergedTracks
    )
    if hasattr(process,'HLTIterativeTrackingIteration0'):
        #delattr(process,'HLTIterativeTrackingIteration0')
        process.HLTIterativeTrackingIteration0 = cms.Sequence( process.HLTIterativeTrackingIteration0Task )
    
    if hasattr(process,'HLTIterativeTrackingIter02'):
        #delattr(process,'HLTIterativeTrackingIter02')
        process.HLTIterativeTrackingIter02 = cms.Sequence( process.HLTIterativeTrackingIteration0 )
    
    if hasattr(process,'MC_ReducedIterativeTracking_v12'):
        #delattr(process,'MC_ReducedIterativeTracking_v12')
        process.MC_ReducedIterativeTracking_v12 = cms.Path( 
            process.HLTBeginSequence +
            process.hltPreMCReducedIterativeTracking +
            process.HLTDoLocalPixelSequence +
            process.HLTRecopixelvertexingSequence +
            process.HLTDoLocalStripSequence +
            process.HLTIterativeTrackingIter02 +
            process.HLTEndSequence
        )

    return process
