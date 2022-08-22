from dataclasses import field
from email.policy import default
from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, select, create_engine, String
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Query




class LinkBase (SQLModel):
    id: str = Field(primary_key = True, index=True)
    url: str 

class LinkModel (LinkBase, table = True):
    pass


class LinkRead (LinkBase):
    url: str

sqlite_file_url = "link.db"
sqlite_url = f"sqlite:///{sqlite_file_url}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

origins = ['*']


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/", response_model=LinkModel)
def create_link(link: LinkModel):
    with Session(engine) as session:
        db_link = LinkModel.from_orm(link)
        session.add(db_link)
        session.commit()
        session.refresh(db_link)
        return db_link


@app.get("/", response_model=List[LinkModel])
def read_links():
    with Session(engine) as session:
        return session.exec(select(LinkModel)).all()


@app.get("/details/{link_id}", response_model=LinkModel)
def read_link(link_id: str):
    with Session(engine) as session:
        link = session.get(LinkModel, link_id)
        if not link:
            raise HTTPException(status_code=404, detail="link not found")
        return link


@app.delete("/details/{link_id}")
def delete_link(link_id: str):
    with Session(engine) as session:
        link = session.get(LinkModel, link_id)
        if not link:
            raise HTTPException(status_code=404, detail="link not found")
        session.delete(link)
        session.commit()
        return {"ok": True}
    
@app.patch("/details/{link_id}", response_model=LinkModel)
def update_link(link_id: str, link: LinkModel):
    with Session(engine) as session:
        db_link = session.get(LinkModel, link_id)
        if not db_link:
            raise HTTPException(status_code=404, detail="link not found")
        link_data = link.dict(exclude_unset=True)
        for key, value in link_data.items():
            setattr(db_link, key, value)
        session.add(db_link)
        session.commit()
        session.refresh(db_link)
        return db_link
