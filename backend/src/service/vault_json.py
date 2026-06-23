import os
import json
import base64
from service.crypto import derive_key, encrypt, decrypt
from cryptography.exceptions import InvalidTag

VAULT_PATH = "passworld.vault"

def vault_exists() -> bool:
    return os.path.exists(VAULT_PATH)

def create_vault(master_password: str):
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    
    empty_vault = json.dumps({"version": "1.0", "entries": []}).encode()
    nonce, ciphertext = encrypt(key, empty_vault)

    data = {
        "salt": base64.b64encode(salt).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }

    with open(VAULT_PATH, "w") as f:
        json.dump(data, f)

    return key  # guarda em memória, nunca em disco

def open_vault(master_password: str) -> tuple[dict, bytes]:
    with open(VAULT_PATH) as f:
        data = json.load(f)

    salt = base64.b64decode(data["salt"])
    nonce = base64.b64decode(data["nonce"])
    ciphertext = base64.b64decode(data["ciphertext"])

    key = derive_key(master_password, salt)

    try:
        plaintext = decrypt(key, nonce, ciphertext)
    except InvalidTag:
        raise ValueError("Senha mestra incorreta")

    return json.loads(plaintext), key

def save_vault(key: bytes, vault: dict):
    with open(VAULT_PATH) as f:
        data = json.load(f)

    salt = base64.b64decode(data["salt"])  # salt original, nunca muda
    plaintext = json.dumps(vault).encode()
    nonce, ciphertext = encrypt(key, plaintext)

    data["nonce"] = base64.b64encode(nonce).decode()
    data["ciphertext"] = base64.b64encode(ciphertext).decode()

    tmp = VAULT_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.replace(tmp, VAULT_PATH)  # atômico — se cair a luz no meio, vault antigo sobrevive