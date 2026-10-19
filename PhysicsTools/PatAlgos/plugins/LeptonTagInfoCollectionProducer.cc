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
#include "DataFormats/Math/interface/libminifloat.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHit.h"
#include "DataFormats/EcalRecHit/interface/EcalRecHitCollections.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "DataFormats/EcalDetId/interface/EEDetId.h"
#include "DataFormats/EcalDetId/interface/ESDetId.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/SiPixelDetId/interface/PixelSubdetector.h"
#include "DataFormats/CaloRecHit/interface/CaloCluster.h"
#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/CaloGeometry/interface/CaloSubdetectorGeometry.h"
#include "CommonTools/Egamma/interface/ConversionTools.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"
#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "RecoEcal/EgammaCoreTools/interface/EcalClusterLazyTools.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"

#include "RecoVertex/VertexTools/interface/VertexDistance3D.h"
#include "RecoVertex/VertexTools/interface/VertexDistanceXY.h"
#include "RecoVertex/VertexPrimitives/interface/VertexState.h"
#include "RecoVertex/VertexPrimitives/interface/ConvertToFromReco.h"
#include "RecoBTag/FeatureTools/interface/deep_helpers.h"

#include <type_traits>
#include <set>
#include <unordered_map>
#include <unordered_set>

using namespace btagbtvdeep;

template <typename LeptonType>
class LeptonTagInfoCollectionProducer : public edm::stream::EDProducer<> {
public:
  explicit LeptonTagInfoCollectionProducer(const edm::ParameterSet& iConfig);
  ~LeptonTagInfoCollectionProducer() override {};

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  using LeptonTagInfoCollection = DeepBoostedJetFeaturesCollection;

  template <typename VarType>
  using VarWithName = std::pair<std::string, StringObjectFunction<VarType, true>>;
  using PFVars = std::vector<std::unique_ptr<VarWithName<pat::PackedCandidate>>>;

  struct SelectedHit {
    const EcalRecHit* hit;
    float fraction;
    bool isBarrel;
  };

  void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) override;

  void fill_lepton_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_lepton_extfeatures(const edm::RefToBase<LeptonType>&, DeepBoostedJetFeatures&, edm::Event&);
  void fill_pf_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_pf_like(const LeptonType&,
                    const std::string& prefix,
                    const std::vector<const pat::PackedCandidate*>&,
                    const PFVars&,
                    bool withTrack,
                    DeepBoostedJetFeatures&);
  void fill_split_pf_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_lt_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_lepton_info(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_sv_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_rechit_features(const LeptonType&, DeepBoostedJetFeatures&, const CaloGeometry&);
  float fill_rechit_training_features(const LeptonType&,
                                      const std::vector<SelectedHit>&,
                                      DeepBoostedJetFeatures&,
                                      const CaloGeometry&);
  void fill_rho_features(const LeptonType&, float tcore, DeepBoostedJetFeatures&, const CaloGeometry&);
  void fill_es_features(const LeptonType&, DeepBoostedJetFeatures&, const CaloGeometry&);
  void fill_cl_features(const LeptonType&, DeepBoostedJetFeatures&);
  void reduce_precision(DeepBoostedJetFeatures&) const;
  void fill_conversion_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_gsf_features(const LeptonType&, DeepBoostedJetFeatures&);
  void fill_hcal_features(const LeptonType&, DeepBoostedJetFeatures&, const CaloGeometry&);
  void fill_esc_features(const LeptonType&, DeepBoostedJetFeatures&);
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
  // training-ntuple mode: sorted collections, CPF/NPF split, extended ECAL content; off for the inference inputs
  bool trainingMode_ = false;
  // electron v5 training tree: extra branches that must not appear in the muon tree (training mode only)
  bool v5Features_ = false;
  edm::EDGetTokenT<double> rho_token_;
  edm::EDGetTokenT<EcalRecHitCollection> es_rh_token_;
  edm::EDGetTokenT<reco::CaloClusterCollection> clusters_token_;
  double rho_ = 0.;
  edm::Handle<EcalRecHitCollection> esHits_;
  edm::Handle<reco::CaloClusterCollection> ebeeClusters_;
  PFVars cpf_vars_;
  PFVars npf_vars_;
  edm::EDGetTokenT<reco::ConversionCollection> conversions_token_;
  edm::EDGetTokenT<reco::ConversionCollection> sl_conversions_token_;
  edm::EDGetTokenT<reco::BeamSpot> beamspot_token_;
  std::optional<EcalClusterLazyToolsBase::ESGetTokens> lazy_tokens_;
  edm::Handle<reco::ConversionCollection> conversions_;
  edm::Handle<reco::ConversionCollection> slConversions_;
  edm::Handle<reco::BeamSpot> beamspot_;
  std::optional<EcalClusterLazyTools> lazy_;
  // per-event scalars (e.g. rho variants), stored as Lepton_<name>
  std::vector<std::pair<std::string, edm::EDGetTokenT<double>>> event_var_tokens_;
  std::vector<std::pair<std::string, float>> event_values_;
  // RHO noise cut [GeV]
  double rho_min_energy_eb_ = 0., rho_min_energy_ee_ = 0.;
  // crystal rawId -> row in the CL collection of the current electron (cluster with the largest fraction)
  std::unordered_map<uint32_t, int> cl_row_of_crystal_;
  // same, only supercluster clusters (used by RH: its crystals belong to the supercluster)
  std::unordered_map<uint32_t, int> cl_row_of_crystal_sc_;
  // optional precision reduction of all non-integer features (0 = off); training and inference stay identical
  // because both run this producer before the model
  int reduce_mantissa_bits_ = 0;
  edm::EDGetTokenT<HBHERecHitCollection> hbhe_token_;
  edm::EDGetTokenT<reco::CaloClusterCollection> es_clusters_token_;
  edm::Handle<HBHERecHitCollection> hbheHits_;
  edm::Handle<reco::CaloClusterCollection> esClusters_;
  // track position extrapolated to the ECAL front face (electron), reference for *_reltrk coordinates
  float trk_eta_ = 0.f, trk_phi_ = 0.f;
  // PF candidate / lost track key -> row in the SV collection of the current lepton (exact: SV daughter refs)
  std::unordered_map<size_t, int> pf_sv_row_;
  // preshower strip rawId -> row in the ESC collection
  std::unordered_map<uint32_t, int> esc_row_of_strip_;

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

  trainingMode_ = iConfig.getParameter<bool>("trainingMode");
  if (iConfig.existsAs<bool>("v5Features"))
    v5Features_ = trainingMode_ && iConfig.getParameter<bool>("v5Features");
  if (iConfig.existsAs<int>("reduceMantissaBits"))
    reduce_mantissa_bits_ = iConfig.getParameter<int>("reduceMantissaBits");
  if (trainingMode_) {
    rho_token_ = consumes<double>(iConfig.getParameter<edm::InputTag>("rhoSrc"));
    if (iConfig.exists("eventVars")) {
      const auto& ev = iConfig.getParameter<edm::ParameterSet>("eventVars");
      for (const auto& name : ev.getParameterNamesForType<edm::InputTag>())
        event_var_tokens_.emplace_back(name, consumes<double>(ev.getParameter<edm::InputTag>(name)));
    }
    parse_vars_into(iConfig.getParameter<edm::ParameterSet>("cpfVars"), cpf_vars_);
    parse_vars_into(iConfig.getParameter<edm::ParameterSet>("npfVars"), npf_vars_);
    if (doRecHits_) {
      es_rh_token_ = consumes<EcalRecHitCollection>(iConfig.getParameter<edm::InputTag>("esHits"));
      clusters_token_ = consumes<reco::CaloClusterCollection>(iConfig.getParameter<edm::InputTag>("ebeeClusters"));
      conversions_token_ = consumes<reco::ConversionCollection>(iConfig.getParameter<edm::InputTag>("conversions"));
      sl_conversions_token_ =
          consumes<reco::ConversionCollection>(iConfig.getParameter<edm::InputTag>("singleLegConversions"));
      beamspot_token_ = consumes<reco::BeamSpot>(iConfig.getParameter<edm::InputTag>("beamSpot"));
      hbhe_token_ = consumes<HBHERecHitCollection>(iConfig.getParameter<edm::InputTag>("hcalHits"));
      es_clusters_token_ = consumes<reco::CaloClusterCollection>(iConfig.getParameter<edm::InputTag>("esClusters"));
      rho_min_energy_eb_ = iConfig.getParameter<double>("rhoMinEnergyEB");
      rho_min_energy_ee_ = iConfig.getParameter<double>("rhoMinEnergyEE");
      lazy_tokens_.emplace(consumesCollector());
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

  desc.add<bool>("trainingMode", false);
  desc.addOptional<bool>("v5Features", false);
  desc.addOptional<int>("reduceMantissaBits", 0)->setComment("0 = full float precision");
  desc.addOptional<edm::InputTag>("rhoSrc", edm::InputTag("fixedGridRhoFastjetAll"));
  desc.addOptional<edm::InputTag>("esHits", edm::InputTag("reducedEgamma", "reducedESRecHits"));
  desc.addOptional<edm::InputTag>("ebeeClusters", edm::InputTag("reducedEgamma", "reducedEBEEClusters"));
  desc.addOptional<edm::InputTag>("conversions", edm::InputTag("reducedEgamma", "reducedConversions"));
  desc.addOptional<edm::InputTag>("singleLegConversions", edm::InputTag("reducedEgamma", "reducedSingleLegConversions"));
  desc.addOptional<edm::InputTag>("beamSpot", edm::InputTag("offlineBeamSpot"));
  desc.addOptional<edm::InputTag>("hcalHits", edm::InputTag("reducedEgamma", "reducedHBHEHits"));
  desc.addOptional<edm::InputTag>("esClusters", edm::InputTag("reducedEgamma", "reducedESClusters"));
  desc.addOptional<double>("rhoMinEnergyEB", 0.);
  desc.addOptional<double>("rhoMinEnergyEE", 0.);
  {
    edm::ParameterSetDescription descNested;
    descNested.addWildcard<edm::InputTag>("*");
    desc.addOptional<edm::ParameterSetDescription>("eventVars", descNested);
  }
  for (auto&& what : {"cpfVars", "npfVars"}) {
    edm::ParameterSetDescription descNested;
    descNested.addWildcard<std::string>("*");
    desc.addOptional<edm::ParameterSetDescription>(what, descNested);
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
      if (trainingMode_) {
        iEvent.getByToken(es_rh_token_, esHits_);
        iEvent.getByToken(clusters_token_, ebeeClusters_);
        iEvent.getByToken(conversions_token_, conversions_);
        iEvent.getByToken(sl_conversions_token_, slConversions_);
        iEvent.getByToken(beamspot_token_, beamspot_);
        iEvent.getByToken(hbhe_token_, hbheHits_);
        iEvent.getByToken(es_clusters_token_, esClusters_);
        lazy_.emplace(iEvent, lazy_tokens_->get(iSetup), barrel_rh_token_, endcap_rh_token_, es_rh_token_);
      }
    }
  }
  if (trainingMode_) {
    rho_ = iEvent.get(rho_token_);
    event_values_.clear();
    for (const auto& [name, token] : event_var_tokens_)
      event_values_.emplace_back("Lepton_" + name, iEvent.get(token));
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
    if (trainingMode_) {
      for (const auto& [name, value] : {std::pair<const char*, float>{"Lepton_rho", static_cast<float>(rho_)},
                                        {"Lepton_nPV", static_cast<float>(pvs_->size())},
                                        {"Lepton_veta", 0.f},
                                        {"Lepton_vphi", 0.f}}) {
        features.add(name);
        features.fill(name, value);
      }
      for (const auto& [name, value] : event_values_) {
        features.add(name);
        features.fill(name, value);
      }
      fill_sv_features(lep, features);
      fill_split_pf_features(lep, features);
    } else
      fill_pf_features(lep, features);
    fill_lt_features(lep, features);
    if (!trainingMode_)
      fill_sv_features(lep, features);
    if constexpr (std::is_same_v<LeptonType, pat::Electron>) {
      if (doRecHits_)
        fill_rechit_features(lep, features, *geometry);
    }

    if (reduce_mantissa_bits_ > 0)
      reduce_precision(features);
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
  std::vector<const pat::PackedCandidate*> pfcands;
  for (size_t ipf = 0; ipf < pfs_->size(); ++ipf) {
    if (reco::deltaR(pfs_->at(ipf), lep) < 0.4)
      pfcands.push_back(&pfs_->at(ipf));
  }
  fill_pf_like(lep, "PF", pfcands, pf_vars_, true, features);
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_pf_like(const LeptonType& lep,
                                                               const std::string& prefix,
                                                               const std::vector<const pat::PackedCandidate*>& pfcands,
                                                               const PFVars& vars,
                                                               bool withTrack,
                                                               DeepBoostedJetFeatures& features) {
  for (auto& var : vars) {
    features.add(var->first);
    features.reserve(var->first, pfcands.size());
    for (const auto* cand : pfcands) {
      features.fill(var->first, var->second(*cand));
    }
  }

  // afaik these need to be hardcoded because I cannot put userFloats to pat::packedCandidates
  const std::string phi_rel = prefix + "_phi_rel", eta_rel = prefix + "_eta_rel", dR_lep = prefix + "_dR_lep",
                    pt_rel = prefix + "_pt_rel", pt_rel_log = prefix + "_pt_rel_log", px = prefix + "_px",
                    py = prefix + "_py", pz = prefix + "_pz", energy = prefix + "_energy";
  // displacement variables, only meaningful for candidates with a track
  const std::string dxySig_log = prefix + "_dxySig_log", dzSig_log = prefix + "_dzSig_log",
                    quality = prefix + "_quality", dxy = prefix + "_dxy", dxy_asinh = prefix + "_dxy_asinh",
                    dxysig = prefix + "_dxysig", dxysig_asinh = prefix + "_dxysig_asinh", dz = prefix + "_dz",
                    dz_asinh = prefix + "_dz_asinh", dzsig = prefix + "_dzsig", dzsig_asinh = prefix + "_dzsig_asinh";
  for (const auto* name : {&phi_rel, &eta_rel, &dR_lep, &pt_rel, &pt_rel_log, &px, &py, &pz, &energy}) {
    features.add(*name);
    features.reserve(*name, pfcands.size());
  }
  if (withTrack) {
    for (const auto* name : {&dxySig_log,
                             &dzSig_log,
                             &quality,
                             &dxy,
                             &dxy_asinh,
                             &dxysig,
                             &dxysig_asinh,
                             &dz,
                             &dz_asinh,
                             &dzsig,
                             &dzsig_asinh}) {
      features.add(*name);
      features.reserve(*name, pfcands.size());
    }
  }
  // v5: dxy in units of the resolution (0.02 cm), so the asinh compresses the tail
  const bool addDxyRes = withTrack && v5Features_;
  const std::string dxyRes_asinh = prefix + "_dxyRes_asinh";
  if (addDxyRes) {
    features.add(dxyRes_asinh);
    features.reserve(dxyRes_asinh, pfcands.size());
  }

  for (const auto* candp : pfcands) {
    const auto& cand = *candp;
    features.fill(phi_rel, reco::deltaPhi(lep.phi(), cand.phi()));
    features.fill(eta_rel, lep.eta() - cand.eta());
    features.fill(dR_lep, reco::deltaR(lep, cand));
    features.fill(pt_rel, cand.pt() / lep.pt());
    // a packed candidate can have pT = 0 (compression); clamp in training mode, keep the inference inputs unchanged
    features.fill(pt_rel_log, trainingMode_ ? std::log(std::max(cand.pt() / lep.pt(), 1e-8)) : log(cand.pt() / lep.pt()));
    features.fill(px, (cand.pt() / lep.pt()) * cos(reco::deltaPhi(lep.phi(), cand.phi())));
    features.fill(py, (cand.pt() / lep.pt()) * sin(reco::deltaPhi(lep.phi(), cand.phi())));
    features.fill(pz, (cand.pt() / lep.pt()) * sinh(lep.eta() - cand.eta()));
    features.fill(energy, (cand.pt() / lep.pt()) * cosh(lep.eta() - cand.eta()));
    if (!withTrack)
      continue;
    if (addDxyRes)
      features.fill(dxyRes_asinh, cand.hasTrackDetails() ? catch_infs(std::asinh(cand.dxy() / 0.02)) : 0.f);
    if (cand.hasTrackDetails()) {
      features.fill(dxySig_log, asinh(cand.dxy() / cand.dxyError()));
      features.fill(dzSig_log, asinh(cand.dz() / cand.dzError()));
      features.fill(dxy, catch_infs(cand.dxy()));
      features.fill(dxy_asinh, catch_infs(asinh(cand.dxy())));
      features.fill(dxysig, catch_infs(cand.dxy() / cand.dxyError()));
      features.fill(dxysig_asinh, catch_infs(asinh(cand.dxy() / cand.dxyError())));
      features.fill(dz, catch_infs(cand.dz()));
      features.fill(dz_asinh, catch_infs(asinh(cand.dz())));
      features.fill(dzsig, catch_infs(cand.dz() / cand.dzError()));
      features.fill(dzsig_asinh, catch_infs(asinh(cand.dz() / cand.dzError())));
    } else {
      for (const auto* name :
           {&dxySig_log, &dzSig_log, &dxy, &dxy_asinh, &dxysig, &dxysig_asinh, &dz, &dz_asinh, &dzsig, &dzsig_asinh})
        features.fill(*name, 0);
    }

    features.fill(quality, cand.hasTrackDetails() ? cand.pseudoTrack().qualityMask() : (1 << reco::TrackBase::loose));
  }
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_split_pf_features(const LeptonType& lep,
                                                                         DeepBoostedJetFeatures& features) {
  std::vector<size_t> idx;
  for (size_t ipf = 0; ipf < pfs_->size(); ++ipf) {
    // pT = 0 candidates (about 4 per million) carry no information
    if (pfs_->at(ipf).pt() > 0 && reco::deltaR(pfs_->at(ipf), lep) < 0.4)
      idx.push_back(ipf);
  }
  std::stable_sort(idx.begin(), idx.end(), [this](size_t a, size_t b) { return pfs_->at(a).pt() > pfs_->at(b).pt(); });

  // the lepton's own PF candidate(s): from the PAT association, dR < 0.02 and same charge as fallback
  std::unordered_set<size_t> lepKeys;
  if constexpr (std::is_same_v<LeptonType, pat::Electron>) {
    for (const auto& ref : lep.associatedPackedPFCandidates())
      if (ref.id() == pfs_.id())
        lepKeys.insert(ref.key());
  } else {
    for (size_t i = 0; i < lep.numberOfSourceCandidatePtrs(); ++i) {
      const auto& ptr = lep.sourceCandidatePtr(i);
      if (ptr.isNonnull() && ptr.id() == pfs_.id())
        lepKeys.insert(ptr.key());
    }
  }

  // the association is a footprint and can hold several charged candidates: flag only the closest one
  size_t lepCand = pfs_->size();
  double lepCandDR = 1e9;
  for (size_t i : idx) {
    const auto& cand = pfs_->at(i);
    if (cand.charge() == 0)
      continue;
    const double dR = reco::deltaR(cand, lep);
    const bool matched = lepKeys.empty() ? (dR < 0.02 && cand.charge() == lep.charge()) : lepKeys.count(i) > 0;
    if (matched && dR < lepCandDR) {
      lepCand = i;
      lepCandDR = dR;
    }
  }

  std::vector<const pat::PackedCandidate*> cpf, npf;
  std::vector<float> isLepCand, qrel, cpfFoot, npfFoot, cpfSv, cpfInSv;
  for (size_t i : idx) {
    const auto& cand = pfs_->at(i);
    // footprint: all PF candidates associated to the lepton (electron: own candidate and brem photons)
    const float inFoot = lepKeys.count(i) ? 1.f : 0.f;
    if (cand.charge() == 0) {
      npf.push_back(&cand);
      npfFoot.push_back(inFoot);
      continue;
    }
    cpf.push_back(&cand);
    cpfFoot.push_back(inFoot);
    auto itsv = pf_sv_row_.find(i);
    cpfSv.push_back(itsv != pf_sv_row_.end() ? itsv->second : -1);
    cpfInSv.push_back(itsv != pf_sv_row_.end() ? 1.f : 0.f);
    isLepCand.push_back(i == lepCand ? 1.f : 0.f);
    qrel.push_back(cand.charge() * lep.charge());
  }

  fill_pf_like(lep, "CPF", cpf, cpf_vars_, true, features);
  fill_pf_like(lep, "NPF", npf, npf_vars_, false, features);
  features.set("CPF_isLeptonCand", isLepCand);
  features.set("CPF_inLeptonFootprint", cpfFoot);
  features.set("NPF_inLeptonFootprint", npfFoot);
  // row of the SV (in SV_*) that uses this track, -1 if none
  features.set("CPF_svIdx", cpfSv);
  features.set("CPF_inSV", cpfInSv);
  // charge relative to the lepton: +1 same sign, -1 opposite sign
  features.set("CPF_qrel", qrel);
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_lt_features(const LeptonType& lep,
                                                                   DeepBoostedJetFeatures& features) {
  std::vector<size_t> ltIdx;
  for (size_t ilt = 0; ilt < lts_->size(); ++ilt) {
    if (reco::deltaR(lts_->at(ilt), lep) < 0.4 && (!trainingMode_ || lts_->at(ilt).pt() > 0))
      ltIdx.push_back(ilt);
  }
  if (trainingMode_)
    std::stable_sort(ltIdx.begin(), ltIdx.end(), [this](size_t a, size_t b) { return lts_->at(a).pt() > lts_->at(b).pt(); });
  pat::PackedCandidateCollection ltcands;
  for (size_t i : ltIdx)
    ltcands.push_back(lts_->at(i));
  if (trainingMode_) {
    std::vector<float> qrel;
    for (size_t i : ltIdx)
      qrel.push_back(lts_->at(i).charge() * lep.charge());
    features.set("LT_qrel", qrel);
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
    features.fill("LT_pt_rel_log",
                  trainingMode_ ? std::log(std::max(cand.pt() / lep.pt(), 1e-8)) : log(cand.pt() / lep.pt()));
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
  if (trainingMode_) {
    std::stable_sort(
        selectedSVs.begin(), selectedSVs.end(), [](const auto& a, const auto& b) { return a.pt() > b.pt(); });
    pf_sv_row_.clear();
    for (size_t row = 0; row < selectedSVs.size(); ++row) {
      const auto& sv = selectedSVs[row];
      for (size_t i = 0; i < sv.numberOfDaughters(); ++i) {
        const auto& d = sv.daughterPtr(i);
        if (d.id() == pfs_.id())
          pf_sv_row_[d.key()] = row;
      }
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
  if (trainingMode_) {
    features.add("SV_enratio_log");
    features.reserve("SV_enratio_log", selectedSVs.size());
  }

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
    if (trainingMode_)
      features.fill("SV_enratio_log", std::log(std::max(sv.energy() / lep.energy(), 1e-6)));
  }
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_rechit_features(const LeptonType& lep,
                                                                        DeepBoostedJetFeatures& features,
                                                                        const CaloGeometry& geometry) {
  std::vector<SelectedHit> hits;

  const auto& sc = lep.superCluster();
  int seedIdx = 0, seedIdy = 0;
  if (sc.isNonnull()) {
    seedIdx = sc->seedCrysIEtaOrIx();
    seedIdy = sc->seedCrysIPhiOrIy();
    // hitsAndFractions() concatenates the hits of all clusters of the supercluster (seed + brem
    // clusters) without merging: a crystal shared by two clusters appears once per cluster.
    std::unordered_map<uint32_t, size_t> row;
    for (const auto& hf : sc->hitsAndFractions()) {
      const DetId& id = hf.first;
      bool isBarrel = (id.subdetId() == EcalBarrel);
      const EcalRecHitCollection& coll = isBarrel ? *barrelHits_ : *endcapHits_;
      auto it = coll.find(id);
      if (it == coll.end())
        continue;
      // training: one row per crystal, fraction = sum over the clusters (the inference inputs stay unchanged)
      if (trainingMode_) {
        auto [r, isNew] = row.emplace(id.rawId(), hits.size());
        if (!isNew) {
          hits[r->second].fraction += hf.second;
          continue;
        }
      }
      hits.push_back({&(*it), hf.second, isBarrel});
    }
  }

  // highest-energy hits first, so that if the ntuplizer downstream caps the multiplicity
  // per lepton, it's always the most important (most energetic) hits that survive the cut.
  std::stable_sort(hits.begin(), hits.end(), [](const SelectedHit& a, const SelectedHit& b) {
    return a.hit->energy() > b.hit->energy();
  });

  for (auto& var : rh_vars_) {
    features.add(var->first);
    features.reserve(var->first, hits.size());
    for (const auto& h : hits)
      features.fill(var->first, var->second(*h.hit));
  }

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
  // individual flags: deadweight in training (constant in >99.9% of crystals); RH_flagBits holds all of them
  if (!trainingMode_) {
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
  }
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
    if (!trainingMode_) {
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
    }
    features.fill("RH_isTimeValid", h.hit->isTimeValid() ? 1.f : 0.f);
    features.fill("RH_isTimeErrorValid", h.hit->isTimeErrorValid() ? 1.f : 0.f);
  }

  if (trainingMode_) {
    const auto trkPos = lep.trackPositionAtCalo();
    trk_eta_ = trkPos.eta();
    trk_phi_ = trkPos.phi();
    for (const auto& [name, value] : {std::pair<const char*, float>{"Lepton_trkCaloEta", trk_eta_},
                                      {"Lepton_trkCaloPhi", trk_phi_},
                                      {"Lepton_pAtCalo", static_cast<float>(lep.trackMomentumAtCalo().R())}}) {
      features.add(name);
      features.fill(name, value);
    }
    fill_gsf_features(lep, features);
    fill_cl_features(lep, features);  // first: RH and RHO point to its rows
    const float tcore = fill_rechit_training_features(lep, hits, features, geometry);
    fill_rho_features(lep, tcore, features, geometry);
    fill_esc_features(lep, features);  // before ES: strips point to its rows
    fill_es_features(lep, features, geometry);
    fill_hcal_features(lep, features, geometry);
    fill_conversion_features(lep, features);
  }
}

namespace {
  // Columns of one per-object collection. Every name is registered up front, so the feature set is
  // the same for every lepton, also when the collection is empty.
  struct Columns {
    explicit Columns(std::initializer_list<std::string> names) {
      for (const auto& name : names)
        cols_[name];
    }
    void push(const std::string& name, float value) {
      auto it = cols_.find(name);
      if (it == cols_.end())
        throw cms::Exception("LogicError") << "column " << name << " not registered";
      it->second.push_back(value);
    }
    void moveTo(DeepBoostedJetFeatures& features) {
      for (auto& [name, vec] : cols_)
        features.set(name, vec);
    }
    std::unordered_map<std::string, std::vector<float>> cols_;
  };

  void setScalar(DeepBoostedJetFeatures& features, const std::string& name, float value) {
    features.add(name);
    features.fill(name, value);
  }

  // crystal indices relative to the supercluster seed: (ieta, iphi) in the barrel, (ix, iy) in the endcap
  std::pair<int, int> relIndices(const DetId& id, bool isBarrel, int seedIdx, int seedIdy) {
    if (isBarrel) {
      EBDetId ebid(id);
      int iphi_rel = ebid.iphi() - seedIdy;
      if (iphi_rel > 180)
        iphi_rel -= 360;
      else if (iphi_rel <= -180)
        iphi_rel += 360;
      return {ebid.ieta() - seedIdx, iphi_rel};
    }
    EEDetId eeid(id);
    return {eeid.ix() - seedIdx, eeid.iy() - seedIdy};
  }


  template <typename T>
  void sortByEnergy(std::vector<T>& v) {
    std::stable_sort(v.begin(), v.end(), [](const T& a, const T& b) { return a.energy > b.energy; });
  }
}  // namespace

template <typename LeptonType>
float LeptonTagInfoCollectionProducer<LeptonType>::fill_rechit_training_features(const LeptonType& lep,
                                                                                const std::vector<SelectedHit>& hits,
                                                                                DeepBoostedJetFeatures& features,
                                                                                const CaloGeometry& geometry) {
  const auto& sc = lep.superCluster();
  int seedIdx = 0, seedIdy = 0;
  // crystal -> (cluster index in superCluster()->clusters(), fraction), for all clusters that contain it
  std::unordered_map<uint32_t, std::vector<std::pair<int, float>>> membership;
  std::unordered_set<uint32_t> seedClusterIds;
  uint32_t seedCrystal = 0;
  if (sc.isNonnull()) {
    seedIdx = sc->seedCrysIEtaOrIx();
    seedIdy = sc->seedCrysIPhiOrIy();
    int k = 0;
    for (auto it = sc->clustersBegin(); it != sc->clustersEnd(); ++it, ++k) {
      if (!it->isAvailable())
        continue;
      for (const auto& hf : (*it)->hitsAndFractions())
        membership[hf.first.rawId()].emplace_back(k, hf.second);
    }
    if (sc->seed().isAvailable()) {
      seedCrystal = sc->seed()->seed().rawId();
      for (const auto& hf : sc->seed()->hitsAndFractions())
        seedClusterIds.insert(hf.first.rawId());
    }
  }

  // inputs as stored in the RH_* branches (float), so the derived values match a recomputation from the ntuple
  const size_t n = hits.size();
  std::vector<float> E(n), t(n), dR(n), sigt(n), eta(n), phi(n);
  std::vector<int> i1(n), i2(n);
  std::vector<bool> tv(n);
  for (size_t j = 0; j < n; ++j) {
    const auto& h = hits[j];
    E[j] = h.hit->energy();
    t[j] = h.hit->time();
    tv[j] = h.hit->isTimeValid();
    std::tie(i1[j], i2[j]) = relIndices(h.hit->detid(), h.isBarrel, seedIdx, seedIdy);
    eta[j] = 0.f;
    phi[j] = 0.f;
    if (const auto* cell = geometry.getGeometry(h.hit->detid()).get()) {
      eta[j] = cell->getPosition().eta();
      phi[j] = cell->getPosition().phi();
    }
    dR[j] = reco::deltaR(lep.eta(), lep.phi(), eta[j], phi[j]);
    sigt[j] = (h.hit->isTimeErrorValid() && tv[j]) ? std::min(std::max(h.hit->timeError(), 0.05f), 20.f) : 0.f;
  }

  // core: 5x5 crystals around the supercluster seed crystal (the track direction at the vertex misses the
  // shower of low-pT electrons because of the bending in the magnetic field)
  std::vector<bool> in5x5(n);
  for (size_t j = 0; j < n; ++j)
    in5x5[j] = std::abs(i1[j]) <= 2 && std::abs(i2[j]) <= 2;
  double esum = 0, wcore = 0, wtcore = 0, isig = 0;
  for (size_t j = 0; j < n; ++j) {
    const bool core = in5x5[j] && tv[j];
    esum += E[j];
    if (core) {
      wcore += E[j];
      wtcore += E[j] * t[j];
    }
    if (in5x5[j] && sigt[j] > 0)
      isig += 1. / std::pow(std::max(sigt[j], 0.05f), 2);
  }
  const float tcore = wtcore / (wcore > 0 ? wcore : 1.);
  const double sigcore2 = 1. / (isig > 0 ? isig : 25.);
  const double esumSafe = esum > 0 ? esum : 1.;

  Columns cols({"RH_sigt",        "RH_trel",         "RH_i1",          "RH_i2",          "RH_eerr_rel",
                "RH_rfnz",        "RH_efrac_log",    "RH_erel_log",    "RH_rank_asinh",  "RH_dR_log",
                "RH_i1_asinh",    "RH_i2_asinh",     "RH_trel_asinh",  "RH_tsig",        "RH_sigt_log",
                "RH_px_glob",     "RH_py_glob",      "RH_pz_glob",     "RH_energy_glob", "RH_region",
                "RH_veta_rel",    "RH_vphi_rel",     "RH_clusterIdx",  "RH_clusterFrac", "RH_clusterIdx2",
                "RH_clusterFrac2", "RH_isSeedCrystal", "RH_inSeedCluster", "RH_x",         "RH_y",
                "RH_z",           "RH_clIdx",       "RH_eta_reltrk",  "RH_phi_reltrk", "RH_tsig_asinh"});
  double wtrms = 0, eoot = 0, escfrac = 0;
  for (size_t j = 0; j < n; ++j) {
    const auto& h = hits[j];
    const uint32_t raw = h.hit->detid().rawId();
    const float trel = (t[j] - tcore) * (tv[j] ? 1.f : 0.f);
    const bool core = in5x5[j] && tv[j];
    if (core)
      wtrms += E[j] * trel * trel;
    if (std::abs(trel) > 3 && tv[j])
      eoot += E[j];
    if (h.fraction > 0.9f)
      escfrac += E[j];

    cols.push("RH_sigt", sigt[j]);
    cols.push("RH_trel", trel);
    cols.push("RH_i1", i1[j]);
    cols.push("RH_i2", i2[j]);
    cols.push("RH_eerr_rel", h.hit->energyError() / std::max(E[j], 1e-3f));
    cols.push("RH_rfnz", h.hit->recoFlag() != 0 ? 1.f : 0.f);
    cols.push("RH_efrac_log", std::log(std::max(E[j] / esumSafe, 1e-6)));
    cols.push("RH_erel_log", std::log(std::max(E[j] / lep.energy(), 1e-6)));
    cols.push("RH_rank_asinh", std::asinh(j / 4.));
    cols.push("RH_dR_log", std::log(std::max(dR[j], 1e-4f)));
    cols.push("RH_i1_asinh", std::asinh(i1[j] / 2.));
    cols.push("RH_i2_asinh", std::asinh(i2[j] / 2.));
    cols.push("RH_trel_asinh", std::asinh(trel / 2.));
    const double tsig = sigt[j] > 0 ? trel / std::sqrt(sigt[j] * sigt[j] + sigcore2 + 1e-4) : 0.;
    cols.push("RH_tsig", tsig);
    cols.push("RH_tsig_asinh", std::asinh(tsig));
    cols.push("RH_sigt_log", std::log(sigt[j] > 0 ? sigt[j] : 1.f));
    cols.push("RH_px_glob", E[j] / std::cosh(eta[j]) * std::cos(phi[j]));
    cols.push("RH_py_glob", E[j] / std::cosh(eta[j]) * std::sin(phi[j]));
    cols.push("RH_pz_glob", E[j] * std::tanh(eta[j]));
    cols.push("RH_energy_glob", E[j]);
    cols.push("RH_region", h.isBarrel ? 1.f : -1.f);
    cols.push("RH_veta_rel", lep.eta() - eta[j]);
    cols.push("RH_eta_reltrk", trk_eta_ - eta[j]);
    cols.push("RH_phi_reltrk", reco::deltaPhi(trk_phi_, phi[j]));
    cols.push("RH_vphi_rel", reco::deltaPhi(lep.phi(), phi[j]));

    // clusters share crystals: keep the two with the largest fraction
    std::vector<std::pair<int, float>> owners;
    if (auto it = membership.find(raw); it != membership.end())
      owners = it->second;
    std::stable_sort(owners.begin(), owners.end(), [](const auto& a, const auto& b) { return a.second > b.second; });
    cols.push("RH_clusterIdx", owners.size() > 0 ? owners[0].first : -1);
    cols.push("RH_clusterFrac", owners.size() > 0 ? owners[0].second : 0.f);
    cols.push("RH_clusterIdx2", owners.size() > 1 ? owners[1].first : -1);
    cols.push("RH_clusterFrac2", owners.size() > 1 ? owners[1].second : 0.f);
    cols.push("RH_isSeedCrystal", raw == seedCrystal ? 1.f : 0.f);
    cols.push("RH_inSeedCluster", seedClusterIds.count(raw) ? 1.f : 0.f);
    if (auto itc = cl_row_of_crystal_sc_.find(raw); itc != cl_row_of_crystal_sc_.end())
      cols.push("RH_clIdx", itc->second);
    else
      cols.push("RH_clIdx", -1.f);

    float x = 0, y = 0, z = 0;
    if (const auto* cell = geometry.getGeometry(h.hit->detid()).get()) {
      x = cell->getPosition().x();
      y = cell->getPosition().y();
      z = cell->getPosition().z();
    }
    cols.push("RH_x", x);
    cols.push("RH_y", y);
    cols.push("RH_z", z);
  }
  cols.moveTo(features);

  setScalar(features, "Lepton_RH_esum", esum);
  setScalar(features, "Lepton_RH_wcore", wcore);
  setScalar(features, "Lepton_RH_tcore", tcore);
  setScalar(features, "Lepton_RH_isig", isig);
  setScalar(features, "Lepton_RH_sigcore2", sigcore2);
  setScalar(features, "Lepton_nRH_asinh", std::asinh(n / 10.));
  setScalar(features, "Lepton_RHesum_log", std::log(std::max(esum, 1e-3)));
  setScalar(features, "Lepton_RHcoreFrac", wcore / esumSafe);
  setScalar(features, "Lepton_RHtrms", std::sqrt(std::max(wtrms / (wcore > 0 ? wcore : 1.), 0.)));
  setScalar(features, "Lepton_RHeoot", eoot / esumSafe);
  setScalar(features, "Lepton_RHscFrac", escfrac / esumSafe);
  return tcore;
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_rho_features(const LeptonType& lep,
                                                                    float tcore,
                                                                    DeepBoostedJetFeatures& features,
                                                                    const CaloGeometry& geometry) {
  struct Sel {
    const EcalRecHit* hit;
    bool isBarrel;
    float energy;
  };
  std::vector<Sel> sel;
  int nGeom = 0, nStored = 0;
  int seedIdx = 0, seedIdy = 0;
  bool seedBarrel = true;
  const auto& sc = lep.superCluster();
  if (sc.isNonnull()) {
    seedIdx = sc->seedCrysIEtaOrIx();
    seedIdy = sc->seedCrysIPhiOrIy();
    seedBarrel = sc->seed().isAvailable() ? sc->seed()->seed().subdetId() == EcalBarrel : std::abs(sc->eta()) < 1.479;
    std::unordered_set<uint32_t> scIds;
    for (const auto& hf : sc->hitsAndFractions())
      scIds.insert(hf.first.rawId());
    const GlobalPoint scPos(sc->x(), sc->y(), sc->z());
    for (int subdet : {EcalBarrel, EcalEndcap}) {
      const auto* subGeom = geometry.getSubdetectorGeometry(DetId::Ecal, subdet);
      const EcalRecHitCollection& coll = subdet == EcalBarrel ? *barrelHits_ : *endcapHits_;
      for (const DetId& id : subGeom->getCells(scPos, 0.3)) {
        ++nGeom;
        auto it = coll.find(id);
        if (it == coll.end())
          continue;
        ++nStored;
        if (scIds.count(id.rawId()))
          continue;
        if (it->energy() < (subdet == EcalBarrel ? rho_min_energy_eb_ : rho_min_energy_ee_))
          continue;
        sel.push_back({&(*it), subdet == EcalBarrel, it->energy()});
      }
    }
  }
  sortByEnergy(sel);

  Columns cols({"RHO_mask",       "RHO_energy",     "RHO_energy_log", "RHO_energyError", "RHO_time",
                "RHO_timeError",  "RHO_chi2",       "RHO_eta",        "RHO_phi",         "RHO_eta_rel",
                "RHO_phi_rel",    "RHO_dR_lep",     "RHO_isBarrel",
                "RHO_i1",         "RHO_i2",         "RHO_x",          "RHO_y",           "RHO_z",
                "RHO_trel",       "RHO_px_glob",    "RHO_py_glob",    "RHO_pz_glob",     "RHO_energy_glob",
                "RHO_flagBits",   "RHO_recoFlag",   "RHO_isTimeValid", "RHO_isTimeErrorValid",
                 "RHO_clIdx", "RHO_eta_reltrk", "RHO_phi_reltrk",
                "RHO_eerr_rel",   "RHO_dR_log",     "RHO_trel_asinh", "RHO_rfnz"});
  for (const auto& s : sel) {
    const auto* hit = s.hit;
    float eta = 0, phi = 0, x = 0, y = 0, z = 0;
    if (const auto* cell = geometry.getGeometry(hit->detid()).get()) {
      const auto& pos = cell->getPosition();
      eta = pos.eta();
      phi = pos.phi();
      x = pos.x();
      y = pos.y();
      z = pos.z();
    }
    // relative indices only make sense in the same subdetector as the seed
    auto [i1, i2] = s.isBarrel == seedBarrel ? relIndices(hit->detid(), s.isBarrel, seedIdx, seedIdy)
                                             : std::pair<int, int>{0, 0};
    const float E = hit->energy();
    cols.push("RHO_mask", 1.f);
    cols.push("RHO_energy", E);
    cols.push("RHO_energy_log", std::log(std::max(E, 1e-3f)));
    cols.push("RHO_energyError", hit->energyError());
    cols.push("RHO_time", hit->time());
    cols.push("RHO_timeError", hit->timeError());
    cols.push("RHO_chi2", hit->chi2());
    cols.push("RHO_eta", eta);
    cols.push("RHO_phi", phi);
    cols.push("RHO_eta_rel", lep.eta() - eta);
    cols.push("RHO_phi_rel", reco::deltaPhi(lep.phi(), phi));
    cols.push("RHO_dR_lep", reco::deltaR(lep.eta(), lep.phi(), eta, phi));
    cols.push("RHO_eta_reltrk", trk_eta_ - eta);
    cols.push("RHO_phi_reltrk", reco::deltaPhi(trk_phi_, phi));
    cols.push("RHO_isBarrel", s.isBarrel ? 1.f : 0.f);
    cols.push("RHO_i1", i1);
    cols.push("RHO_i2", i2);
    cols.push("RHO_x", x);
    cols.push("RHO_y", y);
    cols.push("RHO_z", z);
    const float trel = hit->isTimeValid() ? hit->time() - tcore : 0.f;
    cols.push("RHO_trel", trel);
    // same forms as RH_eerr_rel, RH_dR_log, RH_trel_asinh, RH_rfnz
    cols.push("RHO_eerr_rel", hit->energyError() / std::max(E, 1e-3f));
    cols.push("RHO_dR_log", std::log(std::max(reco::deltaR(lep.eta(), lep.phi(), eta, phi), 1e-4)));
    cols.push("RHO_trel_asinh", std::asinh(trel / 2.));
    cols.push("RHO_rfnz", hit->recoFlag() != 0 ? 1.f : 0.f);
    cols.push("RHO_px_glob", E / std::cosh(eta) * std::cos(phi));
    cols.push("RHO_py_glob", E / std::cosh(eta) * std::sin(phi));
    cols.push("RHO_pz_glob", E * std::tanh(eta));
    cols.push("RHO_energy_glob", E);
    cols.push("RHO_flagBits", hit->flagsBits());
    cols.push("RHO_recoFlag", hit->recoFlag());
    cols.push("RHO_isTimeValid", hit->isTimeValid() ? 1.f : 0.f);
    cols.push("RHO_isTimeErrorValid", hit->isTimeErrorValid() ? 1.f : 0.f);
    if (auto itc = cl_row_of_crystal_.find(hit->detid().rawId()); itc != cl_row_of_crystal_.end())
      cols.push("RHO_clIdx", itc->second);
    else
      cols.push("RHO_clIdx", -1.f);
  }
  cols.moveTo(features);
  setScalar(features, "Lepton_RHO_coverage", nGeom > 0 ? float(nStored) / nGeom : 0.f);
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_es_features(const LeptonType& lep,
                                                                   DeepBoostedJetFeatures& features,
                                                                   const CaloGeometry& geometry) {
  struct Sel {
    const EcalRecHit* hit;
    GlobalPoint pos;
    float energy;
  };
  std::vector<Sel> sel;
  const auto& sc = lep.superCluster();
  if (sc.isNonnull()) {
    for (const auto& hit : *esHits_) {
      const auto cell = geometry.getGeometry(hit.id());
      if (!cell)
        continue;
      const auto& pos = cell->getPosition();
      if (reco::deltaR(sc->eta(), sc->phi(), pos.eta(), pos.phi()) < 0.3)
        sel.push_back({&hit, pos, hit.energy()});
    }
  }
  sortByEnergy(sel);

  Columns cols({"ES_mask",
                "ES_energy",
                "ES_plane",
                "ES_strip",
                "ES_x",
                "ES_y",
                "ES_z",
                "ES_eta",
                "ES_phi",
                "ES_eta_rel",
                "ES_phi_rel",
                "ES_dR_lep",
                "ES_eta_reltrk",
                "ES_phi_reltrk",
                "ES_clIdx",
                "ES_energy_log"});
  for (const auto& s : sel) {
    const ESDetId id(s.hit->id());
    cols.push("ES_mask", 1.f);
    cols.push("ES_energy", s.energy);
    cols.push("ES_energy_log", std::log(std::max(s.energy * 1e3f, 1e-6f)));  // ln(E / 1 MeV)
    cols.push("ES_plane", id.plane());
    cols.push("ES_strip", id.strip());
    cols.push("ES_x", s.pos.x());
    cols.push("ES_y", s.pos.y());
    cols.push("ES_z", s.pos.z());
    cols.push("ES_eta", s.pos.eta());
    cols.push("ES_phi", s.pos.phi());
    cols.push("ES_eta_rel", lep.eta() - s.pos.eta());
    cols.push("ES_phi_rel", reco::deltaPhi(lep.phi(), s.pos.phi()));
    cols.push("ES_dR_lep", reco::deltaR(lep.eta(), lep.phi(), s.pos.eta(), s.pos.phi()));
    cols.push("ES_eta_reltrk", trk_eta_ - s.pos.eta());
    cols.push("ES_phi_reltrk", reco::deltaPhi(trk_phi_, s.pos.phi()));
    auto itc = esc_row_of_strip_.find(s.hit->id().rawId());
    cols.push("ES_clIdx", itc != esc_row_of_strip_.end() ? itc->second : -1);
  }
  cols.moveTo(features);
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_conversion_features(const LeptonType& lep,
                                                                           DeepBoostedJetFeatures& features) {
  const math::XYZPoint bs = beamspot_->position();
  int nMatched = 0, nGood = 0, nSL = 0;
  const reco::Conversion* best = nullptr;
  float bestProb = -1;
  for (const auto& conv : *conversions_) {
    if (!ConversionTools::matchesConversion(lep, conv))
      continue;
    ++nMatched;
    nGood += ConversionTools::isGoodConversion(conv, bs);
    const float prob = ConversionTools::getVtxFitProb(&conv);
    if (prob > bestProb) {
      best = &conv;
      bestProb = prob;
    }
  }
  for (const auto& conv : *slConversions_)
    nSL += ConversionTools::matchesConversion(lep, conv);

  setScalar(features, "Lepton_convNMatched", nMatched);
  setScalar(features, "Lepton_convNGood", nGood);
  setScalar(features, "Lepton_convNSingleLeg", nSL);
  // no matched conversion vertex: all values 0 and Lepton_hasConvVtx = 0 (no sentinels)
  int nHitsBefore = 0;
  if (best)
    for (auto h : best->nHitsBeforeVtx())
      nHitsBefore = std::max<int>(nHitsBefore, h);
  setScalar(features, "Lepton_hasConvVtx", best ? 1.f : 0.f);
  setScalar(features, "Lepton_convVtxProb", best ? bestProb : 0.f);
  setScalar(features, "Lepton_convVtxLxy", best ? best->lxy(bs) : 0.f);
  setScalar(features, "Lepton_convVtxRho", best ? best->conversionVertex().position().rho() : 0.f);
  setScalar(features, "Lepton_convVtxNHitsBefore", nHitsBefore);
  // pairInvariantMass() = -1 when the float tracksPin() give m^2 <= 0 (collinear pair, m ~ 2 m_e): write 0
  setScalar(features, "Lepton_convVtxMass", best ? std::max(best->pairInvariantMass(), 0.) : 0.f);
  setScalar(features, "Lepton_convVtxDCot", best ? best->pairCotThetaSeparation() : 0.f);
  setScalar(features, "Lepton_convVtxDPhiTrk", best ? best->dPhiTracksAtVtx() : 0.f);

  // preshower shape (photon-ID definition), 0 outside 1.6 < |eta_SC| < 3 and when no ES hit is found;
  // Lepton_hasES = 1 when the shape exists, so that 0 means "no preshower information", not "narrow"
  const auto& sc = lep.superCluster();
  const float sxx = sc.isNonnull() ? lazy_->eseffsixix(*sc) : 0.f, syy = sc.isNonnull() ? lazy_->eseffsiyiy(*sc) : 0.f;
  setScalar(features, "Lepton_ES_sigmaXX", sxx);
  setScalar(features, "Lepton_ES_sigmaYY", syy);
  setScalar(features, "Lepton_ES_sigmaRR", sc.isNonnull() ? lazy_->eseffsirir(*sc) : 0.f);
  setScalar(features, "Lepton_hasES", (sxx > 0 || syy > 0) ? 1.f : 0.f);
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_cl_features(const LeptonType& lep,
                                                                   DeepBoostedJetFeatures& features) {
  // one entry per ECAL cluster: all supercluster clusters, plus all stored clusters within dR < 0.4 of the seed
  struct Sel {
    const reco::CaloCluster* cl;
    bool inSC;
    bool isSeed;
    float energy;
  };
  std::vector<Sel> sel;
  cl_row_of_crystal_.clear();
  const auto& sc = lep.superCluster();
  if (sc.isNonnull()) {
    // SC clusters are found in the window by seed crystal and energy: their references do not always
    // point to the same product as the window collection
    std::set<std::pair<uint32_t, float>> scClusters;
    for (auto it = sc->clustersBegin(); it != sc->clustersEnd(); ++it) {
      if (!it->isAvailable())
        continue;
      scClusters.emplace((*it)->seed().rawId(), static_cast<float>((*it)->energy()));
      sel.push_back(
          {it->get(), true, sc->seed().isAvailable() && *it == sc->seed(), static_cast<float>((*it)->energy())});
    }
    if (sc->seed().isAvailable()) {
      const auto& seed = *sc->seed();
      for (size_t i = 0; i < ebeeClusters_->size(); ++i) {
        const auto& cl = (*ebeeClusters_)[i];
        if (scClusters.count({cl.seed().rawId(), static_cast<float>(cl.energy())}))
          continue;
        // dR < 0.4, or a window along phi for far brem clusters (the electron bends in phi)
        const bool inCone = reco::deltaR(cl.eta(), cl.phi(), seed.eta(), seed.phi()) < 0.4;
        const bool inPhiRoad =
            std::abs(cl.eta() - seed.eta()) < 0.1 && std::abs(reco::deltaPhi(cl.phi(), seed.phi())) < 0.6;
        if (inCone || inPhiRoad)
          sel.push_back({&cl, false, false, static_cast<float>(cl.energy())});
      }
    }
  }
  sortByEnergy(sel);

  Columns cols({"CL_mask",
                "CL_energy",
                "CL_eta",
                "CL_phi",
                "CL_eta_rel",
                "CL_phi_rel",
                "CL_dR_lep",
                "CL_nCrystals",
                "CL_seedEnergy",
                "CL_seedTime",
                "CL_inSC",
                "CL_isSeed",
                "CL_eMaxOverE",
                "CL_r9",
                "CL_sigmaIetaIeta",
                "CL_sigmaIphiIphi",
                "CL_eta_reltrk",
                "CL_phi_reltrk",
                "CL_energy_log",
                "CL_trel_asinh",
                "CL_hasShape",
                "CL_hasHits",
                "CL_px_glob",
                "CL_py_glob",
                "CL_pz_glob",
                "CL_energy_glob"});
  // time reference: seed crystal of the supercluster seed cluster
  bool hasTref = false;
  float tref = 0;
  if (sc.isNonnull() && sc->seed().isAvailable()) {
    const DetId sid = sc->seed()->seed();
    const EcalRecHitCollection& coll = sid.subdetId() == EcalBarrel ? *barrelHits_ : *endcapHits_;
    if (auto it = coll.find(sid); it != coll.end() && it->isTimeValid()) {
      hasTref = true;
      tref = it->time();
    }
  }
  std::unordered_map<uint32_t, float> bestFrac, bestFracSC;
  cl_row_of_crystal_sc_.clear();
  for (size_t row = 0; row < sel.size(); ++row) {
    const auto& cl = *sel[row].cl;
    float seedE = 0, seedT = 0;
    bool seedTValid = false;
    const DetId seedId = cl.seed();
    const EcalRecHitCollection& coll = seedId.subdetId() == EcalBarrel ? *barrelHits_ : *endcapHits_;
    if (auto it = coll.find(seedId); it != coll.end()) {
      seedE = it->energy();
      seedT = it->time();
      seedTValid = it->isTimeValid();
    }
    // shower shape of the cluster itself: photon-like variables for every cluster, without a pT threshold
    const float e = cl.energy();
    const auto cov = lazy_->localCovariances(cl);
    cols.push("CL_mask", 1.f);
    cols.push("CL_energy", e);
    cols.push("CL_eta", cl.eta());
    cols.push("CL_phi", cl.phi());
    cols.push("CL_eta_rel", lep.eta() - cl.eta());
    cols.push("CL_phi_rel", reco::deltaPhi(lep.phi(), cl.phi()));
    cols.push("CL_dR_lep", reco::deltaR(lep.eta(), lep.phi(), cl.eta(), cl.phi()));
    cols.push("CL_eta_reltrk", trk_eta_ - cl.eta());
    cols.push("CL_phi_reltrk", reco::deltaPhi(trk_phi_, cl.phi()));
    cols.push("CL_nCrystals", cl.hitsAndFractions().size());
    cols.push("CL_seedEnergy", seedE);
    cols.push("CL_seedTime", seedT);
    cols.push("CL_inSC", sel[row].inSC ? 1.f : 0.f);
    cols.push("CL_isSeed", sel[row].isSeed ? 1.f : 0.f);
    cols.push("CL_eMaxOverE", e > 0 ? lazy_->eMax(cl) / e : 0.f);
    cols.push("CL_r9", e > 0 ? lazy_->e3x3(cl) / e : 0.f);
    // localCovariances returns 999.9 when no crystal passes the log weight: no shape (as for 1-crystal clusters);
    // one zero covariance is a valid shape (e.g. 2 crystals side by side in phi)
    const bool hasShape = cov[0] < 999. && cov[2] < 999. && (cov[0] > 0 || cov[2] > 0);
    cols.push("CL_hasShape", hasShape ? 1.f : 0.f);
    cols.push("CL_sigmaIetaIeta", hasShape ? std::sqrt(std::max(cov[0], 0.f)) : 0.f);
    cols.push("CL_sigmaIphiIphi", hasShape ? std::sqrt(std::max(cov[2], 0.f)) : 0.f);
    bool hasHits = false;
    for (const auto& hf : cl.hitsAndFractions()) {
      const EcalRecHitCollection& c = hf.first.subdetId() == EcalBarrel ? *barrelHits_ : *endcapHits_;
      if (c.find(hf.first) != c.end()) {
        hasHits = true;
        break;
      }
    }
    cols.push("CL_hasHits", hasHits ? 1.f : 0.f);
    cols.push("CL_energy_log", std::log(std::max(e, 1e-3f)));
    cols.push("CL_trel_asinh", hasTref && seedTValid ? std::asinh(seedT - tref) : 0.f);  // 1 ns scale
    cols.push("CL_px_glob", e / std::cosh(cl.eta()) * std::cos(cl.phi()));
    cols.push("CL_py_glob", e / std::cosh(cl.eta()) * std::sin(cl.phi()));
    cols.push("CL_pz_glob", e * std::tanh(cl.eta()));
    cols.push("CL_energy_glob", e);
    for (const auto& hf : cl.hitsAndFractions()) {
      const uint32_t raw = hf.first.rawId();
      auto it = bestFrac.find(raw);
      if (it == bestFrac.end() || hf.second > it->second) {
        bestFrac[raw] = hf.second;
        cl_row_of_crystal_[raw] = row;
      }
      if (sel[row].inSC) {
        auto its = bestFracSC.find(raw);
        if (its == bestFracSC.end() || hf.second > its->second) {
          bestFracSC[raw] = hf.second;
          cl_row_of_crystal_sc_[raw] = row;
        }
      }
    }
  }
  cols.moveTo(features);
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::reduce_precision(DeepBoostedJetFeatures& features) const {
  // integer codes can exceed the exactly representable range (e.g. flag words): keep them at full precision
  static const std::vector<std::string> kIntegerCoded = {"flagBits", "Idx", "recoFlag", "quality", "strip", "HH_ieta", "HH_iphi", "FirstHitLayer"};
  const MiniFloatConverter::ReduceMantissaToNbitsRounding round(reduce_mantissa_bits_);
  std::vector<std::string> names;
  for (const auto& kv : features.get_all())
    names.push_back(kv.first);
  for (const auto& name : names) {
    if (std::any_of(kIntegerCoded.begin(), kIntegerCoded.end(), [&](const std::string& k) {
          return name.find(k) != std::string::npos;
        }))
      continue;
    std::vector<float> values = features.get(name);
    for (auto& v : values)
      v = round(v);
    features.set(name, values);
  }
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_gsf_features(const LeptonType& lep,
                                                                    DeepBoostedJetFeatures& features) {
  // GSF track hit pattern, read directly from the track
  const auto& hp = lep.gsfTrack()->hitPattern();
  setScalar(features, "Lepton_gsfNValidHits", hp.numberOfValidHits());
  setScalar(features, "Lepton_gsfNPixelHits", hp.numberOfValidPixelHits());
  setScalar(features, "Lepton_gsfNPixelLayers", hp.pixelLayersWithMeasurement());
  setScalar(features, "Lepton_gsfNTrackerLayers", hp.trackerLayersWithMeasurement());
  setScalar(features, "Lepton_gsfNLostOuterHits", hp.numberOfLostHits(reco::HitPattern::MISSING_OUTER_HITS));
  setScalar(features, "Lepton_gsfHasHitBPix1", hp.hasValidHitInPixelLayer(PixelSubdetector::PixelBarrel, 1));
  // first valid tracker hit, coded as 10 * sub-detector + layer (1 BPix, 2 FPix, 3 TIB, 4 TID, 5 TOB, 6 TEC)
  int first = -1;
  for (int i = 0; i < hp.numberOfAllHits(reco::HitPattern::TRACK_HITS); ++i) {
    const uint16_t pat = hp.getHitPattern(reco::HitPattern::TRACK_HITS, i);
    if (reco::HitPattern::validHitFilter(pat) && reco::HitPattern::trackerHitFilter(pat)) {
      first = 10 * reco::HitPattern::getSubStructure(pat) + reco::HitPattern::getLayer(pat);
      break;
    }
  }
  setScalar(features, "Lepton_gsfFirstHitLayer", first);
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_hcal_features(const LeptonType& lep,
                                                                     DeepBoostedJetFeatures& features,
                                                                     const CaloGeometry& geometry) {
  // HCAL hits kept by MiniAOD behind e/gamma superclusters, within dR < 0.3 of this supercluster
  struct Sel {
    const HBHERecHit* hit;
    GlobalPoint pos;
    float energy;
  };
  std::vector<Sel> sel;
  const auto& sc = lep.superCluster();
  if (sc.isNonnull()) {
    for (const auto& hit : *hbheHits_) {
      const auto cell = geometry.getGeometry(hit.id());
      if (!cell)
        continue;
      const auto& pos = cell->getPosition();
      if (reco::deltaR(sc->eta(), sc->phi(), pos.eta(), pos.phi()) < 0.3)
        sel.push_back({&hit, pos, hit.energy()});
    }
  }
  sortByEnergy(sel);

  Columns cols({"HH_mask",         "HH_energy",       "HH_energy_log",  "HH_time",        "HH_depth",
                "HH_isBarrel",     "HH_ieta",         "HH_iphi",        "HH_eta",         "HH_phi",
                "HH_eta_rel",      "HH_phi_rel",      "HH_dR_lep",      "HH_eta_reltrk",  "HH_phi_reltrk",
                "HH_px_glob",      "HH_py_glob",      "HH_pz_glob",     "HH_energy_glob"});
  for (const auto& s : sel) {
    const HcalDetId id(s.hit->id());
    const float E = s.energy, eta = s.pos.eta(), phi = s.pos.phi();
    cols.push("HH_mask", 1.f);
    cols.push("HH_energy", E);
    cols.push("HH_energy_log", std::log(std::max(E, 1e-3f)));
    cols.push("HH_time", s.hit->time());
    cols.push("HH_depth", id.depth());
    cols.push("HH_isBarrel", id.subdet() == HcalBarrel ? 1.f : 0.f);
    cols.push("HH_ieta", id.ieta());
    cols.push("HH_iphi", id.iphi());
    cols.push("HH_eta", eta);
    cols.push("HH_phi", phi);
    cols.push("HH_eta_rel", lep.eta() - eta);
    cols.push("HH_phi_rel", reco::deltaPhi(lep.phi(), phi));
    cols.push("HH_dR_lep", reco::deltaR(lep.eta(), lep.phi(), eta, phi));
    cols.push("HH_eta_reltrk", trk_eta_ - eta);
    cols.push("HH_phi_reltrk", reco::deltaPhi(trk_phi_, phi));
    cols.push("HH_px_glob", E / std::cosh(eta) * std::cos(phi));
    cols.push("HH_py_glob", E / std::cosh(eta) * std::sin(phi));
    cols.push("HH_pz_glob", E * std::tanh(eta));
    cols.push("HH_energy_glob", E);
  }
  cols.moveTo(features);
}

template <typename LeptonType>
void LeptonTagInfoCollectionProducer<LeptonType>::fill_esc_features(const LeptonType& lep,
                                                                    DeepBoostedJetFeatures& features) {
  // preshower clusters within dR < 0.3 of the supercluster; inSC = preshower cluster of this supercluster
  struct Sel {
    const reco::CaloCluster* cl;
    bool inSC;
    float energy;
  };
  std::vector<Sel> sel;
  esc_row_of_strip_.clear();
  const auto& sc = lep.superCluster();
  if (sc.isNonnull()) {
    std::set<std::pair<uint32_t, float>> scES;
    for (auto it = sc->preshowerClustersBegin(); it != sc->preshowerClustersEnd(); ++it)
      if (it->isAvailable())
        scES.emplace((*it)->seed().rawId(), static_cast<float>((*it)->energy()));
    for (const auto& cl : *esClusters_)
      if (reco::deltaR(sc->eta(), sc->phi(), cl.eta(), cl.phi()) < 0.3)
        sel.push_back({&cl, scES.count({cl.seed().rawId(), static_cast<float>(cl.energy())}) > 0,
                       static_cast<float>(cl.energy())});
  }
  sortByEnergy(sel);

  Columns cols({"ESC_mask",
                "ESC_energy",
                "ESC_eta",
                "ESC_phi",
                "ESC_x",
                "ESC_y",
                "ESC_z",
                "ESC_eta_rel",
                "ESC_phi_rel",
                "ESC_dR_lep",
                "ESC_eta_reltrk",
                "ESC_phi_reltrk",
                "ESC_nStrips",
                "ESC_plane",
                "ESC_inSC",
                "ESC_energy_log",
                "ESC_px_glob",
                "ESC_py_glob",
                "ESC_pz_glob",
                "ESC_energy_glob"});
  std::unordered_map<uint32_t, float> bestFrac;
  for (size_t row = 0; row < sel.size(); ++row) {
    const auto& cl = *sel[row].cl;
    const auto& hf = cl.hitsAndFractions();
    cols.push("ESC_mask", 1.f);
    const float e = sel[row].energy;
    cols.push("ESC_energy", e);
    cols.push("ESC_energy_log", std::log(std::max(e * 1e3f, 1e-6f)));  // ln(E / 1 MeV)
    cols.push("ESC_px_glob", e / std::cosh(cl.eta()) * std::cos(cl.phi()));
    cols.push("ESC_py_glob", e / std::cosh(cl.eta()) * std::sin(cl.phi()));
    cols.push("ESC_pz_glob", e * std::tanh(cl.eta()));
    cols.push("ESC_energy_glob", e);
    cols.push("ESC_eta", cl.eta());
    cols.push("ESC_phi", cl.phi());
    cols.push("ESC_x", cl.x());
    cols.push("ESC_y", cl.y());
    cols.push("ESC_z", cl.z());
    cols.push("ESC_eta_rel", lep.eta() - cl.eta());
    cols.push("ESC_phi_rel", reco::deltaPhi(lep.phi(), cl.phi()));
    cols.push("ESC_dR_lep", reco::deltaR(lep.eta(), lep.phi(), cl.eta(), cl.phi()));
    cols.push("ESC_eta_reltrk", trk_eta_ - cl.eta());
    cols.push("ESC_phi_reltrk", reco::deltaPhi(trk_phi_, cl.phi()));
    cols.push("ESC_nStrips", hf.size());
    cols.push("ESC_plane", hf.empty() ? 0 : ESDetId(hf.front().first).plane());
    cols.push("ESC_inSC", sel[row].inSC ? 1.f : 0.f);
    for (const auto& h : hf) {
      auto it = bestFrac.find(h.first.rawId());
      if (it == bestFrac.end() || h.second > it->second) {
        bestFrac[h.first.rawId()] = h.second;
        esc_row_of_strip_[h.first.rawId()] = row;
      }
    }
  }
  cols.moveTo(features);
}

typedef LeptonTagInfoCollectionProducer<pat::Muon> MuonTagInfoCollectionProducer;
typedef LeptonTagInfoCollectionProducer<pat::Electron> ElectronTagInfoCollectionProducer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MuonTagInfoCollectionProducer);
DEFINE_FWK_MODULE(ElectronTagInfoCollectionProducer);
