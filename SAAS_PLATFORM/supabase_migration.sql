-- -------------------------------------------------------------
-- 🚀 LEADS AI V2 - MIGRATION SCRIPT
-- Este script cria a infraestrutura de tabelas no Supabase
-- para suportar o ecossistema de agentes do Leads AI.
-- -------------------------------------------------------------

-- 1. Tabela de Marcas (Identidade e Alma)
-- Aqui o Agent 02 guarda o que aprendeu no Onboarding.
CREATE TABLE IF NOT EXISTS leads_ai_brands (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id uuid REFERENCES auth.users NOT NULL, -- Link com Auth do Supabase
  instagram_handle TEXT,
  email TEXT,
  mission TEXT,
  enemy TEXT, -- O inimigo comum
  dor_cliente TEXT,
  method_name TEXT, -- Nome do Método (ex: CASA)
  tone_voice_matrix JSONB, -- { "nao_sou": "...", "sou": "..." }
  created_at TIMESTAMPTZ DEFAULT now()
);

-- RLS: Usuário só vê sua marca
ALTER TABLE leads_ai_brands ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can insert their own brand" ON leads_ai_brands
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can select their own brand" ON leads_ai_brands
  FOR SELECT USING (auth.uid() = user_id);

-- 2. Tabela de Posts (Dados Brutos para o Analista)
-- Aqui o Agent 01 (Scout) joga os dados coletados.
CREATE TABLE IF NOT EXISTS leads_ai_posts (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  brand_id uuid REFERENCES leads_ai_brands(id) ON DELETE CASCADE,
  external_id TEXT, -- ID do post no Instagram (se houver)
  tema TEXT, -- Título ou descritivo curto
  views INTEGER DEFAULT 0,
  likes INTEGER DEFAULT 0,
  saves INTEGER DEFAULT 0,
  comments INTEGER DEFAULT 0,
  ai_transcription TEXT, -- Texto extraído do vídeo (Legenda ou Áudio)
  posted_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- RLS: Usuário só vê posts da sua marca
ALTER TABLE leads_ai_posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own posts via brand" ON leads_ai_posts
  FOR ALL USING (
    brand_id IN (
      SELECT id FROM leads_ai_brands WHERE user_id = auth.uid()
    )
  );

-- 3. Tabela de Estratégias (Output do Conselho)
-- Aqui o Agent 05 (Conselho) guarda o resultado final.
CREATE TABLE IF NOT EXISTS leads_ai_strategies (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  brand_id uuid REFERENCES leads_ai_brands(id) ON DELETE CASCADE,
  persona_markdown TEXT, -- Texto rico gerado pelo Mistral
  strategy_markdown TEXT, -- Texto rico com a estratégia
  scripts_json JSONB, -- Lista dos 5 roteiros gerados
  created_at TIMESTAMPTZ DEFAULT now()
);

-- RLS
ALTER TABLE leads_ai_strategies ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own strategies via brand" ON leads_ai_strategies
  FOR ALL USING (
    brand_id IN (
      SELECT id FROM leads_ai_brands WHERE user_id = auth.uid()
    )
  );

-- Bônus: View para facilitar debug
CREATE OR REPLACE VIEW leads_ai_dashboard_view AS
SELECT 
  b.instagram_handle,
  count(p.id) as total_posts,
  avg(p.views) as avg_views,
  count(s.id) as total_strategies
FROM leads_ai_brands b
LEFT JOIN leads_ai_posts p ON b.id = p.brand_id
LEFT JOIN leads_ai_strategies s ON b.id = s.brand_id
GROUP BY b.id, b.instagram_handle;
