from typing import List

from fastapi import FastAPI, Depends, Query
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from shop_app import view, models, schemas
from shop_app.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory=r"C:\Users\Admin\PycharmProjects\Store\static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/products/", response_model=List[schemas.ProductSchema])
def get_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 20, search: str = "",
                 cat: List[int] = Query(None), store: List[int] = Query(None)):
    q = view.get_products(db, skip=skip, limit=limit, search=search, cat=cat, store=store)
    return q
