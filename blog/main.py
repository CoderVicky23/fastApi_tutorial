# 2:38:00

from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)

app.include_router(blog.router)

app.include_router(user.router)






# if (__name__ == "__main__"):
#     uvicorn.run(app, host="127.0.0.1", port=9000)