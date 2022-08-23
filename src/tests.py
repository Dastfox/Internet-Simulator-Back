from dataclasses import field
from email.policy import default
from typing import List, Optional
import os as _os
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, String, create_engine, select
import random as _random



def _get_image_filenames(directory_name: str) -> List[str]: 
    return _os.listdir(directory_name)

def select_random_image(directory_name: str) -> str:
    # sourcery skip: inline-immediately-returned-variable
    images = _get_image_filenames(directory_name)
    random_image = _random.choice(images)
    path = f"{directory_name}/{random_image}"
    return print(path)

def get_random_file():
    image_path = select_random_image('assets')
    return print(image_path)

get_random_file()