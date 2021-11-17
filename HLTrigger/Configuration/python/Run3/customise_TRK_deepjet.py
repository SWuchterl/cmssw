import FWCore.ParameterSet.Config as cms

def customiseRun3BTagRegionalTracks_DeepJet(process):

    ############################################################################
    #### HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepJet_4p5_v3
    ############################################################################


    process.hltPFCentralJetLooseIDQuad30 = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(4),
        MinPt = cms.double(30.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(86)
    )

    process.hlt1PFCentralJetLooseID75 = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(1),
        MinPt = cms.double(75.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(0)
    )

    process.hlt2PFCentralJetLooseID60 = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(2),
        MinPt = cms.double(60.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(0)
    )

    process.hlt3PFCentralJetLooseID45 = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(3),
        MinPt = cms.double(45.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(0)
    )

    process.hlt4PFCentralJetLooseID40 = cms.EDFilter("HLT1PFJet",
        MaxEta = cms.double(2.5),
        MaxMass = cms.double(-1.0),
        MinE = cms.double(-1.0),
        MinEta = cms.double(-1.0),
        MinMass = cms.double(-1.0),
        MinN = cms.int32(4),
        MinPt = cms.double(40.0),
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
        saveTags = cms.bool(True),
        triggerType = cms.int32(0)
    )

    process.hltPFCentralJetLooseIDQuad30forHt = cms.EDProducer("HLTPFJetCollectionProducer",
        HLTObject = cms.InputTag("hltPFCentralJetLooseIDQuad30"),
        TriggerTypes = cms.vint32(86)
    )

    process.hltHtMhtPFCentralJetsLooseIDQuadC30 = cms.EDProducer("HLTHtMhtProducer",
        excludePFMuons = cms.bool(False),
        jetsLabel = cms.InputTag("hltPFCentralJetLooseIDQuad30forHt"),
        maxEtaJetHt = cms.double(2.5),
        maxEtaJetMht = cms.double(999.0),
        minNJetHt = cms.int32(4),
        minNJetMht = cms.int32(0),
        minPtJetHt = cms.double(30.0),
        minPtJetMht = cms.double(0.0),
        pfCandidatesLabel = cms.InputTag("hltParticleFlow"),
        usePt = cms.bool(True)
    )


    process.hltPFCentralJetsLooseIDQuad30HT330 = cms.EDFilter("HLTHtMhtFilter",
        htLabels = cms.VInputTag("hltHtMhtPFCentralJetsLooseIDQuadC30"),
        meffSlope = cms.vdouble(1.0),
        mhtLabels = cms.VInputTag("hltHtMhtPFCentralJetsLooseIDQuadC30"),
        minHt = cms.vdouble(330.0),
        minMeff = cms.vdouble(0.0),
        minMht = cms.vdouble(0.0),
        saveTags = cms.bool(True)
    )



    process.hltBTagPFDeepCSV4p5Triple = cms.EDFilter("HLTPFJetTag",
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
        Jets = cms.InputTag("hltPFJetForBtag"),
        MaxTag = cms.double(999999.0),
        MinJets = cms.int32(3),
        MinTag = cms.double(0.24),
        TriggerType = cms.int32(86),
        saveTags = cms.bool(True)
    )
    # cloning for DeepJet
    process.hltPrePFHT330PT30QuadPFJet75604540TriplePFBTagDeepJet4p5 = process.hltPrePFHT330PT30QuadPFJet75604540TriplePFBTagDeepCSV4p5.clone()
 
    process.hltBTagPFDeepJet4p5Triple = process.hltBTagPFDeepCSV4p5Triple.clone(
        JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
        Jets = cms.InputTag("hltPFJetForBtag"),
        MaxTag = cms.double(999999.0),
        MinJets = cms.int32(3),
        MinTag = cms.double(0.24),
        TriggerType = cms.int32(86),
        saveTags = cms.bool(True)
    )


    process.HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepJet_4p5_v3 = cms.Path(
        process.HLTBeginSequence+

        process.hltL1sQuadJetC50to60IorHTT280to500IorHTT250to340QuadJet+
        process.hltPrePFHT330PT30QuadPFJet75604540TriplePFBTagDeepJet4p5+

        process.HLTAK4CaloJetsSequence+

        process.hltQuadCentralJet30+
        process.hltCaloJetsQuad30ForHt+
        process.hltHtMhtCaloJetsQuadC30+
        process.hltCaloQuadJet30HT320+

        #  process.HLTBtagDeepCSVSequenceL3+
        #  process.hltBTagCaloDeepCSVp17Double+

        process.HLTAK4PFJetsSequence+

        process.hltPFCentralJetLooseIDQuad30+
        process.hlt1PFCentralJetLooseID75+
        process.hlt2PFCentralJetLooseID60+
        process.hlt3PFCentralJetLooseID45+
        process.hlt4PFCentralJetLooseID40+
        process.hltPFCentralJetLooseIDQuad30forHt+
        process.hltHtMhtPFCentralJetsLooseIDQuadC30+
        process.hltPFCentralJetsLooseIDQuad30HT330+

        process.HLTBtagDeepJetSequencePF+

        process.hltBTagPFDeepJet4p5Triple+

        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepJet_4p5_v8
    ############################################################################



    process.hltPFJetFilterTwo100er3p0 = process.hltPFJetFilterTwo100er3p0.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )
    process.hltPFJetFilterThree60er3p0 = process.hltPFJetFilterThree60er3p0.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )
    process.hltPFJetFilterFive30er3p0 = process.hltPFJetFilterFive30er3p0.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )

    process.hltPFJetsFive30ForHt = process.hltPFJetsFive30ForHt.clone(
        HLTObject = cms.InputTag("hltPFJetFilterFive30er3p0"),
    )
    process.hltHtMhtPFJetsFive30er3p0 = process.hltHtMhtPFJetsFive30er3p0.clone(
        jetsLabel = cms.InputTag("hltPFJetsFive30ForHt"),
        pfCandidatesLabel = cms.InputTag("hltParticleFlow"),
    )
    process.hltPFFiveJet30HT400 = process.hltPFFiveJet30HT400.clone(
        htLabels = cms.VInputTag("hltHtMhtPFJetsFive30er3p0"),
        mhtLabels = cms.VInputTag("hltHtMhtPFJetsFive30er3p0"),
    )

#    process.hltBTagPFDeepCSV4p5Double = process.hltBTagPFDeepCSV4p5Double.clone(
#        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
#        Jets = cms.InputTag("hltPFJetForBtag"),
#    )

    process.hltBTagPFDeepJet4p5Double = process.hltBTagPFDeepCSV4p5Double.clone(
        JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
        Jets = cms.InputTag("hltPFJetForBtag"),
    )

    process.hltPrePFHT400FivePFJet100100603030DoublePFBTagDeepJet4p5 = process.hltPrePFHT400FivePFJet100100603030DoublePFBTagDeepCSV4p5.clone()

    process.HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepJet_4p5_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJetTripleJet+
        process.hltPrePFHT400FivePFJet100100603030DoublePFBTagDeepJet4p5+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterFiveC25+
        process.hltCaloJetsFive25ForHt+
        process.hltHtMhtCaloJetsFiveC25+
        process.hltCaloFiveJet25HT300+

        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV10p01Single+
        process.HLTAK4PFJetsSequence+

        process.hltPFJetFilterTwo100er3p0+
        process.hltPFJetFilterThree60er3p0+
        process.hltPFJetFilterFive30er3p0+
        process.hltPFJetsFive30ForHt+
        process.hltHtMhtPFJetsFive30er3p0+
        process.hltPFFiveJet30HT400+
        process.HLTBtagDeepJetSequencePF+
        process.hltBTagPFDeepJet4p5Double+

        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepJet_4p5_v
    ############################################################################

    process.hltPFJetFilterTwo120er3p0 = process.hltPFJetFilterTwo120er3p0.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )

    process.hltPrePFHT400FivePFJet120120603030DoublePFBTagDeepJet4p5 = process.hltPrePFHT400FivePFJet120120603030DoublePFBTagDeepCSV4p5.clone()

    process.HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepJet_4p5_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJetTripleJet+
        process.hltPrePFHT400FivePFJet120120603030DoublePFBTagDeepJet4p5+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterFiveC25+
        process.hltCaloJetsFive25ForHt+
        process.hltHtMhtCaloJetsFiveC25+
        process.hltCaloFiveJet25HT300+

        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV10p01Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFJetFilterTwo120er3p0+
        process.hltPFJetFilterThree60er3p0+
        process.hltPFJetFilterFive30er3p0+
        process.hltPFJetsFive30ForHt+
        process.hltHtMhtPFJetsFive30er3p0+
        process.hltPFFiveJet30HT400+
        process.HLTBtagDeepJetSequencePF+
        process.hltBTagPFDeepJet4p5Double+

        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_v
    ############################################################################

    process.hltPFJetFilterSix30er2p5 = process.hltPFJetFilterSix30er2p5.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )

    process.hltPFJetFilterSix32er2p5 = process.hltPFJetFilterSix32er2p5.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )

    process.hltPFJetsSix30ForHt = cms.EDProducer("HLTPFJetCollectionProducer",
        HLTObject = cms.InputTag("hltPFJetFilterSix30er2p5"),
        TriggerTypes = cms.vint32(86)
    )

    process.hltHtMhtPFJetsSix30er2p5 = process.hltHtMhtPFJetsSix30er2p5.clone(
        jetsLabel = cms.InputTag("hltPFJetsSix30ForHt"),
        pfCandidatesLabel = cms.InputTag("hltParticleFlow"),
    )

    process.hltPFSixJet30HT400 = process.hltPFSixJet30HT400.clone(
        htLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5"),
        mhtLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5"),
    )

#    process.hltBTagPFDeepCSV2p94Double = process.hltBTagPFDeepCSV2p94Double.clone(
#        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
#        Jets = cms.InputTag("hltPFJetForBtag"),
#    )

    process.hltBTagPFDeepJet2p94Double = process.hltBTagPFDeepCSV2p94Double.clone(
        JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
        Jets = cms.InputTag("hltPFJetForBtag"),
    )

    process.hltPrePFHT400SixPFJet32DoublePFBTagDeepJet2p94 = process.hltPrePFHT400SixPFJet32DoublePFBTagDeepCSV2p94.clone()

    process.HLT_PFHT400_SixPFJet32_DoublePFBTagDeepJet_2p94_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJet+
        process.hltPrePFHT400SixPFJet32DoublePFBTagDeepJet2p94+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterSixC25+
        process.hltCaloJetsSix25ForHt+
        process.hltHtMhtCaloJetsSixC25+
        process.hltCaloSixJet25HT300+

        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV10p01Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFJetFilterSix30er2p5+
        process.hltPFJetFilterSix32er2p5+
        process.hltPFJetsSix30ForHt+
        process.hltHtMhtPFJetsSix30er2p5+
        process.hltPFSixJet30HT400+
        process.HLTBtagDeepJetSequencePF+
        process.hltBTagPFDeepJet2p94Double+

        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59_v
    ############################################################################

    process.hltPFJetFilterSix36er2p5 = process.hltPFJetFilterSix36er2p5.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )

    process.hltPFSixJet30HT450 =process.hltPFSixJet30HT450.clone(
        htLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5"),
        mhtLabels = cms.VInputTag("hltHtMhtPFJetsSix30er2p5"),
    )

#    process.hltBTagPFDeepCSV1p59Single = process.hltBTagPFDeepCSV1p59Single.clone(
#        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
#        Jets = cms.InputTag("hltPFJetForBtag"),
#    )

    process.hltBTagPFDeepJet1p59Single = process.hltBTagPFDeepCSV1p59Single.clone(
        JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
        Jets = cms.InputTag("hltPFJetForBtag"),
    )

    process.hltPrePFHT450SixPFJet36PFBTagDeepJet1p59 = process.hltPrePFHT450SixPFJet36PFBTagDeepCSV1p59.clone()

    process.HLT_PFHT450_SixPFJet36_PFBTagDeepJet_1p59_v7 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sHTT280to500erIorHTT250to340erQuadJet+
        process.hltPrePFHT450SixPFJet36PFBTagDeepJet1p59+
        process.HLTAK4CaloJetsSequence+
        process.hltCaloJetFilterSixC30+
        process.hltCaloJetsSix30ForHt+
        process.hltHtMhtCaloJetsSixC30+
        process.hltCaloSixJet30HT350+

        process.HLTAK4PFJetsSequence+
        process.hltPFJetFilterSix30er2p5+
        process.hltPFJetFilterSix36er2p5+
        process.hltPFJetsSix30ForHt+
        process.hltHtMhtPFJetsSix30er2p5+
        process.hltPFSixJet30HT450+
        process.HLTBtagDeepJetSequencePF+
        process.hltBTagPFDeepJet1p59Single+

        process.HLTEndSequence
    )
    
    ############################################################################
    #### HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v
    ############################################################################

    process.hltPFQuadJetLooseID15 = process.hltPFQuadJetLooseID15.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPFTripleJetLooseID75 = process.hltPFTripleJetLooseID75.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPFDoubleJetLooseID88 = process.hltPFDoubleJetLooseID88.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPFSingleJetLooseID103 = process.hltPFSingleJetLooseID103.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltSelector6PFJets = process.hltSelector6PFJets.clone(
        src = cms.InputTag("hltAK4PFJetsLooseIDCorrected")
    )

#    process.hltBTagPFDeepCSV7p68Double6Jets = process.hltBTagPFDeepCSV7p68Double6Jets.clone(
#        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
#        Jets = cms.InputTag("hltSelector6PFJets"),
#    )

    process.hltBTagPFDeepCSV1p28Single6Jets = process.hltBTagPFDeepCSV1p28Single6Jets.clone(
        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
        Jets = cms.InputTag("hltSelector6PFJets"),
    )

#    process.hltVBFPFJetCSVSortedMqq200Detaqq1p5 = process.hltVBFPFJetCSVSortedMqq200Detaqq1p5.clone(
#        inputJetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
#        inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
#    )
    
    process.hltPreQuadPFJet103887515DoublePFBTagDeepJet1p37p7VBF1 = process.hltPreQuadPFJet103887515DoublePFBTagDeepCSV1p37p7VBF1.clone()

    process.hltBTagPFDeepJet7p68Double6Jets = process.hltBTagPFDeepCSV7p68Double6Jets.clone(
        JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
        Jets = cms.InputTag("hltSelector6PFJets"),
    )

    process.hltBTagPFDeepJet1p28Single6Jets = process.hltBTagPFDeepCSV1p28Single6Jets.clone(
        JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
        Jets = cms.InputTag("hltSelector6PFJets"),
    )
    process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5 = process.hltVBFPFJetCSVSortedMqq200Detaqq1p5.clone(
        inputJetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
        inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJetVBFIorHTTIorSingleJet+
        process.hltPreQuadPFJet103887515DoublePFBTagDeepJet1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID75+
        process.hltPFDoubleJetLooseID88+
        process.hltPFSingleJetLooseID103+
        process.HLTBtagDeepJetSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepJet7p68Double6Jets+
        process.hltBTagPFDeepJet1p28Single6Jets+
        process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5+

        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_QuadPFJet103_88_75_15_PFBTagDeepJet_1p3_VBF2_v
    ############################################################################

#    process.hltVBFPFJetCSVSortedMqq460Detaqq3p5 = process.hltVBFPFJetCSVSortedMqq460Detaqq3p5.clone(
#        inputJetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
#        inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
#    )

    process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5 = process.hltVBFPFJetCSVSortedMqq460Detaqq3p5.clone(
        inputJetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
        inputJets = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPreQuadPFJet103887515PFBTagDeepJet1p3VBF2 = process.hltPreQuadPFJet103887515PFBTagDeepCSV1p3VBF2.clone()

    process.HLT_QuadPFJet103_88_75_15_PFBTagDeepJet_1p3_VBF2_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJetVBFIorHTTIorSingleJet+
        process.hltPreQuadPFJet103887515PFBTagDeepJet1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID75+
        process.hltPFDoubleJetLooseID88+
        process.hltPFSingleJetLooseID103+
        process.HLTBtagDeepJetSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepJet1p28Single6Jets+
        process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v
    ############################################################################

    process.hltPFTripleJetLooseID76 = process.hltPFTripleJetLooseID76.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPFSingleJetLooseID105 = process.hltPFSingleJetLooseID105.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPreQuadPFJet105887615DoublePFBTagDeepJet1p37p7VBF1 = process.hltPreQuadPFJet105887615DoublePFBTagDeepCSV1p37p7VBF1.clone()

    process.HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1008572VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet105887615DoublePFBTagDeepJet1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID76+
        process.hltPFDoubleJetLooseID88+
        process.hltPFSingleJetLooseID105+
        process.HLTBtagDeepJetSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepJet7p68Double6Jets+
        process.hltBTagPFDeepJet1p28Single6Jets+
        process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_QuadPFJet105_88_76_15_PFBTagDeepJet_1p3_VBF2_v
    ############################################################################

    process.hltPreQuadPFJet105887615PFBTagDeepJet1p3VBF2 = process.hltPreQuadPFJet105887615PFBTagDeepCSV1p3VBF2.clone()

    process.HLT_QuadPFJet105_88_76_15_PFBTagDeepJet_1p3_VBF2_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1008572VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet105887615PFBTagDeepJet1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID76+
        process.hltPFDoubleJetLooseID88+
        process.hltPFSingleJetLooseID105+
        process.HLTBtagDeepJetSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepJet1p28Single6Jets+
        process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v
    ############################################################################

    process.hltPFTripleJetLooseID80 = process.hltPFTripleJetLooseID80.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPFDoubleJetLooseID90 = process.hltPFDoubleJetLooseID90.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPFSingleJetLooseID111 = process.hltPFSingleJetLooseID111.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPreQuadPFJet111908015DoublePFBTagDeepJet1p37p7VBF1 = process.hltPreQuadPFJet111908015DoublePFBTagDeepCSV1p37p7VBF1.clone()

    process.HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1058576VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet111908015DoublePFBTagDeepJet1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID80+
        process.hltPFDoubleJetLooseID90+
        process.hltPFSingleJetLooseID111+
        process.HLTBtagDeepJetSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepJet7p68Double6Jets+
        process.hltBTagPFDeepJet1p28Single6Jets+
        process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5+

        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_QuadPFJet111_90_80_15_PFBTagDeepJet_1p3_VBF2_v
    ############################################################################

    process.hltPreQuadPFJet111908015PFBTagDeepJet1p3VBF2 = process.hltPreQuadPFJet111908015PFBTagDeepCSV1p3VBF2.clone()

    process.HLT_QuadPFJet111_90_80_15_PFBTagDeepJet_1p3_VBF2_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet1058576VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet111908015PFBTagDeepJet1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID80+
        process.hltPFDoubleJetLooseID90+
        process.hltPFSingleJetLooseID111+
        process.HLTBtagDeepJetSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepJet1p28Single6Jets+
        process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5+

        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v
    ############################################################################

    process.hltPFTripleJetLooseID71 = process.hltPFTripleJetLooseID71.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPFDoubleJetLooseID83 = process.hltPFDoubleJetLooseID83.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPFSingleJetLooseID98 = process.hltPFSingleJetLooseID98.clone(
        inputTag = cms.InputTag("hltAK4PFJetsLooseIDCorrected"),
    )

    process.hltPreQuadPFJet98837115DoublePFBTagDeepJet1p37p7VBF1 = process.hltPreQuadPFJet98837115DoublePFBTagDeepCSV1p37p7VBF1.clone()

    process.HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepJet_1p3_7p7_VBF1_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet927664VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet98837115DoublePFBTagDeepJet1p37p7VBF1+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID71+
        process.hltPFDoubleJetLooseID83+
        process.hltPFSingleJetLooseID98+
        process.HLTBtagDeepJetSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepJet7p68Double6Jets+
        process.hltBTagPFDeepJet1p28Single6Jets+
        process.hltVBFPFJetDeepJetSortedMqq200Detaqq1p5+
        process.HLTEndSequence
    )

    ############################################################################
    #### HLT_QuadPFJet98_83_71_15_PFBTagDeepJet_1p3_VBF2_v
    ############################################################################

    process.hltPreQuadPFJet98837115PFBTagDeepJet1p3VBF2 = process.hltPreQuadPFJet98837115PFBTagDeepCSV1p3VBF2.clone()

    process.HLT_QuadPFJet98_83_71_15_PFBTagDeepJet_1p3_VBF2_v8 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sTripleJet927664VBFIorHTTIorDoubleJetCIorSingleJet+
        process.hltPreQuadPFJet98837115PFBTagDeepJet1p3VBF2+
        process.HLTAK4CaloJetsSequence+
        process.hltQuadJet15+
        process.hltTripleJet50+
        process.hltDoubleJet65+
        process.hltSingleJet80+
        process.hltVBFCaloJetEtaSortedMqq150Deta1p5+

        # process.HLTFastPrimaryVertexSequence+
        # process.HLTBtagDeepCSVSequenceL3+
        # process.hltBTagCaloDeepCSV1p56Single+

        process.HLTAK4PFJetsSequence+
        process.hltPFQuadJetLooseID15+
        process.hltPFTripleJetLooseID71+
        process.hltPFDoubleJetLooseID83+
        process.hltPFSingleJetLooseID98+
        process.HLTBtagDeepJetSequencePF+
        process.hltSelector6PFJets+
        process.hltBTagPFDeepJet1p28Single6Jets+
        process.hltVBFPFJetDeepJetSortedMqq460Detaqq3p5+
        process.HLTEndSequence
    )


    ############################################################################
    #### HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepJet_1p5_v
    ############################################################################

    process.hltPFJetFilterTwoC30 = process.hltPFJetFilterTwoC30.clone(
        inputTag = cms.InputTag("hltAK4PFJetsCorrected"),
    )

#    process.hltBTagPFDeepCSV1p5Single = process.hltBTagPFDeepCSV1p5Single.clone(
#        JetTags = cms.InputTag("hltDeepCombinedSecondaryVertexBJetTagsPF","probb"),
#        Jets = cms.InputTag("hltPFJetForBtag"),
#    )

    process.hltBTagPFDeepJet1p5Single = process.hltBTagPFDeepCSV1p5Single.clone(
        JetTags = cms.InputTag("hltDeepJetDiscriminatorsJetTags","BvsAll"),
        Jets = cms.InputTag("hltPFJetForBtag"),
    )

    process.hltPreMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZPFDiJet30PFBtagDeepJet1p5 = process.hltPreMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZPFDiJet30PFBtagDeepCSV1p5.clone()


    process.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepJet_1p5_v1 = cms.Path(
        process.HLTBeginSequence+
        process.hltL1sMu5EG23IorMu5IsoEG20IorMu7EG23IorMu7IsoEG20IorMuIso7EG23+
        process.hltPreMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZPFDiJet30PFBtagDeepJet1p5+

        process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegSequence+
        process.HLTMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegSequence+
        process.hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter+

        process.HLTAK4PFJetsSequence+
        process.hltPFJetFilterTwoC30+
        process.HLTBtagDeepJetSequencePF+
        process.hltBTagPFDeepJet1p5Single+
        process.HLTEndSequence
    )


    return process	
