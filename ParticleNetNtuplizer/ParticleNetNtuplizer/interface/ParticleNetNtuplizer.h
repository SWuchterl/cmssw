#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "PhysicsTools/PatAlgos/interface/LeptonTagInfoCollectionProducer.h"
#include "DataFormats/BTauReco/interface/DeepBoostedJetFeatures.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "CommonTools/UtilAlgos/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "TTree.h"
#include <any>
#include <array>
#include <unordered_set>

template <typename T>
class MvaNtuplizer : public edm::one::EDAnalyzer<edm::one::SharedResources> {

 public:
  explicit MvaNtuplizer(const edm::ParameterSet&);
  ~MvaNtuplizer();

 private:
  void beginJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;
  size_t maxLenForCategory(const std::string& cat) const;
  void fill_truth(const T& lep, const edm::Ref<std::vector<T>>& ref, const edm::Event& iEvent);
  void fill_categories(const std::vector<T>& leptons, const std::vector<int>& flav, const edm::Event& iEvent);
  // the trees hold no NaN or inf: a value that cannot be computed is written as 0, counted per branch in nonFinite_
  float finiteOrZero(const std::string& name, float value);

  using LeptonTagInfoCollection = btagbtvdeep::DeepBoostedJetFeaturesCollection;

  // per-category cap on the number of stored entries
  std::map<std::string, size_t> maxLengths_;
  // features not written to the tree
  std::unordered_set<std::string> drop_;
  // truth branches (Lepton_gen*), only if genMatch is configured
  bool doTruth_ = false;
  edm::EDGetTokenT<edm::Association<reco::GenParticleCollection>> genMatch_token_;
  edm::EDGetTokenT<edm::Association<reco::GenJetCollection>> dressedMatch_token_;
  edm::EDGetTokenT<reco::GenParticleCollection> pruned_token_;
  edm::EDGetTokenT<pat::PackedGenParticleCollection> packed_token_;
  bool doDressed_ = false;
  edm::EDGetTokenT<std::vector<PileupSummaryInfo>> pileup_token_;
  std::map<std::string, float> truth_vars_;
  // electrons: Rivet dressed leptons (particleLevel:leptons) give the pT reference of the prompt gen lepton
  bool doDressedLeptons_ = false;
  edm::EDGetTokenT<reco::GenJetCollection> dressedLeptons_token_;
  // per lepton of the event: genCategory, genCatChargeFlip, genPromptDR, genPromptPtRatio, genNearestDR
  std::vector<std::array<float, 5>> categories_;

  //  edm::EDGetTokenT<pat::LeptonTagInfoCollection<T>> src_;
  edm::EDGetTokenT<LeptonTagInfoCollection> src_;
  edm::EDGetTokenT<std::vector<T>> srcLeps_;
  edm::EDGetTokenT<nanoaod::FlatTable> srcMcTable_;
  const std::string cut_;
  const StringCutObjectSelector<T> selector_;

  TTree* outtree;
  edm::Service<TFileService> fs;  
  std::map<std::string, std::vector<float>> output_vars;
  // per-category sizes (e.g. nPF, nLT, nSV)
  std::map<std::string, unsigned> output_cat_sizes;
  // scalar storage for Lepton_* features (fixed length 1)
  std::map<std::string, float> output_scalar_vars;
  // number of non-finite feature values written as 0, per branch (reported in endJob)
  std::map<std::string, unsigned> nonFinite_;
  uint8_t genPartFlav;
  long int event;
  int luminosityBlock;
  int run;
};
