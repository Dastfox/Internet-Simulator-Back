from pydantic import BaseModel

# pydantic model for DB
class HeroBase(BaseModel):
    title:str
# pydantic model for crating Hero        
class HeroAdd(HeroBase):
    pass
# pydantic model for hero
class Hero(HeroBase):
    id: int
    name: str