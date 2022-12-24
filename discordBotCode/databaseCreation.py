import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    
    return conn

#creates the SQLite3 with the provided SQL table 
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)

    except Error as e:
        print(e)


def main():
    database = r"C:\Users\bkowa\Documents\Python Code\discordBotCode\csgamerpings.db"

    sql_create_pings_table = """ CREATE TABLE IF NOT EXISTS pings (
                                        "id" text PRIMARY KEY,
                                        "count" integer 
                                    ); """

    sql_create_messages_table = """ CREATE TABLE IF NOT EXISTS messages (
                                        "id" text PRIMARY KEY,
                                        "count" integer 
                                    ); """


    
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_pings_table)
        create_table(conn, sql_create_messages_table)

    else:
        print("Error!!")

if __name__ == '__main__':
    main()

