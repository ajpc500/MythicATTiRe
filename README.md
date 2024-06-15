# MythicATTiRe

This Python script converts the JSON output from Mythic 3 into a format compatible with Security Risk Advisors' [ATTiRe](https://github.com/SecurityRiskAdvisors/ATTiRe#) format, compatible with [VECTR](https://vectr.io/).

> NOTE: Ensure command output and MITRE ATT&CK coverage is included in Mythic reporting output.

## Usage

```
python3 mythicATTiRe.py mythic-report.json
[+] Created ATTiRe JSON file: ATTiRe_1_Operation_Chimera-report.json
[+] Created ATTiRe JSON file: ATTiRe_2_Operation_Chimera-report.json
```

This script creates an individual JSON file per callback. These can then be imported individually into the same or different VECTR Campaigns as needed. 
