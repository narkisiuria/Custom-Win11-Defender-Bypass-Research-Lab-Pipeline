## encrypt.py guide

# Before giving the commands:
# XOR Encryption, How and Why

## What It Does
XOR encryption takes each byte of the shellcode and flips its bits using a key byte.
The result is a completely different sequence of bytes that no longer matches known signatures in Defender's database.
Decryption is identical — XOR the encrypted bytes with the same key, and you get the original shellcode back.

## Why It Defeats Signature Detection
Antivirus engines maintain a database of known malicious byte patterns (signatures).
When a file is scanned, its bytes are compared against this database.
XOR encryption changes every byte in the payload, so the signature no longer matches — the AV sees an unknown file and marks it clean.

## Why It Fails Against Behavioral Detection
Signature detection scans the file at rest (on disk).
Behavioral/EDR detection watches what the process actually does at runtime.
Once the loader decrypts the shellcode in memory and executes it, the original malicious behavior is visible.
At that point, XOR encryption provides zero protection — the decrypted shellcode is identical to the original.

## Key Rotation
Every time Defender catches a binary, it fingerprints the behavioral pattern and adds it to its cloud database.
Rotating the XOR key produces a different binary each build, resetting the signature — but not the behavior.
Key rotation is a short-term evasion tactic, not a permanent solution.

## Usage
```bash
# Encrypt
python3 encrypt.py

# Verify decryption matches original
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
A CORRECT OUTPUT RESPONSE SHOULD RETURN:
Done. LEN_OF_YOUR_SHELL_CODE_BYTES bytes encrypted.