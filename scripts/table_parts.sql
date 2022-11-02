create table if not exists parts (
  id varchar(16) primary key,
  name varchar(255),
  part_category_id smallint,
  part_material_id varchar(64),
  foreign key(part_category_id) references part_categories(id)
);
delete from parts;

.mode csv
.import tables/parts.csv parts