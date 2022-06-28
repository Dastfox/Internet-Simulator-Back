from pydantic import BaseModel

# pydantic model for hero.db
class Hero(BaseModel):
    id: int
    name: str
# pydantic model for crating Hero        
class HeroAdd(Hero):
    pass
# pydantic model for reading hero
class HeroRead(Hero):
    id : int
    
class HeroUpdate(BaseModel):
    name: str
    

