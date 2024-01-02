import requests
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('movies.db')

# Crear un cursor
c = conn.cursor()

# Crear la tabla de películas si no existe
c.execute('''CREATE TABLE IF NOT EXISTS movies
             (id INTEGER PRIMARY KEY,
              title TEXT,
              director TEXT,
              year INTEGER,
              genre TEXT)''')

# Verificar si la tabla de películas está vacía
c.execute("SELECT COUNT(*) FROM movies")
if c.fetchone()[0] == 0:
    # Hacer solicitudes a la API de OMDB y guardar los datos en la base de datos
    url = "http://www.omdbapi.com/"
    params = {
        "apikey": "34600ae8",
        "type": "movie"
    }

    movies = ["The Shawshank Redemption", "The Godfather", "The Dark Knight", ...]
    

    for movie in movies:
        params["t"] = movie
        response = requests.get(url, params=params)
        data = response.json()

        # Insertar los datos en la tabla de películas
        c.execute("INSERT INTO movies (title, director, year, genre) VALUES (?, ?, ?, ?)",
                  (data["Title"], data["Director"], data["Year"], data["Genre"]))

    # Guardar los cambios
    conn.commit()

# Cerrar el cursor y la conexión
c.close()
conn.close()

    

