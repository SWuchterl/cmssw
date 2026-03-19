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
#include "TTree.h"
#include <any>

template <typename T>
class MvaNtuplizer : public edm::one::EDAnalyzer<edm::one::SharedResources> {

 public:
  explicit MvaNtuplizer(const edm::ParameterSet&);
  ~MvaNtuplizer();

 private:
  void beginJob() override;
  void analyze(const edm::Event&, const edm::EventSetup&) override;
  void endJob() override;

  using LeptonTagInfoCollection = btagbtvdeep::DeepBoostedJetFeaturesCollection;

  //  edm::EDGetTokenT<pat::LeptonTagInfoCollection<T>> src_;
  edm::EDGetTokenT<LeptonTagInfoCollection> src_;
  edm::EDGetTokenT<std::vector<T>> srcLeps_;
  edm::EDGetTokenT<nanoaod::FlatTable> srcMcTable_;
  const std::string cut_;
  const StringCutObjectSelector<T> selector_;

  TTree* outtree;
  edm::Service<TFileService> fs;  
  std::map<std::string, std::vector<float>> output_vars;
  uint8_t genPartFlav;
  long int event;
  int luminosityBlock;
  int run;
};
