
-- Adicionar colunas extras conforme o novo fluxo do PDF
ALTER TABLE leads_ai_brands ADD COLUMN IF NOT EXISTS dream_point TEXT;
ALTER TABLE leads_ai_brands ADD COLUMN IF NOT EXISTS dream_client TEXT;

-- Garantir que posts manuais possam ser inseridos sem external_id obrigatório
ALTER TABLE leads_ai_posts ALTER COLUMN external_id DROP NOT NULL;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS permalink TEXT;
