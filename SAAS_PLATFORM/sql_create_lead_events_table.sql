-- Append-only log para monitoramento de leads e RMKT.
-- Execute no Supabase SQL Editor.

create extension if not exists pgcrypto;

create table if not exists public.leads_ai_lead_events (
  id uuid primary key default gen_random_uuid(),
  brand_id uuid null references public.leads_ai_brands(id) on delete set null,
  event_type text not null,
  email text null,
  instagram_handle text null,
  plan text null,
  event_payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_lead_events_created_at
  on public.leads_ai_lead_events(created_at desc);

create index if not exists idx_lead_events_brand_id
  on public.leads_ai_lead_events(brand_id);

create index if not exists idx_lead_events_type
  on public.leads_ai_lead_events(event_type);

-- Se RLS estiver ativa no projeto, deixe aberto para uso server-to-server via API key atual.
alter table public.leads_ai_lead_events enable row level security;

drop policy if exists "lead_events_select_open" on public.leads_ai_lead_events;
create policy "lead_events_select_open"
on public.leads_ai_lead_events
for select
to anon, authenticated
using (true);

drop policy if exists "lead_events_insert_open" on public.leads_ai_lead_events;
create policy "lead_events_insert_open"
on public.leads_ai_lead_events
for insert
to anon, authenticated
with check (true);
