create table if not exists part_categories (
  id smallint primary key,
  name varchar(64)
);
delete from part_categories;

.mode csv
.import tables/part_categories.csv part_categories