# 🏗️ Boilerplate "Anti-Criptonita" (FastAPI + React + Supabase)

Este é o seu **Template Mestre**. 
O objetivo deste diretório NÃO é ser um projeto rodando, mas sim a **base copiável** para qualquer ideia nova.

## 🛑 Regra de Ouro
**ANTES de escrever qualquer linha de regra de negócio:**
1. Copie esta pasta para um novo diretório (ex: `meu-novo-saas`).
2. Crie o repo no GitHub.
3. Conecte no Render (Backend) e Vercel (Frontend).
4. **Faça o Deploy do "Hello World".**

Só depois que você ver o "Hello World" na URL de produção (ex: `meu-saas.onrender.com`), você tem permissão para começar a codar.

---

## 📂 Estrutura

### `/backend` (FastAPI)
Já configurado com:
- **CORS:** O erro chato que bloqueia o frontend de falar com o backend.
- **Health Check:** Rota `/` e `/health` para o Render saber que o app está vivo.
- **Structure:** Separação básica de `routes`, `services`, `utils`.
- **Dockerfile:** Para garantir que o ambiente de produção seja igual ao local (fim do "funciona na minha máquina").

### `/frontend` (React + Vite)
*Nota: Recomendo rodar `npm create vite@latest` e substituir os arquivos chave.*
Arquivos prontos aqui:
- **`api.ts`**: Cliente Axios configurado já pegando a URL da API das variáveis de ambiente.
- **`vite.config.ts`**: Configuração segura.

---

## 🚀 Como Iniciar um Novo Projeto

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```
