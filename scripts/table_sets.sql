create table if not exists sets (
  id varchar(16) primary key,
  name varchar(300),
  year smallint,
  theme_id smallint,
  num_parts int,
  img_url varchar(300),
  foreign key(theme_id) references themes(id)
);
delete from sets;

pragma foreign_keys = 1;
.mode csv
.import tables/sets.csv sets