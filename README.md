# edu-file-locker
Safe, reversible file-locker demo for learning encryption and defense. Sandbox-only, no ransom, no deletion, no root. Educational use in isolated labs.
cd ~/edu-file-locker
cat > README.md << 'EOF'
# Shadowshell — Educational File Locker (Safe Demo)

A **safe, reversible** file-locker written in Python for learning how
encryption, key handling, and restore procedures work.

> ⚠️ **This is NOT ransomware.**
> It does not delete originals, spread, persist, evade detection, demand
> payment, or require root. It only touches `.txt` files inside a local
> `sandbox_demo/` folder and leaves the originals intact.

---

## Why this exists

Most people learn about "ransomware" from headlines. This project gives you
a hands-on way to see how file encryption and decryption actually work —
without any of the harmful behavior. It is meant for classrooms, study
groups, and personal lab practice.

---

## Safety rules

- Runs only inside `sandbox_demo/`
- Only touches `.txt` files
- Leaves the original files in place (creates `.locked` copies)
- No network calls
- No persistence (no cron, no autorun, no services)
- No root privileges required
- No ransom note, no payment, no countdown
- Fully reversible with the same password

Use only in an isolated VM or lab. Never run on real data.

---

## Features

- Colourful terminal UI (green / yellow / red / cyan / magenta)
- Lock: creates `.locked` copies of every `.txt` file
- Unlock: restores `.txt` files from `.locked` copies
- List, view, create, edit (nano), and delete sandbox files
- Help screen and in-app README viewer
- Password-based key derivation (PBKDF2-HMAC-SHA256 → Fernet/AES)
- Virtual environment + `requirements.txt` for clean installs

---

## Install

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/edu-file-locker.git
cd edu-file-locker
