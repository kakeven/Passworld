from fastapi import APIRouter,HTTPException,Header
from schema.unlock_request import UnlockRequest
from schema.entries_schema import  Entry
from service.session import session
from service.vault_json import vault_exists, create_vault, open_vault,save_vault
from service.gerador_senha import gerador
import secrets

login_router = APIRouter()


@login_router.post("/unlock")
def unlock(body: UnlockRequest):
    if not vault_exists():
        key = create_vault(body.password)
        vault = {"version": "1.0", "entries": []}
    else:
        try:
            vault, key = open_vault(body.password)
        except ValueError:
            raise HTTPException(status_code=401, detail="Senha mestra incorreta")

    token = secrets.token_hex(32)
    session["token"] = token
    session["key"] = key
    session["vault"] = vault

    return {"token": token}

@login_router.get("/entries")
def show_entries(token:str = Header(...)):
    if session["token"] == token:
        return(session["vault"]["entries"])
    raise HTTPException(status_code=401, detail="Sessão expirada")

@login_router.post("/create_entry")
def create_entry(body:Entry,token:str = Header(...)):
    if session["token"] != token:
        return HTTPException(status_code=401, detail="Sessão expirada")
    entry = {
        "id": secrets.token_hex(8),
        "service": body.service,
        "login": body.login,
        "password": body.password,
    }
    
    session["vault"]["entries"].append(entry)
    save_vault(session["key"], session["vault"])

    return {"message": "Entrada criada", "id": entry["id"]}

@login_router.delete("/entries/delete/{entry_id}")
def delete_entry(entry_id,token:str = Header(...)):
    if session["token"] != token:
        return HTTPException(status_code=401, detail="Sessão expirada")
    entries = session["vault"]["entries"]
    filtro = [e for e in entries if e["id"]!= entry_id]
    
    if len(filtro) == len(entries):
        raise HTTPException(status_code=404, detail="Dados não encontrados")
    
    session["vault"]["entries"] = filtro
    save_vault(session["key"], session["vault"])
    return {"message": "Entrada deletada"}

@login_router.patch("/update_entry/{entry_id}")
def update_entry(entry_id: str, body: Entry, token: str = Header(...)):
    if session["token"] != token:
        raise HTTPException(status_code=401, detail="Sessão expirada")

    entries = session["vault"]["entries"]

    for entry in entries:
        if entry["id"] == entry_id:
            entry["service"] = body.service
            entry["login"] = body.login
            entry["password"] = body.password
            save_vault(session["key"], session["vault"])
            return {"message": "Entrada atualizada"}

    raise HTTPException(status_code=404, detail="Entrada não encontrada")


@login_router.get("/generate")
def generate_password(tamanho: int,letras:bool = True,numeros: bool=True,especiais:bool = True):
    password=gerador(tamanho,letras,numeros,especiais)
    return {"password": password}