from fastapi import FastAPI
from app.api import auth, corpuses, search
import uvicorn
from app.celery import celery_app

def get_application():
    app = FastAPI(title="Fuzzy Search Example")

    # Подключаем роутеры
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    app.include_router(corpuses.router, tags=["Corpuses"])
    app.include_router(search.router, tags=["Search"])

    return app

app = get_application()

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)