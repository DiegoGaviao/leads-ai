FROM python:3.11-slim

# Define diretório de trabalho app (raiz no container)
WORKDIR /app

# Copia os arquivos da pasta backend para dentro do container
# IMPORTANTE: Copiando SAAS_PLATFORM/backend para /app
COPY SAAS_PLATFORM/backend/ .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta
EXPOSE 8000

# Comando para rodar
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
