import os
import glob

from datetime import datetime
from zipfile import ZipFile
from module_app import app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTS']

def getTime():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%H%M%S")
    return(timestampStr)

def zip_files(source_folder):
    archive_path = app.config['DONE_FOLDER'] + "\\" + app.config['ARCHIVE_NAME'] + getTime() + ".zip"
    archive_name = app.config['ARCHIVE_NAME'] + getTime() + ".zip"

    with ZipFile(archive_path, 'w') as zipObj:
        for file in os.listdir(source_folder):
            print(f"Added {file} to archive.")
            zipObj.write(source_folder + "\\" + file, arcname=file)

    return archive_name

def clear_folder(folderpath):
    files = glob.glob(folderpath+"\\"+"*")
    for f in files:
        print(f"Removed {f}")
        os.remove(f)