#!/bin/bash
# =============================================================
# Script para enviar o projeto para o GitHub
# =============================================================
# 1. Acesse https://github.com/settings/tokens
# 2. Crie um token (classic) com permissão "repo"
# 3. Substitua <SEU_TOKEN> abaixo pelo token gerado
# 4. Execute: bash GUARDAR_NO_GITHUB.sh
# =============================================================

REPO_URL="https://github.com/thiagomartinsshv-creator/fila-vendas-api.git"
TOKEN="<SEU_TOKEN>"

# URL com token para autenticação
AUTH_URL="https://${TOKEN}@github.com/thiagomartinsshv-creator/fila-vendas-api.git"

# Inicializa o repositório git (se ainda não estiver)
git init
git branch -M main

# Adiciona os arquivos do projeto
find . -maxdepth 1 -type f \( -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.sh" \) -exec git add {} \;

# Commit inicial
git commit -m "feat: API de fila de atendimento — Lista da Vez"

# Conecta ao repositório remoto e faz o push
# (substitua o token antes de executar)
git remote add origin "$AUTH_URL" 2>/dev/null || git remote set-url origin "$AUTH_URL"
git push -u origin main

echo "Projeto enviado com sucesso para $REPO_URL"
