import sqlite3
import config


# connect to the DB
conn = sqlite3.connect(config.database_file)
c = conn.cursor()
