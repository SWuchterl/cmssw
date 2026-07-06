// -*- C++ -*-
//
// Package:    PhysicsTools/PatAlgos
// Class:      LeptonTagInfoCollectionProducer
//
// Original Author:  Sergio Sanchez Cruz
//         Created:  Mon, 15 May 2023 08:32:03 GMT
//
#include <algorithm>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/Utilities/interface/ESGetToken.h"

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "DataFormats/BTauReco/interface/DeepBoostedJetFeatures.h"
#include "DataFormats/Candidate/interface/VertexCompositePtrCandidate.h"
#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"

#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexPrimitives/interface/VertexState.h"
#include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
#include "RecoBTag/FeatureTools/interface/deep_helpers.h"

#include <type_traits>

using namespace btagbtvdeep;

template <typename LeptonType>
class LeptonTagInfoCollectionProducer : public edm::stream::EDProducer<> {
public:
  explicit LeptonTagInfoCollectionProducer(const edm::ParameterSet& iConfig);
  ~LeptonTagInfoCollectionProducer() override {};

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  using LeptonTagInfoCollection = DeepBoostedJetFeaturesCollection;

  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) override;

  void fill_lepton_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_lepton_extfeatures(const edm::RefToBase<LeptonType>&, DeepBoostedJetFeatures&, edm::Event&);
  void fill_pf_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_lt_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_lepton_info(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_sv_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_rechit_features(const LeptonType&, DeepBoostedJetFeatures&, const CaloGeometry&);

  template <typename VarType>
  using VarWithName = std::pair<std::string, StringObjectFunction<VarType, true>>;
  template <typename VarType>
  void parse_vars_into(const edm::ParameterSet& varsPSet, std::vector<std::unique_ptr<VarWithName<VarType>>>& vars) {
    for (const std::string& vname : varsPSet.getParameterNamesForType<std::string>()) {
      const std::string& func = varsPSet.getParameter<std::string>(vname);
      vars.push_back(std::make_unique<VarWithName<VarType>>(vname, StringObjectFunction<VarType, true>(func)));
    }
  }

  template <typename VarType>
  using ExtVarWithName = std::pair<std::string, edm::EDGetTokenT<edm::ValueMap<VarType>>>;
  template <typename VarType>
  void parse_extvars_into(const edm::ParameterSet& varsPSet,
                          std::vector<std::unique_ptr<ExtVarWithName<VarType>>>& vars) {
    for (const std::string& vname : varsPSet.getParameterNamesForType<edm::InputTag>()) {
      vars.push_back(std::make_unique<ExtVarWithName<VarType>>(
          vname, consumes<edm::ValueMap<VarType>>(varsPSet.getParameter<edm::InputTag>(vname))));
    }
  }

  edm::EDGetTokenT<edm::View<LeptonType>> src_token_;
  edm::EDGetTokenT<pat::PackedCandidateCollection> pf_token_;
  edm::EDGetTokenT<pat::PackedCandidateCollection> lt_token_;
  edm::EDGetTokenT<reco::VertexCompositePtrCandidateCollection> sv_token_;
  edm::EDGetTokenT<std::vector<reco::Vertex>> pv_token_;
  edm::EDGetTokenT<EcalRecHitCollection> barrel_rh_token_;
  edm::EDGetTokenT<EcalRecHitCollection> endcap_rh_token_;
  edm::ESGetToken<CaloGeometry, CaloGeometryRecord> geom_token_;
  bool doRecHits_ = false;

  edm::ParameterSet lepton_varsPSet_;
  edm::ParameterSet lepton_varsExtPSet_;
  edm::ParameterSet pf_varsPSet_;
  edm::ParameterSet lt_varsPSet_;
  edm::ParameterSet sv_varsPSet_;
  edm::ParameterSet rh_varsPSet_;

  std::vector<std::unique_ptr<VarWithName<LeptonType>>> lepton_vars_;
  std::vector<std::unique_ptr<VarWithName<pat::PackedCandidate>>> pf_vars_;
  std::vector<std::unique_ptr<VarWithName<pat::PackedCandidate>>> lt_vars_;
  std::vector<std::unique_ptr<VarWithName<reco::VertexCompositePtrCandidate>>> sv_vars_;
  std::vector<std::unique_ptr<VarWithName<EcalRecHit>>> rh_vars_;
  edm::Handle<reco::VertexCompositePtrCandidateCollection> svs_;
  edm::Handle<pat::PackedCandidateCollection> pfs_;
  edm::Handle<pat::PackedCandidateCollection> lts_;
  edm::Handle<std::vector<reco::Vertex>> pvs_;
  edm::Handle<EcalRecHitCollection> barrelHits_;
  edm::Handle<EcalRecHitCollection> endcapHits_;
  std::vector<std::unique_ptr<ExtVarWithName<float>>> extLepton_vars_;
};

template <typename LeptonType>
LeptonTagInfoCollectionProducer<LeptonType>::LeptonTagInfoCollectionProducer(const edm::ParameterSet& iConfig)
    : src_token_(consumes<edm::View<LeptonType>>(iConfig.getParameter<edm::InputTag>("src"))),
      pf_token_(consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("pfCandidates"))),
      lt_token_(consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("ltCandidates"))),
      sv_token_(consumes<reco::VertexCompositePtrCandidateCollection>(
          iConfig.getParameter<edm::InputTag>("secondary_vertices"))),
      pv_token_(consumes<std::vector<reco::Vertex>>(iConfig.getParameter<edm::InputTag>("pvSrc"))),
      lepton_varsPSet_(iConfig.getParameter<edm::ParameterSet>("leptonVars")),
      lepton_varsExtPSet_(iConfig.getParameter<edm::ParameterSet>("leptonVarsExt")),
      pf_varsPSet_(iConfig.getParameter<edm::ParameterSet>("pfVars")),
      lt_varsPSet_(iConfig.getParameter<edm::ParameterSet>("ltVars")),
      sv_varsPSet_(iConfig.getParameter<edm::ParameterSet>("svVars")) {
  parse_vars_into(lepton_varsPSet_, lepton_vars_);
  parse_vars_into(pf_varsPSet_, pf_vars_);
  parse_vars_into(lt_varsPSet_, lt_vars_);
  parse_vars_into(sv_varsPSet_, sv_vars_);
  parse_extvars_into(lepton_varsExtPSet_, extLepton_vars_);

  // RecHits are optional and electron-only; other instances of this producer (muon, or the
  // non-training electron one) simply omit these parameters and doRecHits_ stays false.
  if (iConfig.exists("barrelEcalHits") && iConfig.exists("endcapEcalHits")) {
    doRecHits_ = true;
    barrel_rh_token_ = consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("barrelEcalHits"));
    endcap_rh_token_ = consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("endcapEcalHits"));
    geom_token_ = esConsumes<CaloGeometry, CaloGeometryRecord>();
    if (iConfig.exists("rhVars")) {
      rh_varsPSet_ = iConfig.getParameter<edm::ParameterSet>("rhVars");
      parse_vars_into(rh_varsPSet_, rh_vars_);
    }
  }

  produces<LeptonTagInfoCollection>();
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;

  desc.add<edm::InputTag>("src", edm::InputTag("slimmedMuons"));
  desc.add<edm::InputTag>("pfCandidates", edm::InputTag("packedPFCandidates"));
  desc.add<edm::InputTag>("ltCandidates", edm::InputTag("lostTracks"));
  desc.add<edm::InputTag>("secondary_vertices", edm::InputTag("slimmedSecondaryVertices"));
  desc.add<edm::InputTag>("pvSrc", edm::InputTag("offlineSlimmedPrimaryVertices"));

  for (auto&& what : {"leptonVars", "pfVars", "ltVars", "svVars"}) {
    edm::ParameterSetDescription descNested;
    descNested.addWildcard<std::string>("*");
    desc.add<edm::ParameterSetDescription>(what, descNested);
  }

  for (auto&& what : {"leptonVarsExt"}) {
    edm::ParameterSetDescription descNested;
    descNested.addWildcard<edm::InputTag>("*");
    desc.add<edm::ParameterSetDescription>(what, descNested);
  }

  // optional, electron-only: ECAL RecHits associated to the lepton's supercluster
  desc.addOptional<edm::InputTag>("barrelEcalHits", edm::InputTag(""));
  desc.addOptional<edm::InputTag>("endcapEcalHits", edm::InputTag(""));
  {
    edm::ParameterSetDescription descNested;
    descNested.addWildcard<std::string>("*");
    desc.addOptional<edm::ParameterSetDescription>("rhVars", descNested);
  }

  std::string modname;
  if (typeid(LeptonType) == typeid(pat::Muon))
    modname += "muon";
  else if (typeid(LeptonType) == typeid(pat::Electron))
    modname += "electron";
  modname += "TagInfos";
  descriptions.add(modname, desc);
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto src = iEvent.getHandle(src_token_);
  iEvent.getByToken(sv_token_, svs_);
  iEvent.getByToken(pv_token_, pvs_);
  iEvent.getByToken(pf_token_, pfs_);
  iEvent.getByToken(lt_token_, lts_);

  const CaloGeometry* geometry = nullptr;
  if constexpr (std::is_same_v<LeptonType, pat::Electron>) {
    if (doRecHits_) {
      iEvent.getByToken(barrel_rh_token_, barrelHits_);
      iEvent.getByToken(endcap_rh_token_, endcapHits_);
      geometry = &iSetup.getData(geom_token_);
    }
  }

  auto output_info = std::make_unique<LeptonTagInfoCollection>();

  if (pvs_->empty()) {
    // produce empty TagInfos in case no primary vertex
    iEvent.put(std::move(output_info));
    return;
  }

  for (size_t ilep = 0; ilep < src->size(); ilep++) {
    const auto& lep = (*src)[ilep];
    edm::RefToBase<LeptonType> lep_ref(src, ilep);
    DeepBoostedJetFeatures features;
    fill_lepton_features(lep, features);
    fill_lepton_extfeatures(lep_ref, features, iEvent);  // fixme
    fill_pf_features(lep, features);
    fill_lt_features(lep, features);
    fill_sv_features(lep, features);
    if constexpr (std::is_same_v<LeptonType, pat::Electron>) {
      if (doRecHits_)
        fill_rechit_features(lep, features, *geometry);
    }

    output_info->emplace_back(features);
  }
  iEvent.put(std::move(output_info));
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_lepton_features(const LeptonType& lep,
                                                                       DeepBoostedJetFeatures& features) {
  for (auto& var : lepton_vars_) {
    features.add(var->first);
    features.reserve(var->first, 1);
    features.fill(var->first, var->second(lep));
    
    // afaik these need to be hardcoded because I cannot put userFloats to pat::Leptons
    if (var->first == "Lepton_fbrem"){
      features.add("Lepton_fbrem_log");
      features.reserve("Lepton_fbrem_log", 1);
      features.fill("Lepton_fbrem_log",asinh(var->second(lep)));
    }
  }


}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_lepton_extfeatures(const edm::RefToBase<LeptonType>& lep,
                                                                          DeepBoostedJetFeatures& features,
                                                                          edm::Event& iEvent) {
  for (auto& var : extLepton_vars_) {
    edm::Handle<edm::ValueMap<float>> vmap;
    iEvent.getByToken(var->second, vmap);

    features.add(var->first);
    features.reserve(var->first, 1);
    features.fill(var->first, (*vmap)[lep]);
  }
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_pf_features(const LeptonType& lep,
                                                                   DeepBoostedJetFeatures& features) {
  pat::PackedCandidateCollection pfcands;
  for (size_t ipf = 0; ipf < pfs_->size(); ++ipf) {
    if (reco::deltaR(pfs_->at(ipf), lep) < 0.4)
      pfcands.push_back(pfs_->at(ipf));
  }

  for (auto& var : pf_vars_) {
    features.add(var->first);
    features.reserve(var->first, pfcands.size());
    for (const auto& cand : pfcands) {
      features.fill(var->first, var->second(cand));
    }
  }

  // afaik these need to be hardcoded because I cannot put userFloats to pat::packedCandidates
  features.add("PF_phi_rel");
  features.reserve("PF_phi_rel", pfcands.size());
  features.add("PF_eta_rel");
  features.reserve("PF_eta_rel", pfcands.size());
  features.add("PF_dR_lep");
  features.reserve("PF_dR_lep", pfcands.size());
  features.add("PF_pt_rel");
  features.reserve("PF_pt_rel", pfcands.size());
  features.add("PF_pt_rel_log");
  features.reserve("PF_pt_rel_log", pfcands.size());
  features.add("PF_dxySig_log");
  features.reserve("PF_dxySig_log", pfcands.size());
  features.add("PF_dzSig_log");
  features.reserve("PF_dzSig_log", pfcands.size());
  features.add("PF_quality");
  features.reserve("PF_quality", pfcands.size());

  // relative px, py, pz and energy
  features.add("PF_px");
  features.reserve("PF_px", pfcands.size());
  features.add("PF_py");
  features.reserve("PF_py", pfcands.size());
  features.add("PF_pz");
  features.reserve("PF_pz", pfcands.size());
  features.add("PF_energy");
  features.reserve("PF_energy", pfcands.size());

  // and all displacement variables to catch nans
  features.add("PF_dxy");
  features.add("PF_dxy_asinh");
  features.add("PF_dxysig");
  features.add("PF_dxysig_asinh");
  features.add("PF_dz");
  features.add("PF_dz_asinh");
  features.add("PF_dzsig");
  features.add("PF_dzsig_asinh");
  features.reserve("PF_dxy", pfcands.size());
  features.reserve("PF_dxy_asinh", pfcands.size());
  features.reserve("PF_dxysig", pfcands.size());
  features.reserve("PF_dxysig_asinh", pfcands.size());
  features.reserve("PF_dz", pfcands.size());
  features.reserve("PF_dz_asinh", pfcands.size());
  features.reserve("PF_dzsig", pfcands.size());
  features.reserve("PF_dzsig_asinh", pfcands.size());

  for (const auto& cand : pfcands) {
    features.fill("PF_phi_rel", reco::deltaPhi(lep.phi(), cand.phi()));
    features.fill("PF_eta_rel", lep.eta() - cand.eta());
    features.fill("PF_dR_lep", reco::deltaR(lep, cand));
    features.fill("PF_pt_rel", cand.pt() / lep.pt());
    features.fill("PF_pt_rel_log", log(cand.pt() / lep.pt()));
    features.fill("PF_px", (cand.pt() / lep.pt()) * cos(reco::deltaPhi(lep.phi(), cand.phi())));
    features.fill("PF_py", (cand.pt() / lep.pt()) * sin(reco::deltaPhi(lep.phi(), cand.phi())));
    features.fill("PF_pz", (cand.pt() / lep.pt()) * sinh(lep.eta() - cand.eta()));
    features.fill("PF_energy", (cand.pt() / lep.pt()) * cosh(lep.eta() - cand.eta()));
    if (cand.hasTrackDetails()) {
      features.fill("PF_dxySig_log", asinh(cand.dxy() / cand.dxyError()));
      features.fill("PF_dzSig_log", asinh(cand.dz() / cand.dzError()));
      features.fill("PF_dxy", catch_infs(cand.dxy()));
      features.fill("PF_dxy_asinh", catch_infs(asinh(cand.dxy())));
      features.fill("PF_dxysig", catch_infs(cand.dxy() / cand.dxyError()));
      features.fill("PF_dxysig_asinh", catch_infs(asinh(cand.dxy() / cand.dxyError())));
      features.fill("PF_dz", catch_infs(cand.dz()));
      features.fill("PF_dz_asinh", catch_infs(asinh(cand.dz())));
      features.fill("PF_dzsig", catch_infs(cand.dz() / cand.dzError()));
      features.fill("PF_dzsig_asinh", catch_infs(asinh(cand.dz() / cand.dzError())));
    } else {
      features.fill("PF_dxySig_log", 0);
      features.fill("PF_dzSig_log", 0);
      features.fill("PF_dxy", 0);
      features.fill("PF_dxy_asinh", 0);
      features.fill("PF_dxysig", 0);
      features.fill("PF_dxysig_asinh", 0);
      features.fill("PF_dz", 0);
      features.fill("PF_dz_asinh", 0);
      features.fill("PF_dzsig", 0);
      features.fill("PF_dzsig_asinh", 0);
    }

    features.fill("PF_quality", cand.hasTrackDetails() ? cand.pseudoTrack().qualityMask() : (1 << reco::TrackBase::loose));
  }
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_lt_features(const LeptonType& lep,
                                                                   DeepBoostedJetFeatures& features) {
  pat::PackedCandidateCollection ltcands;
  for (size_t ilt = 0; ilt < lts_->size(); ++ilt) {
    if (reco::deltaR(lts_->at(ilt), lep) < 0.4)
      ltcands.push_back(lts_->at(ilt));
  }

  for (auto& var : lt_vars_) {
    features.add(var->first);
    features.reserve(var->first, ltcands.size());
    for (const auto& cand : ltcands) {
      features.fill(var->first, var->second(cand));
    }
  }

  // afaik these need to be hardcoded because I cannot put userFloats to pat::packedCandidates
  features.add("LT_phi_rel");
  features.reserve("LT_phi_rel", ltcands.size());
  features.add("LT_eta_rel");
  features.reserve("LT_eta_rel", ltcands.size());
  features.add("LT_dR_lep");
  features.reserve("LT_dR_lep", ltcands.size());
  features.add("LT_pt_rel");
  features.reserve("LT_pt_rel", ltcands.size());
  features.add("LT_pt_rel_log");
  features.reserve("LT_pt_rel_log", ltcands.size());
  features.add("LT_dxySig_log");
  features.reserve("LT_dxySig_log", ltcands.size());
  features.add("LT_dzSig_log");
  features.reserve("LT_dzSig_log", ltcands.size());
  features.add("LT_quality");
  features.reserve("LT_quality", ltcands.size());

  // and all displacement variables to catch nans
  features.add("LT_dxy");
  features.add("LT_dxy_asinh");
  features.add("LT_dxysig");
  features.add("LT_dxysig_asinh");
  features.add("LT_dz");
  features.add("LT_dz_asinh");
  features.add("LT_dzsig");
  features.add("LT_dzsig_asinh");
  features.reserve("LT_dxy", ltcands.size());
  features.reserve("LT_dxy_asinh", ltcands.size());
  features.reserve("LT_dxysig", ltcands.size());
  features.reserve("LT_dxysig_asinh", ltcands.size());
  features.reserve("LT_dz", ltcands.size());
  features.reserve("LT_dz_asinh", ltcands.size());
  features.reserve("LT_dzsig", ltcands.size());
  features.reserve("LT_dzsig_asinh", ltcands.size());

  for (const auto& cand : ltcands) {
    features.fill("LT_phi_rel", reco::deltaPhi(lep.phi(), cand.phi()));
    features.fill("LT_eta_rel", lep.eta() - cand.eta());
    features.fill("LT_dR_lep", reco::deltaR(lep, cand));
    features.fill("LT_pt_rel", cand.pt() / lep.pt());
    features.fill("LT_pt_rel_log", log(cand.pt() / lep.pt()));
    if (cand.hasTrackDetails()) {
      features.fill("LT_dxySig_log", asinh(abs(cand.dxy() / cand.dxyError())));
      features.fill("LT_dzSig_log", asinh(abs(cand.dz() / cand.dzError())));
      features.fill("LT_dxy", catch_infs(cand.dxy()));
      features.fill("LT_dxy_asinh", catch_infs(asinh(cand.dxy())));
      features.fill("LT_dxysig", catch_infs(cand.dxy() / cand.dxyError()));
      features.fill("LT_dxysig_asinh", catch_infs(asinh(cand.dxy() / cand.dxyError())));
      features.fill("LT_dz", catch_infs(cand.dz()));
      features.fill("LT_dz_asinh", catch_infs(asinh(cand.dz())));
      features.fill("LT_dzsig", catch_infs(cand.dz() / cand.dzError()));
      features.fill("LT_dzsig_asinh", catch_infs(asinh(cand.dz() / cand.dzError())));
    } else {
      features.fill("LT_dxySig_log", 0);
      features.fill("LT_dzSig_log", 0);
      features.fill("LT_dxy", 0);
      features.fill("LT_dxy_asinh", 0);
      features.fill("LT_dxysig", 0);
      features.fill("LT_dxysig_asinh", 0);
      features.fill("LT_dz", 0);
      features.fill("LT_dz_asinh", 0);
      features.fill("LT_dzsig", 0);
      features.fill("LT_dzsig_asinh", 0);
    }
    features.fill("LT_quality", cand.hasTrackDetails() ? cand.pseudoTrack().qualityMask() : (1 << reco::TrackBase::loose));
  }

}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_sv_features(const LeptonType& lep,
                                                                   DeepBoostedJetFeatures& features) {
  reco::VertexCompositePtrCandidateCollection selectedSVs;
  for (size_t isv = 0; isv < svs_->size(); ++isv) {
    if (reco::deltaR(lep, svs_->at(isv)) < 0.4) {
      selectedSVs.push_back(svs_->at(isv));
    }
  }

  for (auto& var : sv_vars_) {
    features.add(var->first);
    features.reserve(var->first, selectedSVs.size());
    for (auto& sv : selectedSVs)
      features.fill(var->first, var->second(sv));
  }

  // afaik these need to be hardcoded
  const auto& PV0 = pvs_->front();
  VertexDistance3D vdist;
  VertexDistanceXY vdistXY;

  features.add("SV_dlenSig");
  features.reserve("SV_dlenSig", selectedSVs.size());
  features.add("SV_dlenSig_log");
  features.reserve("SV_dlenSig_log", selectedSVs.size());
  features.add("SV_dxy");
  features.reserve("SV_dxy", selectedSVs.size());
  features.add("SV_dxy_log");
  features.reserve("SV_dxy_log", selectedSVs.size());
  features.add("SV_dxy_asinh");
  features.reserve("SV_dxy_asinh", selectedSVs.size());
  features.add("SV_dxysig");
  features.reserve("SV_dxysig", selectedSVs.size());
  features.add("SV_dxysig_asinh");
  features.reserve("SV_dxysig_asinh", selectedSVs.size());
  features.add("SV_eta_rel");
  features.reserve("SV_eta_rel", selectedSVs.size());
  features.add("SV_phi_rel");
  features.reserve("SV_phi_rel", selectedSVs.size());
  features.add("SV_dR_lep");
  features.reserve("SV_dR_lep", selectedSVs.size());
  features.add("SV_pt_rel");
  features.reserve("SV_pt_rel", selectedSVs.size());
  features.add("SV_cospAngle");
  features.reserve("SV_cospAngle", selectedSVs.size());
  features.add("SV_d3d");
  features.reserve("SV_d3d", selectedSVs.size());
  features.add("SV_d3d_asinh");
  features.reserve("SV_d3d_asinh", selectedSVs.size());
  features.add("SV_d3dsig");
  features.reserve("SV_d3dsig", selectedSVs.size());
  features.add("SV_d3dsig_asinh");
  features.reserve("SV_d3dsig_asinh", selectedSVs.size());
  features.add("SV_deltaR");
  features.reserve("SV_deltaR", selectedSVs.size());
  features.add("SV_enratio");
  features.reserve("SV_enratio", selectedSVs.size());

  // relative px, py, pz and energy
  features.add("SV_px");
  features.reserve("SV_px", selectedSVs.size());
  features.add("SV_py");
  features.reserve("SV_py", selectedSVs.size());
  features.add("SV_pz");
  features.reserve("SV_pz", selectedSVs.size());
  features.add("SV_energy");
  features.reserve("SV_energy", selectedSVs.size());

  // relative px, py, pz and energy
  features.add("SV_px");
  features.reserve("SV_px", selectedSVs.size());
  features.add("SV_py");
  features.reserve("SV_py", selectedSVs.size());
  features.add("SV_pz");
  features.reserve("SV_pz", selectedSVs.size());
  features.add("SV_energy");
  features.reserve("SV_energy", selectedSVs.size());

  for (auto& sv : selectedSVs) {
    Measurement1D dl =
        vdist.distance(PV0, VertexState(RecoVertex::convertPos(sv.position()), RecoVertex::convertError(sv.error())));
    features.fill("SV_d3d", dl.value());
    features.fill("SV_d3d_asinh", asinh(dl.value()));
    features.fill("SV_d3dsig", dl.significance());
    features.fill("SV_d3dsig_asinh", asinh(dl.significance()));
    features.fill("SV_dlenSig", dl.significance());
    features.fill("SV_dlenSig_log", log(abs(dl.significance()) + 1e-8));
    Measurement1D d2d =
        vdistXY.distance(PV0, VertexState(RecoVertex::convertPos(sv.position()), RecoVertex::convertError(sv.error())));
    features.fill("SV_dxy", catch_infs(d2d.value()));
    features.fill("SV_dxy_asinh", catch_infs(asinh(d2d.value())));
    features.fill("SV_dxy_log", log(abs(catch_infs(d2d.value())) + 1e-8));
    features.fill("SV_dxysig", catch_infs(d2d.significance()));
    features.fill("SV_dxysig_asinh", catch_infs(asinh(catch_infs(d2d.significance()))));
    features.fill("SV_phi_rel", reco::deltaPhi(lep.phi(), sv.phi()));
    features.fill("SV_eta_rel", lep.eta() - sv.eta());
    features.fill("SV_dR_lep", reco::deltaR(sv, lep));
    features.fill("SV_pt_rel", sv.pt() / lep.pt());
    features.fill("SV_px", (sv.pt() / lep.pt()) * cos(reco::deltaPhi(lep.phi(), sv.phi())));
    features.fill("SV_py", (sv.pt() / lep.pt()) * sin(reco::deltaPhi(lep.phi(), sv.phi())));
    features.fill("SV_pz", (sv.pt() / lep.pt()) * sinh(lep.eta() - sv.eta()));
    features.fill("SV_energy", (sv.pt() / lep.pt()) * cosh(lep.eta() - sv.eta()));
    double dx = (PV0.x() - sv.vx()), dy = (PV0.y() - sv.vy()), dz = (PV0.z() - sv.vz());
    double pdotv = (dx * sv.px() + dy * sv.py() + dz * sv.pz()) / sv.p() / sqrt(dx * dx + dy * dy + dz * dz);
    features.fill("SV_cospAngle", pdotv);

    // new stuff
    features.fill("SV_deltaR", reco::deltaR(sv, lep));
    features.fill("SV_enratio", sv.energy() / lep.energy());
  }
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_rechit_features(const LeptonType& lep,
                                                                        DeepBoostedJetFeatures& features,
                                                                        const CaloGeometry& geometry) {
  struct SelectedHit {
    const EcalRecHit* hit;
    float fraction;
    bool isBarrel;
  };
  std::vector<SelectedHit> hits;

  const auto& sc = lep.superCluster();
  int seedIdx = 0, seedIdy = 0;
  if (sc.isNonnull()) {
    seedIdx = sc->seedCrysIEtaOrIx();
    seedIdy = sc->seedCrysIPhiOrIy();
    // hitsAndFractions() aggregates (and dedupes) hits over all constituent clusters of the
    // supercluster (seed + any bremsstrahlung clusters) -- i.e. exactly the hits used to
    // reconstruct the electron and its shower shape, as opposed to an ad-hoc dR match.
    for (const auto& hf : sc->hitsAndFractions()) {
      const DetId& id = hf.first;
      bool isBarrel = (id.subdetId() == EcalBarrel);
      const EcalRecHitCollection& coll = isBarrel ? *barrelHits_ : *endcapHits_;
      auto it = coll.find(id);
      if (it == coll.end())
        continue;
      hits.push_back({&(*it), hf.second, isBarrel});
    }
  }

  // highest-energy hits first, so that if the ntuplizer downstream caps the multiplicity
  // per lepton, it's always the most important (most energetic) hits that survive the cut.
  std::sort(hits.begin(), hits.end(), [](const SelectedHit& a, const SelectedHit& b) {
    return a.hit->energy() > b.hit->energy();
  });

  for (auto& var : rh_vars_) {
    features.add(var->first);
    features.reserve(var->first, hits.size());
    for (const auto& h : hits)
      features.fill(var->first, var->second(*h.hit));
  }

  features.add("RH_mask");
  features.reserve("RH_mask", hits.size());
  features.add("RH_fraction");
  features.reserve("RH_fraction", hits.size());
  features.add("RH_isBarrel");
  features.reserve("RH_isBarrel", hits.size());
  // option A: raw crystal indices, relative to the supercluster seed crystal.
  // Kept as separate barrel (ieta/iphi) and endcap (ix/iy) branches -- rather than one
  // mixed pair -- since the two index systems are not comparable; use RH_isBarrel to
  // pick which pair is meaningful for a given hit (the other pair is filled with 0).
  features.add("RH_ieta");
  features.reserve("RH_ieta", hits.size());
  features.add("RH_iphi");
  features.reserve("RH_iphi", hits.size());
  features.add("RH_ieta_rel");
  features.reserve("RH_ieta_rel", hits.size());
  features.add("RH_iphi_rel");
  features.reserve("RH_iphi_rel", hits.size());
  features.add("RH_ix");
  features.reserve("RH_ix", hits.size());
  features.add("RH_iy");
  features.reserve("RH_iy", hits.size());
  features.add("RH_ix_rel");
  features.reserve("RH_ix_rel", hits.size());
  features.add("RH_iy_rel");
  features.reserve("RH_iy_rel", hits.size());
  // option B: true geometric position from CaloGeometry
  features.add("RH_eta");
  features.reserve("RH_eta", hits.size());
  features.add("RH_phi");
  features.reserve("RH_phi", hits.size());
  features.add("RH_eta_rel");
  features.reserve("RH_eta_rel", hits.size());
  features.add("RH_phi_rel");
  features.reserve("RH_phi_rel", hits.size());
  features.add("RH_dR_lep");
  features.reserve("RH_dR_lep", hits.size());

  // hit-quality flags (see EcalRecHit::Flags)
  features.add("RH_flagBits");
  features.reserve("RH_flagBits", hits.size());
  features.add("RH_recoFlag");
  features.reserve("RH_recoFlag", hits.size());
  features.add("RH_kGood");
  features.reserve("RH_kGood", hits.size());
  features.add("RH_kPoorReco");
  features.reserve("RH_kPoorReco", hits.size());
  features.add("RH_kOutOfTime");
  features.reserve("RH_kOutOfTime", hits.size());
  features.add("RH_kFaultyHardware");
  features.reserve("RH_kFaultyHardware", hits.size());
  features.add("RH_kNoisy");
  features.reserve("RH_kNoisy", hits.size());
  features.add("RH_kPoorCalib");
  features.reserve("RH_kPoorCalib", hits.size());
  features.add("RH_kSaturated");
  features.reserve("RH_kSaturated", hits.size());
  features.add("RH_kLeadingEdgeRecovered");
  features.reserve("RH_kLeadingEdgeRecovered", hits.size());
  features.add("RH_kNeighboursRecovered");
  features.reserve("RH_kNeighboursRecovered", hits.size());
  features.add("RH_kTowerRecovered");
  features.reserve("RH_kTowerRecovered", hits.size());
  features.add("RH_kDead");
  features.reserve("RH_kDead", hits.size());
  features.add("RH_kWeird");
  features.reserve("RH_kWeird", hits.size());
  features.add("RH_kDiWeird");
  features.reserve("RH_kDiWeird", hits.size());
  features.add("RH_kHasSwitchToGain6");
  features.reserve("RH_kHasSwitchToGain6", hits.size());
  features.add("RH_kHasSwitchToGain1");
  features.reserve("RH_kHasSwitchToGain1", hits.size());
  features.add("RH_isRecovered");
  features.reserve("RH_isRecovered", hits.size());
  features.add("RH_isTimeValid");
  features.reserve("RH_isTimeValid", hits.size());
  features.add("RH_isTimeErrorValid");
  features.reserve("RH_isTimeErrorValid", hits.size());

  for (const auto& h : hits) {
    const DetId& id = h.hit->detid();
    int ieta = 0, iphi = 0, ix = 0, iy = 0;
    int ieta_rel = 0, iphi_rel = 0, ix_rel = 0, iy_rel = 0;
    if (h.isBarrel) {
      EBDetId ebid(id);
      ieta = ebid.ieta();
      iphi = ebid.iphi();
      ieta_rel = ieta - seedIdx;
      iphi_rel = iphi - seedIdy;
      // iphi wraps around at 360
      if (iphi_rel > 180)
        iphi_rel -= 360;
      else if (iphi_rel <= -180)
        iphi_rel += 360;
    } else {
      EEDetId eeid(id);
      ix = eeid.ix();
      iy = eeid.iy();
      ix_rel = ix - seedIdx;
      iy_rel = iy - seedIdy;
    }

    double eta = 0., phi = 0.;
    if (const auto* cell = geometry.getGeometry(id).get()) {
      const auto& pos = cell->getPosition();
      eta = pos.eta();
      phi = pos.phi();
    }

    features.fill("RH_mask", 1.f);
    features.fill("RH_fraction", h.fraction);
    features.fill("RH_isBarrel", h.isBarrel ? 1.f : 0.f);
    features.fill("RH_ieta", static_cast<float>(ieta));
    features.fill("RH_iphi", static_cast<float>(iphi));
    features.fill("RH_ieta_rel", static_cast<float>(ieta_rel));
    features.fill("RH_iphi_rel", static_cast<float>(iphi_rel));
    features.fill("RH_ix", static_cast<float>(ix));
    features.fill("RH_iy", static_cast<float>(iy));
    features.fill("RH_ix_rel", static_cast<float>(ix_rel));
    features.fill("RH_iy_rel", static_cast<float>(iy_rel));
    features.fill("RH_eta", eta);
    features.fill("RH_phi", phi);
    features.fill("RH_eta_rel", lep.eta() - eta);
    features.fill("RH_phi_rel", reco::deltaPhi(lep.phi(), phi));
    features.fill("RH_dR_lep", reco::deltaR(lep.eta(), lep.phi(), eta, phi));

    features.fill("RH_flagBits", static_cast<float>(h.hit->flagsBits()));
    features.fill("RH_recoFlag", static_cast<float>(h.hit->recoFlag()));
    features.fill("RH_kGood", h.hit->checkFlag(EcalRecHit::kGood) ? 1.f : 0.f);
    features.fill("RH_kPoorReco", h.hit->checkFlag(EcalRecHit::kPoorReco) ? 1.f : 0.f);
    features.fill("RH_kOutOfTime", h.hit->checkFlag(EcalRecHit::kOutOfTime) ? 1.f : 0.f);
    features.fill("RH_kFaultyHardware", h.hit->checkFlag(EcalRecHit::kFaultyHardware) ? 1.f : 0.f);
    features.fill("RH_kNoisy", h.hit->checkFlag(EcalRecHit::kNoisy) ? 1.f : 0.f);
    features.fill("RH_kPoorCalib", h.hit->checkFlag(EcalRecHit::kPoorCalib) ? 1.f : 0.f);
    features.fill("RH_kSaturated", h.hit->checkFlag(EcalRecHit::kSaturated) ? 1.f : 0.f);
    features.fill("RH_kLeadingEdgeRecovered",
                   h.hit->checkFlag(EcalRecHit::kLeadingEdgeRecovered) ? 1.f : 0.f);
    features.fill("RH_kNeighboursRecovered",
                   h.hit->checkFlag(EcalRecHit::kNeighboursRecovered) ? 1.f : 0.f);
    features.fill("RH_kTowerRecovered", h.hit->checkFlag(EcalRecHit::kTowerRecovered) ? 1.f : 0.f);
    features.fill("RH_kDead", h.hit->checkFlag(EcalRecHit::kDead) ? 1.f : 0.f);
    features.fill("RH_kWeird", h.hit->checkFlag(EcalRecHit::kWeird) ? 1.f : 0.f);
    features.fill("RH_kDiWeird", h.hit->checkFlag(EcalRecHit::kDiWeird) ? 1.f : 0.f);
    features.fill("RH_kHasSwitchToGain6", h.hit->checkFlag(EcalRecHit::kHasSwitchToGain6) ? 1.f : 0.f);
    features.fill("RH_kHasSwitchToGain1", h.hit->checkFlag(EcalRecHit::kHasSwitchToGain1) ? 1.f : 0.f);
    features.fill("RH_isRecovered", h.hit->isRecovered() ? 1.f : 0.f);
    features.fill("RH_isTimeValid", h.hit->isTimeValid() ? 1.f : 0.f);
    features.fill("RH_isTimeErrorValid", h.hit->isTimeErrorValid() ? 1.f : 0.f);
  }
}

typedef LeptonTagInfoCollectionProducer<pat::Muon> MuonTagInfoCollectionProducer;
typedef LeptonTagInfoCollectionProducer<pat::Electron> ElectronTagInfoCollectionProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MuonTagInfoCollectionProducer);
DEFINE_FWK_MODULE(ElectronTagInfoCollectionProducer);
