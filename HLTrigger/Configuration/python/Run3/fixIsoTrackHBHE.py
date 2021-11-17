## Use PixelQuadruplets in HLT_IsoTrackHE_v and HLT_IsoTrackHB_v to keep timing under control
import FWCore.ParameterSet.Config as cms
def fixIsoTrackHBHE(process):
    process.hltPixelTracksQuadruplets = cms.EDProducer("TrackWithVertexSelector",
        copyExtras = cms.untracked.bool(False),
        copyTrajectories = cms.untracked.bool(False),
        d0Max = cms.double(999.0),
        dzMax = cms.double(999.0),
        etaMax = cms.double(999.0),
        etaMin = cms.double(-999.0),
        nSigmaDtVertex = cms.double(0.0),
        nVertices = cms.uint32(0),
        normalizedChi2 = cms.double(999999.0),
        numberOfLostHits = cms.uint32(999),
        numberOfValidHits = cms.uint32(0),
        numberOfValidPixelHits = cms.uint32(4),
        ptErrorCut = cms.double(999999.0),
        ptMax = cms.double(999999.0),
        ptMin = cms.double(0.),
        quality = cms.string('loose'),
        rhoVtx = cms.double(999999.0),
        src = cms.InputTag("hltPixelTracks"),
        timeResosTag = cms.InputTag(""),
        timesTag = cms.InputTag(""),
        useVtx = cms.bool(False),
        vertexTag = cms.InputTag("hltTrimmedPixelVertices"),
        vtxFallback = cms.bool(False),
        zetaVtx = cms.double(999999.0),
    )
    
    HLT_IsoTrackHE_matches = [path for path in process.pathNames().split(" ") if "HLT_IsoTrackHE_v" in path]
    for HLT_IsoTrackHE in HLT_IsoTrackHE_matches:
        if process.hltIsolPixelTrackProdHE.PixelTracksSources[0]=="hltPixelTracks": 
            process.hltIsolPixelTrackProdHE.PixelTracksSources=['hltPixelTracksQuadruplets']
            getattr(process,HLT_IsoTrackHE).insert ( getattr(process,HLT_IsoTrackHE).index(process.hltIsolPixelTrackProdHE) , process.hltPixelTracksQuadruplets)
        
    
    HLT_IsoTrackHB_matches = [path for path in process.pathNames().split(" ") if "HLT_IsoTrackHB_v" in path]
    for HLT_IsoTrackHB in HLT_IsoTrackHB_matches:
        if process.hltIsolPixelTrackProdHB.PixelTracksSources[0]=="hltPixelTracks": 
            process.hltIsolPixelTrackProdHB.PixelTracksSources=['hltPixelTracksQuadruplets']
            getattr(process,HLT_IsoTrackHB).insert ( getattr(process,HLT_IsoTrackHB).index(process.hltIsolPixelTrackProdHB) , process.hltPixelTracksQuadruplets)
    
    return process

