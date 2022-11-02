create table if not exists minifigs (
  id varchar(20) primary key,
  name varchar(300),
  num_parts smallint,
  img_url varchar(300)
);
delete from minifigs;

.mode csv
.import tables/minifigs.csv minifigs