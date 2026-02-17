# 🌐 Check Frontend (Vite)

Siga este checklist quando for colocar no ar.

## 1. Variáveis de Ambiente (Vercel/Netlify)
Você precisa configurar a variável `VITE_API_URL` no painel de controle do seu host.
- **Key:** `VITE_API_URL`
- **Value:** `https://meu-saas-backend.onrender.com` (Sua URL do Backend no Render)

## 2. Configuração do `api_client.ts`
Certifique-se de que o arquivo `api_client.ts` dentro do seu projeto esteja usando `import.meta.env.VITE_API_URL` e não uma string hardcoded.

## 3. Comandos de Build
No Vercel/Netlify, use:
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm install`

## 4. Teste de CORS
Se o frontend der erro no console (`Access to XMLHttpRequest at '...' from origin '...' has been blocked by CORS policy`), vá no seu backend `main.py` e adicione a URL do seu frontend na lista `origins`.
Exemplo:
```python
origins = [
    "http://localhost:5173",
    "https://meu-novo-saas.vercel.app"  <-- ADICIONE ISSO
]
```
Redeploy o backend.
