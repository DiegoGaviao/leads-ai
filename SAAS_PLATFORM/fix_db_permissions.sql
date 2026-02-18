-- 🛠️ CORREÇÃO URGENTE: Permitir salvar marcas sem exigir login prévio (user_id opcional)
ALTER TABLE leads_ai_brands ALTER COLUMN user_id DROP NOT NULL;

-- 🔓 LIBERAR RLS: Permitir que qualquer um insira dados (Onboarding Livre)
DROP POLICY IF EXISTS "Users can insert their own brand" ON leads_ai_brands;
CREATE POLICY "Allow anonymous inserts" ON leads_ai_brands FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public select" ON leads_ai_brands FOR SELECT USING (true);

DROP POLICY IF EXISTS "Users can manage their own posts via brand" ON leads_ai_posts;
CREATE POLICY "Allow anonymous post inserts" ON leads_ai_posts FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public post select" ON leads_ai_posts FOR SELECT USING (true);

-- 📊 EXPANSÃO DE MÉTRICAS: Adicionar colunas faltantes para posts manuais
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS shares INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS conversions INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS comments INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS saves INTEGER DEFAULT 0; -- Garantir que existe
