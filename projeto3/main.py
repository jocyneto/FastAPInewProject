from fastapi import  FastAPI
import tables as tables
from database import engine
from routers import todo, auth, admin, user

app = FastAPI()

tables.Base.metadata.create_all(bind=engine)

app.include_router(todo.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(user.router)
