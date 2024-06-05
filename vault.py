# vault.py
import json
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode

SALT_SIZE = 16
KEY_SIZE = 32
ITERATIONS = 100_000


def create_vault(vault_name, master_password):
    vault_file = f"{vault_name}.json"
    if os.path.exists(vault_file):
        raise FileExistsError("A vault with this name already exists.")

    salt = os.urandom(SALT_SIZE)
    key = derive_key(master_password, salt)

    vault_data = {
        "vault_name": vault_name,
        "salt": urlsafe_b64encode(salt).decode(),
        "records": []
    }

    with open(vault_file, 'w') as f:
        json.dump(vault_data, f)


def load_vault(vault_name):
    vault_file = f"{vault_name}.json"
    if os.path.exists(vault_file):
        with open(vault_file, 'r') as f:
            return json.load(f)
    else:
        raise FileNotFoundError("No vault found with this name.")


def save_vault(vault_data):
    vault_file = f"{vault_data['vault_name']}.json"
    with open(vault_file, 'w') as f:
        json.dump(vault_data, f)


def sign_in(vault_name, master_password):
    vault_data = load_vault(vault_name)
    if vault_data:
        salt = urlsafe_b64decode(vault_data['salt'])
        key = derive_key(master_password, salt)
        return vault_data, urlsafe_b64encode(key).decode()
    return None, None


def derive_key(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=KEY_SIZE,
                     salt=salt,
                     iterations=ITERATIONS,
                     backend=default_backend())
    return kdf.derive(password.encode())


def encrypt_data(data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key),
                    modes.CFB(iv),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return urlsafe_b64encode(iv + encrypted_data).decode()


def decrypt_data(data, key):
    data = urlsafe_b64decode(data)
    iv = data[:16]
    encrypted_data = data[16:]
    cipher = Cipher(algorithms.AES(key),
                    modes.CFB(iv),
                    backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    return (unpadder.update(decrypted_data) + unpadder.finalize()).decode()


def create_password_record(vault_data, key, name, username, password):
    key = urlsafe_b64decode(key.encode())
    encrypted_password = encrypt_data(password, key)
    record = {
        "name": name,
        "username": username,
        "password": encrypted_password
    }

    vault_data['records'].append(record)
    save_vault(vault_data)


def retrieve_password_record(vault_data, key, name):
    key = urlsafe_b64decode(key.encode())
    for record in vault_data['records']:
        if record['name'] == name:
            username = record['username']
            decrypted_password = decrypt_data(record['password'], key)
            return username, decrypted_password
    return None, None


def update_password_record(vault_data, key, name, new_username, new_password):
    key = urlsafe_b64decode(key.encode())
    for record in vault_data['records']:
        if record['name'] == name:
            if new_username:
                record['username'] = new_username
            if new_password:
                record['password'] = encrypt_data(new_password, key)
            save_vault(vault_data)
            return
    raise ValueError("No record found with that name.")
