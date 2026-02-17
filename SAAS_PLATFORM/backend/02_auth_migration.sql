-- Adicionar colunas para suporte a OAuth do Facebook
-- Será usado pelo Agent 01 (Scout) e Agent 03 (Sentinel)

ALTER TABLE leads_ai_brands 
ADD COLUMN IF NOT EXISTS facebook_access_token TEXT,
ADD COLUMN IF NOT EXISTS facebook_token_expires_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS instagram_business_id TEXT;  -- 1784...

-- Criar índice para buscas rápidas do Sentinel
CREATE INDEX IF NOT EXISTS idx_leads_ai_brands_token ON leads_ai_brands(facebook_access_token) WHERE facebook_access_token IS NOT NULL;
