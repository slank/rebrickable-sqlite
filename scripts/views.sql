create view if not exists set_parts
as 
select 
  inventories.set_num,
  inventory_parts.inventory_id, 
  inventory_parts.part_id, 
  inventory_parts.color_id, 
  inventory_parts.quantity, 
  inventory_parts.is_spare
from inventories
left outer join inventory_parts on
  inventory_parts.inventory_id = inventories.id
where inventories.version = 1;

create view if not exists part_info
as
select
  part_id,
  count(distinct set_parts.set_num) as num_sets,
  sum(quantity) as num_set_parts,
  max(year) as year_to,
  min(year) as year_from,
  "https://rebrickable.com/parts/" || part_id as part_url,
  "https://cdn.rebrickable.com/media/thumbs/parts/elements/" ||
    element_id || ".jpg/85x85p.jpg" as part_img_url
from set_parts
join sets on sets.set_num = set_parts.set_num
natural join elements
group by part_id;

create view if not exists part_color_info
as
select
  part_id,
  color_id,
  count(distinct set_parts.set_num) as num_sets,
  sum(quantity) as num_set_parts,
  max(year) as year_to,
  min(year) as year_from,
  "https://rebrickable.com/parts/" || part_id as part_url,
  "https://m.rebrickable.com/media/parts/ldraw/" ||
    color_id || "/" || part_id || ".png" as part_img_url
from set_parts
join sets on sets.set_num = set_parts.set_num
group by part_id, color_id;

-- The parts table doesn't include absolutely every part_id. This view does.
create view if not exists part_ids
as
select part_id as part_id from parts
union 
select child_part_id as part_id from part_relationships
union
select parent_part_id as part_id from part_relationships;

drop view if exists canonical_parts;
create view if not exists canonical_parts
as
select
  part_id,
  case 
    when parent_part_id is null 
    then part_id else parent_part_id 
    end as canonical_part_id
from part_ids
left join part_relationships on 
  child_part_id = part_id
  and (rel_type = 'M');
