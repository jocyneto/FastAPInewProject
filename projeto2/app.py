from fastapi import FastAPI # type: ignore
from routers import router

app = FastAPI()
app.include_router(router=router)
