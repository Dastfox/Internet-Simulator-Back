from pydantic import BaseModel


# pydantic model for hero
class Hero(BaseModel):
    id: int
    name: str
# pydantic model for crating Hero        
class HeroAdd(Hero):
    pass
