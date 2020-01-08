import psycopg2.extras
from psycopg2 import sql
from config import config
from model import connect, create_schools
conn = connect()
db = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def setup():
    create_schools()
