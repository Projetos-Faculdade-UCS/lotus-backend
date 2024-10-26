# LÓTUS - Backend

Este repositório contém o código do backend para o sistema de gerenciamento de ativos de TI Lótus, que permite o registro e controle de equipamentos como computadores, impressoras, monitores, e licenças de software, além de informações relacionadas, como localização atual e responsável pelo ativo.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python
- **Framework Web**: Django Rest Framework (DRF)
- **Banco de Dados**: PostgreSQL
- **Autenticação**: JWT (JSON Web Tokens)
- **Docker**: Para containerização do projeto

## 📌 Requisitos

Antes de iniciar, verifique se você tem os seguintes softwares instalados:

- [Docker](https://www.docker.com/products/docker-desktop) 
- [Git](https://git-scm.com/)

⚠️ Para o correto funcionamento do projeto é necessário  a instalação da ferramenta Docker Compose, verifique a instalação no seu SO.

## ⬇️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Projetos-Faculdade-UCS/lotus-backend.git
cd lotus-backend
```

### 2. Configure o arquivo .env
Crie um arquivo .env com as variáveis necessárias seguindo o padrão do arquivo [.env-EXAMPLE](app/config/.env-EXAMPLE). **Certifique-se de preencher todas as variáveis exigidas.**

### 3. Construa a imagem docker 
Na raiz do projeto, execute o seguinte comando para construir os containers com base no arquivo [docker-compose.yml](docker-compose.yml):
```bash
docker compose build
```

### 4. Inicie os containers
Na raiz do projeto, execute em seu terminal:
```bash
docker compose up
```

### 5. Acesse a API
Acesse em seu navegador: [http://localhost:8000](http://localhost:8000).


## 🚚 Endpoints
[Em construção...]