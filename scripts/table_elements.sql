create table if not exists elements (
  id varchar(16) primary key,
  part_id varchar(16),
  color_id smallint,
  foreign key(part_id) references parts(id),
  foreign key(color_id) references colors(id)
);
delete from elements;

pragma foreign_keys = 1;
.mode csv
.import tables/elements.csv elements