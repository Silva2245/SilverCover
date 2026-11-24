# Silver Cover

## 📖 What Is This Program?

**SilverCover.py** is a small command-line tool that helps you:

- 🔐 **Encrypt** any file (using AES-GCM + RSA) and save it as `filename.e`
- 🔓 **Decrypt** an encrypted `.e` file back to its original form
- 🥷 **Inject ("steg")** one file's data into another using a hidden delimiter marker → saves as `filename.s`
- 🧲 **Extract ("desteg")** the injected data from a `.s` file

Think of it as a simple "file container" utility. It's designed for learning and experimentation, so treat it as an educational example rather than production-grade security software.

---

## 🧩 How The Program Is Built (Core Components)

The program is organized into four main classes:

| Component | What It Does |
|-----------|--------------|
| **`Loader`** | Reads and writes files as raw bytes — the only part that touches your hard drive. |
| **`Injector`** | Handles the "steganography" feature by joining two data blobs together using a fixed delimiter (an MD5 hash of the word `Spectre`). |
| **`Encryptor`** | The encryption engine: AES-GCM for bulk data, RSA to wrap the authentication tag, plus encrypt/decrypt routines. |
| **`PlayGround`** | The command-line dispatcher — reads your arguments and routes them to the correct operation. |

### A Quick Look at How Encryption Works
1. Your file is encrypted with **AES-GCM** (fast, secure bulk encryption).
2. The authentication **tag** is then wrapped with a **hardcoded RSA key**.
3. Both pieces are joined together and saved as `filename.e`.
4. To decrypt, the process runs in reverse.

---

## 📦 Step 1 — Install Python First

Before installing SilverCover, you need Python installed on your computer.

### On Windows
1. Go to the official site: **https://www.python.org/downloads/**
2. Click **"Download Python"** (grab the latest version).
3. Run the installer. ⚠️ **Important:** Check the box that says **"Add Python to PATH"** before clicking Install.
4. Finish the installation and restart your computer if needed.

### On Linux (Ubuntu/Debian)
Open your terminal and run:

```bash
# Update the package list first
sudo apt update

# Install Python 3
sudo apt install python3

# Verify it's installed
python3 --version
```

&gt; 💡 Tip: You can also download a standalone version from python.org if you prefer not to use your system's package manager.

---

## 📦 Step 2 — Install the Required Libraries

SilverCover depends on several Python libraries. Here's how to install them for each operating system.

### On Windows (Using pip)
1. Open **Command Prompt** or **PowerShell**.
2. Run these commands one at a time:

```bash
pip install pycryptodome rsa colorama
```

### On Linux (Using apt + pip)
Open your terminal and run:

```bash
# Install pip if you don't have it yet
sudo apt-get install python3-pip

# Then install the libraries
pip3 install pycryptodome rsa colorama
```

### ✅ Verify Everything Is Installed
Run this to confirm all three libraries loaded correctly:

```bash
python -c "import Crypto, rsa, colorama; print('All dependencies installed successfully!')"
```

If you see a success message, you're ready to go. 🎉

---

## ▶️ Step 3 — How To Run It

You can run the tool directly from your terminal or command prompt:

```bash
python SilverCover.py [options]
```

### 🔍 Available Commands (Flags)

| Flag | Purpose | Example |
|------|---------|---------|
| `-v` | Verbose mode (prints extra info). Accepts `y`, `yes`, or `true`. | `-v y` |
| `-e` | File you want to **encrypt** | `-e secret.txt` |
| `-d` | File you want to **decrypt** | `-d secret.txt.e` |
| `-mnk` | AES **minor key** (must be exactly 12 characters) | `-mnk "123456789012"` |
| `-mjk` | AES **major key** | `-mjk "my-major-key"` |
| `-s` | Cover file for **steganography injection** | `-s cover.bin` |
| `-f` | Payload to inject into the cover | `-f payload.bin` |
| `-ds` | File to run **desteg/extract** on | `-ds cover.bin.s` |

---

### 🔐 Example: Encrypt a File (Windows)
```bash
python SilverCover.py -e secret.txt -mjk "my-major-key" -mnk "123456789012" -v y
```
➡️ This creates `secret.txt.e`

### 🔓 Example: Decrypt a File (Windows)
```bash
python SilverCover.py -d secret.txt.e -mjk "my-major-key" -mnk "123456789012" -v y
```
➡️ This restores the original `secret.txt`

### 🥷 Example: Inject Data (Steganography)
```bash
python SilverCover.py -s cover.bin -f payload.bin -v y
```
➡️ This creates `cover.bin.s` with your hidden data.

### 🧲 Example: Extract Hidden Data
```bash
python SilverCover.py -ds cover.bin.s -v y
```
➡️ This restores the original cover file and saves the injected data as `StegData`.

---

## ⚙️ A Few Helpful Tips

- **Minor key rule:** The `-mnk` (minor key) must be **exactly 12 characters** — this matches AES-GCM's nonce size. If it's a different length, the program will warn you and stop.
- **Keys are required for encryption/decryption:** You must provide both `-mjk` and `-mnk` when using encrypt (`-e`) or decrypt (`-d`).
- **Everything is case-sensitive** — make sure your keys match exactly between encrypt and decrypt commands.
- **Run from the same folder** where you saved `SilverCover.py`, so it can find the file easily.

---

## 🎯 Quick Start Summary (Copy & Paste)

**Windows:**
```bash
pip install pycryptodome rsa colorama
python SilverCover.py -e secret.txt -mjk "my-major-key" -mnk "123456789012" -v y
```

**Linux:**
```bash
sudo apt update && sudo apt install python3 python3-pip
pip3 install pycryptodome rsa colorama
python3 SilverCover.py -e secret.txt -mjk "my-major-key" -mnk "123456789012" -v y
```

---
