from fastapi import FastAPI
from routes.authorization import auth_router
from routes.posts import posts_router
from routes.user import user_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(user_router)
