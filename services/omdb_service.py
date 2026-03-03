import requests

API_KEY = "b8f82f4"

def buscar_pelicula(titulo, año):
    url = f"http://www.omdbapi.com/?t={titulo}&y={año}&apikey={API_KEY}"
    respuesta = requests.get(url)
    return respuesta.json()