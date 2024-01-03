from fastapi import FastAPI
# from .import models
from  models import models
from database import engine
from routers import login, movie, user

app = FastAPI(
    title="Movies API",
    description="Get details of movies",
    terms_of_service="http://www.google.com",
    contact ={"Developer_name":"Francisco Jimenez"},
    # docs_url="/documentation"
)

app.include_router(movie.router)
app.include_router(user.router)
app.include_router(login.router)

models.Base.metadata.create_all(engine)