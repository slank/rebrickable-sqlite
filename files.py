from subprocess import run

TABLE_FILE_NAMES = [
  "themes",
  "colors",
  "part_categories",
  "parts",
  "part_relationships",
  "elements",
  "minifigs",
  "sets",
  "inventories",
  "inventory_parts",
  "inventory_sets",
  "inventory_minifigs",
]

def download():
  for table in TABLE_FILE_NAMES:
    # FIXME: curl each file into the tables/ directory
    pass
  
def clean():
  run("rm -f dist/*", shell=True)
  pass

def clean_all():
  clean()
  run("rm -f tables/*", shell=True)
