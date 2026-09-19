![Microgrid DevSecOps CI](https://github.com/Haidriyam/microgrid-resilient-control/actions/workflows/devsecops-ci.yml/badge.svg)

# Cyber-Resilient Microgrid Secondary Frequency Consensus Controller

A cyber-physical systems (CPS) modeling engine and distributed secondary consensus controller designed to stabilize islanded AC microgrid frequencies under False Data Injection (FDI) telemetry attacks.

```text
  [ Physical Inverter Grid ] ──(Primary Droop: P-f)──► [ Frequency Sag: 49.3 Hz ]
             │                                                    │
    (Adversarial Link)                                    (Secondary Loop)
             ▼                                                    ▼
 [ FDI Attack Injection: 59.8 Hz ] ──► [ Sanitize Filter ] ──► [ Consensus Engine ] ──► [ 50.0 Hz Restored ]