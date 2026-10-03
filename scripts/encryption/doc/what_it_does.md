# What encrypt.py Does

This Python script is an **obfuscation tool** that takes raw, readable shellcode and scrambles it using a basic math operation before it gets deployed.

---

## Step-by-Step Actions

* **Sets the Secret Key:** It defines a specific byte value (`0xB5`) to act as the encryption key. This exact same key must be hardcoded into the C loader so the loader knows how to unlock the file later.
* **Reads the Raw Code:** It opens the file `shellcode.bin` in read-binary mode and loads the raw, unencrypted payload bytes into the computer's memory.
* **Scrambles the Data (XOR Loop):** It loops through every single byte of the original shellcode and performs a bitwise **XOR operation** (`^`) using the `0xB5` key. This completely alters the byte patterns, stripping away any recognizable file signatures that an antivirus would immediatelyflag.
* **Saves the Output:** It creates a brand-new file called `encrypted_shell.bin` and writes the newly scrambled, safe-looking bytes into it.
* **Confirms Success:** It prints a final confirmation message to the terminal showing exactly how many bytes were successfully processed.
