# PassWorld

PassWorld é um gerenciador de senhas desenvolvido para armazenar credenciais de forma segura utilizando criptografia moderna e autenticação baseada em sessão.

Diferente de aplicações que armazenam dados diretamente em bancos de dados tradicionais, o PassWorld utiliza um arquivo criptografado `.vault`, protegendo todas as informações através de uma senha mestra.

## Principais Funcionalidades

* Armazenamento seguro de credenciais
* Cadastro, edição e remoção de entradas
* Geração automática de senhas fortes
* Autenticação por token
* Sessão com expiração automática
* Arquivo de armazenamento criptografado
* API REST para gerenciamento dos dados

## Tecnologias Utilizadas

### Frontend

* Vue 3
* JavaScript
* Vite

### Backend

* Python
* FastAPI

### Segurança

* Argon2id para derivação de chave criptográfica
* AES-GCM para criptografia dos dados
* Salt aleatório para proteção contra ataques de dicionário
* Tokens de sessão gerados de forma segura
* Expiração automática de sessão

## Arquitetura

O sistema utiliza uma senha mestra para derivar uma chave criptográfica através do algoritmo Argon2id. Essa chave é utilizada para criptografar e descriptografar todo o conteúdo do arquivo `.vault`.

Nenhuma credencial é armazenada em texto puro no disco.

### Fluxo Simplificado

```text
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

## Destaques Técnicos

* Implementação de criptografia simétrica utilizando AES-256-GCM
* Persistência em arquivo `.vault` criptografado
* Escrita atômica para evitar corrupção de dados
* CRUD completo de credenciais via API REST
* Gerador de senhas configurável
* Gerenciamento de sessão com expiração automática

## Segurança

O PassWorld utiliza criptografia AES-256-GCM com chaves derivadas via Argon2id para proteger todas as credenciais armazenadas. A senha mestra nunca é salva em disco, os dados permanecem criptografados em um arquivo `.vault` e o sistema conta com autenticação por token, expiração automática de sessão e salvamento atômico para maior confiabilidade dos dados.

## O que Aprendi

Durante o desenvolvimento deste projeto foram explorados conceitos como:

* Desenvolvimento de APIs com FastAPI
* Criptografia aplicada
* Gerenciamento seguro de credenciais
* Autenticação baseada em token
* Manipulação segura de arquivos
* Arquitetura cliente-servidor
* Boas práticas de segurança


## Instalação

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

## Autor

Kauã — Estudante de Engenharia de Software e Desenvolvedor Full Stack.
