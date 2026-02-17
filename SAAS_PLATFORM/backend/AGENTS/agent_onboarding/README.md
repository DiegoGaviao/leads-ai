# 📝 AGENT 02: THE ONBOARDER
> "Eu entendo a sua alma."

## 📌 Missão
Interagir diretamente com o usuário para capturar a essência da marca. Ele faz as perguntas difíceis (Missão, Inimigo, Dores) e estrutura as respostas para que os outros agentes (04, 05) possam consumir.

## 🛠️ Ferramentas
- Frontend Interativo (Dashboard)
- Supabase (Tabela `leads_ai_brands`)
- LLM (Mistral - Análise de Estilo)

## 📥 Input
- Formulário Web (React)
- Texto Livre do cliente.

## 📤 Output
- `JSONB` estruturado na tabela `leads_ai_brands`.
- Matriz de Tom de Voz (Sou x Não Sou).

## 🔄 Reutilização
Pode ser usado por:
- `Ordini Vita` (Para personalizar o tom da IA da clínica)
- `My Coach` (Para o usuário se apresentar ao treinador)
