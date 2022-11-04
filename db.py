import logging
from subprocess import run

DB_PATH = "dist/bricks.db"

class DBError(Exception):
    pass

def db_execute(command: str):
    logging.debug(f"db_execute:\n{command}")
    result = run(["sqlite3", DB_PATH], input=command.encode("UTF-8"), capture_output=True)
    if result.returncode != 0:
        raise DBError(result.stderr.decode("UTF-8"))


def csv_import(name, tablename=None, pragma_fk=1):
    if tablename is None:
        tablename = name
    command = "\n".join([
        f"pragma foreign_keys = {pragma_fk};",
        ".mode csv",
        f".import tables/{name}.csv {tablename}",
    ])
    logging.debug(f"csv_import: {name}.csv to {tablename}")
    db_execute(command)


def create_table(name, column_statements, fk_statements=None):
    logging.info(f"create_table: {name}")
    create_statement = f"create table if not exists {name} ("
    if fk_statements:
        column_statements.extend(fk_statements)
    create_statement += ",".join(column_statements)
    create_statement += ");"
    db_execute(create_statement)
    db_execute(f"delete from {name};")


def import_table(name, column_statements):
    logging.info(f"import_table: {name}")
    create_table(name, column_statements)
    csv_import(name)


def import_checked_table(name, column_statements, fk_statements, pragma_fk=1):
    logging.info(f"import_checked_table: {name}")
    import_tablename = f"import_{name}"
    create_table(name, column_statements)
    create_table(import_tablename, column_statements, fk_statements)
    csv_import(name, tablename=import_tablename, pragma_fk=pragma_fk)
    db_execute(f"insert into {name} select * from {import_tablename};")
    if pragma_fk:
        db_execute(f"drop table {import_tablename};")
