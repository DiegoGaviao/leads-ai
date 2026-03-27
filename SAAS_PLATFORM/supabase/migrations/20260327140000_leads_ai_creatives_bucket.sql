-- Leads AI — bucket público para criativos (OpenAI → Storage)
-- Projeto: iatbzoowdgzytolcrvbe | env: LEADS_AI_CREATIVES_BUCKET (default leads-ai-creatives)

INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
  'leads-ai-creatives',
  'leads-ai-creatives',
  true,
  10485760,
  ARRAY['image/png', 'image/jpeg', 'image/jpg', 'image/webp']::text[]
)
ON CONFLICT (id) DO UPDATE SET
  public = EXCLUDED.public,
  file_size_limit = EXCLUDED.file_size_limit,
  allowed_mime_types = EXCLUDED.allowed_mime_types;

DROP POLICY IF EXISTS "leads_ai_creatives_public_read" ON storage.objects;
CREATE POLICY "leads_ai_creatives_public_read"
ON storage.objects
FOR SELECT
TO public
USING (bucket_id = 'leads-ai-creatives');
