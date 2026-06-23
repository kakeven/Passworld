# 🔐 PassWorld

> Gerenciador de senhas com criptografia moderna e autenticação baseada em sessão.

PassWorld armazena credenciais de forma segura utilizando um arquivo criptografado `.vault`, ao invés de bancos de dados tradicionais. Todas as informações são protegidas por uma senha mestra, que nunca é salva em disco.

---

## ✨ Funcionalidades

- 🔒 Armazenamento seguro de credenciais
- ➕ Cadastro, edição e remoção de entradas
- 🎲 Geração automática de senhas fortes
- 🔑 Autenticação por token
- ⏱️ Sessão com expiração automática
- 🗂️ Arquivo de armazenamento criptografado
- 🌐 API REST para gerenciamento dos dados

---

## 🛠️ Tecnologias

| Camada | Stack |
|---|---|
| **Frontend** | Vue 3 · JavaScript · Vite |
| **Backend** | Python · FastAPI |

---

## 🏗️ Arquitetura

O sistema deriva uma chave criptográfica a partir da senha mestra usando **Argon2id**. Essa chave é então utilizada para criptografar e descriptografar todo o conteúdo do arquivo `.vault` com **AES-256-GCM**.

Nenhuma credencial é armazenada em texto puro no disco.

### Fluxo simplificado

```
Senha Mestra
     ↓
  Argon2id
     ↓
Chave Criptográfica
     ↓
  AES-GCM
     ↓
passworld.vault
```

---

## 🚀 Destaques Técnicos

- Criptografia simétrica com **AES-256-GCM**
- Persistência em arquivo `.vault` criptografado
- Escrita atômica para evitar corrupção de dados
- CRUD completo de credenciais via API REST
- Gerador de senhas configurável
- Gerenciamento de sessão com expiração automática

---

## 🛡️ Segurança

- Criptografia **AES-256-GCM** com chaves derivadas via **Argon2id**
- A senha mestra **nunca** é salva em disco
- Dados permanecem criptografados no arquivo `.vault`
- Autenticação por token
- Expiração automática de sessão
- Salvamento atômico para maior confiabilidade dos dados

---

## 📚 O que Aprendi

- Desenvolvimento de APIs com FastAPI
- Criptografia aplicada
- Gerenciamento seguro de credenciais
- Autenticação baseada em token
- Manipulação segura de arquivos
- Arquitetura cliente-servidor
- Boas práticas de segurança

---

## ⚙️ Instalação

### Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
npm install
npm run dev
```

---

## 👤 Autor

**Kauã** — Estudante de Engenharia de Software e Desenvolvedor Full Stack.
