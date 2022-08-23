import time
from fastapi import UploadFile
# from .main import ImageModel, Session, engine





def _is_image(filename: str) -> bool:
    valid_extensions = (".png", ".png", ".gif", ".PNG", ".bmp", ".jpeg", "jpg")
    return filename.endswith(valid_extensions)


def upload_image(image: UploadFile):
    if _is_image(image.filename):
        image_name = rename_image(image.filename)
        with open(f"assets/{image_name}", "wb+") as image_file_upload:
            image_file_upload.write(image.file.read())
        return image_name
    return None

def rename_image(filename: str):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return timestr + filename.replace(" ", "-")