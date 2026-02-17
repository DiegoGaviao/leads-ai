# 🐳 Dockerfile Padrão (Leve e Rápido)

# 1. Imagem base limpa do Python 3.10
FROM python:3.10-slim

# 2. Configura o diretório de trabalho no container
WORKDIR /app

# 3. Copia o arquivo de dependências primeiro (cache layer)
COPY requirements.txt .

# 4. Instala as dependências (sem cache pra economizar espaço)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o código fonte do projeto
COPY . .

# 6. Expor a porta 8000 (O Render vai esperar essa porta ou mapear outra)
EXPOSE 8000

# 7. Comando para rodar a aplicação em produção
# O Render espera que a porta seja configurada via variável de ambiente PORT.
# O IP 0.0.0.0 é obrigatório para ser acessível externamente.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
