/**
 * Run3ScoutingLostTrackProducer
 *
 * Filters reco::Track collection produced from scouting tracks and removes those matched to a PFCanidate.
 * Produces an equivalent to offline LostTrack collection
 * Requires vertices and scoutingTracks and packedPFCandidates to be produced first.
 */

#include <memory>
#include <cmath>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"

#include "DataFormats/PatCandidates/interface/PackedCandidate.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"


class Run3ScoutingLostTrackProducer : public edm::stream::EDProducer<> {
public:
  explicit Run3ScoutingLostTrackProducer(const edm::ParameterSet&);
  ~Run3ScoutingLostTrackProducer() override = default;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void produce(edm::Event&, const edm::EventSetup&) override;
  bool sameTrack(const reco::Track& a, const reco::Track& b);
  const edm::EDGetTokenT<pat::PackedCandidateCollection> particleToken_;
  const edm::EDGetTokenT<reco::TrackCollection> trackToken_;
};

bool Run3ScoutingLostTrackProducer::sameTrack(const reco::Track& a, const reco::Track& b)
{
    return
        a.charge() == b.charge() &&
        std::abs(a.pt()  - b.pt())  < 1e-6 &&
        std::abs(a.eta() - b.eta()) < 1e-6 &&
        std::abs(a.phi() - b.phi()) < 1e-6 &&
        std::abs(a.dxy() - b.dxy()) < 1e-6 &&
        std::abs(a.dz()  - b.dz())  < 1e-6;
}


Run3ScoutingLostTrackProducer::Run3ScoutingLostTrackProducer(
    const edm::ParameterSet& iConfig)
    : particleToken_(consumes<pat::PackedCandidateCollection>(iConfig.getParameter<edm::InputTag>("particles"))),
      trackToken_(consumes<reco::TrackCollection>(iConfig.getParameter<edm::InputTag>("src"))) {
  produces<reco::TrackCollection>();
}

void Run3ScoutingLostTrackProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  auto output = std::make_unique<reco::TrackCollection>();

  const auto& particles = iEvent.get(particleToken_);

  const auto& tracks = iEvent.get(trackToken_);

  std::unordered_set<unsigned int> packedTrackKeys;


  for (const auto& trk : tracks) {
     bool found = false;

     for (const auto& pc : particles) {
         if (!pc.hasTrackDetails()) continue;

         const reco::Track& ptrk = pc.pseudoTrack();

         if (sameTrack(trk, ptrk)) {
            found = true;
        }
     }
     if (!found) output->push_back(trk);
     
  }
  iEvent.put(std::move(output));
}

void Run3ScoutingLostTrackProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("particles", edm::InputTag("packedPFCandidates"))
      ->setComment("pat::PackedCandidateCollection to check if tracks are embedded");
  desc.add<edm::InputTag>("src", edm::InputTag("scoutingTracks"))
      ->setComment("Input reco::Track collection to be filtered");
  descriptions.addWithDefaultLabel(desc);
}

DEFINE_FWK_MODULE(Run3ScoutingLostTrackProducer);
