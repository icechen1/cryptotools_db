drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  nick text not null,
  public_key text not null
);