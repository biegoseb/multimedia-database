from flask import Flask, request, Response
from flask_cors import CORS
import json, sys, os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './queries/'
index = RTree()

CORS(app)

@app.route('/query/<k>', methods=["POST"])
def query(k):
  file = request.files['file']
  if file.filename != '':
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    q = get_img_vector(file)
    lres = index.priority_knn(q, k)
  return Response(json.dumps(lres), status = 202, mimetype="application/json")


if __name__ == '__main__':
    # index.create_inverted_index()
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
