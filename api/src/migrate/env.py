import os
import sys

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

if os.environ.get('CASTLE_MOD') == 'development':
    sys.path.append('C:\\workspace\\castle\\api\\src')
else:
    sys.path.append('/CASTLE/api')

from config import GLOBAL_CONFIG

config = context.config

target_metadata = None


def run_migrations_online():
    section = config.config_ini_section
    config.set_section_option(section, "DB_HOST", GLOBAL_CONFIG.DB_HOST)
    config.set_section_option(section, "DB_USER", GLOBAL_CONFIG.DB_USER)
    config.set_section_option(section, "DB_PASS", GLOBAL_CONFIG.DB_PASS)
    config.set_section_option(section, "DB_NAME", GLOBAL_CONFIG.DB_NAME)

    connectable = engine_from_config(config.get_section(config.config_ini_section), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


con = psycopg2.connect(
        user=GLOBAL_CONFIG.DB_USER,
        host=GLOBAL_CONFIG.DB_HOST,
        password=GLOBAL_CONFIG.DB_PASS,
        port=GLOBAL_CONFIG.DB_PORT,
        dbname=GLOBAL_CONFIG.DB_NAME)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()

cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public';")
if not cur.fetchone():
    cur.execute(
        "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{}' AND pid <> pg_backend_pid();".format(
            GLOBAL_CONFIG.DB_NAME))

    f = open(os.path.join(GLOBAL_CONFIG.CASTLE_ROOT_DIR, 'migrate', 'castle.dump'), encoding='utf-8')

    try:
        sql = f.read()
        cur.execute(sql)
    finally:
        f.close()

cur.close()
con.close()

run_migrations_online()