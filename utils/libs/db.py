import sqlite3
import utils.libs.logger as logger

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
        logger.logError('Não foi posível encontrar nenhum usuário')
        unkn = {}
        unkn.name = 'Unknown'
        #todo - Create a class user to better solve this kind of issue
        return unkn

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
    logger.log('Inserindo novo usuário...')
    conn = sqlite3.connect(dbName)
    sQuery = "INSERT INTO users ( id, Name ) VALUES (" + str(iId) + ", '" + sName + "')"

    try :
        conn.execute(sQuery)
        conn.commit()
        logger.log('Novo usuário inserido com sucesso')
    except :
        logger.logError('Não foi possível inserir novo usuário')
    conn.close()
