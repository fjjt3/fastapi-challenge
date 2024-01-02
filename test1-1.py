import httpx
import sqlite3

# Realizar solicitud a la API de OMDB
async def get_movies_from_omdb():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://www.omdbapi.com/', params={'s': 'movie', 'apikey': '34600ae8', 'page': 100})
        data = response.json()
        return data['Search']

# Guardar películulas en la base de datos SQLite
def save_movies_to_sqlite(movies):
    conn = sqlite3.connect('movies1.db')
    c = conn.cursor()

    # Crear tabla si no existe
    c.execute('''CREATE TABLE IF NOT EXISTS movies
                 (title text, year text, imdbID text, poster text)''')

    # Insertar películulas en la base de datos
    for movie in movies:
        c.execute("INSERT INTO movies VALUES (?, ?, ?, ?)", (movie['Title'], movie['Year'], movie['imdbID'], movie['Poster']))

    conn.commit()
    conn.close()

# Obtener películulas de OMDB y guardarlas en la base de datos SQLite
async def main():
    movies = await get_movies_from_omdb()
    save_movies_to_sqlite(movies)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())