create table if not exists colors (
  id smallint primary key,
  name varchar(64),
  rgb varchar(6),
  is_trans varchar(1)
);
delete from colors;

.mode csv
.import tables/colors.csv colors