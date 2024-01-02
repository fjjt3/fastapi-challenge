import httpx
import sqlite3

# Realizar solicitud a la API de OMDB
async def get_movies_from_omdb():
    async with httpx.AsyncClient() as client:
        movies = []
        for page in range(1, 11):  # Hacer 10 solicitudes para obtener 100 películas (cada página devuelve 10 películas)
            response = await client.get('http://www.omdbapi.com/', params={'s': 'movie', 'apikey': '34600ae8', 'page': page})
            data = response.json()
            movies.extend(data['Search'])
        return movies

# Guardar películulas en la base de datos SQLite
def save_movies_to_sqlite(movies):
    conn = sqlite3.connect('movies2.db')
    c = conn.cursor()
    # Crear tabla si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS movies (title text, year text, imdbID text, poster text)''')

    # Verificar si la tabla está vacía
    c.execute("SELECT * FROM movies")
    existing_movies = c.fetchall()

    if not existing_movies:  # Si no hay registros, insertar las películas
        # Insertar películulas en la base de datos
        for movie in movies:
            c.execute("INSERT INTO movies VALUES (?, ?, ?, ?)", (movie['Title'], movie['Year'], movie['imdbID'], movie['Poster']))
        conn.commit()

    conn.close()

# Obtener películulas de OMDB y guardarlas en la base de datos SQLite si está vacía
async def main():
    movies = await get_movies_from_omdb()
    save_movies_to_sqlite(movies)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())