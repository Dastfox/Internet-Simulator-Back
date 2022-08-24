from dataclasses import field
from email.policy import default
from tkinter import Image
from typing import Any, Dict, List, Optional
import os as _os
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, String, create_engine, select
import random as _random
import time
from .services import  upload_image
import json


class LinkBase (SQLModel):
    id: str = Field(primary_key=True, index=True)
    url: str


class LinkModel (LinkBase, table=True):
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
        if link := session.get(LinkModel, link_id):
            return link
        else:
            raise HTTPException(status_code=404, detail="link not found")


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


# ############ Files:

class ImageBase(SQLModel):
    id: str = Field(primary_key=True, index=True)
    name: str


class ImageModel (ImageBase, table=True):
    pass

class ImageFile (SQLModel):
    id: str
    name: str
    file: UploadFile
    
@app.get("/files/", response_model=List[ImageModel])
def read_images():
    with Session(engine) as session:
        return session.exec(select(ImageModel)).all()



@app.get("/files/rand", response_class=FileResponse)
def get_random_file():
    images = read_images()
    random_image = _random.choice(images)
    random_image_name= random_image.name
    return f"assets/{random_image_name}"


@app.get("/files/{image_id}", response_class=FileResponse)
def read_file_path_from_id(image_id: str):
    filename = read_file_from_id(image_id).name
    return f"assets/{filename}"

def read_file_from_id(image_id: str):
    with Session(engine) as session:
        if image := session.get(ImageModel, image_id):
            return image
        else:
            raise HTTPException(status_code=404, detail="file not found")


@app.post("/files/")
def create_image(image_file: ImageFile):
    # image_file =  
    print(image_file)
    file_name = image_file.name
    imageItem = ImageModel(name=file_name)
    if file_name is None:
        return HTTPException(status_code=409, detail='incorrect file type')
    return upload_image_in_db(imageItem), FileResponse(file_name)


def upload_image_in_db(imageItem: ImageModel):
    with Session(engine) as session:
        db_image = ImageModel.from_orm(imageItem)
        session.add(db_image)
        session.commit()
        session.refresh(db_image)
        return db_image





@app.delete("/files/{image_id}")
def delete_file(image_id: str):
    file = read_file_from_id(image_id)
    file_name = file.name
    file_path = f"assets/{file_name}"
    _os.remove(file_path)
    with Session(engine) as session:
        image = session.get(ImageModel, image_id)
        if not image:
            raise HTTPException(status_code=404, detail="file not found")
        session.delete(image)
        session.commit()
        return {"ok": True}


@app.patch("/files/{image_id}", response_model=ImageModel)
def update_image(image_id: str, imageUp: UploadFile = File(...)):
    file = read_file_from_id(image_id)
    file_name = file.name
    file_path = f"assets/{file_name}"
    _os.remove(file_path)
    upload_image(imageUp)
    image = ImageModel(id=image_id, name=imageUp.filename)
    with Session(engine) as session:
        db_image = session.get(ImageModel, image_id)
        if not db_image:
            raise HTTPException(status_code=404, detail="file not found")
        image_data = image.dict(exclude_unset=True)
        for key, value in image_data.items():
            setattr(db_image, key, value)
        session.add(db_image)
        session.commit()
        session.refresh(db_image)
        return db_image
