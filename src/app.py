from flask import Flask, render_template, url_for, request, redirect
from werkzeug.utils import secure_filename
import os
import flask
from data import *


UPLOAD_FOLDER = './static/text'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEXT_DIR'] = './text'

@app.route('/', methods=['GET'])
@app.route('/search', methods=['GET'])
def search_page():
    if request.method=='GET':
        query = request.args.get('s')

    if not query:
        return render_template('search.html')
    else:
        stemmed_query = stemstring(query)

        unique = get_unique(stemmed_file,stemmed_query)
        bowlist = get_bow(stemmed_file,unique)
        bow_query1 = bow_query(stemmed_query,unique)
        sorted_result = get_result(bowlist,bow_query1)
        files_qty1 = files_qty
        #Dapatkan dataframe untuk termtable
        termtable = pd.DataFrame()
        termtable = get_term_table(stemmed_query,bow_query1,bowlist)
        termtable.add_prefix('d')

        #render dataframe as html
        html = termtable.add_prefix('d').to_html()

        #Mengwrite termtable ke html pada folder templates
        path = os.getcwd()
        with open(os.path.join(path,'templates','termtable.html'), "w") as file1:
            file1.write(html)
            file1.close()
        
        return render_template('results.html', query = query, sorted_result=sorted_result, stemmed_query=stemmed_query, bow_query=bow_query1, bowlist=bowlist, files_qty = files_qty1)

@app.route('/upload', methods = ['GET'])
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods = ['POST'])
def upload_file():
   if request.method == 'POST':
       f = request.files['file[]']
       filename = secure_filename(f.filename)
       
       f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
       return render_template('upload_success.html')
    
@app.route('/about')
def about_files():
    return render_template('about.html')

@app.route('/text/<txt_name>')
def return_txt(txt_name):
    try:
        return redirect(url_for('static', filename=app.config['TEXT_DIR'] + secure_filename(txt_name)))
    except:
        abort(404)
@app.route('/table')
def print_term_table():
    return render_template('termtable.html')

if __name__ == "__main__":
    app.run(debug=True)