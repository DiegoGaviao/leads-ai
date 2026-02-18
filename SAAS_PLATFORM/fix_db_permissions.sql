
-- 🛠️ CORREÇÃO DEFINITIVA DO BANCO (LEADS AI)
-- Este script resolve: RLS, User_ID obrigatório e falta de constraint única.

-- 1. Desabilitar RLS para permitir onboarding sem login (MVP/Free)
ALTER TABLE leads_ai_brands DISABLE ROW LEVEL SECURITY;
ALTER TABLE leads_ai_posts DISABLE ROW LEVEL SECURITY;
ALTER TABLE leads_ai_strategies DISABLE ROW LEVEL SECURITY;

-- 2. Tornar o user_id opcional (estava obrigatório e bloqueando inserts)
ALTER TABLE leads_ai_brands ALTER COLUMN user_id DROP NOT NULL;

-- 3. Adicionar constraint única para o instagram_handle (Necessário para o Upsert funcionar)
-- Primeiro remove se já existir para não dar erro
ALTER TABLE leads_ai_brands DROP CONSTRAINT IF EXISTS leads_ai_brands_instagram_handle_key;
ALTER TABLE leads_ai_brands ADD CONSTRAINT leads_ai_brands_instagram_handle_key UNIQUE (instagram_handle);

-- 4. Criar a tabela de estratégias se ela estiver com nome diferente (Sincronização com o Worker)
CREATE TABLE IF NOT EXISTS leads_ai_strategies (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  brand_id uuid REFERENCES leads_ai_brands(id) ON DELETE CASCADE,
  persona_markdown TEXT,
  strategy_markdown TEXT,
  scripts_json JSONB,
  created_at TIMESTAMPTZ DEFAULT now()
);
