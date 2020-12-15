from flask import Flask, request, Response, render_template, redirect
from flask_cors import CORS
from werkzeug.utils import secure_filename
import r_tree
import json
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './queries/'

CORS(app)

@app.route('/query', methods=["POST"])
def query():
  file = request.files['file']
  k = json.loads(request.form['data'])['k']
  if file.filename != '':
    filename = secure_filename(file.filename)
  file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  q = r_tree.get_img_vector(file)
  lres = index.priority_knn(q, k)
  return Response(json.dumps(lres), status = 202, mimetype="application/json")

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    r_tree.clear_files()
    index = r_tree.RTree()
    app.secret_key = ".."
    app.run(port=8082, threaded=True, host=('127.0.0.1'))