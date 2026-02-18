#!/bin/bash

# Define cores para saída
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Iniciando Script de Push para Leads AI V2...${NC}"

# Define o diretório do projeto
PROJECT_DIR="/Users/diegorufino/Desktop/DEV/2026/02 - Plano 2026/06_PROJETOS_ATIVOS/LEADS_AI 2"
REPO_URL="https://github.com/DiegoGaviao/leads-ai-v2.git"

# Navega para o diretório
cd "$PROJECT_DIR" || { echo -e "${RED}Erro: Diretório não encontrado!${NC}"; exit 1; }

# Verifica se git está inicializado
if [ ! -d ".git" ]; then
    echo -e "${GREEN}📦 Inicializando repositório Git...${NC}"
    git init
    git branch -M main
else
    echo -e "${GREEN}✅ Repositório Git já inicializado.${NC}"
fi

# Adiciona o remote se não existir
if ! git remote | grep -q "origin"; then
    echo -e "${GREEN}🌐 Adicionando remote origin...${NC}"
    git remote add origin "$REPO_URL"
else
    echo -e "${GREEN}✅ Remote origin já configurado.${NC}"
    # Atualiza URL caso tenha mudado
    git remote set-url origin "$REPO_URL"
fi

# Adiciona arquivos
echo -e "${GREEN}➕ Adicionando arquivos...${NC}"
git add .

# Commit
echo -e "${GREEN}💾 Realizando commit...${NC}"
git commit -m "Auto-deploy: Leads AI V2 Full Stack Update"

# Push
echo -e "${GREEN}⬆️ Enviando para o GitHub...${NC}"
git push -u origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Sucesso! Código enviado para $REPO_URL${NC}"
    echo -e "${GREEN}👉 Agora acesse o Render.com e conecte este repositório para o deploy automático.${NC}"
else
    echo -e "${RED}❌ Erro ao enviar para o GitHub. Verifique suas credenciais.${NC}"
fi
