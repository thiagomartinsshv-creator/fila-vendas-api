# Como Publicar no GitHub

## Opção 1: Pelo Terminal do Replit (Mais Fácil)

1. Abra o **Shell** do Replit (painel inferior)
2. Execute os comandos:

```bash
cd artifacts/sales-queue-api

git init
git add -A
git commit -m "feat: API de fila de atendimento - Lista da Vez v1.0"

# Substitua <SEU_TOKEN> pelo seu GitHub PAT
git remote add origin https://<SEU_TOKEN>@github.com/thiagomartinsshv-creator/fila-vendas-api.git
git branch -M main
git push -u origin main
```

## Opção 2: Pelo seu computador

1. Baixe o arquivo `fila-vendas-api.tar.gz` (apresentado acima)
2. Extraia em uma pasta:
```bash
tar -xzf fila-vendas-api.tar.gz
cd fila-vendas-api
```
3. Envie para o GitHub:
```bash
git init
git add -A
git commit -m "feat: API de fila de atendimento - Lista da Vez v1.0"
git remote add origin https://github.com/thiagomartinsshv-creator/fila-vendas-api.git
git branch -M main
git push -u origin main
```

## Como criar um GitHub PAT (Token)

1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token (classic)"**
3. Dê um nome (ex: "Fila Vendas API")
4. Marque a permissão **repo** (acesso total aos repositórios)
5. Clique em **Generate token**
6. **Copie o token** (só aparece uma vez!)

## Arquivos do projeto

```
fila-vendas-api/
├── main.py          # Endpoints da API
├── database.py      # Configuração SQLite
├── models.py        # Tabelas do banco
├── schemas.py       # Validação de dados
├── requirements.txt # Dependências
├── README.md        # Documentação
├── APRESENTACAO.md  # Roteiro de 10 minutos
└── .gitignore       # Ignora arquivos desnecessários
```

---

**Pronto!** Seu projeto está no GitHub. 

Para executar localmente:
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Acesse: http://localhost:8000/docs
