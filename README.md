# AV-Evasion-Lab

A custom Windows Defender bypass and persistence framework built for red team education and lab practice.
Tested against a fully updated Windows 11 host with cloud protection enabled.

---

## ⚠️ Disclaimer
This project is for **educational purposes only**. All testing was performed in an isolated lab environment.
Do not use against systems you do not own or have explicit written permission to test.

---

## Attack Chain

```
Phishing Email → Victim runs runner.exe → Downloads loader + shellcode → 
Injects into explorer.exe → Meterpreter session → Registry persistence
```

---

## Techniques Used

**Sandbox Evasion**
- 30-second sleep before execution — causes automated sandboxes to time out and mark the binary as clean

**AMSI Bypass**
- Patches `AmsiScanBuffer` in memory to always return clean before shellcode decryption

**Shellcode Encryption**
- XOR encryption with a rotating key — changes the binary signature on every build, defeating static signature detection

**Process Injection**
- `VirtualAllocEx` + `WriteProcessMemory` + `CreateRemoteThread` into `explorer.exe`
- Memory allocated as `PAGE_READWRITE` first, then changed to `PAGE_EXECUTE_READ` via `VirtualProtectEx` — avoids the classic `PAGE_EXECUTE_READWRITE` allocation pattern flagged by behavioral detection

**Persistence**
- Registry Run key under `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- runner.exe downloads a fresh loader binary on every execution — each run produces a new binary signature

---

## Project Structure

```
├── commands/
│   ├── KALI-ATTACKER/commands.md     # Listener and msfvenom commands
│   └── WINDOWS11-VICTIM/commands.md  # Victim-side commands
├── encryption/
│   └── encrypt.py                    # XOR encryption script
├── loader/
│   └── code/loader.c                 # Custom C loader source
├── runner/
│   ├── code/runner.py                # Python runner source
│   └── run_flow.md                   # Execution flow documentation
└── shellcode/
    └── creation.md                   # Shellcode generation commands
```

---

## Lab Setup

**Attacker:** Kali Linux, Metasploit Framework  
**Target:** Windows 11 (fully updated, Defender + cloud protection enabled)  
**Network:** Isolated VirtualBox host-only network  
**Compiler:** mingw-w64 cross-compiler on Kali  

**Compile command:**
```bash
x86_64-w64-mingw32-gcc loader.c -o output.exe -mwindows -O2 -fvisibility=hidden -s -Wl,--strip-all -lkernel32 -lntdll
```

---

## Detection & Mitigation (Blue Team)

| Technique | Windows Event ID | Detection Method |
|---|---|---|
| Process injection into explorer.exe | 8 (Sysmon) | CreateRemoteThread on explorer.exe |
| Registry Run key persistence | 4657 / Sysmon 13 | Write to CurrentVersion\Run |
| AMSI patch | Sysmon 10 | VirtualProtect on amsi.dll memory |
| Suspicious process spawn | 4688 | notepad.exe spawned by explorer.exe |

**Mitigations:**
- Enable Sysmon with a comprehensive config (SwiftOnSecurity template)
- Enable Attack Surface Reduction (ASR) rules in Defender
- Block outbound connections from explorer.exe to non-Microsoft IPs
- Monitor registry Run keys for unexpected entries

---

## Status

- [x] XOR encrypted shellcode loader
- [x] AMSI bypass
- [x] Process injection bypassing Defender on Win11
- [x] Registry persistence
- [ ] UAC bypass to High integrity
- [ ] SYSTEM via local privilege escalation
- [ ] Hash dumping (Mimikatz)
- [ ] Pass-the-Hash lateral movement
```