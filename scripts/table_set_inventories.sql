create table if not exists set_inventories (
  id int primary key,
  revision smallint,
  set_id varchar(16),
  foreign key(set_id) references sets(id)
);
delete from set_inventories;

.mode csv
.import tables/set_inventories.csv set_inventories