#!/usr/bin/env python3
from subprocess import run

DB_PATH = "dist/bricks.db"

TABLE_NAMES = [
  "themes",
  "colors",
  "part_categories",
  "parts",
  "part_relationships",
  "elements",
  "minifigs",
  "inventories",
  "sets",
  "inventory_parts",
  "inventory_sets",
  "inventory_minifigs",
]

def download():
  for table in TABLE_NAMES:
    # FIXME: curl each file into the tables/ directory
    pass
  split_inventories()
  
def split_inventories():
  set_inventory_file = open("tables/set_inventories.csv", "w")
  minifig_inventory_file = open("tables/minifig_inventories.csv", "w")
  with open("tables/inventories.csv") as inventories_csv:
    for line in inventories_csv.readlines():
      if line.split(",")[-1].startswith("fig-"):
        minifig_inventory_file.writelines([line])
        continue
      set_inventory_file.writelines([line])
  minifig_inventory_file.close()
  set_inventory_file.close()

def clean():
  run("rm -f dist/*", shell=True)
  pass

def clean_all():
  clean()
  run("rm -f tables/*", shell=True)

def create_script(table_name):
  # TODO: test: count the lines in each csv and compare it to the number of records present after the import.
  run(f"sqlite3 {DB_PATH} < scripts/table_{table_name}.sql", shell=True)

def build():
  create_script("themes")
  create_script("colors")
  create_script("part_categories")
  create_script("parts")
  create_script("part_relationships")
  create_script("elements")
  create_script("minifigs")
  create_script("sets")
  create_script("set_inventories")
  create_script("minifig_inventories")
  create_script("inventory_parts")
  create_script("inventory_sets")
  create_script("inventory_minifigs")


def main():
  clean()
  build()

if __name__ == "__main__":
  main()
