-- 🛠️ CORREÇÃO DEFINITIVA (Pode rodar quantas vezes quiser)

-- 1. Tornar user_id opcional
ALTER TABLE leads_ai_brands ALTER COLUMN user_id DROP NOT NULL;

-- 2. Limpar e Criar Políticas para Brands (INSERT, SELECT, UPDATE)
DROP POLICY IF EXISTS "Allow anonymous inserts" ON leads_ai_brands;
DROP POLICY IF EXISTS "Allow public select" ON leads_ai_brands;
DROP POLICY IF EXISTS "Allow public update" ON leads_ai_brands;

CREATE POLICY "Allow anonymous inserts" ON leads_ai_brands FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public select" ON leads_ai_brands FOR SELECT USING (true);
CREATE POLICY "Allow public update" ON leads_ai_brands FOR UPDATE USING (true);

-- 3. Limpar e Criar Políticas para Posts (INSERT, SELECT, UPDATE)
DROP POLICY IF EXISTS "Allow anonymous post inserts" ON leads_ai_posts;
DROP POLICY IF EXISTS "Allow public post select" ON leads_ai_posts;
DROP POLICY IF EXISTS "Allow public post update" ON leads_ai_posts;

CREATE POLICY "Allow anonymous post inserts" ON leads_ai_posts FOR INSERT WITH CHECK (true);
CREATE POLICY "Allow public post select" ON leads_ai_posts FOR SELECT USING (true);
CREATE POLICY "Allow public post update" ON leads_ai_posts FOR UPDATE USING (true);

-- 4. Criar colunas de métricas se não existirem
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS shares INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS conversions INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS comments INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS saves INTEGER DEFAULT 0;
