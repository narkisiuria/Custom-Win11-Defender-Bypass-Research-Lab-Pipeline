# Flow Explanation: Victim Execution Lifecycle

This sequence outlines the execution phase on the **Windows 11** victim machine. It covers fetching the stager script, converting it into a standard standalone executable, and running it to trigger the final payload deployment.

---

## Step-by-Step Flow

* **Fetches the Stager Script (Step 1):** Uses PowerShell (`wget`) to download the `runner.py` script directly from the attacker's web server. 
* **Packages Into a Standalone Binary (Step 2):** Uses `pyinstaller` to bundle the Python script into a single `.exe` file (`--onefile`). It applies the `--noconsole` flag so that when the executable runs, it stays completely invisible without popping up a command prompt window.
* **Locates the Output (Step 3):** Navigates into the newly generated `dist` folder where PyInstaller places the completed, standalone executable.
* **Launches the Attack Chain (Step 4):** Executes `runner.exe`. This starts the background process that downloads the main loader and the encrypted payload, decrypts the shellcode, injects it into `explorer.exe`, and initiates the 30-second delay before connecting back to the listener.
