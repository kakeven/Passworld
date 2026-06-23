from typing import Any
import threading
import secrets

session: dict[str, Any] = {
    "token": None,
    "key": None,
    "vault": None
}

def expirar_token():
    session["key"] = None
    session["token"] = None
    session["vault"] = None

def criar_token(tempo=900):
    token =secrets.token_hex(32)
    session["token"] = token
    
    timer = threading.Timer(tempo, expirar_token) 
    timer.start()
    
    return token