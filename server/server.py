from flask import Flask, request, Response, render_template, redirect
from flask_cors import CORS
from werkzeug.utils import secure_filename
import r_tree
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './queries/'
r_tree.clear_files()
index = r_tree.RTree()

CORS(app)

@app.route('/query', methods=["POST"])
def query():
  """ if request.files:
    image = request.files['image']
    image.save(app.config['UPLOAD_FOLDER'], image.filename)
    print("img saved")
    return redirect(request.url)
  return render_template("public/upload_image.html") """

  print(request.files)
  file = request.files['image']
  print(request.form)
  k = request.form['k']
  print('debug2')
  if file.filename != '':
    print('debug3')
    filename = secure_filename(file.filename)
    print('debug4')
  file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
  print('debug5')
  q = r_tree.get_img_vector(file)
  print('debug6')
  lres = index.priority_knn(q, k)
  print('debug7')
  return Response(json.dumps(lres), status = 202, mimetype="application/json")

@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # index.create_inverted_index()
    app.secret_key = ".."
    app.run(port=8082, threaded=True, host=('127.0.0.1'))