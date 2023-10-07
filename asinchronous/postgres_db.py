import psycopg2

from db_config import PostgresSettings


class PostgresDb:

    def __init__(self, config_object):
        self.config: PostgresSettings = config_object
        self.cursor = None
        self.connection = None

    def connect_db(self):
        try:
            self.connection = psycopg2.connect(
                database=self.config.pg_db_name,
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
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {self.config.pg_table_name} (
        {self.config.pg_columns_to_initialize}
        )
        """)
        self.cursor.close()
        self.connection.commit()
        self.connection.close()

    def __enter__(self):
        self.connect_db()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

