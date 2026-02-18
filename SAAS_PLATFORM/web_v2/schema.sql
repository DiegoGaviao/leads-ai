
-- Tabela de Clientes (Lids Capturados)
create table public.clients (
  id uuid not null default gen_random_uuid (),
  created_at timestamp with time zone not null default now(),
  instagram_handle text not null,
  email text not null,
  whatsapp text null,
  status text null default 'new'::text,
  constraint clients_pkey primary key (id),
  constraint clients_instagram_handle_key unique (instagram_handle)
) tablespace pg_default;

-- Tabela de Briefings (Estratégia Profunda)
create table public.briefings (
  id uuid not null default gen_random_uuid (),
  client_id uuid not null,
  created_at timestamp with time zone not null default now(),
  updated_at timestamp with time zone null,
  mission text null,
  tone_voice text null,
  authority_proof text null,
  big_promise text null,
  enemy text null,
  pain_point text null,
  desire_point text null,
  method_name text null,
  dream_client text null,
  constraint briefings_pkey primary key (id),
  constraint briefings_client_id_key unique (client_id),
  constraint briefings_client_id_fkey foreign key (client_id) references clients (id) on delete cascade
) tablespace pg_default;

-- Tabela de Posts Analisados
create table public.analyzed_posts (
  id uuid not null default gen_random_uuid (),
  client_id uuid not null,
  created_at timestamp with time zone not null default now(),
  post_link text not null,
  views integer null default 0,
  likes integer null default 0,
  saves integer null default 0,
  shares integer null default 0,
  comments integer null default 0,
  status text null default 'pending'::text,
  analysis_result jsonb null,
  constraint analyzed_posts_pkey primary key (id),
  constraint analyzed_posts_client_id_fkey foreign key (client_id) references clients (id) on delete cascade
) tablespace pg_default;
