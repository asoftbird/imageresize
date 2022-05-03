import os

class Config(object):
    CURRENT_DIR = os.getcwd()
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asdf'
    ALLOWED_EXTS = {"png", "jpg", "jpeg"}
    UPLOADS_FOLDER  = CURRENT_DIR + '\\' + 'uploads'
    PROCESSED_FOLDER = CURRENT_DIR + '\\' + 'processed'
    DONE_FOLDER = CURRENT_DIR + '\\' + 'done' 
    ARCHIVE_NAME = "compressed_imgs"