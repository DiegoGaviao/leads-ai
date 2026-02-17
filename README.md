# 🤖 Leads AI - Central de Operações

**Projeto:** Automação de Estratégia de Conteúdo Baseada em Dados
**Status:** Em Organização / Reestruturação
**Versão:** 2.0 (SaaS Multi-Tenant em Construção)

## 📁 Estrutura de Pastas

1.  **`SAAS_PLATFORM`**: O Frontend e Aplicação Web.
    *   `web_v1`: O site estático recuperado (Landing Page + Formulário HTML). Use este como referência visual.
    *   `frontend` (Futuro): Onde vamos construir o App React.
    *   `backend` (Futuro): API FastAPI/Node.

2.  **`WORKERS`**: O Cérebro Python (Backend de Processamento).
    *   `robo_analista.py`: O script principal que lê planilhas e gera estratégias.
    *   `app_karina.py`: O gerador de prompts (Streamlit).
    *   `CLIENTES/`: Onde saem os resultados (Markdown, JSON).
    *   `.env`: Configure suas chaves de API aqui (NÃO APAGUE).

3.  **`DOCS`**: Documentação Estratégica.
    *   `CONTEXTO/`: Briefings e Estratégias salvas.
    *   `ROTEIROS/`: Exemplos de roteiros gerados.
    *   `PRODUCT_VISION.md`: A visão de longo prazo.

4.  **`DADOS`**: Arquivos brutos (CSV) para análise local.

## 🚀 Como Rodar (Localmente)

### 1. Configurar Ambiente
```bash
cd WORKERS
pip install -r requirements.txt
# Edite o arquivo .env com suas chaves (OpenAI, DeepSeek)
```

### 2. Rodar o Robô Analista
```bash
python robo_analista.py
```
*Ele ficará escutando a planilha configurada em `CLIENTES/banco_de_links.json`.*

### 3. Rodar o Gerador de Prompts (Karina AI)
```bash
streamlit run app_karina.py
```

---
**Observação Importante:**
Todo o código legado de "Facebook Login" que rodava no servidor antigo não está presente aqui. Estamos reconstruindo a integração com base no `formulario.html` recuperado e na lógica moderna de API.
