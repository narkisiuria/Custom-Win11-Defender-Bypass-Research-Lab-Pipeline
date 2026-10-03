# What This Loader Does

This software is a **payload loader** designed to run a hidden file (`encrypted_shell.bin`) silently inside the memory of a legitimate Windows process (**explorer.exe**). 

Instead of running the payload directly—which security tools would easily catch—this loader acts as a delivery vehicle that hides, decrypts, and injects the code into a safe system process.

---

## Step-by-Step Actions

* **Pauses for 30 Seconds:** The program sits completely still at start-up (`Sleep`). This tricks basic automated security scanners, which usually stop monitoring a file after a few seconds.
* **Gathers System Information:** It collects basic details about the computer, like its name and total memory size (`checkSystem`).
* **Blinds Windows Defender:** It alters a Windows security feature called **AMSI** (`bypassAMSI`). By modifying a specific function in memory, it forces the system to always report that the running code is completely safe.
* **Reads and Decrypts the Payload:** It opens the file `encrypted_shell.bin`, reads the scrambled data, and uses a bitwise **XOR** math loop with the key `0xB5` to turn it back into working code.
* **Finds the Target Process:** It scans all running programs on the computer to locate the Process ID (PID) for **explorer.exe** (the standard Windows desktop environment).
* **Injects the Code:** It opens a backdoor into `explorer.exe`, allocates a tiny sliver of memory inside it, and copies the decrypted code over.
* **Executes Silently:** It changes the memory rules to allow execution and creates a remote execution thread (`CreateRemoteThread`). This forces `explorer.exe` to run the payload under its own name.
