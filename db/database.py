import sqlite3
import config

# connect to the DB
conn = sqlite3.connect(config.database_file)
c = conn.cursor()


# initialise if necessary
c.execute('''create table if not exists respect
             (user text, f integer) ''')
# user is the discord user id
# f is an integer with the number of times a user has paid respects

c.execute('''create table if not exists harambe
             (server text, last text,
              number integer, chain integer, max integer)''')
# channel is a discord channel id
# last is a datetime containing the last noted harambe reference

c.execute('''create table if not exists ratings
              (thing text, rater text,
              without integer, with integer)''')

