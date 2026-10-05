-- Users table
create table users (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    email text unique not null,
    google_id text unique not null,
    created_at timestamptz default now()
);

-- Tasks table
create table tasks (
    id uuid primary key default gen_random_uuid(),
    title text not null,
    description text,
    assigned_to uuid references users(id),
    created_by uuid references users(id),
    status text default 'pending',
    due_date date,
    created_at timestamptz default now(),
    completed_at timestamptz
);