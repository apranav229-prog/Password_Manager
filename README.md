# Password Manager
A simple local password manager built with Python that encrypts and stores your passwords securely on your own device.

## Introduction
Password Manager is a lightweight command line tool that lets you encrypt, store, and retrieve passwords directly on your computer. It uses the Fernet symmetric encryption algorithm from Python's cryptography library, which means your password is scrambled into unreadable text that can only be unlocked with your secret key and master PIN. No cloud, no servers, no third parties involved. Everything stays on your machine.

## How It Works
The project is built around three core ideas:

**Encryption** — When you save a password, it is encrypted using a unique secret key generated on your device. The encrypted version looks like completely random gibberish to anyone who finds the file without the key.

**PIN Protection** — A master PIN is required before you can save or view any password. The PIN itself is never stored in plain text — it is hashed using SHA-256, meaning even if someone opens the PIN file they cannot reverse it back to your original PIN.

**Local Storage** — Everything is stored as files on your own computer. There is no database, no internet connection, and no external service involved at any point.
The tool runs as a simple menu in the terminal with options to save, view, delete, and update your password, as well as change your PIN at any time.

## Why I Built This
Honestly, I kept forgetting my Instagram password. Every time I got logged out I had to go through the whole reset process, which was annoying. I wanted a way to save my password somewhere safe on my computer so I could just look it up whenever I needed it, without writing it on a sticky note or saving it in a plain text file where anyone could read it.
I also wanted to learn a bit about how encryption actually works in Python. I had heard about things like hashing and encryption before but never actually used them. Building this project was a way to understand it hands on rather than just reading about it. It turns out encrypting something is not as complicated as it sounds once you have the right library, and now I actually understand what is happening under the hood when passwords get stored securely.

### Project Structure
```
password_encryptor/

├── password_manager.py       the main script with the full menu system
├── secret.key                auto generated on first run, never share this
├── pin.txt                   stores your hashed PIN
└── instagram_password.txt    stores your encrypted password
```
Setup and Usage
Requirements

Python 3.x
uv (package manager)

### Installation
```
uv init password_encryptor
cd password_encryptor
uv add cryptography
.venv\Scripts\python.exe password_manager.py
```
*On first run it will automatically generate your secret key and ask you to set up a master PIN. After that you will see the main menu every time you run it.*
``` py
import os
import hashlib
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"
PASSWORD_FILE = "instagram_password.txt"
PIN_FILE = "pin.txt"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    print("Key created and saved.")

def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def save_pin(pin):
    with open(PIN_FILE, "w") as f:
        f.write(hash_pin(pin))

def check_pin(pin):
    with open(PIN_FILE, "r") as f:
        stored = f.read()
    return hash_pin(pin) == stored

def setup_pin():
    print("\n-- Set up your master PIN --")
    pin = input("Choose a PIN: ")
    confirm = input("Confirm your PIN: ")
    if pin == confirm:
        save_pin(pin)
        print("PIN saved successfully.")
    else:
        print("PINs did not match. Try again.")
        setup_pin()

def verify_pin():
    pin = input("Enter your master PIN: ")
    if not check_pin(pin):
        print("Wrong PIN. Access denied.")
        return False
    return True

def save_password():
    if not os.path.exists(KEY_FILE):
        generate_key()
    if not verify_pin():
        return
    cipher = Fernet(load_key())
    password = input("Enter your Instagram password: ")
    encrypted = cipher.encrypt(password.encode())
    with open(PASSWORD_FILE, "wb") as f:
        f.write(encrypted)
    print("Password encrypted and saved.")

def view_password():
    if not os.path.exists(PASSWORD_FILE):
        print("No password saved yet.")
        return
    if not verify_pin():
        return
    cipher = Fernet(load_key())
    with open(PASSWORD_FILE, "rb") as f:
        encrypted = f.read()
    decrypted = cipher.decrypt(encrypted)
    print(f"\nYour Instagram password is: {decrypted.decode()}")

def delete_password():
    if not os.path.exists(PASSWORD_FILE):
        print("No password saved yet.")
        return
    if not verify_pin():
        return
    os.remove(PASSWORD_FILE)
    print("Password deleted.")

def menu():
    if not os.path.exists(KEY_FILE):
        print("\nFirst time setup detected...")
        generate_key()
    if not os.path.exists(PIN_FILE):
        setup_pin()
    while True:
        print("\n==============================")
        print("     Instagram Password Manager")
        print("==============================")
        print("1. Save / Update password")
        print("2. View password")
        print("3. Delete password")
        print("4. Change PIN")
        print("5. Exit")
        print("==============================")
        choice = input("Choose an option (1-5): ")
        if choice == "1":
            save_password()
        elif choice == "2":
            view_password()
        elif choice == "3":
            delete_password()
        elif choice == "4":
            if verify_pin():
                setup_pin()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please enter 1 to 5.")

menu()
```
*Main code that encrypts and stores your Instagram password using Fernet symmetric encryption. Protected by a master PIN using SHA-256 hashing, with a simple terminal menu to save, view, delete and update your password.*
### Security Notes

Never share or delete the secret.key file. Without it, your encrypted password cannot be recovered by anyone, including you.

Never upload secret.key to GitHub or any public place. Add it to your .gitignore file.

The encrypted password file is completely useless without the key, so it is safe to store on its own.

This tool protects your password on your local device. It does not affect how the password is stored on Instagram's servers, which handle their own encryption separately.


# Conclusion
This started as a simple idea to stop forgetting a password and turned into a proper introduction to encryption in Python. The project covers real concepts used in security every day — symmetric encryption, hashing, key management, and PIN based access control — all in a small, readable codebase. It is not a replacement for a full featured password manager like Bitwarden or 1Password, but it does the job for local storage and it was genuinely useful to build from scratch.