import copy
import FWCore.ParameterSet.Config as cms
from HLTrigger.Configuration.common import *
from HLTrigger.Configuration.customizeHLTforPatatrack import *
from Configuration.ProcessModifiers.pixelNtupletFit_cff import pixelNtupletFit
from Configuration.ProcessModifiers.gpu_cff import gpu

def customizeHLTforRun3Tracking(process):
    
    process.extend(pixelNtupletFit)
    process.extend(gpu)

    process = customizeHLTforPatatrackTriplets(process)    
    if hasattr(process,'hltPixelTracksCUDA'):
        process.hltPixelTracksCUDA.includeJumpingForwardDoublets = cms.bool(True)
        process.hltPixelTracksCUDA.idealConditions               = cms.bool(False)
        process.hltPixelTracksCUDA.fillStatistics                = cms.bool(True)
        process.hltPixelTracksCUDA.useSimpleTripletCleaner       = cms.bool(False)
    if hasattr(process,'hltPixelTracksSoA'):
        process.hltPixelTracksSoA.cpu.includeJumpingForwardDoublets = cms.bool(True)
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
        process.hltMergedTracks = process.hltIter0PFlowTrackSelectionHighPurity.clone()

    process.HLTIterativeTrackingIteration0Task = cms.Sequence(
        process.hltIter0PFLowPixelSeedsFromPixelTracks +
        process.hltIter0PFlowCkfTrackCandidates +
        process.hltIter0PFlowCtfWithMaterialTracks +
        process.hltIter0PFlowTrackCutClassifier +
        process.hltMergedTracks
    )
    if hasattr(process,'HLTIterativeTrackingIteration0'):
        process.HLTIterativeTrackingIteration0 = cms.Sequence( process.HLTIterativeTrackingIteration0Task )
    
    if hasattr(process,'HLTIterativeTrackingIter02'):
        process.HLTIterativeTrackingIter02 = cms.Sequence( process.HLTIterativeTrackingIteration0 )
    
    if hasattr(process,'MC_ReducedIterativeTracking_v12'):
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
