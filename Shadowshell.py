(kali㉿localhost)-[~/edu-file-locker]
└─$ cat ~/edu-file-locker/shadowshell.py
#!/usr/bin/env python3
import os
import subprocess
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

SANDBOX = "sandbox_demo"
README = "README.md"
SALT = b"educational-demo-salt"

# --- ANSI colors ---
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
MAGENTA= "\033[95m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def clear():
    os.system("clear")

def banner():
    clear()
    print(f"{GREEN}{BOLD}" + r"""
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗███████╗██╗  ██╗███████╗██╗     ██╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔════╝██║  ██║██╔════╝██║     ██║
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║███████╗███████║█████╗  ██║     ██║
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║╚════██║██╔══██║██╔══╝  ██║     ██║
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝███████║██║  ██║███████╗███████╗███████╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
""" + f"{RESET}")
    print(f"{CYAN}{BOLD}" + " " * 16 + "SHADOWSHELL v2 — EDUCATIONAL FILE LOCKER" + f"{RESET}")
    print(f"{YELLOW}" + " " * 10 + "Safe, reversible, non-destructive lab demo" + f"{RESET}")
    print(f"{RED}" + " " * 10 + "No ransom. No deletion. No root. No network." + f"{RESET}\n")

def info(m): print(f"{CYAN}[*] {m}{RESET}")
def ok(m):   print(f"{GREEN}[+] {m}{RESET}")
def warn(m): print(f"{YELLOW}[!] {m}{RESET}")
def err(m):  print(f"{RED}[-] {m}{RESET}")

def get_key(password: str) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32,
        salt=SALT, iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

# ---------- Core ops ----------
def lock(password: str):
    f = Fernet(get_key(password))
    count = 0
    for name in os.listdir(SANDBOX):
        path = os.path.join(SANDBOX, name)
        if os.path.isfile(path) and name.endswith(".txt"):
            data = open(path, "rb").read()
            with open(path + ".locked", "wb") as out:
                out.write(f.encrypt(data))
            count += 1
            warn(f"Locked copy created: {name}.locked")
    ok(f"Created {count} .locked copies. Originals were left intact.") if count else err("No .txt files found.")

def unlock(password: str):
    f = Fernet(get_key(password))
    count = 0
    for name in os.listdir(SANDBOX):
        if name.endswith(".txt.locked"):
            path = os.path.join(SANDBOX, name)
            try:
                data = f.decrypt(open(path, "rb").read())
            except Exception:
                err(f"Failed to decrypt {name} (wrong password?)")
                continue
            original = path[:-7]
            with open(original, "wb") as out:
                out.write(data)
            os.remove(path)
            count += 1
            ok(f"Restored: {original}")
    ok(f"Restored {count} files.") if count else err("No .locked files found.")

# ---------- File tools ----------
def safe_path(name: str) -> str:
    name = os.path.basename(name.strip())
    if not name.endswith(".txt"):
        name += ".txt"
    return os.path.join(SANDBOX, name)

def list_files():
    info("Sandbox contents:")
    files = sorted(os.listdir(SANDBOX))
    if not files:
        warn("Sandbox is empty.")
        return []
    for i, name in enumerate(files, 1):
        color = YELLOW if name.endswith(".locked") else GREEN
        print(f"  {MAGENTA}{i:>2}){RESET} {color}{name}{RESET}")
    return files

def view_file(name: str):
    path = safe_path(name)
    if not os.path.isfile(path):
        err(f"File not found: {name}")
        return
    if name.endswith(".locked"):
        err("Cannot view .locked files (encrypted). Unlock first.")
        return
    print(f"\n{CYAN}--- {os.path.basename(path)} ---{RESET}")
    try:
        print(open(path, "r", errors="replace").read())
    except Exception as e:
        err(f"Read error: {e}")
    print(f"{CYAN}--- end ---{RESET}")

def create_file(name: str):
    path = safe_path(name)
    if os.path.exists(path):
        warn(f"File exists: {os.path.basename(path)}")
        return
    print(f"{YELLOW}Enter content. End with a single line containing only EOF:{RESET}")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "EOF":
            break
        lines.append(line)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    ok(f"Created: {os.path.basename(path)}")

def edit_in_nano(name: str):
    path = safe_path(name)
    try:
        subprocess.run(["nano", path])
        ok(f"Saved via nano: {os.path.basename(path)}")
    except FileNotFoundError:
        err("nano not installed. Run: apt install nano -y")
    except Exception as e:
        err(f"nano error: {e}")

def delete_file(name: str):
    path = safe_path(name)
    if not os.path.isfile(path):
        err(f"File not found: {name}")
        return
    confirm = input(f"{RED}Delete {os.path.basename(path)}? (y/N): {RESET}").strip().lower()
    if confirm == "y":
        os.remove(path)
        ok(f"Deleted: {os.path.basename(path)}")
    else:
        warn("Cancelled.")

def show_readme():
    if os.path.exists(README):
        print(f"\n{CYAN}" + open(README).read() + f"{RESET}")
    else:
        warn("README.md not found.")

def help_screen():
    clear()
    banner()
    print(f"{CYAN}{BOLD}HELP — SHADOWSHELL v2{RESET}\n")
    print(f"{GREEN}Lock / Unlock{RESET}")
    print(f"  {YELLOW}Lock{RESET}   -> creates .locked copies of .txt files (originals stay)")
    print(f"  {YELLOW}Unlock{RESET} -> restores .txt files using the same password\n")
    print(f"{GREEN}File tools{RESET}")
    print(f"  {CYAN}List{RESET}   -> shows files inside sandbox_demo")
    print(f"  {CYAN}View{RESET}   -> reads a .txt file to the screen")
    print(f"  {CYAN}Create{RESET} -> write a new .txt (type EOF on its own line to finish)")
    print(f"  {CYAN}Edit{RESET}   -> open a file in nano")
    print(f"  {RED}Delete{RESET} -> removes a sandbox file (asks first)\n")
    print(f"{GREEN}Tips{RESET}")
    print(f"  - You can pick files by number or by name")
    print(f"  - Add .txt automatically if you forget")
    print(f"  - Password is required for Lock and Unlock\n")
    print(f"{RED}Reminder:{RESET} This is a lab demo. Do not use outside an isolated VM.\n")

# ---------- Menu ----------
def menu():
    print(f"{GREEN} 1){RESET} {YELLOW}Lock{RESET}      create .locked copies")
    print(f"{GREEN} 2){RESET} {YELLOW}Unlock{RESET}    restore from .locked copies")
    print(f"{GREEN} 3){RESET} {CYAN}List{RESET}      sandbox files")
    print(f"{GREEN} 4){RESET} {CYAN}View{RESET}      read a .txt file")
    print(f"{GREEN} 5){RESET} {CYAN}Create{RESET}    new .txt file")
    print(f"{GREEN} 6){RESET} {CYAN}Edit{RESET}      open file in nano")
    print(f"{GREEN} 7){RESET} {RED}Delete{RESET}    remove a sandbox file")
    print(f"{GREEN} 8){RESET} {CYAN}Read{RESET}      README/help")
    print(f"{MAGENTA} 9){RESET} {MAGENTA}Help{RESET}      quick usage guide")
    print(f"{RED} 0){RESET} {RED}Exit{RESET}")

def pick_file(prompt="Filename"):
    files = list_files()
    if not files:
        return None
    name = input(f"\n{YELLOW}{prompt} (name or number): {RESET}").strip()
    if name.isdigit():
        idx = int(name) - 1
        if 0 <= idx < len(files):
            return files[idx]
        err("Invalid number.")
        return None
    return name

def main():
    os.makedirs(SANDBOX, exist_ok=True)
    while True:
        banner()
        menu()
        choice = input(f"\n{BOLD}Select:{RESET} ").strip()

        if choice == "1":
            lock(input(f"{YELLOW}Password:{RESET} "))
        elif choice == "2":
            unlock(input(f"{YELLOW}Password:{RESET} "))
        elif choice == "3":
            list_files()
        elif choice == "4":
            name = pick_file("View which file")
            if name: view_file(name)
        elif choice == "5":
            create_file(input(f"{YELLOW}New filename (e.g. notes): {RESET}"))
        elif choice == "6":
            name = pick_file("Edit which file")
            if name: edit_in_nano(name)
        elif choice == "7":
            name = pick_file("Delete which file")
            if name: delete_file(name)
        elif choice == "8":
            show_readme()
        elif choice == "9":
            help_screen()
        elif choice == "0":
            ok("Bye.")
            break
        else:
            err("Invalid choice.")
        input(f"\n{DIM}{CYAN}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main()
