import sqlite3
from sqlite3 import Error

class Ping:
    user =  None
    count = 1

# Connects to the SQLite3 database
def create_connection(db_file):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# Inserts the SQLite3 Database appropriately
def create_ping(conn, ping):
    
    sql = '''INSERT INTO pings(id, count)
            VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, ping)
    conn.commit()
    
    return cur.lastrowid

def update_ping(conn, ping):
    sql = '''UPDATE pings
            SET count = ?
            WHERE id = ? ''' 
    cur = conn.cursor()
    cur.execute(sql, (ping[1], ping[0]))
    conn.commit()

def create_message(conn, ping):
    
    sql = '''INSERT INTO messages(id, count)
            VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, ping)
    conn.commit()
    
    return cur.lastrowid

def update_message(conn, ping):
    sql = '''UPDATE messages
            SET count = ?
            WHERE id = ? ''' 
    cur = conn.cursor()
    cur.execute(sql, (ping[1], ping[0]))
    conn.commit()

def checkForUserMessages(conn, user):
    cur = conn.cursor()
    sql = "SELECT * FROM messages WHERE id=\'"+user+"\'"
    #update with Try Catch statement to handle error where user has no messages
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def insertOrUpdateUserMessages(conn, user):
    query = checkForUserMessages(conn, user)
    if(len(query) > 0):
        ping = (query[0][0], query[0][1]+1)
        update_message(conn,ping)
    else:
        create_message(conn,(user, 1))


def print_pings(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM pings  ORDER BY count DESC;")

    rows = cur.fetchall()
    for row in rows:
        print(row)

    return rows

def print_pings_messages(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM messages ORDER BY count DESC;")

    rows = cur.fetchall()
    return rows

def checkForUser(conn, user):
    cur = conn.cursor()
    sql = "SELECT * FROM pings WHERE id=\'"+user+"\'"
    cur.execute(sql)
    rows = cur.fetchall()
    return rows

def insertOrUpdateUser(conn, user):
    query = checkForUser(conn, user)
    if(len(query) > 0):
        ping = (query[0][0], query[0][1]+1)
        update_ping(conn,ping)
    else:
        create_ping(conn,(user, 1))


# def main():
#     # set database to access
#     database = r"C:\Users\bkowa\Documents\Python Code\OhioBot\discordBotCode\csgamerpings.db"
#     conn = create_connection(database)
        


# if __name__ == '__main__':
#     main()
