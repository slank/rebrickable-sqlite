create table if not exists inventory_parts (
  inventory_id int,
  part_id varchar(16),
  color_id smallint,
  quantity smallint,
  is_spare varchar(1),
  img_url varchar(300),
  foreign key(inventory_id) references inventories(id),
  foreign key(color_id) references colors(id),
  foreign key(part_id) references parts(id),
  primary key (inventory_id, part_id, color_id, is_spare)
);
delete from inventory_parts;

pragma foreign_key = 1;
.mode csv
.import tables/inventory_parts.csv inventory_parts