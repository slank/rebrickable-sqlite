DB = dist/bricks.db

all: tables/themes.csv \
 tables/colors.csv \
 tables/part_categories.csv \
 tables/parts.csv \
 tables/part_relationships.csv \
 tables/elements.csv \
 tables/minifigs.csv \
 tables/inventories.csv \
 tables/sets.csv \
 tables/inventory_parts.csv \
 tables/inventory_sets.csv \
 tables/inventory_minifigs.csv

tables/%.csv:
	test -f $@ || curl --silent https://cdn.rebrickable.com/media/downloads/$(subst tables/,,$@).gz | gunzip -c | tail -n +2 > $@

views: $(DB)
	sqlite3 $(DB) < scripts/views.sql

indices: $(DB)
	sqlite3 $(DB) < scripts/indices.sql

test: $(DB)
	sqlite3 $(DB) < examples.sql

clean:
	rm -f $(DB)

cleanall: clean
	rm -f tables/*.csv