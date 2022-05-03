import os
from flask import request, redirect, render_template, send_from_directory, url_for
from werkzeug.utils import secure_filename
from module_app import app, hlpfnc, compress_image



@app.route('/done/<name>')
def download_single(name):
    return send_from_directory(app.config["DONE_FOLDER"], name), hlpfnc.clear_folder(app.config['UPLOADS_FOLDER']), hlpfnc.clear_folder(app.config['PROCESSED_FOLDER'])

def servefile(filename):
    render_template('index.html', UPLOAD_STATUS="", DOWNLOAD_URL=filename, DOWNLOAD_TEXT="Download file")



@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global UPLOAD_STATUS
    global FILECOUNT
    UPLOAD_STATUS = ""
    FILECOUNT = 0
    
    if request.method == 'POST':

        hlpfnc.clear_folder(app.config['DONE_FOLDER'])
        # check if the post request has the file part
        if "button_upload" in request.form:
            if 'file' not in request.files:
                pass
            files = request.files.getlist('file')
            quality = int(request.form.get('i_quality'))
            desired_size = int(request.form.get('i_size'))
            blur = float(request.form.get('i_blur'))
            padding = bool(request.form.get('ck_padding'))
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            for file in files:
                if file.filename == '':
                    # flash('No selected file')
                    UPLOAD_STATUS = "No files selected!"
                    return render_template('index.html', UPSTAT=UPLOAD_STATUS)

                if file and hlpfnc.allowed_file(file.filename):
                    FILECOUNT += 1
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOADS_FOLDER'], filename))

            
            if FILECOUNT > 1:
                for file in os.listdir(app.config['UPLOADS_FOLDER']):
                    filepath = app.config['UPLOADS_FOLDER'] + "\\" + file
                    filename = file[:-4]
                    compress_image.resample_image(filepath, filename, desired_size, quality, blur, padding, app.config['PROCESSED_FOLDER'])  
                zipfile = hlpfnc.zip_files(app.config['PROCESSED_FOLDER'])
                print(f" {zipfile}, {app.config['PROCESSED_FOLDER']}")
                app.add_url_rule('/done/<filename>', '/done/<filename>', servefile)
                return render_template('index.html', UPLOAD_STATUS="", DOWNLOAD_URL="/done/" + zipfile, DOWNLOAD_TEXT="Download file")
            if FILECOUNT == 1:
                for file in os.listdir(app.config['UPLOADS_FOLDER']):
                    filepath = app.config['UPLOADS_FOLDER'] + "\\" + file
                    filename = file[:-4]
                    downloadfile = compress_image.resample_image(filepath, filename, desired_size, quality, blur, padding, app.config['DONE_FOLDER'])
                app.add_url_rule('/done/<filename>', '/done/<filename>', servefile)
                return render_template('index.html', UPSTAT="", DOWNLOAD_URL=url_for('download_single', name=downloadfile), DOWNLOAD_TEXT="Download file")

        if "button_clear" in request.form:
            hlpfnc.clear_folder(app.config['PROCESSED_FOLDER'])
            hlpfnc.clear_folder(app.config['UPLOADS_FOLDER'])
            hlpfnc.clear_folder(app.config['DONE_FOLDER'])
            


    return render_template('index.html', UPSTAT=UPLOAD_STATUS, DOWNLOAD_URL="", DOWNLOAD_TEXT="")
