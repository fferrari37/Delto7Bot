import sqlite3
import os

#Inicia o inicializa la DB del contador dependiendo de su existencia.
def iniciar_db():
    if not os.path.exists("db"):
        os.makedirs("db")

    conn = sqlite3.connect("db/contador.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contador_usuarios (
            usuario_id INTEGER PRIMARY KEY, contador INTEGER DEFAULT 0)
    """)
    conn.commit()
    conn.close()


#Obtiene el contador total del usuario
def obtener_contador(usuario_id):
    conn = sqlite3.connect("db/contador.db")
    cursor = conn.cursor()
    cursor.execute("SELECT contador FROM contador_usuarios WHERE usuario_id = ?", (usuario_id,))
    contador = cursor.fetchone()
    conn.close()
    
    if contador:
        return contador[0]
    else:
        return 0


#Aumenta el total del contador del usuario en += 1.
def incrementar_contador(usuario_id):
    conn = sqlite3.connect("db/contador.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO contador_usuarios (usuario_id) VALUES (?)", (usuario_id,))
    cursor.execute("UPDATE contador_usuarios SET contador = contador+1 WHERE usuario_id = ?", (usuario_id,))
    conn.commit()
    conn.close()