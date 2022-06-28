from urllib import response
from fastapi import FastAPI, Depends, HTTPException
import database as dab
from sqlalchemy.orm import Session
import models as md
import schemas as sc

app = FastAPI()

md.Base.metadata.create_all(bind=dab.engine)


def get_db():
    try:
        db = dab.SessionLocal()
        yield db
    finally:
        db.close()

#redirected to dbord anyway so dunno if necessary
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

@app.patch ("/details/{id}", response_model=sc.HeroRead)
async def  updateHero (id: int, name: sc.HeroUpdate):
    with Session as session:
        db_hero = session.get(sc.Hero, id)
        if not db_hero:
            raise HTTPException(status_code=404, detail="Pas de Joueur à ce numéro!")
        hero_data = name.dict(exclude_unset=True)
        for key, value in hero_data.items():
            setattr(db_hero, key, value)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero
    
@app.delete("/details/{id}")
async def delete_hero(id: int):
    with Session as session:
        hero = session.get(sc.Hero, id)
        if not hero:
            raise HTTPException(status_code=404, detail="Pas de Joueur à ce numéro!")
        session.delete(hero)
        session.commit()
        return {"ok": True}
    