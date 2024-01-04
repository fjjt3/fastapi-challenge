import sqlite3
import requests
from fastapi import FastAPI
from  models import models
from database import engine
from routers import movie
from db.db_script import populate_movies_db

# Application Configuration 
db_path = "movies4.db"
table_name = "movies"

# Fast Api Configuration
app = FastAPI(
    title="Movies API",
    description="Get details of movies",
    terms_of_service="http://www.google.com",
    contact ={"Developer_name":"Francisco Jimenez"},
    # docs_url="/documentation"
)

@app.on_event("startup")
async def startup_event():
    populate_movies_db(db_path, table_name)

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutdown event")

# Fast API: Router Configuration
app.include_router(movie.router)

models.Base.metadata.create_all(engine)

