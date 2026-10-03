# Flow Explanation: Attack Lifecycle

This sequence outlines the complete setup phase on the **Kali Linux** attacker machine. It follows a logical pipeline: generating the raw agent, scrambling it to beat static scans, building the delivery executable, hosting the tools, and waiting for the connection.

---

## Step-by-Step Flow

* **Generates the Payload (Step 1):** Uses `msfvenom` to create the raw, unencrypted implant (`shellcode.bin`). This specific payload is configured to establish a secure, encrypted HTTPS reverse connection back to the attacker's machine.
* **Scrambles the Signatures (Step 2):** Runs `encrypt.py` to process the raw binary file. This strips away the obvious `msfvenom` byte patterns, outputting a completely scrambled file (`encrypted_shell.bin`) that disk-based scanners will not recognize.
* **Double-Checks the Logic (Step 3):** Executes a quick, one-line Python test to decrypt the newly scrambled file in memory and compare it back to the original. A `Match: True` output guarantees the loader will be able to successfully unlock it later.
* **Builds the Executable (Step 4):** Compiles the C source code into a Windows binary using a cross-compiler (`mingw32-gcc`). It uses specific flags to strip out debugging symbols (`-s`, `--strip-all`) and hide the console window (`-mwindows`) to keep the file size minimal and stealthy.
* **Hosts the Infrastructure (Step 5):** Spins up a simple local web server on port `8080`. This makes both the compiled loader executable and the encrypted payload file accessible for the target system or stager script to download.
* **Awaits the Connection (Step 6):** Launches the Metasploit handler listener. It is configured to match the HTTPS payload settings exactly and will automatically manage the incoming connection once the loader successfully triggers the payload in memory.
