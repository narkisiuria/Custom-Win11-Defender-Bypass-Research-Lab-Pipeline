key = 0xB5 # YOUR KEY HERE

with open("shellcode.bin", "rb") as f:
    shellcode = f.read()

encrypted = bytes([b ^ key for b in shellcode])

with open("encrypted_shell.bin", "wb") as f:
    f.write(encrypted)

print(f"Done. {len(encrypted)} bytes encrypted.")
