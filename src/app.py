from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import os
import flask


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
@app.route('/')
def index():
    
    return render_template('search2.html')
    
@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       f = request.files['dokumentxt']
       filename = secure_filename(f.filename)
       
       f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
       return render_template('search2uploadsucces.html')

if __name__ == "__main__":
    app.run(debug=True)