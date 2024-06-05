import sqlite3


def openDB(db):
    """Acceder a la conexión y cursor."""

    con = sqlite3.connect(db)
    cursor = con.cursor()
    return cursor, con


def createDB():
    """Función de un único uso."""

    cursor, con = openDB('temas1.db')
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grafo (
        id INTEGER PRIMARY KEY,
        temas TEXT UNIQUE NOT NULL, 
        ideas TEXT, 
        importancia TEXT,
        grupo_grafo TEXT,
        conexiones TEXT UNIQUE,
        label TEXT
        )""")
    con.close()

def check_user_db():
    """Contiene el 'historial' del usuario."""

    con = sqlite3.connect('user.db')
    cursor = con.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        materia TEXT UNIQUE,
        temas TEXT,
        relaciones TEXT
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_info (
        id INTEGER PRIMARY KEY,
        relevancia status BOOL
    )""")
    cursor.execute("INSERT INTO user_info (relevancia) VALUES (?)", (False,))
    con.commit()
    con.close()


def getTopicList():
    """Selecciona la columna temas de la db."""

    cursor, con = openDB('temas1.db')
    lista_temas = []
    temas = cursor.execute("SELECT temas FROM grafo")
    for tema in temas.fetchall():
        lista_temas.append(tema[0])

    total_busqueda_temas = cursor.execute("SELECT COUNT(temas) FROM grafo")
    total_temas = total_busqueda_temas.fetchone()[0]
    con.close()

    # Verificar si hay temas
    if lista_temas:
        return [lista_temas, total_temas]
    else:
        return [None, None]


def checkTopic(tema):
    """Verifica si un tema existe."""

    cursor, con = openDB('temas1.db')
    params = (tema,)
    cursor.execute("SELECT * FROM grafo WHERE temas = ?", params)
    verificar = cursor.fetchall()
    
    if verificar:
        status = True
    else:
        status = False

    con.close()
    return status


def addTopic(tema_nuevo):
    """Añade el tema que el usuario de."""

    cursor, con = openDB('temas1.db')
    if checkTopic(tema_nuevo) == False:
        data = (tema_nuevo, ' ', ' ')
        cursor.execute("INSERT INTO grafo (temas, ideas, importancia) VALUES (?, ?, ?)", data)
        con.commit()
        status = True
    else:
        status = False

    con.close()
    return status

def addIdea(topic, relevance, idea):
    """Añade la relevancia y la idea al tema asociado"""

    cursor, con = openDB('temas1.db')
    sql = "UPDATE grafo SET ideas = ?, importancia = ? WHERE temas = ?"
    params = (idea, relevance, topic,)
    cursor.execute(sql, params)
    con.commit()
    
    cursor.close()
    con.close()



def updateTopic(antiguo_tema, nuevo_tema):
    """Actualiza el tema"""

    cursor, con = openDB('temas1.db')
    sql = "UPDATE grafo SET temas = ? WHERE temas = ?"
    params = (nuevo_tema, antiguo_tema,)
    cursor.execute(sql, params)
    con.commit()
    con.close()


def addIdeaRelevance(reltype_entry, label_entry):
    """Añade el tipo de relación y la idea a la DB."""

    status = False
    try:
        params = (label_entry.get(), reltype_entry.get())
        cursor, con = openDB('temas1.db')
        cursor.execute('INSERT INTO grafo (conexiones, label, tipconexion) VALUES (?, ?)', params)
        con.commit()
        con.close()
        status = True
    finally:
        return status


def deleteTopic(tema_eliminar):
    """Elimina la fila correspondiente al tema a eliminar."""

    cursor, con = openDB('temas1.db')
    if checkTopic(tema_eliminar):
        cursor.execute("DELETE FROM grafo WHERE temas = ?", (tema_eliminar,))
        con.commit()
        status = True
    else:
        status = False
    
    con.close()
    return status

