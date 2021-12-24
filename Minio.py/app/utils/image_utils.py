
from io import BytesIO
from os import remove
from PIL import Image
import base64
from werkzeug.datastructures import FileStorage
# import cv2
def read_file(file: FileStorage):
    return Image.open(file)

def convert_format_of_image(file,filename , format = 'JPEG'):
    file = file.convert('RGB')
    file.save(f"images/{filename}", format)
    new_file = open(f"images/{filename}",mode="rb")
    remove(f"images/{filename}")
    return new_file
    
def resize_image(file ,size = (1280,720)):
        return file.resize(size)

