from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "b8f82f4"

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/buscar")
def buscar():
    titulo = request.args.get("titulo")
    año = request.args.get("año")

    url = f"http://www.omdbapi.com/?t={titulo}&y={año}&apikey={API_KEY}"
    respuesta = requests.get(url)
    datos = respuesta.json()

    if datos["Response"] == "False":
        return render_template("resultado.html", error="Película no encontrada 😢")

    return render_template("resultado.html", pelicula=datos)

if __name__ == "__main__":
    app.run(debug=True)