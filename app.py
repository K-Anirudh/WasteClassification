#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
from Logic import pred
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
file_arr = []
pred_class_arr = []
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index2.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file1' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file1 = request.files['file1']
    if file1.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file1 and allowed_file(file1.filename):
        filename1 = secure_filename(file1.filename)
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))

        # print('upload_image filename: ' + filename)
        #flash('Image successfully uploaded and displayed below')
        # flash('\n FileName = '+filename)
        f1 = UPLOAD_FOLDER+filename1
        print('FileName1 = '+filename1)
        #Processing the images
        pred_class = pred(file1)
        pred_class_arr.append(pred_class)
        flash("It is a "+pred_class+" waste")
        file_arr.append(filename1)
        return render_template('index2.html', filename1=filename1)

    else:
        flash('Allowed image types are - png, jpg, jpeg')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)




if __name__ == "__main__":
    app.debug = True
    app.run()