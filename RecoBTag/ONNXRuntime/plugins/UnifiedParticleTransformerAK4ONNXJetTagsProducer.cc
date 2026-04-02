#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/makeRefToBaseProdFrom.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/BTauReco/interface/JetTag.h"

#include "DataFormats/BTauReco/interface/UnifiedParticleTransformerAK4TagInfo.h"
#include "DataFormats/BTauReco/interface/UnifiedParticleTransformerAK4Features.h"

#include "PhysicsTools/ONNXRuntime/interface/ONNXRuntime.h"
#include <algorithm>
#include <iostream>
#include <cassert>

using namespace cms::Ort;

class UnifiedParticleTransformerAK4ONNXJetTagsProducer : public edm::stream::EDProducer<edm::GlobalCache<ONNXRuntime>> {
public:
  explicit UnifiedParticleTransformerAK4ONNXJetTagsProducer(const edm::ParameterSet&, const ONNXRuntime*);
  ~UnifiedParticleTransformerAK4ONNXJetTagsProducer() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions&);

  static std::unique_ptr<ONNXRuntime> initializeGlobalCache(const edm::ParameterSet&);
  static void globalEndJob(const ONNXRuntime*);

private:
  typedef std::vector<reco::UnifiedParticleTransformerAK4TagInfo> TagInfoCollection;
  typedef reco::JetTagCollection JetTagCollection;

  void produce(edm::Event&, const edm::EventSetup&) override;

  void make_inputs(btagbtvdeep::UnifiedParticleTransformerAK4Features features);
  void make_test_inputs();
  void print_inputs();
  void get_input_sizes(const reco::FeaturesTagInfo<btagbtvdeep::UnifiedParticleTransformerAK4Features> taginfo);

  const edm::EDGetTokenT<TagInfoCollection> src_;
  std::vector<std::string> flav_names_;
  std::vector<std::string> input_names_;
  bool use_dynamic_axes_ = false;
  bool usePID_ = true; // default for UParT v00 and v01 models
  bool verbose_ = false;
  std::vector<std::string> output_names_;

  enum InputIndexes {
    kChargedCandidates = 0,
    kLostTracks = 1,
    kNeutralCandidates = 2,
    kVertices = 3,
    kChargedCandidates4Vec = 4,
    kLostTracks4Vec = 5,
    kNeutralCandidates4Vec = 6,
    kVertices4Vec = 7
  };
  unsigned n_cpf_;
  unsigned n_features_cpf_ = 25;
  constexpr static unsigned n_pairwise_features_cpf_ = 4;
  unsigned n_lt_;
  constexpr static unsigned n_features_lt_ = 18;
  constexpr static unsigned n_pairwise_features_lt_ = 4;
  unsigned n_npf_;
  constexpr static unsigned n_features_npf_ = 8;
  constexpr static unsigned n_pairwise_features_npf_ = 4;
  unsigned n_sv_;
  constexpr static unsigned n_features_sv_ = 14;
  constexpr static unsigned n_pairwise_features_sv_ = 4;
  std::vector<unsigned> input_sizes_;
  std::vector<std::vector<int64_t>> input_shapes_;  // shapes of each input group (-1 for dynamic axis)

  // hold the input data
  FloatArrays data_;

  // test mode config: "off" | "N" | "N+M"
  std::string testMode_ = "off"; // For ONNX & dyn. shapes integration tests
  unsigned testN_ = 1;
  unsigned testM_ = 0;
};

UnifiedParticleTransformerAK4ONNXJetTagsProducer::UnifiedParticleTransformerAK4ONNXJetTagsProducer(
    const edm::ParameterSet& iConfig, const ONNXRuntime* cache)
    : src_(consumes<TagInfoCollection>(iConfig.getParameter<edm::InputTag>("src"))),
      flav_names_(iConfig.getParameter<std::vector<std::string>>("flav_names")),
      input_names_(iConfig.getParameter<std::vector<std::string>>("input_names")),
        use_dynamic_axes_(
          (iConfig.getParameter<edm::FileInPath>("model_path").fullPath().find("V01") != std::string::npos)
                ||
          (iConfig.getParameter<edm::FileInPath>("model_path").fullPath().find("V02") != std::string::npos)
              ),
        usePID_(iConfig.getParameter<bool>("usePID")),
        verbose_(iConfig.getParameter<bool>("verbose")),
      output_names_(iConfig.getParameter<std::vector<std::string>>("output_names")),
      testMode_(iConfig.getParameter<std::string>("testMode")),
      testN_(iConfig.getParameter<unsigned>("testN")),
      testM_(iConfig.getParameter<unsigned>("testM")) {
  // get output names from flav_names
  // n_features_cpf_ = usePID_ ? 25 : 24;
  n_features_cpf_ = usePID_ ? 25 : 22;
  for (const auto& flav_name : flav_names_) {
    produces<JetTagCollection>(flav_name);
  }

  if (testMode_ != "off" && testMode_ != "N" && testMode_ != "N+M" && testMode_ != "print") {
    throw cms::Exception("Configuration") << "Invalid value for testMode: '" << testMode_
                                          << "'. Allowed values are: off, N, N+M, print";
  }
}

void UnifiedParticleTransformerAK4ONNXJetTagsProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  // pfUnifiedParticleTransformerAK4JetTags
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("src", edm::InputTag("pfUnifiedParticleTransformerAK4TagInfos"));
  desc.add<std::vector<std::string>>(
      "input_names", {"input_1", "input_2", "input_3", "input_4", "input_5", "input_6", "input_7", "input_8"});
  desc.add<edm::FileInPath>("model_path",
                            edm::FileInPath("RecoBTag/Combined/data/UParTAK4/PUPPI/V01/modelfile/model.onnx"));
  desc.add<std::vector<std::string>>("output_names", {"softmax"});
  desc.add<bool>("usePID", true);
  desc.add<bool>("verbose", false);
  desc.add<std::string>("testMode", "off");  // "off" | "N" | "N+M"
  desc.add<unsigned>("testN", 1);
  desc.add<unsigned>("testM", 0);
  desc.add<std::vector<std::string>>(
      "flav_names",
      std::vector<std::string>{"probb",        "probbb",       "problepb",     "probc",         "probs",
                               "probu",        "probd",        "probg",        "probele",       "probmu",
                               "probtaup1h0p", "probtaup1h1p", "probtaup1h2p", "probtaup3h0p",  "probtaup3h1p",
                               "probtaum1h0p", "probtaum1h1p", "probtaum1h2p", "probtaum3h0p",  "probtaum3h1p",
                               "ptcorr",       "ptreshigh",    "ptreslow",     "ptnu",          "probemudata",
                               "probemumc",    "probdimudata", "probdimumc",   "probmutaudata", "probmutaumc"});

  descriptions.add("pfUnifiedParticleTransformerAK4JetTags", desc);
}

std::unique_ptr<ONNXRuntime> UnifiedParticleTransformerAK4ONNXJetTagsProducer::initializeGlobalCache(
    const edm::ParameterSet& iConfig) {
  return std::make_unique<ONNXRuntime>(iConfig.getParameter<edm::FileInPath>("model_path").fullPath());
}

void UnifiedParticleTransformerAK4ONNXJetTagsProducer::globalEndJob(const ONNXRuntime* cache) {}

void UnifiedParticleTransformerAK4ONNXJetTagsProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  edm::Handle<TagInfoCollection> tag_infos;
  iEvent.getByToken(src_, tag_infos);

  // initialize output collection
  std::vector<std::unique_ptr<JetTagCollection>> output_tags;
  if (!tag_infos->empty()) {
    auto jet_ref = tag_infos->begin()->jet();
    auto ref2prod = edm::makeRefToBaseProdFrom(jet_ref, iEvent);
    for (std::size_t i = 0; i < flav_names_.size(); i++) {
      output_tags.emplace_back(std::make_unique<JetTagCollection>(ref2prod));
    }
  } else {
    for (std::size_t i = 0; i < flav_names_.size(); i++) {
      output_tags.emplace_back(std::make_unique<JetTagCollection>());
    }
  }

  for (unsigned jet_n = 0; jet_n < tag_infos->size(); ++jet_n) {
    const auto& taginfo = (*tag_infos)[jet_n];
    std::vector<float> outputs(flav_names_.size(), -1.0);
    if (taginfo.features().is_filled) {
      get_input_sizes(taginfo);

      // run prediction with dynamic batch size per event
      input_shapes_ = {{(int64_t)1, (int64_t)n_cpf_, (int64_t)n_features_cpf_},
                       {(int64_t)1, (int64_t)n_lt_, (int64_t)n_features_lt_},
                       {(int64_t)1, (int64_t)n_npf_, (int64_t)n_features_npf_},
                       {(int64_t)1, (int64_t)n_sv_, (int64_t)n_features_sv_},
                       {(int64_t)1, (int64_t)n_cpf_, (int64_t)n_pairwise_features_cpf_},
                       {(int64_t)1, (int64_t)n_lt_, (int64_t)n_pairwise_features_lt_},
                       {(int64_t)1, (int64_t)n_npf_, (int64_t)n_pairwise_features_npf_},
                       {(int64_t)1, (int64_t)n_sv_, (int64_t)n_pairwise_features_sv_}};

      if (verbose_){
        // print input names
        std::cout << "Input names: ";
        for (const auto& name : input_names_) {
          std::cout << name << " ";
        }
        std::cout << std::endl;
        // print output names
        std::cout << "Output names: ";
        for (const auto& name : output_names_) {
          std::cout << name << " ";
        }      std::cout << std::endl;

      }

      if (testMode_ == "print") {
        print_inputs();
      }
      // Always run the model to produce real scores (also for 'print' mode)
      outputs = globalCache()->run(input_names_, data_, input_shapes_, output_names_, 1)[0];
      assert(outputs.size() == flav_names_.size());
    }

    const auto& jet_ref = tag_infos->at(jet_n).jet();
    for (std::size_t flav_n = 0; flav_n < flav_names_.size(); flav_n++) {
      // print flav name and output value
      if (verbose_) {
        std::cout << "Jet " << jet_ref.key() << ": " << flav_names_[flav_n] << " = " << outputs[flav_n] << std::endl;
      }
      (*(output_tags[flav_n]))[jet_ref] = outputs[flav_n];
    }
  }

  // put into the event
  for (std::size_t flav_n = 0; flav_n < flav_names_.size(); ++flav_n) {
    iEvent.put(std::move(output_tags[flav_n]), flav_names_[flav_n]);
  }
}

void UnifiedParticleTransformerAK4ONNXJetTagsProducer::get_input_sizes(
    const reco::FeaturesTagInfo<btagbtvdeep::UnifiedParticleTransformerAK4Features> taginfo) {
  const auto& features = taginfo.features();

  const unsigned max_cpf = use_dynamic_axes_ ? (usePID_ ? 29u : 25u) : 29u;
  const unsigned max_lt = 5u;
  const unsigned max_npf = use_dynamic_axes_ ? (usePID_ ? 25u : 20u) : 25u;
  const unsigned max_sv = use_dynamic_axes_ ? (usePID_ ? 5u : 5u) : 5u;

  if (testMode_ == "N" || testMode_ == "N+M") {
    const unsigned fakeLen = (testMode_ == "N") ? testN_ : (testN_ + testM_);
    n_cpf_ = std::min(std::max<unsigned>(1u, fakeLen), max_cpf);
    n_lt_ = std::min(std::max<unsigned>(1u, fakeLen), max_lt);
    n_npf_ = std::min(std::max<unsigned>(1u, fakeLen), max_npf);
    n_sv_ = std::min(std::max<unsigned>(1u, fakeLen), max_sv);

    if (verbose_) {
      std::cout << "[TEST MODE] mode=" << testMode_ << " N=" << testN_ << " M=" << testM_
                << " -> n_cpf=" << n_cpf_ << ", n_lt=" << n_lt_ << ", n_npf=" << n_npf_ << ", n_sv=" << n_sv_
                << std::endl;
    }
  } else if (use_dynamic_axes_) {
    // Use actual sizes for dynamic axes version
    if (!usePID_) {
      if (verbose_) std::cout << "Using dynamic axes without PID features, setting max sizes to 25, 5, 20, 6 respectively" << std::endl;
      n_cpf_ = std::min<unsigned>(std::max<unsigned>(1u, (unsigned)features.c_pf_features.size()), 25u);
      n_lt_ = std::min<unsigned>(std::max<unsigned>(1u, (unsigned)features.lt_features.size()), 5u);
      n_npf_ = std::min<unsigned>(std::max<unsigned>(1u, (unsigned)features.n_pf_features.size()), 20u);
      n_sv_ = std::min<unsigned>(std::max<unsigned>(1u, (unsigned)features.sv_features.size()), 6u);
    } else {
      if (verbose_) std::cout << "Using dynamic axes with PID features, setting max sizes to 29, 5, 25, 5 respectively" << std::endl;
      n_cpf_ = std::min<unsigned>(std::max<unsigned>(1u, (unsigned)features.c_pf_features.size()), 29u);
      n_lt_ = std::min<unsigned>(std::max<unsigned>(1u, (unsigned)features.lt_features.size()), 5u);
      n_npf_ = std::min<unsigned>(std::max<unsigned>(1u, (unsigned)features.n_pf_features.size()), 25u);
      n_sv_ = std::min<unsigned>(std::max<unsigned>(1u, (unsigned)features.sv_features.size()), 5u);
    }

  } else {
    // Use fixed sizes for original version
    n_cpf_ = (unsigned int)29;
    n_lt_ = (unsigned int)5;
    n_npf_ = (unsigned int)25;
    n_sv_ = (unsigned int)5;
  }

    if (verbose_) {
                std::cout << "Jet " << taginfo.jet().key() << ": n_cpf = " << n_cpf_ << ", n_lt = " << n_lt_
                          << ", n_npf = " << n_npf_ << ", n_sv = " << n_sv_ << std::endl;
              }

  input_sizes_ = {
      n_cpf_ * n_features_cpf_,
      n_lt_ * n_features_lt_,
      n_npf_ * n_features_npf_,
      n_sv_ * n_features_sv_,
      n_cpf_ * n_pairwise_features_cpf_,
      n_lt_ * n_pairwise_features_lt_,
      n_npf_ * n_pairwise_features_npf_,
      n_sv_ * n_pairwise_features_sv_,
  };

  if (verbose_) {
    std::cout << "Input sizes: ";
    for (const auto& size : input_sizes_) {
      std::cout << size << " ";
    }
    std::cout << std::endl;
  }

  // init data storage
  data_.clear();
  for (const auto& len : input_sizes_) {
    data_.emplace_back(1 * len, 0);
  }
  if (testMode_ == "off" || testMode_ == "print") {
    make_inputs(features);
  } else {
    make_test_inputs();
  }
}

void UnifiedParticleTransformerAK4ONNXJetTagsProducer::make_inputs(
    btagbtvdeep::UnifiedParticleTransformerAK4Features features) {
  float* ptr = nullptr;
  const float* start = nullptr;
  unsigned offset = 0;

  // c_pf candidates
  auto max_c_pf_n = std::min(features.c_pf_features.size(), (std::size_t)n_cpf_);
  if (verbose_) {
    std::cout << "Filling c_pf features, max candidates: " << max_c_pf_n << std::endl;
  }
  for (std::size_t c_pf_n = 0; c_pf_n < max_c_pf_n; c_pf_n++) {
    const auto& c_pf_features = features.c_pf_features.at(c_pf_n);
    ptr = &data_[kChargedCandidates][offset + c_pf_n * n_features_cpf_];
    start = ptr;
    // common fields
    *ptr = c_pf_features.btagPf_trackEtaRel;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackEtaRel = " << c_pf_features.btagPf_trackEtaRel << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackPtRel;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackPtRel = " << c_pf_features.btagPf_trackPtRel << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackPPar;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackPPar = " << c_pf_features.btagPf_trackPPar << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackDeltaR;
     if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackDeltaR = " << c_pf_features.btagPf_trackDeltaR << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackPParRatio;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackPParRatio = " << c_pf_features.btagPf_trackPParRatio << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackSip2dVal;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackSip2dVal = " << c_pf_features.btagPf_trackSip2dVal << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackSip2dSig;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackSip2dSig = " << c_pf_features.btagPf_trackSip2dSig << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackSip3dVal;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackSip3dVal = " << c_pf_features.btagPf_trackSip3dVal << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackSip3dSig;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackSip3dSig = " << c_pf_features.btagPf_trackSip3dSig << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackJetDistVal;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackJetDistVal = " << c_pf_features.btagPf_trackJetDistVal << std::endl;}
    *(++ptr) = c_pf_features.ptrel;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": ptrel = " << c_pf_features.ptrel << std::endl;}
    *(++ptr) = c_pf_features.drminsv;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": drminsv = " << c_pf_features.drminsv << std::endl;}
    *(++ptr) = c_pf_features.vtx_ass;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": vtx_ass = " << c_pf_features.vtx_ass << std::endl;}
    *(++ptr) = c_pf_features.puppiw;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": puppiw = " << c_pf_features.puppiw << std::endl;}
    *(++ptr) = c_pf_features.chi2;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": chi2 = " << c_pf_features.chi2 << std::endl;}
    *(++ptr) = c_pf_features.quality;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": quality = " << c_pf_features.quality << std::endl;}
    *(++ptr) = c_pf_features.charge;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": charge = " << c_pf_features.charge << std::endl;}
    *(++ptr) = c_pf_features.dz;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": dz = " << c_pf_features.dz << std::endl;}
    *(++ptr) = c_pf_features.btagPf_trackDecayLen;
    if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": btagPf_trackDecayLen = " << c_pf_features.btagPf_trackDecayLen << std::endl;}
    if (usePID_) {
      *(++ptr) = c_pf_features.HadFrac;
        if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": HadFrac = " << c_pf_features.HadFrac << std::endl;}
      *(++ptr) = c_pf_features.CaloFrac;
        if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": CaloFrac = " << c_pf_features.CaloFrac << std::endl;}
      *(++ptr) = c_pf_features.pdgID;
        if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": pdgID = " << c_pf_features.pdgID << std::endl;}
    }

    *(++ptr) = c_pf_features.lostInnerHits;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": lostInnerHits = " << c_pf_features.lostInnerHits << std::endl;}
    *(++ptr) = c_pf_features.numberOfPixelHits;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": numberOfPixelHits = " << c_pf_features.numberOfPixelHits << std::endl;}
    *(++ptr) = c_pf_features.numberOfStripHits;
      if (verbose_) {std::cout << "Charged candidate " << c_pf_n << ": numberOfStripHits = " << c_pf_features.numberOfStripHits << std::endl;}

    assert(start + n_features_cpf_ - 1 == ptr);
  }

  // n_lt candidates
  auto max_lt_n = std::min(features.lt_features.size(), (std::size_t)n_lt_);
  if (verbose_) {
    std::cout << "Filling lt features, max " << max_lt_n << std::endl;
  }
  for (std::size_t lt_n = 0; lt_n < max_lt_n; lt_n++) {
    const auto& lt_features = features.lt_features.at(lt_n);
    ptr = &data_[kLostTracks][offset + lt_n * n_features_lt_];
    start = ptr;
    *ptr = lt_features.btagPf_trackEtaRel;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackEtaRel = " << lt_features.btagPf_trackEtaRel << std::endl;}
    *(++ptr) = lt_features.btagPf_trackPtRel;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackPtRel = " << lt_features.btagPf_trackPtRel << std::endl;}
    *(++ptr) = lt_features.btagPf_trackPPar;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackPPar = " << lt_features.btagPf_trackPPar << std::endl;}
    *(++ptr) = lt_features.btagPf_trackDeltaR;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackDeltaR = " << lt_features.btagPf_trackDeltaR << std::endl;}
    *(++ptr) = lt_features.btagPf_trackPParRatio;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackPParRatio = " << lt_features.btagPf_trackPParRatio << std::endl;}
    *(++ptr) = lt_features.btagPf_trackSip2dVal;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackSip2dVal = " << lt_features.btagPf_trackSip2dVal << std::endl;}
    *(++ptr) = lt_features.btagPf_trackSip2dSig;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackSip2dSig = " << lt_features.btagPf_trackSip2dSig << std::endl;}
    *(++ptr) = lt_features.btagPf_trackSip3dVal;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackSip3dVal = " << lt_features.btagPf_trackSip3dVal << std::endl;}
    *(++ptr) = lt_features.btagPf_trackSip3dSig;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackSip3dSig = " << lt_features.btagPf_trackSip3dSig << std::endl;}
    *(++ptr) = lt_features.btagPf_trackJetDistVal;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": btagPf_trackJetDistVal = " << lt_features.btagPf_trackJetDistVal << std::endl;}
    *(++ptr) = lt_features.drminsv;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": drminsv = " << lt_features.drminsv << std::endl;}
    *(++ptr) = lt_features.charge;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": charge = " << lt_features.charge << std::endl;}
    *(++ptr) = lt_features.puppiw;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": puppiw = " << lt_features.puppiw << std::endl;}
    *(++ptr) = lt_features.chi2;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": chi2 = " << lt_features.chi2 << std::endl;}
    *(++ptr) = lt_features.quality;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": quality = " << lt_features.quality << std::endl;}
    *(++ptr) = lt_features.lostInnerHits;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": lostInnerHits = " << lt_features.lostInnerHits << std::endl;}
    *(++ptr) = lt_features.numberOfPixelHits;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": numberOfPixelHits = " << lt_features.numberOfPixelHits << std::endl;}
    *(++ptr) = lt_features.numberOfStripHits;
    if (verbose_) {std::cout << "Lost track " << lt_n << ": numberOfStripHits = " << lt_features.numberOfStripHits << std::endl;}
    assert(start + n_features_lt_ - 1 == ptr);
  }

  // n_pf candidates
  auto max_n_pf_n = std::min(features.n_pf_features.size(), (std::size_t)n_npf_);
    if (verbose_) {
      std::cout << "Filling n_pf features, max " << max_n_pf_n << std::endl;
    }
  for (std::size_t n_pf_n = 0; n_pf_n < max_n_pf_n; n_pf_n++) {
    const auto& n_pf_features = features.n_pf_features.at(n_pf_n);
    ptr = &data_[kNeutralCandidates][offset + n_pf_n * n_features_npf_];
    start = ptr;
    *ptr = n_pf_features.ptrel;
      if (verbose_) {std::cout << "Neutral candidate " << n_pf_n << ": ptrel = " << n_pf_features.ptrel << std::endl;}
    *(++ptr) = n_pf_features.etarel;
    if (verbose_) {std::cout << "Neutral candidate " << n_pf_n << ": etarel = " << n_pf_features.etarel << std::endl;}
    *(++ptr) = n_pf_features.phirel;
    if (verbose_) {std::cout << "Neutral candidate " << n_pf_n << ": phirel = " << n_pf_features.phirel << std::endl;}
    *(++ptr) = n_pf_features.deltaR;
    if (verbose_) {std::cout << "Neutral candidate " << n_pf_n << ": deltaR = " << n_pf_features.deltaR << std::endl;}
    *(++ptr) = n_pf_features.isGamma;
    if (verbose_) {std::cout << "Neutral candidate " << n_pf_n << ": isGamma = " << n_pf_features.isGamma << std::endl;}
    *(++ptr) = n_pf_features.hadFrac;
    if (verbose_) {std::cout << "Neutral candidate " << n_pf_n << ": hadFrac = " << n_pf_features.hadFrac << std::endl;}
    *(++ptr) = n_pf_features.drminsv;
    if (verbose_) {std::cout << "Neutral candidate " << n_pf_n << ": drminsv = " << n_pf_features.drminsv << std::endl;}
    *(++ptr) = n_pf_features.puppiw;
    if (verbose_) {std::cout << "Neutral candidate " << n_pf_n << ": puppiw = " << n_pf_features.puppiw << std::endl;}
    assert(start + n_features_npf_ - 1 == ptr);
  }

  // sv candidates
  auto max_sv_n = std::min(features.sv_features.size(), (std::size_t)n_sv_);
    if (verbose_) {
        std::cout << "Filling sv features, max " << max_sv_n << std::endl;
      }
  for (std::size_t sv_n = 0; sv_n < max_sv_n; sv_n++) {
    const auto& sv_features = features.sv_features.at(sv_n);
    ptr = &data_[kVertices][offset + sv_n * n_features_sv_];
    start = ptr;
    *ptr = sv_features.pt;
      if (verbose_) {std::cout << "SV " << sv_n << ": pt = " << sv_features.pt << std::endl;}
    *(++ptr) = sv_features.deltaR;
    if (verbose_) {std::cout << "SV " << sv_n << ": deltaR = " << sv_features.deltaR << std::endl;}
    *(++ptr) = sv_features.mass;
    if (verbose_) {std::cout << "SV " << sv_n << ": mass = " << sv_features.mass << std::endl;}
    *(++ptr) = sv_features.etarel;
    if (verbose_) {std::cout << "SV " << sv_n << ": etarel = " << sv_features.etarel << std::endl;}
    *(++ptr) = sv_features.phirel;
    if (verbose_) {std::cout << "SV " << sv_n << ": phirel = " << sv_features.phirel << std::endl;}
    *(++ptr) = sv_features.ntracks;
    if (verbose_) {std::cout << "SV " << sv_n << ": ntracks = " << sv_features.ntracks << std::endl;}
    *(++ptr) = sv_features.chi2;
    if (verbose_) {std::cout << "SV " << sv_n << ": chi2 = " << sv_features.chi2 << std::endl;}
    *(++ptr) = sv_features.normchi2;
    if (verbose_) {std::cout << "SV " << sv_n << ": normchi2 = " << sv_features.normchi2 << std::endl;}
    *(++ptr) = sv_features.dxy;
    if (verbose_) {std::cout << "SV " << sv_n << ": dxy = " << sv_features.dxy << std::endl;}
    *(++ptr) = sv_features.dxysig;
    if (verbose_) {std::cout << "SV " << sv_n << ": dxysig = " << sv_features.dxysig << std::endl;}
    *(++ptr) = sv_features.d3d;
    if (verbose_) {std::cout << "SV " << sv_n << ": d3d = " << sv_features.d3d << std::endl;}
    *(++ptr) = sv_features.d3dsig;
    if (verbose_) {std::cout << "SV " << sv_n << ": d3dsig = " << sv_features.d3dsig << std::endl;}
    *(++ptr) = sv_features.costhetasvpv;
    if (verbose_) {std::cout << "SV " << sv_n << ": costhetasvpv = " << sv_features.costhetasvpv << std::endl;}
    *(++ptr) = sv_features.enratio;
    if (verbose_) {std::cout << "SV " << sv_n << ": enratio = " << sv_features.enratio << std::endl;}
    assert(start + n_features_sv_ - 1 == ptr);
  }

  // cpf pairwise features (4-vectors)
  auto max_cpf_n = std::min(features.c_pf_features.size(), (std::size_t)n_cpf_);
  if (verbose_) {
    std::cout << "Filling pairwise cpf features, max " << max_cpf_n << std::endl;
  }
  for (std::size_t cpf_n = 0; cpf_n < max_cpf_n; cpf_n++) {
    const auto& cpf_pairwise_features = features.c_pf_features.at(cpf_n);
    ptr = &data_[kChargedCandidates4Vec][offset + cpf_n * n_pairwise_features_cpf_];
    start = ptr;
    *ptr = cpf_pairwise_features.px;
    if (verbose_) {std::cout << "Charged candidate " << cpf_n << ": px = " << cpf_pairwise_features.px << std::endl;}
    *(++ptr) = cpf_pairwise_features.py;
    if (verbose_) {std::cout << "Charged candidate " << cpf_n << ": py = " << cpf_pairwise_features.py << std::endl;}
    *(++ptr) = cpf_pairwise_features.pz;
    if (verbose_) {std::cout << "Charged candidate " << cpf_n << ": pz = " << cpf_pairwise_features.pz << std::endl;}
    *(++ptr) = cpf_pairwise_features.e;
    if (verbose_) {std::cout << "Charged candidate " << cpf_n << ": e = " << cpf_pairwise_features.e << std::endl;}

    assert(start + n_pairwise_features_cpf_ - 1 == ptr);
  }

  // lt pairwise features (4-vectors) specific case requiring (pt,eta,phi,e)
  auto max_lt_N = std::min(features.lt_features.size(), (std::size_t)n_lt_);
  if (verbose_) {
    std::cout << "Filling pairwise lt features, max " << max_lt_n << std::endl;
  }
  for (std::size_t lt_N = 0; lt_N < max_lt_N; lt_N++) {
    const auto& lt_pairwise_features = features.lt_features.at(lt_N);
    ptr = &data_[kLostTracks4Vec][offset + lt_N * n_pairwise_features_lt_];
    start = ptr;
    *ptr = lt_pairwise_features.pt;
    if (verbose_) {std::cout << "Lost track " << lt_N << ": pt = " << lt_pairwise_features.pt << std::endl;}
    *(++ptr) = lt_pairwise_features.eta;
    if (verbose_) {std::cout << "Lost track " << lt_N << ": eta = " << lt_pairwise_features.eta << std::endl;}
    *(++ptr) = lt_pairwise_features.phi;
    if (verbose_) {std::cout << "Lost track " << lt_N << ": phi = " << lt_pairwise_features.phi << std::endl;}
    *(++ptr) = lt_pairwise_features.e;
    if (verbose_) {std::cout << "Lost track " << lt_N << ": e = " << lt_pairwise_features.e << std::endl;}

    assert(start + n_pairwise_features_lt_ - 1 == ptr);
  }

  // npf pairwise features (4-vectors)
  auto max_npf_n = std::min(features.n_pf_features.size(), (std::size_t)n_npf_);
  if (verbose_) {
    std::cout << "Filling pairwise n_pf features, max " << max_npf_n << std::endl;
  }
  for (std::size_t npf_n = 0; npf_n < max_npf_n; npf_n++) {
    const auto& npf_pairwise_features = features.n_pf_features.at(npf_n);
    ptr = &data_[kNeutralCandidates4Vec][offset + npf_n * n_pairwise_features_npf_];
    start = ptr;
    *ptr = npf_pairwise_features.px;
      if (verbose_) {std::cout << "Neutral candidate " << npf_n << ": px = " << npf_pairwise_features.px << std::endl;}
    *(++ptr) = npf_pairwise_features.py;
    if (verbose_) {std::cout << "Neutral candidate " << npf_n << ": py = " << npf_pairwise_features.py << std::endl;}
    *(++ptr) = npf_pairwise_features.pz;
    if (verbose_) {std::cout << "Neutral candidate " << npf_n << ": pz = " << npf_pairwise_features.pz << std::endl;}
    *(++ptr) = npf_pairwise_features.e;
    if (verbose_) {std::cout << "Neutral candidate " << npf_n << ": e = " << npf_pairwise_features.e << std::endl;}

    assert(start + n_pairwise_features_npf_ - 1 == ptr);
  }

  // sv pairwise features (4-vectors)
  auto max_sv_N = std::min(features.sv_features.size(), (std::size_t)n_sv_);
  if (verbose_) {
    std::cout << "Filling pairwise sv features, max " << max_sv_n << std::endl;
  }
  for (std::size_t sv_N = 0; sv_N < max_sv_N; sv_N++) {
    const auto& sv_pairwise_features = features.sv_features.at(sv_N);
    ptr = &data_[kVertices4Vec][offset + sv_N * n_pairwise_features_sv_];
    start = ptr;
    *ptr = sv_pairwise_features.px;
      if (verbose_) {std::cout << "SV " << sv_N << ": px = " << sv_pairwise_features.px << std::endl;}
    *(++ptr) = sv_pairwise_features.py;
    if (verbose_) {std::cout << "SV " << sv_N << ": py = " << sv_pairwise_features.py << std::endl;}
    *(++ptr) = sv_pairwise_features.pz;
    if (verbose_) {std::cout << "SV " << sv_N << ": pz = " << sv_pairwise_features.pz << std::endl;}
    *(++ptr) = sv_pairwise_features.e;
    if (verbose_) {std::cout << "SV " << sv_N << ": e = " << sv_pairwise_features.e << std::endl;}

    assert(start + n_pairwise_features_sv_ - 1 == ptr);
  }
}

void UnifiedParticleTransformerAK4ONNXJetTagsProducer::make_test_inputs() {
  // data_ already zero-initialized in get_input_sizes()

  const unsigned ones_cpf = (testMode_ == "N") ? n_cpf_ : std::min(testN_, n_cpf_);
  const unsigned ones_lt = (testMode_ == "N") ? n_lt_ : std::min(testN_, n_lt_);
  const unsigned ones_npf = (testMode_ == "N") ? n_npf_ : std::min(testN_, n_npf_);
  const unsigned ones_sv = (testMode_ == "N") ? n_sv_ : std::min(testN_, n_sv_);

  auto fillLeadingOnes = [&](unsigned idx, unsigned nObj, unsigned nFeat, unsigned nOnesObj) {
    for (unsigned i = 0; i < std::min(nObj, nOnesObj); ++i) {
      const unsigned base = i * nFeat;
      for (unsigned f = 0; f < nFeat; ++f) {
        data_[idx][base + f] = 1.f;
      }
    }
  };

  fillLeadingOnes(kChargedCandidates, n_cpf_, n_features_cpf_, ones_cpf);
  fillLeadingOnes(kLostTracks, n_lt_, n_features_lt_, ones_lt);
  fillLeadingOnes(kNeutralCandidates, n_npf_, n_features_npf_, ones_npf);
  fillLeadingOnes(kVertices, n_sv_, n_features_sv_, ones_sv);

  fillLeadingOnes(kChargedCandidates4Vec, n_cpf_, n_pairwise_features_cpf_, ones_cpf);
  fillLeadingOnes(kLostTracks4Vec, n_lt_, n_pairwise_features_lt_, ones_lt);
  fillLeadingOnes(kNeutralCandidates4Vec, n_npf_, n_pairwise_features_npf_, ones_npf);
  fillLeadingOnes(kVertices4Vec, n_sv_, n_pairwise_features_sv_, ones_sv);

  if (verbose_) {
    std::cout << "[TEST MODE] Filled synthetic inputs: mode=" << testMode_ << " N=" << testN_ << " M=" << testM_
              << std::endl;
  }
}

void UnifiedParticleTransformerAK4ONNXJetTagsProducer::print_inputs() {
  // Print each input group as a Python nested list with shape info.
  for (std::size_t idx = 0; idx < input_names_.size(); ++idx) {
    const auto& name = input_names_[idx];
    const auto& shape = input_shapes_[idx];
    const int64_t batch = shape[0];
    const int64_t nObj = shape[1];
    const int64_t nFeat = shape[2];

    std::cout << "# Input '" << name << "' shape=(" << batch << "," << nObj << "," << nFeat << ")\n";
    std::cout << name << " = [" << std::endl;
    // batch dim (expected 1)
    for (int64_t b = 0; b < batch; ++b) {
      std::cout << "  [" << std::endl;
      // each object
      const auto& flat = data_[idx];
      for (int64_t i = 0; i < nObj; ++i) {
        std::cout << "    [";
        for (int64_t f = 0; f < nFeat; ++f) {
          const std::size_t pos = static_cast<std::size_t>(i * nFeat + f);
          // ensure within vector bounds
          float v = 0.f;
          if (pos < flat.size()) v = flat[pos];
          std::cout << v;
          if (f + 1 < nFeat) std::cout << ", ";
        }
        std::cout << "]";
        if (i + 1 < nObj) std::cout << ",";
        std::cout << std::endl;
      }
      std::cout << "  ]" << std::endl;
    }
    std::cout << "]" << std::endl << std::endl;
  }
}

//define this as a plug-in
DEFINE_FWK_MODULE(UnifiedParticleTransformerAK4ONNXJetTagsProducer);
