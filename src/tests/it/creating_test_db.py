from pathlib import Path

import psycopg2

from settings import settings


def create_db() -> None:
    connection = psycopg2.connect(settings.DATABASE_URL.replace('qbot_admin_test', 'postgres'))
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE DATABASE qbot_admin_test')
    except psycopg2.errors.DuplicateDatabase:
        drop_db()
        cursor.execute('CREATE DATABASE qbot_admin_test')
    connection.close()


def apply_migrations(cursor) -> None:
    migrations = sorted(
        [
            path
            for path in Path('migrations').iterdir()
            if path.name.endswith('.sql') and not path.name.endswith('rollback.sql')
        ],
        key=lambda file_path: file_path.name,
    )
    for migration in migrations:
        cursor.execute(migration.read_text())


def fill_test_db() -> None:
    qbot_connection = psycopg2.connect(settings.DATABASE_URL)
    qbot_connection.autocommit = True
    qbot_cursor = qbot_connection.cursor()
    apply_migrations(qbot_cursor)
    fixtures = (
        'src/tests/it/db-fixtures/admin/files.sql',
        'src/tests/it/db-fixtures/admin/suras.sql',
        'src/tests/it/db-fixtures/admin/ayats.sql',
    )
    for fixture in fixtures:
        qbot_cursor.execute(Path(fixture).read_text())
    qbot_connection.close()


def drop_db() -> None:
    connection = psycopg2.connect(settings.DATABASE_URL.replace('qbot_admin_test', 'postgres'))
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute(
        '\n'.join([
            'SELECT pg_terminate_backend (pg_stat_activity.pid)',
            'FROM pg_stat_activity',
            "WHERE pg_stat_activity.datname = 'qbot_admin_test' AND pid <> pg_backend_pid();",
        ]),
    )
    cursor.execute('DROP DATABASE qbot_admin_test')
