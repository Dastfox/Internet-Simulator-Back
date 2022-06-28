from fastapi import FastAPI, Depends, HTTPException
import database as db
from sqlalchemy.orm import Session
import models, schemas

app = FastAPI()

models.Base.metadata.create_all(bind=db.engine)


def get_db():
    try:
        db = db.SessionLocal()
        yield db
    finally:
        db.close()

#redirected to dbord anyway 
@app.get("/")
async def root(db: Session = Depends(get_db)):
    return db.query(models.Hero).all()

# adding an hero
@app.post("/heroes")
async def HeroAdd(hero: schemas.Hero, db: Session = Depends(get_db)):
    
    hero_model = models.Hero()
    hero_model.name = hero.name

    db.add(hero_model)
    db.commit()

    return hero
    