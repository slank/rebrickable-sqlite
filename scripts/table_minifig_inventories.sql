create table if not exists minifig_inventories (
  id int primary key,
  revision smallint,
  minifig_id varchar(16),
  foreign key(minifig_id) references minifigs(id)
);
delete from minifig_inventories;

pragma foreign_key = 1;
.mode csv
.import tables/minifig_inventories.csv minifig_inventories