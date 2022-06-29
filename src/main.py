from fastapi import FastAPI, Depends
from . import database as dab
from sqlalchemy.orm import Session
from . import models as md
from . import schemas as sc

app = FastAPI()

md.Base.metadata.create_all(bind=dab.engine)

# keep the connection all the time is ok cuz its a local file
# Don't on postgre  
def get_db():
    try:
        db = dab.SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/dashboard")
async def dashboard(db: Session = Depends(get_db)):
    return db.query(md.Hero).all()

# adding an hero
@app.post("/heroes")
async def HeroAdd(hero: sc.Hero, db: Session = Depends(get_db)):
    hero_model = md.Hero()
    hero_model.name = hero.name
    db.add(hero_model)
    db.commit()
    
    return hero

# Updating a hero  
@app.put("/details/{id}")
async def UpdateHero(id: int, hero: sc.Hero, db: Session = Depends(get_db)):

    heroes = db.query(md.Hero).filter(
        md.Hero.id == id).first()

    heroes.name = hero.name

    db.add(heroes)
    db.commit()

    return hero
    
@app.delete("/heroes/")
async def delete_hero(id: int, db: Session = Depends(get_db)):
        
        db.query(md.Hero).filter(md.Hero.id==id).delete()
        db.commit()
        return {"deleted": True}
    