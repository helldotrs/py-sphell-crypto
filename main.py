from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

def generate_key(password):
    # Use a key derivation function (KDF) to generate a 32-byte key
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=b'salt_',  # You should use a different salt for each user
        iterations=100000,  # Adjust the number of iterations according to your needs
        length=32,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_text(message, key):
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(message.encode())
    return encrypted_text

def decrypt_text(encrypted_text, key):
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode()
    return decrypted_text

def main():
    choice = input("Do you want to encrypt or decrypt? (e/d): ").lower()

    if choice not in ['e', 'd']:
        print("Invalid choice. Please enter 'e' for encrypt or 'd' for decrypt.")
        return

    password = input("Enter your encryption key (password): ")

    if not password:
        print("Please enter a valid encryption key.")
        return

    key = generate_key(password)

    if choice == 'e':
        text = input("Enter the text to encrypt: ")
        encrypted_text = encrypt_text(text, key)
        print("Encrypted text:", encrypted_text.decode())
    else:
        encrypted_text = input("Enter the text to decrypt: ")
        try:
            decrypted_text = decrypt_text(encrypted_text.encode(), key)
            print("Decrypted text:", decrypted_text)
        except Exception as e:
            print("Error decrypting: ", e)

if __name__ == "__main__":
    main()
