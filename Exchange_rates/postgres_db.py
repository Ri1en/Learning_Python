import psycopg2

from db_config import PostgresSettings


class PostgresDb:
    def __init__(self, config_object):
        self.config: PostgresSettings = config_object
        self.cursor = None
        self.connection = None
        self.connect_db()

    def create_db(self):
        self.connection.autocommit = True
        self.cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.config.pg_name}'")
        exists = self.cursor.fetchone()
        if not exists:
            self.cursor.execute(f"CREATE DATABASE {self.config.pg_name}")
        self.cursor.close()
        self.connection.close()

    def connect_db(self):
        try:
            self.connection = psycopg2.connect(
                database=self.config.pg_name,
                user=self.config.pg_user,
                password=self.config.pg_password,
                port=self.config.pg_port,
                host=self.config.pg_host
            )
            print("[INFO] Подключение установлено")
            self.cursor = self.connection.cursor()
        except Exception as e:
            print("[INFO] Нет соединения с БД", e)

    def create_table(self):
        self.connect_db()
        self.connection.autocommit = True
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.config.pg_table_name} (
        {self.config.pg_columns_initialize}
        )
        """)
        self.cursor.close()
        self.connection.close()

    def __enter__(self):
        self.connect_db()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
