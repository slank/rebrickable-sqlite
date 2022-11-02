create table if not exists inventory_minifigs (
  minifig_inventory_id int,
  minifig_id varchar(16),
  quantity smallint,
  foreign key(minifig_inventory_id) references minifig_inventories(id),
  foreign key(minifig_id) references minifigs(id),
  primary key (minifig_inventory_id, minifig_id)
);
delete from inventory_minifigs;

pragma foreign_key = 1;
.mode csv
.import tables/inventory_minifigs.csv inventory_minifigs