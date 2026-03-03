import sqlite3
from datetime import datetime

DATABASE = "database.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pelicula TEXT,
            persona TEXT,
            comentario TEXT,
            fecha TEXT
        )
    """)

    conn.commit()
    conn.close()


def guardar_comentario(id_pelicula, persona, comentario):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO comentarios (id_pelicula, persona, comentario, fecha)
        VALUES (?, ?, ?, ?)
    """, (id_pelicula, persona, comentario, datetime.now()))

    conn.commit()
    conn.close()


def obtener_comentarios(id_pelicula):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT persona, comentario, fecha
        FROM comentarios
        WHERE id_pelicula = ?
    """, (id_pelicula,))

    comentarios = cursor.fetchall()
    conn.close()

    return comentarios
    