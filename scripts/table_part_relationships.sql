create table if not exists part_relationships (
  id integer primary key autoincrement,
  rel_type varchar(1),
  child_part_id varchar(20),
  parent_part_id varchar(20)
);
delete from part_relationships;

-- the source data does not include a useful primary key for each
-- record and we'd like one to use with our ORM. Import into a
-- temporary table, then move into the real one.
drop table if exists import_part_relationships;
create temporary table import_part_relationships (
  rel_type varchar(1),
  child_part_id varchar(20),
  parent_part_id varchar(20)
);
.mode csv
.import tables/part_relationships.csv import_part_relationships

insert into part_relationships (rel_type, child_part_id, parent_part_id)
  select rel_type, child_part_id, parent_part_id from import_part_relationships;

drop table if exists import_part_relationships;