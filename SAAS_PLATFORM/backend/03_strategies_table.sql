
-- Tabela para guardar a Estratégia e Roteiros Gerados pela IA
create table public.strategies (
  id uuid not null default gen_random_uuid (),
  client_id uuid not null,
  created_at timestamp with time zone not null default now(),
  
  -- Aqui fica o JSON completo (Persona, Pilares, Roteiros)
  content_json jsonb not null,
  
  -- Metadados
  model_used text null default 'gpt-4o-mini',
  status text default 'completed',

  constraint strategies_pkey primary key (id),
  constraint strategies_client_id_key unique (client_id), -- Uma estratégia por cliente por enquanto
  constraint strategies_client_id_fkey foreign key (client_id) references clients (id) on delete cascade
) tablespace pg_default;
