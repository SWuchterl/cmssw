#ifndef L1TPFJetFilter_h
#define L1TPFJetFilter_h

/** \class L1TPFJetFilter
 *
 *
 *  This class is an HLTFilter (-> EDFilter) implementing a very basic
 *  HLT trigger acting on TkMuon candidates
 *
 *
 *
 *  \author Simone gennai
 *
 */

#include "HLTrigger/HLTcore/interface/HLTFilter.h"
// #include "DataFormats/L1TCorrelator/interface/TkMuon.h"
// #include "DataFormats/L1TCorrelator/interface/TkMuonFwd.h"
#include "DataFormats/L1TParticleFlow/interface/PFJet.h"
#include "DataFormats/JetReco/interface/PFJetCollection.h"

//
// class declaration
//

class L1TPFJetFilter : public HLTFilter {
public:
  explicit L1TPFJetFilter(const edm::ParameterSet&);
  ~L1TPFJetFilter() override;
  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
  bool hltFilter(edm::Event&,
                 const edm::EventSetup&,
                 trigger::TriggerFilterObjectWithRefs& filterproduct) const override;

private:
  // edm::InputTag l1TkMuonTag_; //input tag for L1 Tk Muon product
  edm::InputTag l1PFJetTag_; //input tag for L1 Tk Muon product

  // typedef std::vector<l1t::PFJet> PFJetCollection;
  // edm::EDGetTokenT<PFJetCollection> pfJetToken_;  // token identifying product containing L1 TkMuons
  edm::EDGetTokenT<l1t::PFJetCollection> pfJetToken_;  // token identifying product containing L1 TkMuons

  double min_Pt_;  // min pt cut
  int    min_N_;   // min number of candidates above pT cut
};

#endif  //L1TPFJetFilter_h
