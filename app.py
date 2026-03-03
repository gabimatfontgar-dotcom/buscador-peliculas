from flask import Flask
from models.db import init_db
from controllers.movie_controller import movie_blueprint

app = Flask(__name__)

# Registrar rutas del controller
app.register_blueprint(movie_blueprint)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)