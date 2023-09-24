from functools import lru_cache
import psycopg2
import db_config


@lru_cache()
def get_db_config():
    config_object = db_config.PostgresSettings()
    return config_object


class PostgresDb:
    def __init__(self, config_object):
        self.config: db_config.PostgresSettings = config_object
        self.cursor = None
        self.connection = None
        self.connect_db()
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.initialize_bd()
            self.create_table()

    def initialize_bd(self):
        self.connection.autocommit = True
        self.cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'weather_db'")
        exists = self.cursor.fetchone()
        if not exists:
            self.cursor.execute("CREATE DATABASE weather_db")
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
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_table (
        weather_id SERIAL PRIMARY KEY,
        city VARCHAR(255),
        temp REAL,
        temp_max REAL,
        temp_min REAL,
        weather VARCHAR(255),
        weather_description VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
