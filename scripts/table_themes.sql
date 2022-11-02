create table if not exists themes (
  id smallint primary key,
  name varchar(64),
  parent_id smallint
);
delete from themes;

.mode csv
.import tables/themes.csv themes