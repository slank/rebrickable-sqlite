from functools import partial

from db import (create_table, csv_import, db_execute, import_checked_table,
                import_table)


def import_themes():
    import_table(
        "themes",
        [
            "id smallint primary key",
            "name varchar(64)",
            "parent_id smallint",
        ],
    )


def import_colors():
    import_table(
        "colors",
        [
            "id smallint primary key",
            "name varchar(64)",
            "rgb varchar(6)",
            "is_trans varchar(1)",
        ],
    )


def import_part_categories():
    import_table(
        "part_categories",
        [
            "id smallint primary key",
            "name varchar(64)",
        ],
    )


def import_parts():
    import_checked_table(
        "parts",
        [
            "id varchar(16) primary key",
            "name varchar(255)",
            "part_category_id smallint",
            "part_material_id varchar(64)",
        ],
        [
            "foreign key(part_category_id) references part_categories(id)",
        ],
    )


def import_part_relationships():
    # The source data does not include a useful primary key for each
    # record and we'd like one to use with our ORM. Import into a
    # temporary table, then move into the real one.
    tablename = "part_relationships"
    columns = ["rel_type varchar(1)", "child_part_id varchar(20)", "parent_part_id varchar(20)"]
    create_table(f"import_{tablename}", columns)
    csv_import(tablename, f"import_{tablename}")

    columns = ["id integer primary key autoincrement"] + columns
    create_table(tablename, columns)
    db_execute(
        f"insert into {tablename} (rel_type, child_part_id, parent_part_id)"
        f"select * from import_{tablename};"
    )
    db_execute(f"drop table import_{tablename};")


def import_elements():
    import_checked_table(
        "elements",
        [
            "id varchar(16) primary key",
            "part_id varchar(16)",
            "color_id smallint",
        ],
        [
            "foreign key(part_id) references parts(id)",
            "foreign key(color_id) references colors(id)",
        ],
    )


def import_minifigs():
    import_table(
        "minifigs",
        [
            "id varchar(20) primary key",
            "name varchar(300)",
            "num_parts smallint",
            "img_url varchar(300)",
        ],
    )


def import_sets():
    import_checked_table(
        "sets",
        [
            "id varchar(16) primary key",
            "name varchar(300)",
            "year smallint",
            "theme_id smallint",
            "num_parts int",
            "img_url varchar(300)",
        ],
        [
            "foreign key(theme_id) references themes(id)",
        ],
    )


def import_inventories():
    import_table(
        "inventories",
        [
            "id int primary key",
            "revision smallint",
            "set_id varchar(16)",
        ],
    )



def inventory_columns(name_singular):
    name = name_singular
    if name == "part":
        return [
            f"{name}_inventory_id int",
            f"{name}_id varchar(16)",
            "color_id smallint",  # only in parts inventory
            "quantity smallint",
            "is_spare varchar(1)",  # only in parts inventory
            "img_url varchar(300)",
            f"primary key ({name}_inventory_id, {name}_id, color_id, is_spare)",  # more columns
        ]
    else:
        return [
            f"{name}_inventory_id int",
            f"{name}_id varchar(16)",
            "quantity smallint",
            f"primary key ({name}_inventory_id, {name}_id)",
        ]


def inventories_table(name_singular):
    name = name_singular
    table_name = f"{name}_inventories"
    if name_singular == "minifig":
        rel = "minifig_id"
        rel_table = "minifigs"
    else:
        rel = "set_id"
        rel_table = "sets"
    create_table(
        table_name,
        [
            "id int primary key",
            "revision smallint",
            f"{rel} varchar(16)",
        ],
        [
            f"foreign key({rel}) references {rel_table}(id)",
        ],
    )
    return table_name


def import_inventory(name_singular):
    name = name_singular
    inv_table = inventories_table(name)
    create_table(f"import_inventory_{name}s", inventory_columns(name))
    csv_import(f"inventory_{name}s", f"import_inventory_{name}s")
    db_execute(
        "pragma foreign_keys = 1; "
        f"insert into {inv_table} select * from inventories as i "
        f"where i.id in (select {name}_inventory_id from import_inventory_{name}s);"
    )
    db_execute(f"drop table import_inventory_{name}s")
    import_checked_table(
        f"inventory_{name}s",
        inventory_columns(name),
        [
            f"foreign key({name}_inventory_id) references {inv_table}(id)",
            f"foreign key({name}_id) references {name}s(id)",
        ],
        pragma_fk=0,
    )
