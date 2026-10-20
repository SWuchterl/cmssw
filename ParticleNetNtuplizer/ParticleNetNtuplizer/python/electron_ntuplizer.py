import FWCore.ParameterSet.Config as cms

ntuplizer_electron = cms.EDAnalyzer('ElectronNtuplizer',
                                    src=cms.InputTag(
                                        "electronParTTrainVariables"),
                                    srcLeptons=cms.InputTag(
                                        "linkedObjects", "electrons"),
                                    srcMcTable=cms.InputTag("electronMCTable"),
                                    leptonSelection=cms.string(
                                        "pt > 5 && abs(eta)< 2.4"),
                                    )


def customize_ntuplizer(process):
    process.ntuplizer_electron = ntuplizer_electron
    process.nanoSequenceMC.insert(process.nanoSequenceMC.index(
        process.nanoSequenceOnlyFullSim)+1, process.ntuplizer_electron)
    process.TFileService = cms.Service("TFileService",
                                       fileName=cms.string("tree.root"),
                                       closeFileFast=cms.untracked.bool(True)
                                       )

    return process


# ---------------------------------------------------------------------------
# Training ntuple (Run 3): own feature producer, independent of the inputs of the ONNX models in NanoAOD
# ---------------------------------------------------------------------------


_HASSHAPE = "full5x5_sigmaIetaIeta()<30 && (full5x5_sigmaIetaIeta()>0 || full5x5_sigmaIphiIphi()>0)"


def _asinh(x, scale=None):
    """String expression for asinh(x / scale): the string parser has no asinh; this form is exact for both signs."""
    y = "(%s)" % x if scale is None else "((%s)/%s)" % (x, scale)
    return "%s/max(abs(%s),1.e-30)*log(abs(%s)+sqrt(%s*%s+1))" % (y, y, y, y, y)


_cpfVars = cms.PSet(
    CPF_pt=cms.string("pt"),
    CPF_pt_log=cms.string("log(max(pt,1.e-8))"),
    CPF_px_glob=cms.string("px"),
    CPF_py_glob=cms.string("py"),
    CPF_pz_glob=cms.string("pz"),
    CPF_energy_glob=cms.string("energy"),
    CPF_energy_glob_log=cms.string("log(max(energy,1.e-8))"),
    CPF_charge=cms.string("charge"),
    CPF_isElectron=cms.string("?abs(pdgId)==11?1:0"),
    CPF_isMuon=cms.string("?abs(pdgId)==13?1:0"),
    CPF_isChargedHadron=cms.string("?abs(pdgId)==211?1:0"),
    CPF_puppiWeightNoLep=cms.string("puppiWeightNoLep"),
    CPF_fromPV=cms.string("fromPV"),
    CPF_numberOfPixelHits=cms.string("numberOfPixelHits"),
    CPF_hcalFraction=cms.string("hcalFraction"),
    CPF_trackerLayersWithMeasurement=cms.string(
        "?hasTrackDetails?bestTrack().hitPattern().trackerLayersWithMeasurement():0"),
    CPF_mask=cms.string("1"),
    CPF_qoverp=cms.string("?hasTrackDetails && pt()>0?charge()/pt():0"),
    CPF_qdotp=cms.string("?hasTrackDetails?charge()*pt():0"),
    CPF_ass=cms.string("?hasTrackDetails?pvAssociationQuality():0"),
    CPF_chi2=cms.string("?hasTrackDetails?bestTrack().chi2():0"),
    CPF_caloFraction=cms.string("caloFraction"),
    CPF_lostInnerHits=cms.string("?hasTrackDetails?lostInnerHits():0"),
    CPF_qdotp_asinh=cms.string("?hasTrackDetails?" + _asinh("charge()*pt()") + ":0"),
    CPF_chi2_asinh=cms.string("?hasTrackDetails?" + _asinh("bestTrack().chi2()") + ":0"),
)

# neutral candidates: no track variables, isNeutralHadron == !isPhoton, hcalFraction == !isPhoton, fromPV constant
_npfVars = cms.PSet(
    NPF_pt=cms.string("pt"),
    NPF_pt_log=cms.string("log(max(pt,1.e-8))"),
    NPF_px_glob=cms.string("px"),
    NPF_py_glob=cms.string("py"),
    NPF_pz_glob=cms.string("pz"),
    NPF_energy_glob=cms.string("energy"),
    NPF_energy_glob_log=cms.string("log(max(energy,1.e-8))"),
    NPF_isPhoton=cms.string("?abs(pdgId)==22?1:0"),
    NPF_puppiWeightNoLep=cms.string("puppiWeightNoLep"),
    NPF_caloFraction=cms.string("caloFraction"),
    NPF_mask=cms.string("1"),
)

_ltVars = cms.PSet(
    LT_pt=cms.string("pt"),
    LT_pt_log=cms.string("log(max(pt,1.e-8))"),
    LT_px_glob=cms.string("px"),
    LT_py_glob=cms.string("py"),
    LT_pz_glob=cms.string("pz"),
    LT_energy_glob=cms.string("energy"),
    LT_energy_glob_log=cms.string("log(max(energy,1.e-8))"),
    LT_charge=cms.string("charge"),
    LT_isMuon=cms.string("?abs(pdgId)==13?1:0"),
    LT_isChargedHadron=cms.string("?abs(pdgId)==211?1:0"),
    LT_fromPV=cms.string("fromPV"),
    LT_numberOfPixelHits=cms.string("numberOfPixelHits"),
    LT_trackerLayersWithMeasurement=cms.string(
        "?hasTrackDetails?bestTrack().hitPattern().trackerLayersWithMeasurement():0"),
    LT_mask=cms.string("1"),
    LT_qoverp=cms.string("?hasTrackDetails && pt()>0?charge()/pt():0"),
    LT_qdotp=cms.string("?hasTrackDetails?charge()*pt():0"),
    LT_ass=cms.string("?hasTrackDetails?pvAssociationQuality():0"),
    LT_chi2=cms.string("?hasTrackDetails?bestTrack().chi2():0"),
    LT_lostInnerHits=cms.string("?hasTrackDetails?lostInnerHits():0"),
    LT_qdotp_asinh=cms.string("?hasTrackDetails?" + _asinh("charge()*pt()") + ":0"),
    LT_chi2_asinh=cms.string("?hasTrackDetails?" + _asinh("bestTrack().chi2()") + ":0"),
)

_svVars = cms.PSet(
    SV_eta=cms.string("eta"),
    SV_phi=cms.string("phi"),
    SV_pt=cms.string("pt"),
    SV_px_glob=cms.string("px"),
    SV_py_glob=cms.string("py"),
    SV_pz_glob=cms.string("pz"),
    SV_energy_glob=cms.string("energy"),
    SV_energy_glob_log=cms.string("log(max(energy,1.e-8))"),
    SV_pt_log=cms.string("log(max(pt,1.e-8))"),
    SV_ndof=cms.string("vertexNdof"),
    SV_chi2=cms.string("vertexChi2"),
    SV_chi2norm=cms.string("vertexChi2/vertexNdof"),
    # vertexNdof can be negative (adaptive fit weights), so log(chi2/ndof) is not defined for all SVs:
    # log(chi2) (chi2 > 0 always) together with SV_ndof carries the same information
    SV_chi2_log=cms.string("log(max(vertexChi2,1.e-7))"),
    SV_nTracks=cms.string("numberOfDaughters"),
    SV_mass=cms.string("mass"),
    # an SV can have a (slightly) negative mass, clamp before the log
    SV_mass_log=cms.string("log(max(mass,1.e-3))"),
    SV_mask=cms.string("1"),
)

electronParTLLTrainingFeatures = cms.EDProducer(
    "ElectronTagInfoCollectionProducer",
    src=cms.InputTag("linkedObjects", "electrons"),
    pvSrc=cms.InputTag("offlineSlimmedPrimaryVertices"),
    secondary_vertices=cms.InputTag("slimmedSecondaryVertices"),
    pfCandidates=cms.InputTag("packedPFCandidates"),
    ltCandidates=cms.InputTag("lostTracks"),
    barrelEcalHits=cms.InputTag("reducedEgamma", "reducedEBRecHits"),
    endcapEcalHits=cms.InputTag("reducedEgamma", "reducedEERecHits"),
    trainingMode=cms.bool(True),
    # v5 branches made in C++ (CPF_dxyRes_asinh, LT_dxyRes_asinh)
    v5Features=cms.bool(True),
    # full float32 precision as in the CMSSW inference: 12 bits made ParT pair ln m2 noise for close pairs (+27% size)
    reduceMantissaBits=cms.int32(0),
    rhoSrc=cms.InputTag("fixedGridRhoFastjetAll"),
    esHits=cms.InputTag("reducedEgamma", "reducedESRecHits"),
    ebeeClusters=cms.InputTag("reducedEgamma", "reducedEBEEClusters"),
    conversions=cms.InputTag("reducedEgamma", "reducedConversions"),
    singleLegConversions=cms.InputTag("reducedEgamma", "reducedSingleLegConversions"),
    beamSpot=cms.InputTag("offlineBeamSpot"),
    hcalHits=cms.InputTag("reducedEgamma", "reducedHBHEHits"),
    esClusters=cms.InputTag("reducedEgamma", "reducedESClusters"),
    # RHO noise cut [GeV]: removes 63% of the RHO crystals and 7% of the RHO energy
    rhoMinEnergyEB=cms.double(0.1),
    rhoMinEnergyEE=cms.double(0.3),
    # rhoCentral and rhoCentralChargedPileUp removed (correlation 0.98 with Lepton_rho)
    eventVars=cms.PSet(
        rhoCentralNeutral=cms.InputTag("fixedGridRhoFastjetCentralNeutral"),
    ),
    leptonVars=cms.PSet(
        Lepton_mask=cms.string("1"),
        Lepton_pt=cms.string("pt"),
        Lepton_pt_log=cms.string("log(max(pt,1.e-8))"),
        Lepton_eta=cms.string("eta"),
        Lepton_phi=cms.string("phi"),
        Lepton_px=cms.string("px"),
        Lepton_py=cms.string("py"),
        Lepton_pz=cms.string("pz"),
        Lepton_energy=cms.string("energy"),
        Lepton_energy_log=cms.string("log(max(energy,1.e-8))"),
        Lepton_charge=cms.string("charge"),
        Lepton_jetNDauChargedMVASel=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?userFloat('jetNDauChargedMVASel'):0"),
        Lepton_miniPFRelIso_all=cms.string("userFloat('miniIsoAll')/pt"),
        Lepton_miniRelIsoCharged=cms.string("userFloat('miniIsoChg')/pt"),
        Lepton_miniRelIsoNeutral=cms.string("(userFloat('miniIsoAll')-userFloat('miniIsoChg'))/pt"),
        Lepton_pfRelIso03_all=cms.string("userFloat('PFIsoAll')/pt"),
        Lepton_jetPtRelv2_asinh=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?" + _asinh("userFloat('ptRel')", 1.0) + ":0"),
        Lepton_jetPtRatio=cms.string(
            "?userCand('jetForLepJetVar').isNonnull()?min(userFloat('ptRatio'),1.5):1.0/(1.0+(pfIsolationVariables().sumChargedHadronPt + max(pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - pfIsolationVariables().sumPUPt/2,0.0))/pt)"),
        Lepton_dxy=cms.string("dB('PV2D')"),
        Lepton_dxy_sig=cms.string("?edB('PV2D')>0?dB('PV2D')/edB('PV2D'):0"),
        Lepton_dxy_asinh=cms.string("log(abs(dB('PV2D')+sqrt(dB('PV2D')*dB('PV2D')+1.0+1.e-8)))"),
        Lepton_dxy_sig_asinh=cms.string(
            "?edB('PV2D')>0?log(abs((dB('PV2D')/edB('PV2D'))+sqrt((dB('PV2D')/edB('PV2D'))*(dB('PV2D')/edB('PV2D')) + 1))+1.e-8):0"),
        Lepton_sip3d=cms.string("dB('PV3D')"),
        Lepton_sip3d_asinh=cms.string("log(abs(dB('PV3D')+sqrt(dB('PV3D')*dB('PV3D')+1.0+1.e-8)))"),
        Lepton_sip3d_sig=cms.string("?edB('PV3D')>0?dB('PV3D')/edB('PV3D'):0"),
        Lepton_sip3d_sig_asinh=cms.string(
            "?edB('PV3D')>0?log(abs((dB('PV3D')/edB('PV3D'))+sqrt((dB('PV3D')/edB('PV3D'))*(dB('PV3D')/edB('PV3D')) + 1))+1.e-8):0"),
        Lepton_dz=cms.string("dB('PVDZ')"),
        Lepton_dz_asinh=cms.string("log(abs(dB('PVDZ')+sqrt(dB('PVDZ')*dB('PVDZ')+1.0+1.e-8)))"),
        Lepton_dz_sig_asinh=cms.string(
            "?edB('PVDZ')>0?log(abs((dB('PVDZ')/edB('PVDZ'))+sqrt((dB('PVDZ')/edB('PVDZ'))*(dB('PVDZ')/edB('PVDZ'))+1.0+1.e-8))):0"),
        # v5: impact parameters in units of the resolution (the *_asinh above are asinh(x / 1 cm), kept)
        Lepton_dxyRes_asinh=cms.string(_asinh("dB('PV2D')", 0.005)),
        Lepton_dzRes_asinh=cms.string(_asinh("dB('PVDZ')", 0.02)),
        Lepton_sip3dRes_asinh=cms.string(_asinh("dB('PV3D')", 0.02)),
        # electron specific variables
        Lepton_closeTrackNLayers=cms.string("closestCtfTrackNLayers()"),
        Lepton_deltaetacltrkcalo=cms.string("deltaEtaSeedClusterTrackAtCalo"),
        Lepton_dEtaInSeed=cms.string(
            "deltaEtaSuperClusterTrackAtVtx()-superCluster().eta()+superCluster().seed().eta()"),
        Lepton_hcaloverecal=cms.string("full5x5_hcalOverEcal()"),
        Lepton_hcaloverecal_asinh=cms.string(_asinh("full5x5_hcalOverEcal()", 0.05)),
        Lepton_r9full=cms.string("full5x5_r9()"),
        Lepton_e1x5bye5x5=cms.string("1-full5x5_e1x5()/full5x5_e5x5()"),
        # EGM writes sigmaIetaIeta = sigmaIphiIphi = sqrt(999.9) when the shape fails (0.008 %), and 0 for 1 crystal: then all 0 and Lepton_hasShape = 0 (as CL_hasShape)
        Lepton_hasShape=cms.string("?%s?1:0" % _HASSHAPE),
        Lepton_sigmaietaieta=cms.string("?%s?full5x5_sigmaIetaIeta():0" % _HASSHAPE),
        Lepton_sigmaiphiiphi=cms.string("?%s?full5x5_sigmaIphiIphi():0" % _HASSHAPE),
        Lepton_supcl_etaWidth=cms.string("superCluster().etaWidth()"),
        Lepton_supcl_phiWidth=cms.string("superCluster().phiWidth()"),
        Lepton_fbrem=cms.string("fbrem()"),
        Lepton_eoverp=cms.string("eSuperClusterOverP()"),
        Lepton_eoverp_log=cms.string("log(max(eSuperClusterOverP(),1.e-8))"),
        Lepton_passConversionVeto=cms.string("passConversionVeto()"),
        Lepton_dr03HcalDepth1TowerSumEt_Rel=cms.string("?(pt()>0.)?(dr03HcalTowerSumEt(1)*1./pt()):0."),
        # track / cluster matching and brem
        Lepton_pIn=cms.string("trackMomentumAtVtx().R()"),
        Lepton_pOut=cms.string("trackMomentumOut().R()"),
        Lepton_scFbrem=cms.string("superClusterFbrem()"),
        Lepton_nBrems=cms.string("numberOfBrems()"),
        Lepton_class=cms.string("classification()"),
        Lepton_dEtaSCTrkVtx=cms.string("deltaEtaSuperClusterTrackAtVtx()"),
        Lepton_dPhiSCTrkVtx=cms.string("deltaPhiSuperClusterTrackAtVtx()"),
        Lepton_dPhiSeedTrkCalo=cms.string("deltaPhiSeedClusterTrackAtCalo()"),
        Lepton_dEtaEleTrkCalo=cms.string("deltaEtaEleClusterTrackAtCalo()"),
        Lepton_dPhiEleTrkCalo=cms.string("deltaPhiEleClusterTrackAtCalo()"),
        Lepton_eSeedOverPout=cms.string("eSeedClusterOverPout()"),
        Lepton_eEleOverPout=cms.string("eEleClusterOverPout()"),
        Lepton_ooEmooP=cms.string("?ecalEnergy()>0?(1-eSuperClusterOverP())/ecalEnergy():0"),
        # v5 final input forms (section 2.1 of ELECTRON_V5_TREE_SPEC.md)
        Lepton_eEleOverPout_log=cms.string("log(max(eEleClusterOverPout(),1.e-6))"),
        Lepton_eSeedOverPout_log=cms.string("log(max(eSeedClusterOverPout(),1.e-6))"),
        # ooEmooP = 1/E - 1/p (EGM definition, E = ecalEnergy)
        Lepton_ooEmooP_asinh=cms.string(
            "?ecalEnergy()>0?" + _asinh("(1-eSuperClusterOverP())/ecalEnergy()", 0.02) + ":0"),
        Lepton_scRawOverE=cms.string("superCluster().rawEnergy()/energy()"),
        Lepton_scSeedOverRaw=cms.string(
            "?superCluster().rawEnergy()>0?superCluster().seed().energy()/superCluster().rawEnergy():0"),
        Lepton_e2x5OverE5x5=cms.string("?full5x5_e5x5()>0?full5x5_e2x5Max()/full5x5_e5x5():0"),
        Lepton_ecalEnergyErrRel=cms.string("?ecalEnergy()>0?ecalEnergyError()/ecalEnergy():0"),
        Lepton_pCombErrRel=cms.string("p4Error('P4_COMBINATION')/energy()"),
        Lepton_sigmaIetaIphi_asinh=cms.string("?%s?%s:0" % (_HASSHAPE, _asinh(
            "full5x5_showerShape().sigmaIetaIphi*full5x5_sigmaIetaIeta()*full5x5_sigmaIphiIphi()", "1.e-4"))),
        Lepton_psOverRaw=cms.string(
            "?superCluster().rawEnergy()>0?superCluster().preshowerEnergy()/superCluster().rawEnergy():0"),
        Lepton_ps1OverRaw=cms.string(
            "?superCluster().rawEnergy()>0?superCluster().preshowerEnergyPlane1()/superCluster().rawEnergy():0"),
        Lepton_ps2OverRaw=cms.string(
            "?superCluster().rawEnergy()>0?superCluster().preshowerEnergyPlane2()/superCluster().rawEnergy():0"),
        Lepton_dEtaInSeed_asinh=cms.string(_asinh(
            "deltaEtaSuperClusterTrackAtVtx()-superCluster().eta()+superCluster().seed().eta()", 0.005)),
        Lepton_deltaetacltrkcalo_asinh=cms.string(_asinh("deltaEtaSeedClusterTrackAtCalo()", 0.005)),
        Lepton_dEtaEleTrkCalo_asinh=cms.string(_asinh("deltaEtaEleClusterTrackAtCalo()", 0.005)),
        Lepton_dEtaSCTrkVtx_asinh=cms.string(_asinh("deltaEtaSuperClusterTrackAtVtx()", 0.005)),
        Lepton_dPhiSCTrkVtx_asinh=cms.string(_asinh("deltaPhiSuperClusterTrackAtVtx()", 0.02)),
        Lepton_dPhiEleTrkCalo_asinh=cms.string(_asinh("deltaPhiEleClusterTrackAtCalo()", 0.015)),
        Lepton_dPhiSeedTrkCalo_asinh=cms.string(_asinh("deltaPhiSeedClusterTrackAtCalo()", 0.04)),
        Lepton_missingInnerHits=cms.string("gsfTrack.hitPattern.numberOfLostHits('MISSING_INNER_HITS')"),
        # conversions
        # no partner track: GsfElectron stores -1e4; write 0 and Lepton_hasConvPartner = 0 instead
        Lepton_hasConvPartner=cms.string("?convDist()>-9000?1:0"),
        Lepton_convDist=cms.string("?convDist()>-9000?convDist():0"),
        Lepton_convDcot=cms.string("?convDist()>-9000?convDcot():0"),
        Lepton_convRadius=cms.string("?convDist()>-9000?convRadius():0"),
        # PAT computes passConversionVeto with ConversionTools::hasMatchedConversion
        Lepton_hasMatchedConv=cms.string("?passConversionVeto()?0:1"),
        Lepton_ecalDriven=cms.string("ecalDrivenSeed()"),
        # charge measurements: GSF, closest CTF track, SC-pixel direction
        Lepton_scPixCharge=cms.string("scPixCharge()"),
        Lepton_ctfCharge=cms.string("?closestCtfTrackRefValid()?closestCtfTrackRef().charge():0"),
        Lepton_gsfChargeMode=cms.string("gsfTrack().chargeMode()"),
        Lepton_isGsfCtfScPixChargeConsistent=cms.string("isGsfCtfScPixChargeConsistent()"),
        Lepton_isGsfScPixChargeConsistent=cms.string("isGsfScPixChargeConsistent()"),
        Lepton_isGsfCtfChargeConsistent=cms.string("isGsfCtfChargeConsistent()"),
        Lepton_qoverpSig=cms.string(
            "?gsfTrack().qoverpModeError()>0?abs(gsfTrack().qoverpMode())/gsfTrack().qoverpModeError():0"),
        Lepton_ctfGsfOverlap=cms.string("ctfGsfOverlap()"),
        Lepton_trackerDriven=cms.string("trackerDrivenSeed()"),
        # ECAL geometry gaps
        Lepton_isEBEEGap=cms.string("isEBEEGap()"),
        Lepton_isEBEtaGap=cms.string("isEBEtaGap()"),
        Lepton_isEBPhiGap=cms.string("isEBPhiGap()"),
        Lepton_isEEDeeGap=cms.string("isEEDeeGap()"),
        # supercluster
        Lepton_scRawEnergy=cms.string("superCluster().rawEnergy()"),
        Lepton_scEnergy=cms.string("superCluster().energy()"),
        Lepton_scEta=cms.string("superCluster().eta()"),
        Lepton_scPhi=cms.string("superCluster().phi()"),
        Lepton_scPreshowerEnergy=cms.string("superCluster().preshowerEnergy()"),
        Lepton_scPreshowerEnergyPlane1=cms.string("superCluster().preshowerEnergyPlane1()"),
        Lepton_scPreshowerEnergyPlane2=cms.string("superCluster().preshowerEnergyPlane2()"),
        Lepton_scNClusters=cms.string("superCluster().clustersSize()"),
        Lepton_scSeedEnergy=cms.string("superCluster().seed().energy()"),
        # GsfElectron stores cov/(sigmaIetaIeta*sigmaIphiIphi); multiply back to get the covariance
        Lepton_sigmaIetaIphi=cms.string(
            "?%s?full5x5_showerShape().sigmaIetaIphi*full5x5_sigmaIetaIeta()*full5x5_sigmaIphiIphi():0" % _HASSHAPE),
        Lepton_e2x5Max=cms.string("full5x5_e2x5Max()"),
        Lepton_e5x5=cms.string("full5x5_e5x5()"),
        # energy / momentum regression references
        Lepton_ecalEnergy=cms.string("ecalEnergy()"),
        Lepton_ecalEnergyError=cms.string("ecalEnergyError()"),
        Lepton_pCombError=cms.string("p4Error('P4_COMBINATION')"),
        Lepton_trkPMode=cms.string("gsfTrack().pMode()"),
        Lepton_trkPModeError=cms.string("gsfTrack().pMode()*gsfTrack().pMode()*gsfTrack().qoverpModeError()"),
        # other IDs and isolations, for comparison only (not model inputs)
        Lepton_ID_cutBased=cms.string(
            "userInt('cutBasedID_veto')+userInt('cutBasedID_loose')+userInt('cutBasedID_medium')+userInt('cutBasedID_tight')"),
        Lepton_ID_cutBasedHEEP=cms.string("userInt('cutBasedID_HEEP')"),
        Lepton_ID_mvaIso=cms.string("userFloat('mvaIso')"),
        Lepton_ID_mvaIso_WP80=cms.string("userInt('mvaIso_WP80')"),
        Lepton_ID_mvaIso_WP90=cms.string("userInt('mvaIso_WP90')"),
        Lepton_ID_mvaNoIso=cms.string("userFloat('mvaNoIso')"),
        Lepton_ID_mvaNoIso_WP80=cms.string("userInt('mvaNoIso_WP80')"),
        Lepton_ID_mvaNoIso_WP90=cms.string("userInt('mvaNoIso_WP90')"),
        Lepton_ID_mvaHZZIso=cms.string("userFloat('mvaHZZIso')"),
        Lepton_ID_mvaIso_WPHZZ=cms.string("userInt('mvaIso_WPHZZ')"),
        Lepton_ISO_pfRelIso03_chg=cms.string("userFloat('PFIsoChg')/pt"),
        Lepton_ISO_pfRelIso04_all=cms.string("userFloat('PFIsoAll04')/pt"),
    ),
    leptonVarsExt=cms.PSet(
        Lepton_ID_promptMVA=cms.InputTag("electronPROMPTMVA"),
        Lepton_ID_ParTLL_prompt=cms.InputTag("electronParTLLScores:prompt"),
        Lepton_ID_ParTLL_tau=cms.InputTag("electronParTLLScores:tau"),
        Lepton_ID_ParTLL_heavy=cms.InputTag("electronParTLLScores:heavy"),
        Lepton_ID_ParTLL_light=cms.InputTag("electronParTLLScores:light"),
        Lepton_ID_ParTLL_fake=cms.InputTag("electronParTLLScores:fake"),
    ),
    pfVars=cms.PSet(),
    cpfVars=_cpfVars,
    npfVars=_npfVars,
    ltVars=_ltVars,
    svVars=_svVars,
    # RH_energy (= RH_energy_glob), RH_time, RH_timeError, RH_energyError removed: raw forms of RH_* inputs
    rhVars=cms.PSet(
        RH_energy_log=cms.string("log(max(energy,1.e-3))"),
        RH_chi2=cms.string("chi2"),
        RH_mask=cms.string("1"),
    ),
)

# v5: branches not written to the electron tree (raw forms and duplicates, ELECTRON_V5_TREE_SPEC.md 3a).
# Made in C++ or in string sets shared with the muon tree, which keeps them.
_electronDropBranches = cms.vstring(
    "CPF_pt", "CPF_pt_rel", "CPF_energy", "CPF_px", "CPF_py", "CPF_pz", "CPF_charge", "CPF_dxy", "CPF_dz",
    "CPF_dxysig", "CPF_dzsig", "CPF_dxySig_log", "CPF_dzSig_log", "CPF_quality", "CPF_qdotp", "CPF_chi2",
    "NPF_pt", "NPF_pt_rel", "NPF_energy", "NPF_px", "NPF_py", "NPF_pz",
    "LT_pt", "LT_pt_rel", "LT_charge", "LT_dxy", "LT_dz", "LT_dxysig", "LT_dzsig", "LT_dxySig_log",
    "LT_dzSig_log", "LT_qdotp", "LT_chi2",
    "SV_pt", "SV_pt_rel", "SV_mass", "SV_energy", "SV_px", "SV_py", "SV_pz", "SV_chi2", "SV_deltaR", "SV_d3d",
    "SV_d3dsig", "SV_dxy", "SV_dxysig", "SV_dlenSig", "SV_dlenSig_log", "SV_dxy_log", "SV_eta", "SV_phi",
    "SV_enratio",
    "CL_seedEnergy", "CL_seedTime", "CL_energy", "CL_eta", "CL_phi",
    "RH_dR_lep", "RH_veta_rel", "RH_vphi_rel", "RH_region", "RH_eta", "RH_phi", "RH_x", "RH_y", "RH_z",
    "RH_ieta_rel", "RH_iphi_rel", "RH_ix_rel", "RH_iy_rel", "RH_trel", "RH_sigt", "RH_flagBits", "RH_recoFlag",
    "RHO_energy", "RHO_energyError", "RHO_dR_lep", "RHO_eta", "RHO_phi", "RHO_x", "RHO_y", "RHO_z", "RHO_time",
    "RHO_trel", "RHO_timeError", "RHO_flagBits", "RHO_recoFlag",
    "HH_energy", "HH_time", "HH_eta", "HH_phi",
    "ES_energy", "ES_strip", "ES_eta", "ES_phi", "ES_x", "ES_y", "ES_z",
    "ESC_energy", "ESC_eta", "ESC_phi", "ESC_x", "ESC_y", "ESC_z",
    "Lepton_fbrem_log", "Lepton_pAtCalo", "Lepton_RH_esum", "Lepton_RH_wcore", "Lepton_RH_tcore",
    "Lepton_RH_isig", "Lepton_RH_sigcore2",
)

_trainingMaxLengths = cms.PSet(
    CPF=cms.uint32(100),
    NPF=cms.uint32(100),
    LT=cms.uint32(60),
    SV=cms.uint32(60),
    RH=cms.uint32(250),
    RHO=cms.uint32(300),
    ES=cms.uint32(200),
    CL=cms.uint32(60),
    HH=cms.uint32(100),
    ESC=cms.uint32(100),
)

ntuplizer_electron_training = ntuplizer_electron.clone(
    src="electronParTLLTrainingFeatures",
    maxLengths=_trainingMaxLengths,
    dropBranches=_electronDropBranches,
    genMatch=cms.InputTag("electronsMCMatchForTable"),
    dressedMatch=cms.InputTag("electronsMCMatchForTableAlt"),
    dressedLeptons=cms.InputTag("particleLevel", "leptons"),
    prunedGenParticles=cms.InputTag("prunedGenParticles"),
    packedGenParticles=cms.InputTag("packedGenParticles"),
    pileupInfo=cms.InputTag("slimmedAddPileupInfo"),
)


def customize_training_ntuplizer(process):
    process.electronParTLLTrainingFeatures = electronParTLLTrainingFeatures
    process.electronTablesTask.add(process.electronParTLLTrainingFeatures)
    process.ntuplizer_electron = ntuplizer_electron_training
    process.nanoSequenceMC.insert(process.nanoSequenceMC.index(
        process.nanoSequenceOnlyFullSim)+1, process.ntuplizer_electron)
    process.TFileService = cms.Service("TFileService",
                                       fileName=cms.string("tree.root"),
                                       closeFileFast=cms.untracked.bool(True)
                                       )
    return process
