#include "RecoBTag/FeatureTools/interface/LostTracksConverter.h"

namespace btagbtvdeep {

  void packedCandidateToFeatures(const pat::PackedCandidate* c_pf,
                                 const pat::Jet& jet,
                                 const TrackInfoBuilder& track_info,
                                 const bool isWeightedJet,
                                 const float drminpfcandsv,
                                 const float jetR,
                                 const float puppiw,
                                 LostTracksFeatures& lt_features,
                                 const bool flip,
                                 const float distminpfcandsv) {
    commonCandidateToFeatures(
        c_pf, jet, track_info, isWeightedJet, drminpfcandsv, jetR, puppiw, lt_features, flip, distminpfcandsv);

    lt_features.puppiw = puppiw;
    lt_features.charge = c_pf->charge();

    lt_features.lostInnerHits = catch_infs(c_pf->lostInnerHits(), 2);
    lt_features.numberOfPixelHits = catch_infs(c_pf->numberOfPixelHits(), -1);
    lt_features.numberOfStripHits = catch_infs(c_pf->stripLayersWithMeasurement(), -1);

    lt_features.HadFrac = c_pf->hcalFraction();
    lt_features.CaloFrac = c_pf->caloFraction();

    lt_features.dz = c_pf->dz();
    lt_features.px = c_pf->px();
    lt_features.py = c_pf->py();
    lt_features.pz = c_pf->pz();

    // if PackedCandidate does not have TrackDetails this gives an Exception
    // because unpackCovariance might be called for pseudoTrack/bestTrack
    if (c_pf->hasTrackDetails()) {
      const auto& pseudo_track = c_pf->pseudoTrack();
      lt_features.chi2 = catch_infs_and_bound(pseudo_track.normalizedChi2(), 300, -1, 300);
      // this returns the quality enum not a mask.
      lt_features.quality = pseudo_track.qualityMask();
    } else {
      // default negative chi2 and loose track if notTrackDetails
      lt_features.chi2 = catch_infs_and_bound(-1, 300, -1, 300);
      lt_features.quality = (1 << reco::TrackBase::loose);
    }

    float pdgid_;
    if (abs(c_pf->pdgId()) == 11 and c_pf->charge() != 0) {
      pdgid_ = 0.0;
    } else if (abs(c_pf->pdgId()) == 13 and c_pf->charge() != 0) {
      pdgid_ = 1.0;
    } else if (abs(c_pf->pdgId()) == 22 and c_pf->charge() == 0) {
      pdgid_ = 2.0;
    } else if (abs(c_pf->pdgId()) != 22 and c_pf->charge() == 0 and abs(c_pf->pdgId()) != 1 and
               abs(c_pf->pdgId()) != 2) {
      pdgid_ = 3.0;
    } else if (abs(c_pf->pdgId()) != 11 and abs(c_pf->pdgId()) != 13 and c_pf->charge() != 0) {
      pdgid_ = 4.0;
    } else if (c_pf->charge() == 0 and abs(c_pf->pdgId()) == 1) {
      pdgid_ = 5.0;
    } else if (c_pf->charge() == 0 and abs(c_pf->pdgId()) == 2) {
      pdgid_ = 6.0;
    } else {
      pdgid_ = 7.0;
    }
    lt_features.pdgID = pdgid_;


  }
  void recoCandidateToFeatures(const reco::PFCandidate* c_pf,
                               const reco::Jet& jet,
                               const TrackInfoBuilder& track_info,
                               const bool isWeightedJet,
                               const float drminpfcandsv,
                               const float jetR,
                               const float puppiw,
                               const int pv_ass_quality,
                               const reco::VertexRef& pv,
                               LostTracksFeatures& lt_features,
                               const bool flip,
                               const float distminpfcandsv) {
    commonCandidateToFeatures(
        c_pf, jet, track_info, isWeightedJet, drminpfcandsv, jetR, puppiw, lt_features, flip, distminpfcandsv);

    lt_features.puppiw = puppiw;

    const auto& pseudo_track = (c_pf->bestTrack()) ? *c_pf->bestTrack() : reco::Track();
    lt_features.chi2 = catch_infs_and_bound(std::floor(pseudo_track.normalizedChi2()), 300, -1, 300);
    lt_features.quality = quality_from_pfcand(*c_pf);

    lt_features.charge = c_pf->charge();

    int lostHits = 0;
    int nlost = pseudo_track.hitPattern().numberOfLostHits(reco::HitPattern::MISSING_INNER_HITS);
    if (nlost == 0) {
      if (pseudo_track.hitPattern().hasValidHitInPixelLayer(PixelSubdetector::SubDetector::PixelBarrel, 1)) {
        lostHits = pat::PackedCandidate::validHitInFirstPixelBarrelLayer;
      }
    } else {
      lostHits = (nlost == 1 ? pat::PackedCandidate::oneLostInnerHit : pat::PackedCandidate::moreLostInnerHits);
    }
    lostHits = 2; // weird hacks
    lt_features.lostInnerHits = catch_infs(lostHits, 2);
    lt_features.numberOfPixelHits = catch_infs(pseudo_track.hitPattern().numberOfValidPixelHits(), -1);
    lt_features.numberOfStripHits = catch_infs(pseudo_track.hitPattern().stripLayersWithMeasurement(), -1);

    math::XYZPoint pvPosition = pv->position();
    double dxy = pseudo_track.dxy(pvPosition);
    double dz  = pseudo_track.dz(pvPosition);	

    //lt_features.dxy = catch_infs(dxy);
    lt_features.dz = catch_infs(dz);
    //lt_features.dxysig = c_pf->bestTrack() ? catch_infs(dxy / c_pf->dxyError()) : 0;
    //lt_features.dzsig = c_pf->bestTrack() ? catch_infs(dz / c_pf->dzError()) : 0;

  }

}  // namespace btagbtvdeep
