-- 🎯 SOLUÇÃO DEFINITIVA: Sincronizar Cache do Supabase e Colunas

-- 1. Garantir que todas as colunas existem na tabela de posts
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS permalink TEXT;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS shares INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS conversions INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS saves INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS views INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS likes INTEGER DEFAULT 0;
ALTER TABLE leads_ai_posts ADD COLUMN IF NOT EXISTS comments INTEGER DEFAULT 0;

-- 2. Garantir que as colunas existem na tabela de brands
ALTER TABLE leads_ai_brands ADD COLUMN IF NOT EXISTS dream_point TEXT;
ALTER TABLE leads_ai_brands ADD COLUMN IF NOT EXISTS dream_client TEXT;
ALTER TABLE leads_ai_brands ALTER COLUMN user_id DROP NOT NULL;

-- 3. Resetar Cache do PostgREST (O 'Pulo do Gato')
-- Execute este comando para forçar o Supabase a ler o novo esquema imediatamente
NOTIFY pgrst, 'reload schema';

-- 4. Liberar Permissões (Caso o reset tenha limpado)
DROP POLICY IF EXISTS "Allow anonymous inserts" ON leads_ai_brands;
CREATE POLICY "Allow anonymous inserts" ON leads_ai_brands FOR INSERT WITH CHECK (true);
DROP POLICY IF EXISTS "Allow public select" ON leads_ai_brands;
CREATE POLICY "Allow public select" ON leads_ai_brands FOR SELECT USING (true);
DROP POLICY IF EXISTS "Allow public update" ON leads_ai_brands;
CREATE POLICY "Allow public update" ON leads_ai_brands FOR UPDATE USING (true);

DROP POLICY IF EXISTS "Allow anonymous post inserts" ON leads_ai_posts;
CREATE POLICY "Allow anonymous post inserts" ON leads_ai_posts FOR INSERT WITH CHECK (true);
DROP POLICY IF EXISTS "Allow public post select" ON leads_ai_posts;
CREATE POLICY "Allow public post select" ON leads_ai_posts FOR SELECT USING (true);
DROP POLICY IF EXISTS "Allow public post update" ON leads_ai_posts;
CREATE POLICY "Allow public post update" ON leads_ai_posts FOR UPDATE USING (true);
