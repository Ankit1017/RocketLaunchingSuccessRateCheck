from flask import Flask, flash, request, redirect, url_for, render_template,jsonify
import os
import numpy as np
from model import result
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['csv','xls'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
 
@app.route('/')
def index():
    return render_template('t1.html')
 
@app.route('/launch', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No csv selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        str=os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        x=str.replace(os.sep, '/')
        
        pred=result(x)
        print(pred)
        return render_template('t2.html', user = pred)
    else:
        flash('Allowed image types are - csv,xls')
        return redirect(request.url)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4000)   
    
    
   
