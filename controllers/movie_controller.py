from flask import Blueprint, render_template, request
from services.omdb_service import buscar_pelicula
from models.db import guardar_comentario, obtener_comentarios

movie_blueprint = Blueprint("movie", __name__)

@movie_blueprint.route("/")
def inicio():
    return render_template("index.html")


@movie_blueprint.route("/buscar", methods=["GET", "POST"])
def buscar():
    titulo = request.args.get("titulo")
    año = request.args.get("año")

    datos = buscar_pelicula(titulo, año)

    if datos["Response"] == "False":
        return render_template("resultado.html", error="Película no encontrada 😢")

    id_pelicula = datos["imdbID"]

    if request.method == "POST":
        persona = request.form.get("persona")
        comentario = request.form.get("comentario")

        if persona and comentario:
            guardar_comentario(id_pelicula, persona, comentario)

    comentarios = obtener_comentarios(id_pelicula)

    return render_template(
        "resultado.html",
        pelicula=datos,
        comentarios=comentarios
    )