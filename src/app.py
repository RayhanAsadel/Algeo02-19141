from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import os
import flask


UPLOAD_FOLDER = './static/text'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEXT_DIR'] = './text'


@app.route('/')
def index():
    return render_template('search2.html')
    
@app.route('/', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
       f = request.files['file[]']
       filename = secure_filename(f.filename)
       
       f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
       return render_template('search2uploadsucces.html')

@app.route('/about')
def about_files():
    return render_template('about.html')

@app.route('/text/<txt_name>')
def return_pdf(txt_name):
    try:
        return redirect(url_for('static', filename=app.config['TEXT_DIR'] + secure_filename(txt_name)))
    except:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)