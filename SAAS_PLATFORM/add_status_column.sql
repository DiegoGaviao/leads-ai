-- Adicionar coluna de status na tabela antiga para evitar re-processamento
ALTER TABLE briefings ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending';

-- Adicionar coluna de status na tabela nova se necessário (leads_ai_brands)
ALTER TABLE leads_ai_brands ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'pending';
