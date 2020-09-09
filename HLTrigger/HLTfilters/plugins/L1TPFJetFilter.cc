/** \class L1TPFJetFilter
 *
 * See header file for documentation
 *
 *
 *  \author Martin Grunewald
 *
 */

#include "L1TPFJetFilter.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"

#include "DataFormats/Common/interface/Handle.h"

#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/HLTReco/interface/TriggerFilterObjectWithRefs.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

//
// constructors and destructor
//

L1TPFJetFilter::L1TPFJetFilter(const edm::ParameterSet& iConfig)
    : HLTFilter(iConfig),
      l1PFJetTag_(iConfig.getParameter<edm::InputTag>("inputTag")),
      pfJetToken_(consumes<l1t::PFJetCollection>(l1PFJetTag_)){
        min_Pt_= iConfig.getParameter<double>("MinPt");
        min_N_ = iConfig.getParameter<int>("MinN");}

L1TPFJetFilter::~L1TPFJetFilter() = default;

//
// member functions
//

void L1TPFJetFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  makeHLTFilterDescription(desc);
  desc.add<double>("MinPt", -1.0);
  desc.add<int>("MinN",1);
  desc.add<edm::InputTag>("inputTag",edm::InputTag("L1PFJets"));
  descriptions.add("L1TPFJetFilter", desc);
}

// ------------ method called to produce the data  ------------
bool L1TPFJetFilter::hltFilter(edm::Event& iEvent,
                            const edm::EventSetup& iSetup,
                            trigger::TriggerFilterObjectWithRefs& filterproduct) const {
  using namespace std;
  using namespace edm;
  using namespace reco;
  using namespace trigger;

  // All HLT filters must create and fill an HLT filter object,
  // recording any reconstructed physics objects satisfying (or not)
  // this HLT filter, and place it in the Event.

  // The filter object
  if (saveTags()) {
    filterproduct.addCollectionTag(l1PFJetTag_);
  }

  // Specific filter code

  // get hold of products from Event

  Handle<l1t::PFJetCollection> pfJets;

  iEvent.getByToken(pfJetToken_,pfJets);


// trkMuon
  int ntrkmuon(0);
  auto atrkmuons(pfJets->begin());
  auto otrkmuons(pfJets->end());
  l1t::PFJetCollection::const_iterator itkMuon;
  for (itkMuon = atrkmuons; itkMuon != otrkmuons; itkMuon++) {
    if (itkMuon->pt() >= min_Pt_) {
      ntrkmuon++;
      // l1t::TkMuonRef ref = l1t::TkMuonRef(pfJets, distance(atrkmuons, itkMuon));
      l1t::PFJetRef ref = l1t::PFJetRef(pfJets, distance(atrkmuons, itkMuon));
      filterproduct.addObject(-80, ref);
    }
  }


  // error case
  // filterproduct.addObject(0,Ref<vector<int> >());

  // final filter decision:
  const bool accept(ntrkmuon >= min_N_);


  // return with final filter decision
  return accept;
}
