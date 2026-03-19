#include"ParticleNetNtuplizer/ParticleNetNtuplizer/interface/ParticleNetNtuplizer.h"

template <typename T>
MvaNtuplizer<T>::MvaNtuplizer(const edm::ParameterSet& iConfig) :
  //src_(consumes<pat::LeptonTagInfoCollection<T>>(iConfig.getParameter<edm::InputTag>("src"))),
  src_(consumes<LeptonTagInfoCollection>(iConfig.getParameter<edm::InputTag>("src"))),
  srcLeps_(consumes<std::vector<T>>(iConfig.getParameter<edm::InputTag>("srcLeptons"))),
  srcMcTable_(consumes<nanoaod::FlatTable>(iConfig.getParameter<edm::InputTag>("srcMcTable"))),
  cut_(iConfig.getParameter<std::string>("leptonSelection")),
  selector_(cut_)
{
  outtree = fs->make<TTree>( "Events"  , "Events");

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
    //    const pat::LeptonTagInfo<T> taginfo = (*src)[0];
    const btagbtvdeep::DeepBoostedJetFeatures taginfo = (*src)[0];
    //    const pat::LeptonTagInfo<T> taginfo = (*src);
    //    for (auto& var : taginfo.features().get_all()){
    for (auto& var : taginfo.get_all()){
      output_vars[var.first]=std::vector<float>();
      outtree->Branch(var.first.c_str(), &output_vars[var.first]);
    }
    outtree->Branch("genPartFlav", &genPartFlav);
    outtree->Branch("event", &event);
    outtree->Branch("luminosityBlock", &luminosityBlock);
    outtree->Branch("run", &run);
  
  }
  event=iEvent.eventAuxiliary().id().event();
  luminosityBlock = iEvent.eventAuxiliary().luminosityBlock();
  run=iEvent.eventAuxiliary().run();
  // now lets actually fill things
  for (size_t ilep=0; ilep < src->size(); ilep++){
    if (!selector_( leptons->at(ilep))) continue;

    //    const pat::LeptonTagInfo<T> taginfo = (*src)[ilep];
    const btagbtvdeep::DeepBoostedJetFeatures taginfo = (*src)[0];
    //    for (auto& var : taginfo.features().get_all()){
    for (auto& var : taginfo.get_all()){
      output_vars[var.first]=var.second;
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
void MvaNtuplizer<T>::beginJob(){}

template <typename T>
void MvaNtuplizer<T>::endJob(){}

typedef MvaNtuplizer<pat::Muon> MuonNtuplizer;
typedef MvaNtuplizer<pat::Electron> ElectronNtuplizer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MuonNtuplizer);
DEFINE_FWK_MODULE(ElectronNtuplizer);
		  
