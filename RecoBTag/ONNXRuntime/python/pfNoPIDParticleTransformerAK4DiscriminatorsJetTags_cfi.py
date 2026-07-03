import FWCore.ParameterSet.Config as cms

pfNoPIDParticleTransformerAK4DiscriminatorsJetTags = cms.EDProducer(
   'BTagProbabilityToDiscriminator',
   discriminators = cms.VPSet(
      cms.PSet(
         name = cms.string('BvsAll'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            ),
         denominator=cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probg'),
         ),
      ),
      cms.PSet(
         name = cms.string('CvsL'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probg'),
            ),
         ),
      cms.PSet(
         name = cms.string('CvsB'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            ),
         ),
      cms.PSet(
         name = cms.string('CvsNotB'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probg'),
            ),
         ),
      cms.PSet(
         name = cms.string('BvsC'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            ),
         ),
      cms.PSet(
         name = cms.string('QvsG'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probg'),
            ),
         ),
      cms.PSet(
         name = cms.string('SvsUDG'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probg'),
            ),
         ),
      cms.PSet(
         name = cms.string('SvsBC'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            ),
         ),
      cms.PSet(
         name = cms.string('AllvsPU'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probg'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probg'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probpu'),
            ),
         ),
      cms.PSet(
         name = cms.string('HFvsLF'),
         numerator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            ),
         denominator = cms.VInputTag(
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probbb'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probcc'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probs'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probud'),
            cms.InputTag('pfNoPIDParticleTransformerAK4JetTags', 'probg'),
            ),
         ),
      )
   )
