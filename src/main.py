from dataclasses import field
from email.policy import default
from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Query


class LinkBase(SQLModel):
    url: str = Field(index=True)
    guid: Optional[str] = Field(default=None)


class Link(LinkBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    

class LinkCreate(LinkBase):
    pass


class LinkRead(LinkBase):
    id: Optional[int]

class LinkUpdate(SQLModel):
    url: Optional[str] = None


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


@app.post("/", response_model=LinkRead)
def create_link(link: LinkCreate):
    with Session(engine) as session:
        db_link = Link.from_orm(link)
        session.add(db_link)
        session.commit()
        session.refresh(db_link)
        return db_link


@app.get("/", response_model=List[LinkRead])
def read_links():
    with Session(engine) as session:
        return session.exec(select(Link)).all()


@app.get("/details/{link_id}", response_model=LinkRead)
def read_link(link_id: str):
    with Session(engine) as session:
        link = session.get(Link, link_id)
        if not link:
            raise HTTPException(status_code=404, detail="link not found")
        return link


@app.delete("/{link_id}")
def delete_link(link_guid: str):
    with Session(engine) as session:
        link = session.get(Link, link_guid)
        if not link:
            raise HTTPException(status_code=404, detail="link not found")
        session.delete(link)
        session.commit()
        return {"ok": True}
