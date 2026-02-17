# 🕵️‍♂️ AGENT 01: THE SCOUT
> "Eu vejo tudo."

## 📌 Missão
Entrar no Instagram do cliente (via Selenium ou API), coletar métricas de performance (views, likes, saves) e capturar o conteúdo bruto (texto da legenda, transcrição de áudio).

## 🛠️ Ferramentas
- Selenium (Chrome Headless)
- OCR / Transcrição (Whisper)
- Pandas (Estruturação CSV)

## 📥 Input
- `@usuario_instagram`
- `cookies_sessao` (Opcional)

## 📤 Output
- Tabela `leads_ai_posts` atualizada no Supabase.
- Arquivos de mídia temporários (se necessário).

## 🔄 Reutilização
Pode ser usado por:
- `My Filmi` (Para analisar tendências de filmes)
- `Strike3` (Para monitorar posts de times rivais)
