-- 🔨 CORREÇÃO DE ÍNDICES: Resolver erro de conflito (Unique Constraint)

-- 1. Garantir que instagram_handle seja ÚNICO na tabela de brands
-- (Isso permite que o 'on_conflict="instagram_handle"' funcione)
ALTER TABLE leads_ai_brands DROP CONSTRAINT IF EXISTS leads_ai_brands_instagram_handle_key;
ALTER TABLE leads_ai_brands ADD CONSTRAINT leads_ai_brands_instagram_handle_key UNIQUE (instagram_handle);

-- 2. Garantir que external_id seja ÚNICO na tabela de posts
-- (Isso permite que o 'on_conflict="external_id"' funcione para posts manuais)
ALTER TABLE leads_ai_posts DROP CONSTRAINT IF EXISTS leads_ai_posts_external_id_key;
ALTER TABLE leads_ai_posts ADD CONSTRAINT leads_ai_posts_external_id_key UNIQUE (external_id);

-- 3. Resetar o Cache novamente por precaução
NOTIFY pgrst, 'reload schema';

-- 4. Re-aplicar Políticas de Acesso
ALTER TABLE leads_ai_brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads_ai_posts ENABLE ROW LEVEL SECURITY;

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
