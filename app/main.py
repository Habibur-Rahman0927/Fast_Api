from fastapi import FastAPI
from . import models, schema, utils
from .config import settings
from .database import engine
from .router import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# models.Base.metadata.create_all(bind=engine) ## alembic wroking so this line is no need
origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(vote.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"Habib Rahman api is runing"}

