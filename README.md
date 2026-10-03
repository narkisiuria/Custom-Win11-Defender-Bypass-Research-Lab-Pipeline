# Custom Win 11 Defender Bypass Research Lab Pipeline

A custom Windows Defender bypass and persistence pipeline built for Red Team education and lab practice. This repository provides an end-to-end (ETE) blueprint and documentation suite demonstrating how custom loaders, stagers, and encryption routines interact to defeat modern security controls on a fully updated Windows 11 host with Cloud Protection enabled.

---

## Disclaimer
This project is for educational, research, and authorized testing purposes only. All testing was performed in an isolated lab environment. Do not use against systems you do not own or have explicit written permission to test. The author assumes no liability for misuse.

---

## The End-to-End Attack Chain Pipeline

The entire lab operates as a continuous, automated delivery and execution pipeline:

    [ Phase 1: Attacker Setup ]
      ├── 1. Generate Raw Shellcode (msfvenom)
      ├── 2. Obfuscate Payload (encrypt.py via 0xB5 XOR Key)
      └── 3. Cross-Compile Stealth Loader (x86_64-w64-mingw32-gcc)
                │
                ▼
    [ Phase 2: Victim Staging & Delivery ]
      ├── 4. Initial access simulation (Victim runs packaged runner.exe)
      ├── 5. Runner script silently pulls loader.exe & encrypted_shell.bin via HTTP
      └── 6. Runner launches loader.exe with hidden window flags
                │
                ▼
    [ Phase 3: Memory Injection & Session Trigger ]
      ├── 7. Loader.exe patches AMSI in memory to blind Windows Defender
      ├── 8. Loader decrypts shellcode back into raw executable bytes
      └── 9. Loader injects payload into explorer.exe -> Spawns Remote HTTPS Meterpreter Session
                │
                ▼
    [ Phase 4: Persistence Maintenance ]
      └── 10. Establishes a Registry Run key under HKCU for survivability

---

## Techniques Implemented

*   **Sandbox Evasion:** Implements a 30-second execution delay (Sleep). This causes automated sandbox environments to time out during analysis and mark the binary as clean before any logic runs.
*   **AMSI Bypass:** Dynamically patches AmsiScanBuffer in memory before shellcode decryption. This forces the function to always report code as safe, blinding Windows Defender script and memory scanning.
*   **Shellcode Encryption:** Uses a bitwise XOR math operation with a rotating key. This completely alters the byte signatures on every separate build, stripping away static patterns caught by disk-based antivirus definitions.
*   **Process Injection:** Injects code into explorer.exe using VirtualAllocEx -> WriteProcessMemory -> CreateRemoteThread. 
*   **DEP/OPSEC Clean Memory:** Allocates target memory strictly as PAGE_READWRITE first, copying code, and then changing permissions to PAGE_EXECUTE_READ via VirtualProtectEx. This avoids the classic PAGE_EXECUTE_READWRITE (RWX) allocation pattern universally flagged by behavioral sensors.
*   **Registry Persistence:** Writes to the user environment Run key (HKCU\Software\Microsoft\Windows\CurrentVersion\Run). Because the runner script pulls a fresh loader binary from the attacker's server on every single execution, every system boot generates a completely new binary signature.

---

## Repository Structure & Index

Use the links below to quickly jump through the code blocks, command configurations, and technical breakdowns:

    ├── commands/
    │   ├── KALI-ATTACKER/
    │   │   ├── commands.md                 # Listener setup and msfvenom commands
    │   │   └── flow_explanation.md         # The "why and how" behind attacker configurations
    │   └── WINDOWS11-VICTIM/
    │       ├── commands.md                 # Stager conversion and victim-side triggers
    │       └── flow_explanation.md         # The "why and how" behind client-side staging
    ├── loader/
    │   ├── code/loader.c                   # Core C loader source (AMSI patch & injection)
    │   └── doc/what_it_does.md              # Step-by-step memory logic walkthrough
    ├── scripts/
    │   ├── encryption/
    │   │   ├── encrypt.py                  # XOR encryption script utility
    │   │   └── doc/what_it_does.md         # Scrambling process breakdown
    │   └── runner/
    │       ├── source/runner.py            # Python stager/downloader code
    │       └── doc/what_it_does.md         # Network delivery walkthrough
    └── shellcode/
        └── doc/creation.md                 # Analysis of Staged vs Stageless architecture

---

## Lab Setup Reference

*   **Attacker Node:** Kali Linux, Metasploit Framework  
*   **Target Endpoint:** Windows 11 Workstation (Fully Updated, Real-time Defender + Cloud Protection active)  
*   **Network Layout:** Isolated VirtualBox host-only network  
*   **Cross-Compiler Command (Kali):**
    ```bash
    x86_64-w64-mingw32-gcc loader.c -o output.exe -mwindows -O2 -fvisibility=hidden -s -Wl,--strip-all -lkernel32 -lntdll
    ```

---

## Detection & Mitigation (Blue Team Playbook)

To hunt or block this exact pipeline pattern, defenders can leverage the following telemetry indicators:

| Technical Indicator / Behavior | Windows Event ID | Monitoring & Detection Method |
| :--- | :--- | :--- |
| **Process injection into explorer.exe** | Sysmon Event ID 8 | Track anomalies where CreateRemoteThread targets explorer.exe. |
| **Registry Run key persistence** | Security 4657 / Sysmon 13 | Monitor unexpected registry modifications under the CurrentVersion\Run hives. |
| **AMSI Patch modification** | Sysmon Event ID 10 | Audit unexpected VirtualProtect API calls aiming directly at memory pages inside amsi.dll. |
| **Suspicious process spawn** | Security 4688 | Detect unusual sub-processes spawned directly out of explorer.exe (e.g. system binaries executing without user interface activity). |

### Recommended Defense Configurations:
1. **Sysmon Integration:** Deploy Microsoft Sysmon alongside a robust configuration profile (such as the SwiftOnSecurity template) to guarantee deep process visibility.
2. **ASR Rule Deployment:** Turn on native Microsoft Attack Surface Reduction (ASR) rules—particularly blocking process creations stemming from obfuscated scripts.
3. **Egress Firewall Filtering:** Enforce strict outbound firewall policies blocking core system processes like explorer.exe from initiating network sessions to external, non-Microsoft IP blocks.
4. **Behavioral Key Auditing:** Constantly look for unexpected modifications to standard startup run registries.

---

## Lab Pipeline Status

- [x] XOR encrypted shellcode loader
- [x] Memory-space AMSI bypass patch
- [x] Hidden remote process injection defeating Windows 11 Defender
- [x] Automated registry persistence workflow
- [ ] UAC bypass implementation to High Integrity
- [ ] SYSTEM context elevation via Local Privilege Escalation (LPE)
- [ ] LSASS memory dumping / credential harvesting
- [ ] Pass-the-Hash lateral movement capabilities
