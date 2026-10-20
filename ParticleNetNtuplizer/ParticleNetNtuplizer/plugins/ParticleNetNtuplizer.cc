#include"ParticleNetNtuplizer/ParticleNetNtuplizer/interface/ParticleNetNtuplizer.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/isFinite.h"
#include <algorithm>
#include <cmath>
#include <unordered_set>
#include <unordered_map>
static constexpr size_t kMaxFeatureLen = 60;
// RecHits can exceed the other categories' typical multiplicity (bremsstrahlung clusters,
// endcap 5x5 windows), so give that category its own, larger cap.
static constexpr size_t kMaxRecHitLen = 250;

namespace {
  std::string categoryOf(const std::string& name) {
    auto pos = name.find('_');
    return (pos == std::string::npos) ? name : name.substr(0, pos);
  }

  // missing values: -1 for indices / pdgIds / flag words, -999 for kinematics, 0 for booleans and sums
  const std::vector<std::pair<std::string, float>> kTruthDefaults = {
      {"Lepton_genIdx", -1},           {"Lepton_genPdgId", -1},           {"Lepton_genStatusFlags", -1},
      {"Lepton_genMother1PdgId", -1},  {"Lepton_genMother2PdgId", -1},   {"Lepton_genMother3PdgId", -1},
      {"Lepton_genHasBAncestor", 0},   {"Lepton_genHasCAncestor", 0},    {"Lepton_genHadronPdgId", -1},
      {"Lepton_genHadronPt", -999},    {"Lepton_genFromPhoton", 0},      {"Lepton_genPhotonMotherPdgId", -1},
      {"Lepton_genConvRadius", -999},  {"Lepton_genFromDalitz", 0},      {"Lepton_genPt", -999},
      {"Lepton_genEta", -999},         {"Lepton_genPhi", -999},          {"Lepton_genEnergy", -999},
      {"Lepton_genDressedPt", -999},   {"Lepton_genDressedEta", -999},   {"Lepton_genDressedPhi", -999},
      {"Lepton_genDressedEnergy", -999}, {"Lepton_genMatchDR", -999},   {"Lepton_genChargeFlip", -1},
      {"Lepton_genNPUTrue", -1},       {"Lepton_genCategory", -1},       {"Lepton_genCatChargeFlip", -1},
      {"Lepton_genPromptDR", -999},    {"Lepton_genPromptPtRatio", -999}, {"Lepton_genNearestDR", -999}};
  // electron only: gen activity around the GSF track and the supercluster
  const std::vector<std::pair<std::string, float>> kTruthDefaultsEle = {
      {"Lepton_genTrkMatchPdgId", -1},    {"Lepton_genTrkMatchPt", -999},       {"Lepton_genTrkMatchDR", -999},
      {"Lepton_genTrkMatchMotherPdgId", -1}, {"Lepton_genEMEnergySC", -999},    {"Lepton_genEMFracSC", -999},
      {"Lepton_genLeadPhotonPt", -999},   {"Lepton_genLeadPhotonMotherPdgId", -1}, {"Lepton_genHadEnergySC", -999},
      {"Lepton_genNInCone", -999},        {"Lepton_genNPi0PhotonsSC", -999},  {"Lepton_genPi0PhotonEFracSC", -999}};

  bool isBHadron(int pdg) {
    pdg = std::abs(pdg);
    return pdg > 100 && ((pdg / 100) % 10 == 5 || (pdg / 1000) % 10 == 5);
  }
  bool isCHadron(int pdg) {
    pdg = std::abs(pdg);
    return pdg > 100 && !isBHadron(pdg) && ((pdg / 100) % 10 == 4 || (pdg / 1000) % 10 == 4);
  }
  bool isNeutrino(int pdg) {
    pdg = std::abs(pdg);
    return pdg == 12 || pdg == 14 || pdg == 16;
  }

  // same bit word as NanoAOD GenPart_statusFlags
  int statusFlagWord(const reco::GenParticle& p) {
    const auto& f = p.statusFlags();
    return f.isPrompt() * 1 + f.isDecayedLeptonHadron() * 2 + f.isTauDecayProduct() * 4 +
           f.isPromptTauDecayProduct() * 8 + f.isDirectTauDecayProduct() * 16 + f.isDirectPromptTauDecayProduct() * 32 +
           f.isDirectHadronDecayProduct() * 64 + f.isHardProcess() * 128 + f.fromHardProcess() * 256 +
           f.isHardProcessTauDecayProduct() * 512 + f.isDirectHardProcessTauDecayProduct() * 1024 +
           f.fromHardProcessBeforeFSR() * 2048 + f.isFirstCopy() * 4096 + f.isLastCopy() * 8192 +
           f.isLastCopyBeforeFSR() * 16384;
  }

  // first ancestor (via mother(0)) whose pdgId differs from pdg
  const reco::Candidate* firstDifferentAncestor(const reco::Candidate* p, int pdg) {
    while (p && p->numberOfMothers() > 0) {
      p = p->mother(0);
      if (p->pdgId() != pdg)
        return p;
    }
    return nullptr;
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
MvaNtuplizer<T>::MvaNtuplizer(const edm::ParameterSet& iConfig) :
  //src_(consumes<pat::LeptonTagInfoCollection<T>>(iConfig.getParameter<edm::InputTag>("src"))),
  src_(consumes<LeptonTagInfoCollection>(iConfig.getParameter<edm::InputTag>("src"))),
  srcLeps_(consumes<std::vector<T>>(iConfig.getParameter<edm::InputTag>("srcLeptons"))),
  srcMcTable_(consumes<nanoaod::FlatTable>(iConfig.getParameter<edm::InputTag>("srcMcTable"))),
  cut_(iConfig.getParameter<std::string>("leptonSelection")),
  selector_(cut_)
{
  usesResource("TFileService");
  if (iConfig.exists("maxLengths")) {
    const auto& pset = iConfig.getParameter<edm::ParameterSet>("maxLengths");
    for (const auto& cat : pset.getParameterNamesForType<unsigned>())
      maxLengths_[cat] = pset.getParameter<unsigned>(cat);
  }
  if (iConfig.exists("dropBranches"))
    for (const auto& name : iConfig.getParameter<std::vector<std::string>>("dropBranches"))
      drop_.insert(name);
  if (iConfig.exists("genMatch")) {
    doTruth_ = true;
    genMatch_token_ = consumes<edm::Association<reco::GenParticleCollection>>(iConfig.getParameter<edm::InputTag>("genMatch"));
    pruned_token_ = consumes<reco::GenParticleCollection>(iConfig.getParameter<edm::InputTag>("prunedGenParticles"));
    packed_token_ = consumes<pat::PackedGenParticleCollection>(iConfig.getParameter<edm::InputTag>("packedGenParticles"));
    pileup_token_ = consumes<std::vector<PileupSummaryInfo>>(iConfig.getParameter<edm::InputTag>("pileupInfo"));
    if (iConfig.exists("dressedMatch")) {
      doDressed_ = true;
      dressedMatch_token_ = consumes<edm::Association<reco::GenJetCollection>>(iConfig.getParameter<edm::InputTag>("dressedMatch"));
    }
    if (iConfig.exists("dressedLeptons")) {
      doDressedLeptons_ = true;
      dressedLeptons_token_ = consumes<reco::GenJetCollection>(iConfig.getParameter<edm::InputTag>("dressedLeptons"));
    }
    for (const auto& kv : kTruthDefaults)
      truth_vars_[kv.first] = kv.second;
    if constexpr (std::is_same_v<T, pat::Electron>) {
      for (const auto& kv : kTruthDefaultsEle)
        truth_vars_[kv.first] = kv.second;
    }
  }
  outtree = fs->make<TTree>( "Events", "Events");
  outtree->SetAutoFlush(-30000000);

}

template <typename T>
MvaNtuplizer<T>::~MvaNtuplizer() {}

template <typename T>
size_t MvaNtuplizer<T>::maxLenForCategory(const std::string& cat) const {
  auto it = maxLengths_.find(cat);
  if (it != maxLengths_.end())
    return it->second;
  return (cat == "RH") ? kMaxRecHitLen : kMaxFeatureLen;
}

template <typename T>
void MvaNtuplizer<T>::fill_truth(const T& lep, const edm::Ref<std::vector<T>>& ref, const edm::Event& iEvent) {
  for (const auto& kv : kTruthDefaults)
    truth_vars_[kv.first] = kv.second;
  if constexpr (std::is_same_v<T, pat::Electron>) {
    for (const auto& kv : kTruthDefaultsEle)
      truth_vars_[kv.first] = kv.second;
  }
  auto set = [this](const char* name, float v) { truth_vars_.at(name) = v; };

  const auto& match = iEvent.get(genMatch_token_);
  const auto& pruned = iEvent.get(pruned_token_);
  const auto& packed = iEvent.get(packed_token_);
  // true number of pile-up interactions (in-time bunch crossing): for pile-up reweighting, not a model input
  for (const auto& pu : iEvent.get(pileup_token_))
    if (pu.getBunchCrossing() == 0)
      set("Lepton_genNPUTrue", pu.getTrueNumInteractions());

  // 9a / 10a: the gen particle matched by the NanoAOD matcher (same as <Lepton>_genPartIdx)
  const reco::GenParticleRef gen = match[ref];
  if (gen.isNonnull()) {
    set("Lepton_genIdx", gen.key());
    set("Lepton_genPdgId", gen->pdgId());
    set("Lepton_genStatusFlags", statusFlagWord(*gen));
    set("Lepton_genPt", gen->pt());
    set("Lepton_genEta", gen->eta());
    set("Lepton_genPhi", gen->phi());
    set("Lepton_genEnergy", gen->energy());
    set("Lepton_genMatchDR", reco::deltaR(lep, *gen));
    // charge flip: only defined if the matched particle is a lepton of the same flavour (pdgId 11 = e-, charge -1)
    if (std::abs(gen->pdgId()) == std::abs(lep.pdgId()))
      set("Lepton_genChargeFlip", lep.charge() * gen->pdgId() > 0 ? 1 : 0);

    // ancestry is taken from prunedGenParticles; the matched particle is a copy of one of them
    const reco::Candidate* self = nullptr;
    for (const auto& p : pruned) {
      if (p.pdgId() == gen->pdgId() && p.status() == gen->status() && std::abs(p.pt() - gen->pt()) < 1e-4 * gen->pt() &&
          reco::deltaR(p, *gen) < 1e-4) {
        self = &p;
        break;
      }
    }
    if (self) {
      // first three ancestors with a pdgId different from the lepton, consecutive copies counted once
      std::vector<int> anc;
      const reco::Candidate* hadron = nullptr;
      bool hasB = false, hasC = false;
      for (const reco::Candidate* p = self; p->numberOfMothers() > 0;) {
        p = p->mother(0);
        const int pdg = p->pdgId();
        if (pdg != self->pdgId() && anc.size() < 3 && (anc.empty() || anc.back() != pdg))
          anc.push_back(pdg);
        hasB |= isBHadron(pdg);
        hasC |= isCHadron(pdg);
        if (!hadron && (isBHadron(pdg) || isCHadron(pdg)))
          hadron = p;
      }
      const char* motherNames[3] = {"Lepton_genMother1PdgId", "Lepton_genMother2PdgId", "Lepton_genMother3PdgId"};
      for (size_t i = 0; i < anc.size(); ++i)
        set(motherNames[i], anc[i]);
      set("Lepton_genHasBAncestor", hasB);
      set("Lepton_genHasCAncestor", hasC);
      if (hadron) {
        set("Lepton_genHadronPdgId", hadron->pdgId());
        set("Lepton_genHadronPt", hadron->pt());
      }
      const reco::Candidate* mother = firstDifferentAncestor(self, self->pdgId());
      // material conversions are not in the gen record (Geant4): the matcher then picks the photon itself
      if (self->pdgId() == 22) {
        set("Lepton_genFromPhoton", 1);
        if (mother)
          set("Lepton_genPhotonMotherPdgId", mother->pdgId());
      } else if (mother && mother->pdgId() == 22) {
        set("Lepton_genFromPhoton", 1);
        if (const auto* gm = firstDifferentAncestor(mother, 22))
          set("Lepton_genPhotonMotherPdgId", gm->pdgId());
        set("Lepton_genConvRadius", gen->vertex().rho());
      }
      // Dalitz: pi0 / eta -> e+ e- gamma
      if (mother && (mother->pdgId() == 111 || mother->pdgId() == 221) && mother->numberOfDaughters() == 3) {
        int nEle = 0, nPho = 0;
        for (size_t i = 0; i < mother->numberOfDaughters(); ++i) {
          nEle += std::abs(mother->daughter(i)->pdgId()) == 11;
          nPho += mother->daughter(i)->pdgId() == 22;
        }
        set("Lepton_genFromDalitz", nEle == 2 && nPho == 1);
      }
    }
  }

  if (doDressed_) {
    const auto& dressedMatch = iEvent.get(dressedMatch_token_);
    const reco::GenJetRef dressed = dressedMatch[ref];
    if (dressed.isNonnull()) {
      set("Lepton_genDressedPt", dressed->pt());
      set("Lepton_genDressedEta", dressed->eta());
      set("Lepton_genDressedPhi", dressed->phi());
      set("Lepton_genDressedEnergy", dressed->energy());
    }
  }

  // 9b (electrons): status-1 gen activity around the GSF track and the supercluster
  if constexpr (std::is_same_v<T, pat::Electron>) {
    const auto trk = lep.trackMomentumAtVtx();
    const double trkEta = trk.eta(), trkPhi = trk.phi(), trkPt = std::sqrt(trk.perp2());
    const pat::PackedGenParticle* best = nullptr;
    double bestDPt = 1e9, bestDR = -999;
    int nInCone = 0;
    for (const auto& p : packed) {
      if (isNeutrino(p.pdgId()))
        continue;
      if (p.pt() > 1 && reco::deltaR(p, lep) < 0.1)
        ++nInCone;
      if (p.charge() == 0 || trkPt <= 0)
        continue;
      const double dR = reco::deltaR(p.eta(), p.phi(), trkEta, trkPhi);
      const double dPt = std::abs(p.pt() - trkPt) / trkPt;
      if (dR < 0.05 && dPt < bestDPt) {
        best = &p;
        bestDPt = dPt;
        bestDR = dR;
      }
    }
    set("Lepton_genNInCone", nInCone);
    if (best) {
      set("Lepton_genTrkMatchPdgId", best->pdgId());
      set("Lepton_genTrkMatchPt", best->pt());
      set("Lepton_genTrkMatchDR", bestDR);
      if (best->numberOfMothers() > 0)
        set("Lepton_genTrkMatchMotherPdgId", best->mother(0)->pdgId());
    }

    const auto& sc = lep.superCluster();
    if (sc.isNonnull()) {
      double emE = 0, hadE = 0, pi0E = 0;
      int nPi0Pho = 0;
      const pat::PackedGenParticle* leadPho = nullptr;
      for (const auto& p : packed) {
        if (reco::deltaR(p.eta(), p.phi(), sc->eta(), sc->phi()) >= 0.1)
          continue;
        const int apdg = std::abs(p.pdgId());
        if (apdg == 22 || apdg == 11) {
          emE += p.energy();
          if (apdg == 22 && (!leadPho || p.pt() > leadPho->pt()))
            leadPho = &p;
          // photons from pi0 / eta decays
          if (apdg == 22 && p.numberOfMothers() > 0 &&
              (p.mother(0)->pdgId() == 111 || p.mother(0)->pdgId() == 221)) {
            ++nPi0Pho;
            pi0E += p.energy();
          }
        } else if (p.charge() == 0 && !isNeutrino(apdg)) {
          hadE += p.energy();
        }
      }
      set("Lepton_genEMEnergySC", emE);
      set("Lepton_genEMFracSC", sc->energy() > 0 ? emE / sc->energy() : -999);
      set("Lepton_genHadEnergySC", hadE);
      set("Lepton_genNPi0PhotonsSC", nPi0Pho);
      set("Lepton_genPi0PhotonEFracSC", sc->energy() > 0 ? pi0E / sc->energy() : -999);
      if (leadPho) {
        set("Lepton_genLeadPhotonPt", leadPho->pt());
        if (leadPho->numberOfMothers() > 0)
          set("Lepton_genLeadPhotonMotherPdgId", leadPho->mother(0)->pdgId());
      }
    }
  }
}

// Lepton_genCategory and its companions; needs all selected leptons of the event for the one-to-one assignment
template <typename T>
void MvaNtuplizer<T>::fill_categories(const std::vector<T>& leptons, const std::vector<int>& flav, const edm::Event& iEvent) {
  const auto& pruned = iEvent.get(pruned_token_);
  const auto& packed = iEvent.get(packed_token_);
  constexpr bool isEle = std::is_same_v<T, pat::Electron>;
  constexpr int fl = isEle ? 11 : 13;
  std::vector<size_t> gen;
  for (size_t k = 0; k < pruned.size(); ++k)
    if (pruned[k].status() == 1 && std::abs(pruned[k].pdgId()) == fl)
      gen.push_back(k);
  const reco::GenJetCollection* dressed = (isEle && doDressedLeptons_) ? &iEvent.get(dressedLeptons_token_) : nullptr;

  // nearest gen lepton (g) and nearest prompt gen lepton (p) within dR < 0.3
  const size_t n = leptons.size();
  std::vector<bool> sel(n, false);
  std::vector<int> g(n, -1), p(n, -1);
  std::vector<double> gdr(n, 999), pdr(n, 999), ratio(n, -999);
  for (size_t i = 0; i < n; ++i) {
    if (!selector_(leptons[i]))
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

  categories_.assign(n, {{-1, -1, -999, -999, -999}});
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
    categories_[i][0] = cat;
    if (ref)
      categories_[i][1] = lep.charge() * ref->pdgId() > 0 ? 1 : 0;
    if (p[i] >= 0)
      categories_[i][2] = pdr[i];
    categories_[i][3] = ratio[i];
    if (g[i] >= 0)
      categories_[i][4] = gdr[i];
  }
}

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
      // not written to the tree (the producer still computes them)
      if (drop_.count(name))
        continue;
      // treat Lepton_* features as scalars (fixed length 1)
      if (name.rfind("Lepton", 0) == 0) {
        output_scalar_vars[name] = 0.f;
        continue;
      }
      // extract category prefix before first underscore, e.g. PF_var -> PF
      std::string cat = categoryOf(name);
      output_vars[name] = std::vector<float>(maxLenForCategory(cat));
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
    for (auto &kv : truth_vars_) {
      outtree->Branch(kv.first.c_str(), &kv.second, (kv.first + "/F").c_str());
    }
    // now create variable branches referencing the category length branch (variable-length)
    for (const auto& kv : output_vars) {
      const std::string& name = kv.first;
      std::string cat = categoryOf(name);
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
  if (doTruth_) {
    std::vector<int> flav(leptons->size(), 0);
    for (auto ivar = 0u; ivar < mcTable->nColumns(); ++ivar)
      if (mcTable->columnName(ivar) == "genPartFlav")
        for (size_t i = 0; i < flav.size(); ++i)
          flav[i] = mcTable->columnData<uint8_t>(ivar)[i];
    fill_categories(*leptons, flav, iEvent);
  }
  // now lets actually fill things
  for (size_t ilep=0; ilep < src->size(); ilep++){
    if (!selector_( leptons->at(ilep))) continue;

    const auto& taginfo = (*src)[ilep];
    // reset per-category lengths and track per-category length for this lepton
    for (auto &p : output_cat_sizes) p.second = 0u;
    std::unordered_map<std::string, size_t> cat_len;
    for (const auto& var : taginfo.get_all()){
      // handle scalar Lepton_* features
      auto sit = output_scalar_vars.find(var.first);
      if (sit != output_scalar_vars.end()){
        sit->second = (var.second.size() > 0) ? finiteOrZero(var.first, var.second[0]) : 0.f;
        continue;
      }
      auto it = output_vars.find(var.first);
      if (it == output_vars.end()) continue;
      // all variables of one category must have the same length, otherwise the shorter ones are padded with stale values
      const std::string cat = categoryOf(var.first);
      auto cit = cat_len.find(cat);
      if (cit == cat_len.end())
        cat_len[cat] = var.second.size();
      else if (cit->second != var.second.size())
        throw cms::Exception("InconsistentLength") << "variable " << var.first << " has length " << var.second.size()
                                                   << ", other " << cat << " variables have " << cit->second;
      const size_t ncopy = std::min(var.second.size(), maxLenForCategory(cat));
      if (ncopy > 0)
        std::transform(var.second.begin(), var.second.begin() + ncopy, it->second.begin(),
                       [&](float value) { return finiteOrZero(var.first, value); });
    }
    // write per-category lengths into the output map (branches point to these)
    for (const auto& kv : cat_len) {
      output_cat_sizes[kv.first] = std::min(kv.second, maxLenForCategory(kv.first));
    }
    // a link to a row cut by the cap of the target collection points to nothing: -1
    for (const auto& [link, target] : {std::pair<const char*, const char*>{"ES_clIdx", "ESC"},
                                       {"RH_clIdx", "CL"},
                                       {"RHO_clIdx", "CL"},
                                       {"CPF_svIdx", "SV"}}) {
      auto lit = output_vars.find(link);
      if (lit == output_vars.end() || !cat_len.count(target))
        continue;
      const float nTarget = output_cat_sizes[target];
      for (size_t i = 0; i < output_cat_sizes[categoryOf(link)]; ++i)
        if (lit->second[i] >= nTarget)
          lit->second[i] = -1.f;
    }
    for (auto ivar=0u; ivar<mcTable->nColumns(); ++ivar){
      if (mcTable->columnName(ivar).compare("genPartFlav") == 0){
	      genPartFlav = mcTable->columnData<uint8_t>(ivar)[ilep];
      }
    }
    if (doTruth_) {
      fill_truth(leptons->at(ilep), edm::Ref<std::vector<T>>(leptons, ilep), iEvent);
      const auto& c = categories_[ilep];
      truth_vars_.at("Lepton_genCategory") = c[0];
      truth_vars_.at("Lepton_genCatChargeFlip") = c[1];
      truth_vars_.at("Lepton_genPromptDR") = c[2];
      truth_vars_.at("Lepton_genPromptPtRatio") = c[3];
      truth_vars_.at("Lepton_genNearestDR") = c[4];
    }
    outtree->Fill();
  }

}



template <typename T>
void MvaNtuplizer<T>::beginJob(){
  edm::Service<TFileService> fs;
  if (!fs) return;
  // ZSTD-5: 16% smaller than LZ4-4 on the training ntuples, similar read speed
  fs->file().SetCompressionAlgorithm(ROOT::kZSTD);
  fs->file().SetCompressionLevel(5);
}

template <typename T>
float MvaNtuplizer<T>::finiteOrZero(const std::string& name, float value) {
  if (edm::isFinite(value))
    return value;
  ++nonFinite_[name];
  return 0.f;
}

template <typename T>
void MvaNtuplizer<T>::endJob(){
  for (const auto& [name, n] : nonFinite_)
    edm::LogWarning("ParticleNetNtuplizer") << n << " non-finite values of " << name << " written as 0";
}

typedef MvaNtuplizer<pat::Muon> MuonNtuplizer;
typedef MvaNtuplizer<pat::Electron> ElectronNtuplizer;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MuonNtuplizer);
DEFINE_FWK_MODULE(ElectronNtuplizer);

