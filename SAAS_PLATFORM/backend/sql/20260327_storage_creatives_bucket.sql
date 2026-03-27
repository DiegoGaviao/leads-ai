-- =============================================================================
-- Leads AI — cópia de referência (já aplicada via Supabase migrations).
-- Fonte canônica: ../supabase/migrations/20260327140000_leads_ai_creatives_bucket.sql
-- Projeto: iatbzoowdgzytolcrvbe
-- =============================================================================

-- 1) Bucket (leitura pública para e-mail / front exibirem <img src="...">)
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'leads-ai-creatives',
  'leads-ai-creatives',
  true,
  10485760, -- 10 MB por arquivo
  ARRAY['image/png', 'image/jpeg', 'image/jpg', 'image/webp']::text[]
)
ON CONFLICT (id) DO UPDATE SET
  public = EXCLUDED.public,
  file_size_limit = EXCLUDED.file_size_limit,
  allowed_mime_types = EXCLUDED.allowed_mime_types;

-- 2) Qualquer pessoa pode LER objetos deste bucket (URL pública)
DROP POLICY IF EXISTS "leads_ai_creatives_public_read" ON storage.objects;
CREATE POLICY "leads_ai_creatives_public_read"
ON storage.objects
FOR SELECT
TO public
USING (bucket_id = 'leads-ai-creatives');

-- 3) Backend com service_role ignora RLS e faz upload sem policy extra.
--    Se você usar SOMENTE a anon key no backend, descomente e ajuste (não recomendado):
-- DROP POLICY IF EXISTS "leads_ai_creatives_service_insert" ON storage.objects;
-- CREATE POLICY "leads_ai_creatives_service_insert"
-- ON storage.objects
-- FOR INSERT TO authenticated
-- WITH CHECK (bucket_id = 'leads-ai-creatives');
