# 📡 AGENT 03: THE SENTINEL
> "Eu garanto a verdade."

## 📌 Missão
Um worker autônomo. Ele roda em background (Cron Job ou Worker Server) e vigia os perfis monitorados. Se algo novo for postado, ele acorda o Agent 01 (Scout) para atualizar o banco.

## 🛠️ Ferramentas
- Celery / Redis (Fila de Tarefas)
- Cron (Agendamento)
- Supabase Realtime (Notificações)

## 📥 Input
- Lista de Usuários Habilitados (Tabela `leads_ai_brands`)
- Intervalo de Checagem.

## 📤 Output
- Trigger de atualização para o Agent 01.
- Log de atividade (`activity_logs`).

## 🔄 Reutilização
Pode ser usado por:
- `Don't Call Me` (Para monitorar novas ligações no blacklist)
- `Strike3` (Para avisar quando o jogo começar)
