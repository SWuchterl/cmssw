import FWCore.ParameterSet.Config as cms
from NanoTuples.NanoTuples.ak15_cff import setupAK15
# from PhysicsTools.NanoTuples.ak8_cff import addCustomTaggerAK8
# from PhysicsTools.NanoTuples.pfcands_cff import addPFCands


def nanoTuples_customizeCommon(process, addAK15=True,
                            #    addPFcands=False,
                               customAK8Taggers=[],
                            #    customAK15Taggers=['InclParticleTransformerV2']):
                               customAK15Taggers=['GlobalParticleTransformerV3']):

    runOnMC = True
    if hasattr(process, "NANOEDMAODoutput") or hasattr(process, "NANOAODoutput"):
        runOnMC = False

    pfcand_params = {'srcs': [], 'isPuppiJets': [], 'jetTables': []}
    if addAK15:
        setupAK15(process, runOnMC=runOnMC, runParticleNetMD=True, customAK15Taggers=customAK15Taggers)
        pfcand_params['srcs'].append('ak15WithUserData')
        pfcand_params['isPuppiJets'].append(True)
        pfcand_params['jetTables'].append('ak15Table')
    # if len(customAK8Taggers) > 0:
    #     addCustomTaggerAK8(process, customAK8Taggers)
    #     pfcand_params['srcs'].append('updatedJetsAK8WithUserData')
    #     pfcand_params['isPuppiJets'].append(True)
    #     pfcand_params['jetTables'].append('fatJetTable')
    # if addPFcands:
    #     addPFCands(process, outTableName='PFCands', **pfcand_params)

    return process


def nanoTuples_withAK15(process):
    process = nanoTuples_customizeCommon(process, addAK15=True)
    return process
