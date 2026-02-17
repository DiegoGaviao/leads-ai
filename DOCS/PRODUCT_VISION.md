# 💎 LEADS AI: Visão do Produto & Roadmap (SaaS)

**Slogan:** "Conteúdo com Alma e Estratégia. Chega de Robôs."
**Público-Alvo Inicial:** Terapeutas, Mentoras e Criadores de Conteúdo Profundo ("High Ticket").
**Diferencial:** Deep Personalization (O sistema "aprende" a voz da pessoa melhor que ela mesma).

---

## 🏗️ Arquitetura do Sistema (SaaS V1)

O sistema será dividido em 3 módulos principais:

### 1. 🧠 O CÉREBRO (Identity Engine)
Não é só um chat. É onde a "alma" da marca vive.
- **Input:** Usuário preenche "Quem Sou Eu", "Quem é meu Cliente (Persona)", "Meu Método (Ex: C.A.S.A)".
- **Processamento:** O sistema gera um `System Prompt` gigante e fixo para aquele usuário.
- **Impacto:** Nunca mais o usuário precisa explicar quem ele é. O sistema já sabe que a Karina "não fala palavrão" e "gosta de café".

### 2. ⚡ A FÁBRICA (Content Generator)
A interface de operação diária. Simples, Zen, Focada.
- **Modo "Tenho uma Ideia":** Usuário digita "Falar sobre birra no mercado". -> Sistema cospe Roteiro de Reels + Legenda + Stories.
- **Modo "Estou sem Ideias":** Sistema olha os pilares e sugere: "Faz tempo que você não fala sobre 'Aliança'. Que tal um post sobre conexão pai e filho?"
- **Modo "Multiplicador":** Cola um texto ou link de vídeo -> Vira 5 formatos diferentes.

### 3. 📊 O ANALISTA (Feedback Loop)
Usa o script Python `robo_analista.py` que já temos.
- Conecta no Instagram.
- Diz: "Seus posts sobre 'Dor' estão engajando 20% mais que 'Dicas'. Foca na Dor semana que vem."
- O sistema se retroalimenta dessa análise.

---

## 🛠️ Stack Tecnológico (O que vamos usar)
- **Frontend:** React + Vite + Tailwind (Estética "Clean/Notion-like"). Nada de cores neon de marketing digital. Branco, preto, tipografia elegante.
- **Backend:** FastAPI (Python). É a linguagem nativa da IA.
- **AI Core:** OpenAI GPT-4o ou Anthropic Claude 3.5 (Melhor para texto humano).
- **Banco de Dados:** Supabase (Para salvar os "Cérebros" dos usuários).

---

## 📅 Roadmap de Desenvolvimento

### Fase 1: "Dogfooding" (Uso Interno - Fev/26)
- [ ] Criar Interface Web Simples (React) rodando local.
- [ ] Conectar ao script `robo_analista.py` e `ESTRATEGIA_SUPREMA`.
- [ ] Karina usa todo dia e valida: "Isso soa como eu?".

### Fase 2: "Private Beta" (Mar/26)
- [ ] Implementar Login Multi-usuário (Supabase Auth).
- [ ] Criar o "Onboarding" onde o usuário cadastra sua Persona.
- [ ] Liberar para 5 amigas da Karina testarem de graça em troca de feedback.

### Fase 3: "Public Launch" (Abr/26)
- [ ] Integração com Stripe/MercadoPago.
- [ ] Landing Page focada em "Paz para Produtores de Conteúdo".
- [ ] Preço: R$ 49/mês (Entrada) a R$ 197/mês (Pro com Análise).

---

## ⚠️ Regra de Ouro da Engenharia
**Não comece do zero.** Temos o `05_BOILERPLATE`.
Amanhã, vamos copiar o Boilerplate para `LEADS_AI/SAAS` e começar a codar a Tela 1 (O Chat).
