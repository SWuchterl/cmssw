### HLT customization functions for Run-3

```
cmsrel CMSSW_12_1_0
cd CMSSW_12_1_0/src
cmsenv
git cms-merge-topic  silviodonato:customizeHLTforRun3
scram b -j4
hltGetConfiguration (....) > hlt.py
```

then you can call the customization function(s) by adding at the bottom of your `hlt.py`, as usual. Example:

```
from HLTrigger.Configuration.customizeHLTforRun3 import *
process = TRK_newTracking(process)
```

This is the list of the customization functions available:

- **TRK_newTracking**: includes the new GPU-ready pixel tracking (customizeHLTforPatatrackTriplets) and the single iteration tracking in the outer tracker ( https://its.cern.ch/jira/browse/CMSHLT-2187)
This function should be always included in your studies.
- **MUO_newTracking**: uses the global pixel tracks and the single-iteration regional tracking in muon reconstruction ( https://its.cern.ch/jira/browse/CMSHLT-2191)
- **MUO_updateTkMu**: uses the global pixel tracks and the single-iteration regional tracking in TkMu paths (https://its.cern.ch/jira/browse/CMSHLT-2191)
- **MUO_updateOpenMu**: uses the global pixel tracks and the single-iteration regional tracking in TkMu paths (https://its.cern.ch/jira/browse/CMSHLT-2191)
- **MUO_updateNoVtx**: uses the global pixel tracks and the single-iteration regional tracking in TkMu paths (https://its.cern.ch/jira/browse/CMSHLT-2191)
- **MUO_newOI**: use the new ML-based outside-in muon for muon reconstruction ( https://its.cern.ch/jira/browse/CMSHLT-2181)
- **MUO_newIO**: uses the new ML-based inside-out seeding for muon reconstruction (https://its.cern.ch/jira/browse/CMSHLT-2182)
This function requires MUO_newTracking

- If you want to test the new DeepTau you can import the sequence from **/users/lwezenbe/12_1_X/TauPOG/NewMenu** (https://its.cern.ch/jira/browse/CMSHLT-2175)
- **TAU_newL2sequence** Update the L2.5 Tau recostruction to the new reconstruction based on ML new pixel tracking (https://its.cern.ch/jira/browse/CMSHLT-2176)
At the moment, this function can be used only on DeepTau paths.

- **BTV_noCalo_roiPF**: duplicates all PFBTagDeepCSV  to a version based on Calo b-tagging: none. PF b-tagging: DeepCSV and new regional PF and tracking. ( https://its.cern.ch/jira/browse/CMSHLT-2186) The CaloBTagDeepCSV paths remain unchanged.
- **BTV_moveToDeepJetROI**: duplicates all PFBTagDeepCSV  to a version based on Calo b-tagging: none. PF b-tagging: DeepJet and new regional PF and tracking (https://its.cern.ch/jira/browse/CMSHLT-2184)

Other b-tagging functions with a lower priority are also available for testing:

- BTV_roiCalo_roiPF_DeepCSV. Calo b-tagging: new regional calo b-tagging [new sequence] ## PF b-tagging: new regional DeepCSV PF b-tagging [add new paths] (https://its.cern.ch/jira/browse/CMSHLT-2186)
- BTV_roiCalo_roiPF_DeepJet. Calo b-tagging: new regional calo b-tagging [new sequence] ## PF b-tagging: new regional DeepJet PF b-tagging [add new paths] (https://its.cern.ch/jira/browse/CMSHLT-2186)
- BTV_roiCalo_globalPF_DeepCSV. Calo b-tagging: new regional calo b-tagging [new sequence] ## PF b-tagging: new global PF DeepCSV b-tagging (https://its.cern.ch/jira/browse/CMSHLT-2186)
- BTV_roiCalo_globalPF_DeepPF. Calo b-tagging: new regional calo b-tagging [new sequence] ## PF b-tagging: new global PF DeepPF b-tagging (https://its.cern.ch/jira/browse/CMSHLT-2186)
All the BTV_roiCalo functions require TRK_newTracking.
- BTV_globalCalo_globalPF. Calo b-tagging: version based on the global PF tracking. PF b-tagging: global PF b-tagging (https://its.cern.ch/jira/browse/CMSHLT-2186)
- BTV_moveToDeepJet. duplicates all *PFBTagDeepCSV*  to a version based on Calo b-tagging: none. PF b-tagging:  DeepJet (https://its.cern.ch/jira/browse/CMSHLT-2184)
- BTV_addMCDeepJetROIForBTagPath. adds MC_PFBTagDeepJetROIForBTag based on DeepJet and the new regional PF (https://its.cern.ch/jira/browse/CMSHLT-2184).
The DeepJet sequence can be later included in your favorite path.


More info can be found in the google doc of the POG developments https://docs.google.com/spreadsheets/d/1nqd3qhFuM7TQgFRO_ZKNaGzCR0a21r4FLZQDC-JI-u0/edit#gid=0 




### Credits

The customization functions have been downloaded from several repositories (see https://github.com/silviodonato/cmssw/blob/customizeHLTforRun3/HLTrigger/Configuration/python/Run3/downloadCustomizationFunctions.sh )

https://github.com/SWuchterl/RecoBTag-PerformanceMeasurements

https://github.com/mmasciov/cmssw/defaultRun3Tracking_forJIRA

https://github.com/annamasce/TauTriggerTools/triggerRnD_counter

https://github.com/khaosmos93/MuonHLTForRun3

