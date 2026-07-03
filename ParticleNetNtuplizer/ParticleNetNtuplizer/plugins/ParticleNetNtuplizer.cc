#include"ParticleNetNtuplizer/ParticleNetNtuplizer/interface/ParticleNetNtuplizer.h"
#include <algorithm>
#include <unordered_set>
#include <unordered_map>
static constexpr size_t kMaxFeatureLen = 60;

template <typename T>
MvaNtuplizer<T>::MvaNtuplizer(const edm::ParameterSet& iConfig) :
  //src_(consumes<pat::LeptonTagInfoCollection<T>>(iConfig.getParameter<edm::InputTag>("src"))),
  src_(consumes<LeptonTagInfoCollection>(iConfig.getParameter<edm::InputTag>("src"))),
  srcLeps_(consumes<std::vector<T>>(iConfig.getParameter<edm::InputTag>("srcLeptons"))),
  srcMcTable_(consumes<nanoaod::FlatTable>(iConfig.getParameter<edm::InputTag>("srcMcTable"))),
  cut_(iConfig.getParameter<std::string>("leptonSelection")),
  selector_(cut_)
{
  outtree = fs->make<TTree>( "Events", "Events");
  outtree->SetAutoFlush(-30000000);

}

template <typename T>
MvaNtuplizer<T>::~MvaNtuplizer() {}

template <typename T>
void MvaNtuplizer<T>::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  //  edm::Handle<pat::LeptonTagInfoCollection<T>> src;
  edm::Handle<LeptonTagInfoCollection> src;
  iEvent.getByToken(src_, src); 

  edm::Handle<nanoaod::FlatTable> mcTable;
  iEvent.getByToken(srcMcTable_, mcTable); 

  edm::Handle<std::vector<T>> leptons;
  iEvent.getByToken(srcLeps_, leptons); 

  if (src->size() != leptons->size()){throw cms::Exception("Tables and leptons not aligned");}
  if (src->size() != mcTable->nRows()){throw cms::Exception("Tables and leptons not aligned");}

  // First time initialize branches if theres a lepton to read them from
  if (src->size() > 0 && output_vars.empty()){
    const auto& taginfo = (*src)[0];
    // create fixed-size arrays (vectors sized to kMaxFeatureLen) and collect categories
    std::unordered_set<std::string> categories;
    for (const auto& var : taginfo.get_all()){
      const std::string& name = var.first;
      // treat Lepton_* features as scalars (fixed length 1)
      if (name.rfind("Lepton", 0) == 0) {
        output_scalar_vars[name] = 0.f;
        continue;
      }
      output_vars[name] = std::vector<float>(kMaxFeatureLen);
      // extract category prefix before first underscore, e.g. PF_var -> PF
      auto pos = name.find('_');
      std::string cat = (pos == std::string::npos) ? name : name.substr(0, pos);
      categories.insert(cat);
    }
    // create one length branch per category (named n<cat>) first
    for (const auto& cat : categories) {
      output_cat_sizes[cat] = 0u;
      outtree->Branch((std::string("n") + cat).c_str(), &output_cat_sizes[cat], (std::string("n") + cat + "/i").c_str());
    }
    // create scalar branches for Lepton_* features
    for (auto &kv : output_scalar_vars) {
      outtree->Branch(kv.first.c_str(), &output_scalar_vars[kv.first], (kv.first + "/F").c_str());
    }
    // now create variable branches referencing the category length branch (variable-length)
    for (const auto& kv : output_vars) {
      const std::string& name = kv.first;
      auto pos = name.find('_');
      std::string cat = (pos == std::string::npos) ? name : name.substr(0, pos);
      const std::string leaf = name + "[n" + cat + "]/F";
      outtree->Branch(name.c_str(), output_vars[name].data(), leaf.c_str());
      // set the basket size for this branch for efficient python read
      outtree->GetBranch(name.c_str())->SetBasketSize(1000000);
    }
    outtree->Branch("genPartFlav", &genPartFlav, "genPartFlav/b", 1000000);
    outtree->Branch("event", &event, "event/l", 1000000);
    outtree->Branch("luminosityBlock", &luminosityBlock, "luminosityBlock/i", 1000000);
    outtree->Branch("run", &run, "run/i", 1000000);
  
  }
  event=iEvent.eventAuxiliary().id().event();
  luminosityBlock = iEvent.eventAuxiliary().luminosityBlock();
  run=iEvent.eventAuxiliary().run();
  // now lets actually fill things
  for (size_t ilep=0; ilep < src->size(); ilep++){
    if (!selector_( leptons->at(ilep))) continue;

    const auto& taginfo = (*src)[ilep];
    // reset per-category lengths and track per-category length for this lepton
    for (auto &p : output_cat_sizes) p.second = 0u;
    std::unordered_map<std::string, unsigned> cat_len;
    for (const auto& var : taginfo.get_all()){
      // handle scalar Lepton_* features
      auto sit = output_scalar_vars.find(var.first);
      if (sit != output_scalar_vars.end()){
        sit->second = (var.second.size() > 0) ? var.second[0] : 0.f;
        continue;
      }
      auto it = output_vars.find(var.first);
      if (it == output_vars.end()) continue;
      const size_t ncopy = std::min(var.second.size(), kMaxFeatureLen);
      if (ncopy > 0)
        std::copy(var.second.begin(), var.second.begin() + ncopy, it->second.begin());
      // determine category and update its length
      auto pos = var.first.find('_');
      std::string cat = (pos == std::string::npos) ? var.first : var.first.substr(0, pos);
      auto cit = cat_len.find(cat);
      if (cit == cat_len.end() || cat_len[cat] < ncopy) cat_len[cat] = static_cast<unsigned>(ncopy);
    }
    // write per-category lengths into the output map (branches point to these)
    for (const auto& kv : cat_len) {
      output_cat_sizes[kv.first] = kv.second;
    }
    for (auto ivar=0u; ivar<mcTable->nColumns(); ++ivar){
      if (mcTable->columnName(ivar).compare("genPartFlav") == 0){
	      genPartFlav = mcTable->columnData<uint8_t>(ivar)[ilep];
      }
    }
    outtree->Fill();    
  }

}



template <typename T>
void MvaNtuplizer<T>::beginJob(){
  edm::Service<TFileService> fs;
  if (!fs) return;
  // set compression settings for the output file, optimized for speed and reasonable compression
  fs->file().SetCompressionAlgorithm(ROOT::kLZ4);
  fs->file().SetCompressionLevel(4);
}

template <typename T>
void MvaNtuplizer<T>::endJob(){}

typedef MvaNtuplizer<pat::Muon> MuonNtuplizer;
typedef MvaNtuplizer<pat::Electron> ElectronNtuplizer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MuonNtuplizer);
DEFINE_FWK_MODULE(ElectronNtuplizer);
		  
