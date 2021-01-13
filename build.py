from flask import Flask, render_template, request, url_for, redirect, send_from_directory, flash
from werkzeug import secure_filename
import os




# Flask is WSGI application instance
myapp = Flask(__name__, template_folder='template')  # Create an instance


myapp.config['UPLOAD_FOLDER'] = 'D:/AI_platform'
myapp.config['MAX_CONTENT_PATH'] = 500000000


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['.png', '.jpg']

@myapp.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(myapp.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@myapp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(myapp.config['UPLOAD_FOLDER'], filename)



    

if __name__ == '__main__':
    myapp.run(debug=True)