import sqlite3
from datetime import datetime
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "b8f82f4"


# 🔹 Crear base de datos si no existe
def init_db():
    conn = sqlite3.connect("database.db")
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


# 🔹 Página principal
@app.route("/")
def inicio():
    return render_template("index.html")


# 🔹 Buscar película y gestionar comentarios
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    titulo = request.args.get("titulo")
    año = request.args.get("año")

    url = f"http://www.omdbapi.com/?t={titulo}&y={año}&apikey={API_KEY}"
    respuesta = requests.get(url)
    datos = respuesta.json()

    if datos["Response"] == "False":
        return render_template("resultado.html", error="Película no encontrada 😢")

    id_pelicula = datos["imdbID"]

    # Guardar comentario si se envía el formulario
    if request.method == "POST":
        persona = request.form.get("persona")
        comentario = request.form.get("comentario")

        if persona and comentario:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO comentarios (id_pelicula, persona, comentario, fecha)
                VALUES (?, ?, ?, ?)
            """, (id_pelicula, persona, comentario, datetime.now()))

            conn.commit()
            conn.close()

    # Obtener comentarios guardados
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT persona, comentario, fecha FROM comentarios WHERE id_pelicula = ?",
        (id_pelicula,)
    )
    comentarios = cursor.fetchall()
    conn.close()

    return render_template(
        "resultado.html",
        pelicula=datos,
        comentarios=comentarios
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)