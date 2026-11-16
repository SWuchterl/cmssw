// -*- C++ -*-
//
// Package:    PhysicsTools/NanoAOD
// Class:      LeptonGenCategoryProducer
//
// Truth category of the lepton ParT trainings (Lepton_genCategory, Lepton_genCatChargeFlip of the training ntuples).
// The categorisation is copied from MvaNtuplizer<T>::fill_categories and ancestryCategory in
// ParticleNetNtuplizer/ParticleNetNtuplizer/plugins/ParticleNetNtuplizer.cc (SWuchterl/cmssw, commit 089ae6d24a4,
// branch dev/CMSSW_15_0_17_leptonParT_ntuples_speedup) and must stay identical to it.
//
#include <algorithm>
#include <array>
#include <cmath>
#include <map>
#include <optional>
#include <type_traits>
#include <unordered_set>
#include <vector>

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/global/EDProducer.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/Utilities/interface/Exception.h"

namespace {
  bool isBHadron(int pdg) {
    pdg = std::abs(pdg);
    return pdg > 100 && ((pdg / 100) % 10 == 5 || (pdg / 1000) % 10 == 5);
  }
  bool isCHadron(int pdg) {
    pdg = std::abs(pdg);
    return pdg > 100 && !isBHadron(pdg) && ((pdg / 100) % 10 == 4 || (pdg / 1000) % 10 == 4);
  }

  // Lepton_genCategory codes; weaver merges them into the training classes
  enum GenCategory {
    kPrompt = 1,             // genPartFlav 1
    kPromptRecovered = 2,    // prompt gen lepton at dR < 0.1, one-to-one, 0.2 < reco/ref pT < 3 (brem, FSR)
    kTau = 3,                // genPartFlav 15 or recovered lepton from a prompt tau
    kB = 4,                  // b hadron -> l
    kBtoC = 5,               // b hadron -> c hadron -> l
    kC = 6,                  // c hadron -> l (no b hadron)
    kLightHadron = 7,        // pi0 / eta Dalitz, omega, phi, quarkonium, other light-hadron decays
    kConversion = 8,         // gen lepton from a gen photon, or (electrons) no gen lepton and a gen photon > 0.5 reco pT
    kHadron = 9,             // no gen lepton, charged gen hadron at dR < 0.1
    kNothing = 10,           // no gen lepton, no charged gen hadron
    kAmbDuplicate = 11,      // second reco lepton on the same gen lepton
    kAmbWideMatch = 12,      // gen lepton only at 0.1 < dR < 0.3
    kAmbSoftQED = 13,        // gen lepton whose first other ancestor is a parton or proton (QED shower)
    kAmbPromptFragment = 14  // prompt gen lepton at dR < 0.1 outside the pT window
  };
  const std::unordered_set<int> kOnia = {443, 100443, 553, 100553, 200553, 10441, 20443, 445, 30443};

  // ancestry of a status-1 gen lepton: kPrompt, kTau, kB, kBtoC, kC, kLightHadron, kConversion or kAmbSoftQED
  int ancestryCategory(const reco::GenParticle& g) {
    if (g.isPromptFinalState())
      return kPrompt;
    if (g.isDirectPromptTauDecayProductFinalState())
      return kTau;
    int first = 0;
    for (const reco::Candidate* m = &g; m->numberOfMothers() > 0;) {
      m = m->mother(0);
      if (std::abs(m->pdgId()) != std::abs(g.pdgId())) {
        first = std::abs(m->pdgId());
        break;
      }
    }
    bool hasB = false, hasC = false;
    std::vector<const reco::Candidate*> stack = {&g};
    for (int seen = 0; !stack.empty() && seen < 300; ++seen) {
      const reco::Candidate* p = stack.back();
      stack.pop_back();
      for (size_t k = 0; k < p->numberOfMothers(); ++k) {
        const int a = std::abs(p->mother(k)->pdgId());
        hasB |= isBHadron(a);
        hasC |= isCHadron(a) && !kOnia.count(a);
        stack.push_back(p->mother(k));
      }
    }
    if (hasB)
      return hasC ? kBtoC : kB;
    if (kOnia.count(first))
      return kLightHadron;
    if (hasC)
      return kC;
    if (first > 100)
      return kLightHadron;
    return first == 22 ? kConversion : kAmbSoftQED;
  }
}  // namespace

template <typename T>
class LeptonGenCategoryProducer : public edm::global::EDProducer<> {
public:
  explicit LeptonGenCategoryProducer(const edm::ParameterSet& iConfig)
      : src_token_(consumes<edm::View<T>>(iConfig.getParameter<edm::InputTag>("src"))),
        mc_table_token_(consumes<nanoaod::FlatTable>(iConfig.getParameter<edm::InputTag>("mcTable"))),
        pruned_token_(consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("prunedGenParticles"))),
        packed_token_(
            consumes<pat::PackedGenParticleCollection>(iConfig.getParameter<edm::InputTag>("packedGenParticles"))),
        dressed_token_(consumes<reco::GenJetCollection>(iConfig.getParameter<edm::InputTag>("dressedLeptons"))) {
    if (const auto& cut = iConfig.getParameter<std::string>("leptonSelection"); !cut.empty())
      selection_.emplace(cut);
    produces<edm::ValueMap<int>>("genCategory");
    produces<edm::ValueMap<int>>("genCatChargeFlip");
  }

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
    edm::ParameterSetDescription desc;
    desc.add<edm::InputTag>("src")->setComment("leptons, in the order of the NanoAOD table");
    desc.add<edm::InputTag>("mcTable")->setComment("MC match table of src, for its genPartFlav column");
    desc.add<edm::InputTag>("prunedGenParticles", edm::InputTag("prunedGenParticles"));
    desc.add<edm::InputTag>("packedGenParticles", edm::InputTag("packedGenParticles"));
    desc.add<edm::InputTag>("dressedLeptons", edm::InputTag("particleLevel", "leptons"))
        ->setComment("dressed gen leptons, pT reference of prompt gen electrons");
    desc.add<std::string>("leptonSelection", "")
        ->setComment("leptons taking part in the one-to-one gen assignment; the others get -1; empty = all");
    std::string modname;
    if (typeid(T) == typeid(pat::Muon))
      modname += "muon";
    else if (typeid(T) == typeid(pat::Electron))
      modname += "electron";
    modname += "GenCategory";
    descriptions.add(modname, desc);
  }

private:
  void produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup&) const override;

  const edm::EDGetTokenT<edm::View<T>> src_token_;
  const edm::EDGetTokenT<nanoaod::FlatTable> mc_table_token_;
  const edm::EDGetTokenT<reco::GenParticleCollection> pruned_token_;
  const edm::EDGetTokenT<pat::PackedGenParticleCollection> packed_token_;
  const edm::EDGetTokenT<reco::GenJetCollection> dressed_token_;
  std::optional<StringCutObjectSelector<T>> selection_;
};

// fill_categories of the training ntuplizer; only the inputs (View, optional cut, genPartFlav) differ
template <typename T>
void LeptonGenCategoryProducer<T>::produce(edm::StreamID, edm::Event& iEvent, const edm::EventSetup&) const {
  const auto leptonsHandle = iEvent.getHandle(src_token_);
  const auto& leptons = *leptonsHandle;
  const auto& mcTable = iEvent.get(mc_table_token_);
  const auto& pruned = iEvent.get(pruned_token_);
  const auto& packed = iEvent.get(packed_token_);
  constexpr bool isEle = std::is_same_v<T, pat::Electron>;
  constexpr int fl = isEle ? 11 : 13;

  const size_t n = leptons.size();
  if (mcTable.nRows() != n)
    throw cms::Exception("LeptonGenCategoryProducer") << "mcTable has " << mcTable.nRows() << " rows, src " << n;
  std::vector<int> flav(n, 0);
  for (auto ivar = 0u; ivar < mcTable.nColumns(); ++ivar)
    if (mcTable.columnName(ivar) == "genPartFlav")
      for (size_t i = 0; i < n; ++i)
        flav[i] = mcTable.columnData<uint8_t>(ivar)[i];

  std::vector<size_t> gen;
  for (size_t k = 0; k < pruned.size(); ++k)
    if (pruned[k].status() == 1 && std::abs(pruned[k].pdgId()) == fl)
      gen.push_back(k);
  const reco::GenJetCollection* dressed = isEle ? &iEvent.get(dressed_token_) : nullptr;

  // nearest gen lepton (g) and nearest prompt gen lepton (p) within dR < 0.3
  std::vector<bool> sel(n, false);
  std::vector<int> g(n, -1), p(n, -1);
  std::vector<double> gdr(n, 999), pdr(n, 999), ratio(n, -999);
  for (size_t i = 0; i < n; ++i) {
    if (selection_ && !(*selection_)(leptons[i]))
      continue;
    sel[i] = true;
    for (size_t k : gen) {
      const double dr = reco::deltaR(leptons[i], pruned[k]);
      if (dr < 0.3 && dr < gdr[i]) {
        gdr[i] = dr;
        g[i] = k;
      }
      const auto& f = pruned[k];
      if (dr < 0.3 && dr < pdr[i] && (f.isPromptFinalState() || f.isDirectPromptTauDecayProductFinalState())) {
        pdr[i] = dr;
        p[i] = k;
      }
    }
    if (p[i] < 0)
      continue;
    // pT reference: dressed partner of the prompt gen electron (FSR in the ECAL), bare pT for muons
    double ref = pruned[p[i]].pt(), best = 0.05;
    if (dressed)
      for (const auto& d : *dressed)
        if (d.pdgId() == pruned[p[i]].pdgId() && reco::deltaR(d, pruned[p[i]]) < best) {
          best = reco::deltaR(d, pruned[p[i]]);
          ref = d.pt();
        }
    ratio[i] = leptons[i].pt() / ref;
  }
  // one gen lepton -> the reco lepton nearest in dR among the candidates
  auto nearestPerGen = [&](const std::vector<int>& key, const std::vector<double>& dr, const std::vector<bool>& ok) {
    std::map<int, size_t> best;
    for (size_t i = 0; i < n; ++i)
      if (ok[i] && (!best.count(key[i]) || dr[i] < dr[best[key[i]]]))
        best[key[i]] = i;
    std::vector<bool> first(n, false);
    for (const auto& kv : best)
      first[kv.second] = true;
    return first;
  };
  std::vector<bool> cand(n), isPrompt(n), near(n);
  for (size_t i = 0; i < n; ++i)
    cand[i] = sel[i] && pdr[i] < 0.1 && ratio[i] > 0.2 && ratio[i] < 3;
  const auto recovered = nearestPerGen(p, pdr, cand);
  for (size_t i = 0; i < n; ++i) {
    isPrompt[i] = sel[i] && (flav[i] == 1 || flav[i] == 15 || recovered[i]);
    near[i] = sel[i] && !isPrompt[i] && gdr[i] < 0.1;
  }
  const auto firstOnGen = nearestPerGen(g, gdr, near);

  std::vector<int> category(n, -1), chargeFlip(n, -1);
  for (size_t i = 0; i < n; ++i) {
    if (!sel[i])
      continue;
    const T& lep = leptons[i];
    int cat;
    const reco::GenParticle* ref = nullptr;
    const int anc = g[i] >= 0 ? ancestryCategory(pruned[g[i]]) : -1;
    if (isPrompt[i]) {
      const bool tau = flav[i] == 15 || (flav[i] != 1 && g[i] == p[i] && anc == kTau);
      cat = flav[i] == 1 ? kPrompt : (tau ? kTau : kPromptRecovered);
      ref = p[i] >= 0 ? &pruned[p[i]] : nullptr;
    } else if (near[i]) {
      if (!firstOnGen[i])
        cat = kAmbDuplicate;
      else if (anc == kPrompt || anc == kTau)
        cat = kAmbPromptFragment;
      else
        cat = anc;
      if (cat >= kB && cat <= kLightHadron)
        ref = &pruned[g[i]];
    } else {
      double hadDR = 999, phoPt = -1;
      for (const auto& c : packed) {
        const double dr = reco::deltaR(c, lep);
        if (dr >= 0.1)
          continue;
        const int a = std::abs(c.pdgId());
        if (c.charge() != 0 && a != 11 && a != 13)
          hadDR = std::min(hadDR, dr);
        if (a == 22 && c.pt() > 1)
          phoPt = std::max(phoPt, c.pt());
      }
      if (isEle && phoPt > 0.5 * lep.pt())
        cat = kConversion;
      else if (gdr[i] < 0.3)
        cat = kAmbWideMatch;
      else
        cat = hadDR < 0.1 ? kHadron : kNothing;
    }
    category[i] = cat;
    if (ref)
      chargeFlip[i] = lep.charge() * ref->pdgId() > 0 ? 1 : 0;
  }

  for (const auto& [label, values] :
       {std::pair<const char*, const std::vector<int>*>{"genCategory", &category}, {"genCatChargeFlip", &chargeFlip}}) {
    auto out = std::make_unique<edm::ValueMap<int>>();
    edm::ValueMap<int>::Filler filler(*out);
    filler.insert(leptonsHandle, values->begin(), values->end());
    filler.fill();
    iEvent.put(std::move(out), label);
  }
}

typedef LeptonGenCategoryProducer<pat::Electron> ElectronGenCategoryProducer;
DEFINE_FWK_MODULE(ElectronGenCategoryProducer);
