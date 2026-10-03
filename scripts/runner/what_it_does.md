# What This Script Does

This Python script acts as a **stager and downloader**. Its main job is to silently download the loader executable and its encrypted payload from a remote server, verify the downloads, and then launch the loader in the background without opening any visible windows.

---

## 🛠️ Step-by-Step Actions

* **Creates a Log File:** Every time the script takes an action, it writes a status update to a local file named `log.txt`. This helps track whether the process succeeded or failed.
* **Downloads the Loader:** It runs a hidden PowerShell command (`Invoke-WebRequest`) to download your main loader executable (`YOUR_LOADER_EXE_NAME.exe`) from a specific IP address on port `8080`.
* **Downloads the Payload:** It runs another hidden PowerShell command to download the scrambled payload file (`encrypted_shell.bin`) from the same remote server.
* **Checks the Results:** The script looks at the current folder to verify that both files were successfully downloaded. If either file is missing, it logs an error and stops immediately.
* **Launches the Loader Silently:** If both files are present, it runs the loader executable in the background. It uses specific settings (`CREATE_NO_WINDOW`) to ensure no command prompt or window pops up on the screen when the loader starts.
