#!/usr/bin/env python3
import logging
from pathlib import Path
from subprocess import run

import files
import logger
import schema


def import_tables():
    schema.import_themes()
    schema.import_colors()
    schema.import_part_categories()
    schema.import_parts()
    # schema.import_part_relationships()
    schema.import_sets()
    schema.import_elements()
    # schema.import_minifigs()
    schema.import_inventories()
    # schema.import_inventory("set")
    # schema.import_inventory("minifig")
    schema.import_inventory("part")


def build():
    import_tables()


def main():
    files.clean()
    build()


if __name__ == "__main__":
    logger.setupLogging()
    main()
