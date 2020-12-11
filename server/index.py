import face_recognition
from rtree import index
import os
from os.path import join
import math
from queue import PriorityQueue
import numpy as np

ROOT = './data3/'
EXT = '.jpg'

def extract_features():
  face_encodings = {}
  c = 0
  for base, dirs, files in os.walk(ROOT):
    for file in files:
      img = join(base, file)
      c += 1
      print(c,img)
      if img.endswith(EXT):    
        picture = face_recognition.load_image_file(img)
        try:
          encoding = face_recognition.face_encodings(picture)[0] # feature vector
        except IndexError as e:
          print(e)
        face_encodings[img] = encoding
  return face_encodings


print(extract_features())

class RTree:
  idx = None
  def __init__(self):
    p = index.Property()
    p.dimension = 128 #D
    p.buffering_capacity = 10 #M
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    self.idx = index.Index('multimedia_index', properties=p)
  
  def insert(self, features_vectors):
    id = 0
    for img, vector in features_vectors:
      self.idx.insert(id, (vector, vector), img)
      id += 1
  
  def euclidian_distance(self, query_encoding, known_encoding):
    #sum = 0
    #for i in range(len(query_encoding)): #128
    #    sum += math.pow((query_encoding[i] - known_encoding[i]), 2)
    #return math.sqrt(sum)
    a = np.array(query_encoding)
    b = np.array(known_encoding)
    return np.linalg.norm(a[:, None, :] - b[None, :, :], axis=-1)

  def sequential_knn(self, query, k_results):
    #queue = PriorityQueue()
    #for img, enconding in
    pass

  def priority_knn(self, query, k_results):
    pass

q = [-8.17060545e-02,  1.10632911e-01,  1.34635970e-01, -1.34403482e-01,
       -1.03805944e-01,  8.44166055e-02, -1.04080759e-01, -4.16047908e-02,
        1.95701629e-01, -1.67427927e-01,  1.79220498e-01,  4.48846333e-02,
       -2.17200279e-01,  6.77665472e-02, -3.55402976e-02,  2.01166853e-01,
       -2.27251306e-01, -5.37830144e-02, -7.88426325e-02, -2.99380627e-02,
       -5.41799702e-03,  8.20221528e-02, -1.25187682e-04,  6.92237914e-02,
       -1.15610182e-01, -3.63576800e-01, -6.08736798e-02, -6.05255850e-02,
       -2.44289264e-02, -5.58598526e-02, -7.78094083e-02, -2.90645007e-02,
       -6.81176335e-02,  5.42129278e-02,  6.98324293e-04,  7.18935579e-02,
       -7.29248151e-02, -1.48384139e-01,  1.47973537e-01,  5.41693382e-02,
       -2.34226465e-01,  3.83732170e-02,  2.91751847e-02,  2.40074784e-01,
        3.28711182e-01, -4.04151827e-02,  4.47870456e-02, -2.15760060e-02,
        1.78307265e-01, -3.14212501e-01,  2.04810128e-02,  1.35312125e-01,
        3.91880274e-02,  6.35476112e-02,  1.31961435e-01, -8.78701955e-02,
       -3.88183370e-02,  1.23081788e-01, -1.28752261e-01, -2.97301523e-02,
        4.80069965e-02, -9.37548839e-03,  4.22566161e-02, -2.79410984e-02,
        1.64822400e-01,  1.41396657e-01, -1.61143333e-01, -1.78153545e-01,
        1.48894235e-01, -1.58329651e-01, -4.88454066e-02,  5.30780666e-02,
       -1.78077221e-01, -1.90231964e-01, -1.94352537e-01,  4.54105809e-02,
        3.89185637e-01,  2.28393301e-01, -1.17950879e-01,  1.46170231e-02,
       -1.09868877e-01, -3.77075411e-02,  4.81450930e-02,  1.11299857e-01,
        4.63757925e-02, -4.51420099e-02, -4.33302820e-02,  5.20643741e-02,
        1.98564082e-01, -3.14868465e-02, -2.29052585e-02,  2.81788141e-01,
        2.89902501e-02, -4.97175492e-02, -1.45653421e-02,  9.27092656e-02,
       -1.35954052e-01,  2.73514017e-02, -1.44894689e-01, -5.45141473e-02,
        3.24090123e-02,  3.19179222e-02,  5.52787185e-02,  1.46901757e-01,
       -1.94407806e-01,  2.09360659e-01, -5.40934764e-02,  2.66586021e-02,
        6.41235709e-02,  4.35599200e-02, -1.08820818e-01, -2.82902420e-02,
        1.68558180e-01, -2.08340645e-01,  8.23031738e-02,  1.56753868e-01,
        2.41979342e-02,  8.08062181e-02,  5.07892706e-02,  3.29900756e-02,
        3.31640169e-02, -2.94894800e-02, -1.33808047e-01, -8.35199803e-02,
       -1.20777534e-02,  6.05441816e-03,  3.82863060e-02,  1.89689863e-02]

idx1 = RTree()
lres = list(idx1.idx.nearest(coordinates=q, num_results=3))
print("Vecino mas cercano es: ", lres)