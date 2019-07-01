"""
db.py

DB.py é responsável por fazer a ponte entre o banco de dados em SQLite 3.0 e a aplicação. Com ele é feita a consulta, a 
importação de dados e a gravação de novos registros.
"""

import sqlite3

dbName = 'TCC-database.db'

def getUserData(sId) :
    conn = sqlite3.connect(dbName)
    sQuery = "SELECT Name FROM users WHERE id = " + str(sId)

    cursor = conn.execute(sQuery)
    oUserData = None

    for row in cursor :
        oUserData = row
        break

    conn.close()

    if oUserData != None :
        return oUserData
    else :
        return ['Visitante']

def getNextId() :
    conn = sqlite3.connect(dbName)

    sQuery = 'SELECT COUNT(*) AS MAXID FROM users'

    cursor = conn.execute(sQuery)
    iMaxId = 0;

    for row in cursor :
        iMaxId = row[0]
        break

    iNextId = iMaxId + 1

    return iNextId


def insertNewUser(iId, sName) :
    conn = sqlite3.connect(dbName)
    sQuery = "INSERT INTO users ( id, Name ) VALUES (" + str(iId) + ", '" + sName + "')"

    try :
        conn.execute(sQuery)
        conn.commit()
    except :
        print('Não foi possível inserir novo usuário')
    conn.close()
