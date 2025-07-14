from cryptography.fernet import Fernet
import os

def encrypt_data(data: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(token: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    return fernet.decrypt(token.encode()).decode()


def load_key() -> bytes:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    KEY_PATH = os.path.join(BASE_DIR, "secret.key")
    with open(KEY_PATH, "rb") as key_file:
        return key_file.read()