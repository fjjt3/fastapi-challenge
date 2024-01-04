import sqlite3
import requests

# Database Configuration
db_path = "movies5.db"
table_name = "movies"

# OMDB Rest Client COnfiguration
api_key="34600ae8"
base_url = "http://www.omdbapi.com/"

def get_db_connection():
    return sqlite3.connect(db_path)

def get_db_cursor(db_connection):
    return db_connection.cursor()

def make_db_commit(db_connection):
    return db_connection.commit()

def close_db_connection(db_connection):
    return db_connection.close()

def does_table_exist(table_name, db_cursor):
    db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return db_cursor.fetchone() is not None

def create_movie_table(table_name, db_cursor):
    db_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (imdbID TEXT PRIMARY KEY, title TEXT, year TEXT, poster TEXT)")

def is_table_empty(table_name, db_cursor):
    try:
        db_cursor.execute(f"SELECT count(*) FROM {table_name}")
        return db_cursor.fetchone()[0] == 0
    except sqlite3.OperationalError:
        return True

def get_table_row_count(table_name, db_cursor):
    db_cursor.execute(f"SELECT count(*) FROM {table_name}")
    return db_cursor.fetchone()[0]

def insert_movie_table():
    return None

def delete_movie_table(table_name, db_cursor):
    db_cursor.execute(f"DELETE FROM {table_name}")

def get_top_100_movies():
    for page in range(1, 11):  
        movies = omd_rest_client(page)
        if movies is not None:
            insert_movies_db(movies)

def omd_rest_client(page):
    try:
        params = {"type": "movie", "apikey": api_key, "s": "movie", "page": {page}}  # 's' stands for 'search'
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        movie_data = response.json()
        if movie_data["Response"] == "True":
            return movie_data["Search"]
        else:
            print(f"Error: {movie_data['Error']}")
            print(f"Error getting data in page: {page}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None 

def insert_movies_db(movies):
    for movie in movies:
        insert_movie_table()

def populate_movies_db():
    db_connection = get_db_connection()
    db_cursor = get_db_cursor(db_connection)
    if not does_table_exist(table_name, db_cursor):
        create_movie_table(table_name, db_cursor)
        get_top_100_movies()
    elif not is_table_empty(db_path, table_name) and get_table_row_count(table_name, db_connection) < 100:
        delete_movie_table(table_name, db_cursor)
        get_top_100_movies()
    make_db_commit(db_connection)
    close_db_connection(db_connection)
    