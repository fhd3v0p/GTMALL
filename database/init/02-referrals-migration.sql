-- GTM Supabase: referrals migration with invited_by_referral_code and trigger
-- Выполняйте в Supabase SQL Editor или через миграции

begin;

-- 1) Добавляем колонку, чей код использовали
alter table if exists public.referrals
  add column if not exists invited_by_referral_code varchar(20);

-- 2) (Опционально) FK на users.referral_code, если он уникален
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conrelid = 'public.referrals'::regclass
      and conname = 'referrals_invited_by_code_fk'
  ) then
    alter table public.referrals
      add constraint referrals_invited_by_code_fk
      foreign key (invited_by_referral_code)
      references public.users (referral_code)
      on update cascade
      on delete restrict;
  end if;
end
$$;

-- 3) Снимаем старый unique(referral_code), если мешает логировать несколько событий
do $$
begin
  if exists (
    select 1 from pg_constraint
    where conrelid = 'public.referrals'::regclass
      and conname = 'referrals_referral_code_key'
  ) then
    alter table public.referrals
      drop constraint referrals_referral_code_key;
  end if;
end
$$;

-- 4) Гарантируем уникальность приглашённого по telegram_id
do $$
begin
  if not exists (
    select 1 from pg_constraint
    where conrelid = 'public.referrals'::regclass
      and conname = 'referrals_unique_invited'
  ) then
    alter table public.referrals
      add constraint referrals_unique_invited unique (telegram_id);
  end if;
end
$$;

-- Индексы
create index if not exists idx_referrals_invited_by_code
  on public.referrals (invited_by_referral_code);

create index if not exists idx_referrals_telegram_id
  on public.referrals (telegram_id);

-- 5) Триггер: начисление билета пригласителю (users.referral_tickets, users.total_tickets)
create or replace function public.trg_award_inviter_ticket()
returns trigger
language plpgsql
as $$
declare
  inviter_id bigint;
begin
  -- Находим пригласителя по его реф.коду
  select u.telegram_id
    into inviter_id
  from public.users u
  where u.referral_code = new.invited_by_referral_code;

  if inviter_id is null then
    return new;
  end if;

  -- Защита от самоприглашения
  if new.telegram_id = inviter_id then
    return new;
  end if;

  -- Начисляем 1 билет пригласителю (уникальность обеспечивается уникальностью telegram_id в referrals)
  update public.users
  set referral_tickets = coalesce(referral_tickets, 0) + 1,
      total_tickets    = coalesce(total_tickets, 0) + 1
  where telegram_id = inviter_id;

  return new;
end;
$$;

drop trigger if exists referrals_after_insert_award on public.referrals;

create trigger referrals_after_insert_award
after insert on public.referrals
for each row
execute function public.trg_award_inviter_ticket();

-- 6) (Опционально) RPC для записи реферала ботом
create or replace function public.add_referral(p_invited_id bigint, p_ref_code text)
returns void
language sql
as $$
  insert into public.referrals (telegram_id, referral_code, invited_by_referral_code)
  values (p_invited_id, p_ref_code, p_ref_code)
  on conflict (telegram_id) do nothing;
$$;

commit;

