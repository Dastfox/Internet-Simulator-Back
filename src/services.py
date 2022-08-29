import time
from fastapi import UploadFile
# from .main import ImageModel, Session, engine
import base64
import uuid




def _is_image(filename: str) -> bool:
    valid_extensions = (".png", ".png", ".gif", ".PNG", ".bmp", ".jpeg", "jpg")
    return filename.endswith(valid_extensions)


def renameFile(formData: UploadFile):
    if _is_image(formData.filename):
        image_name = rename_image(formData.filename)
        with open(f"assets/{image_name}", "wb+") as image_file_upload:
            image_file_upload.write(formData.file.read())
        return image_name
    return None

def rename_image(filename: str):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    lastChars = filename[-5:]
    return timestr + lastChars.replace(" ", "-")

def get_a_uuid() -> str :
    id32 = uuid.uuid4
    str(id32)
    return id32