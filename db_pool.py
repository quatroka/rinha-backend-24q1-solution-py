from psycopg_pool import ConnectionPool
import os

POSTGRES_HOSTNAME = os.getenv('POSTGRES_HOSTNAME')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

conn_string = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}'
pool = ConnectionPool(conn_string, open=True, min_size=4, max_size=8)
