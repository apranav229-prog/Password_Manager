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
