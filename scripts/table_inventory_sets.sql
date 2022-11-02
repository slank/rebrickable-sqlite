create table if not exists inventory_sets (
  set_inventory_id int,
  set_id varchar(16),
  quantity smallint,
  foreign key(set_inventory_id) references set_inventories(id),
  foreign key(set_id) references sets(id),
  primary key (set_inventory_id, set_id)
);
delete from inventory_sets;

pragma foreign_key = 1;
.mode csv
.import tables/inventory_sets.csv inventory_sets