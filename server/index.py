import face_recognition
from rtree import index
from os.path import join
import os
import sys
import math
import heapq 
import numpy as np

ROOT = './data/'
EXT = '.jpg'

class RTree:
  idx = None
  id_person = {}
  face_encodings = {}
  def __init__(self):
    p = index.Property()
    p.dimension = 128 #D
    p.buffering_capacity = 10 #M
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    self.idx = index.Index('128d_index', properties=p)
    self.extract_features()
    self.insert_all()
  
  def extract_features(self):
    i = -1
    for base, dirs, files in os.walk(ROOT):
      i += 1
      encodings = []
      for file in files:
        img = join(base, file)
        if img.endswith(EXT):    
          picture = face_recognition.load_image_file(img)
          if len(face_recognition.face_encodings(picture)) > 0:
            encoding = face_recognition.face_encodings(picture)[0] # feature vector
            encodings.append(encoding)
        self.face_encodings[base.replace('./data/','')] = encodings
      if i >= 1:
        print(i, base)
    #print(self.face_encodings)
  
  def insert_all(self):   
    id = 0
    for person, encodings in self.face_encodings.items():
      for encoding in encodings:
        point = tuple(encoding)
        point += point
        self.id_person[id] = (person,encoding)
        self.idx.insert(id, point)
        id += 1
  
  def euclidian_distance(self, query_encoding, known_encoding):
    sum = 0
    for i in range(len(query_encoding)): #D=128
        sum += math.pow((query_encoding[i] - known_encoding[i]), 2)
    return math.sqrt(sum)

  def mindist(self, query, region):
    sum = 0
    for i in range(len(query)): #D=128
      r = None
      if query[i] < region[i]:
        r = region[i]
      elif query[i] > region[i + 128]:
        r = region[i + 128]
      else:
        r = query[i]
      sum += math.pow((query[i] - r), 2)
    return math.sqrt(sum)
  
  def sequential_knn(self, query, k_results):
    q = tuple(query)
    q += q
    lres = list(self.idx.nearest(coordinates=q, num_results=k_results))
    return lres #self.id_person[lres[0]]

  def search(self, query, k_results):
    heap = []
    self.priority_knn(heap, query, k_results)
    heap = [(person, -dist) for dist, person in heap]
    heap.sort(key=lambda tup:tup[1]) # O(k_results x log(k_results))
    return heap

  def priority_knn(self, heap, query, k_results):
    min_distance = sys.float_info.max
    leaf_region = None
    for leaf in self.idx.leaves():
      if self.mindist(query, leaf[2]) < min_distance: # leaf[2] -> region bounds
        min_distance = self.mindist(query, leaf[2])
        leaf_region = leaf
    for point in leaf_region[1]: # leaf_region[1] -> points
      person = self.id_person[point][0]
      encoding = self.id_person[point][1]
      distance = self.euclidian_distance(query, encoding)
      if len(heap) < k_results:
        heapq.heappush(heap, (-distance, person))
      else:
        r = heap[0] # front
        if distance <= -r[0]:
          heapq.heappush(heap, (-distance, person))
          heapq.heappop(heap)

# Adam Herbert
q = [-3.19065750e-02,  8.69898424e-02,  8.07745680e-02, -3.87815610e-02,
      2.28712019e-02, -1.39828399e-03, -6.87419176e-02, -4.42669354e-02,
      1.22500800e-01, -6.06134012e-02,  2.02753022e-01, -6.36082934e-03,
     -2.17242450e-01, -9.78881717e-02,  4.49896827e-02,  9.26477611e-02,
     -1.52959853e-01, -9.35620368e-02, -1.43870279e-01, -3.40235457e-02,
      1.75849479e-02, -2.83234473e-02,  5.63562773e-02, -3.50938644e-04,
     -1.05743632e-01, -3.70030224e-01, -9.04477760e-02, -6.96004331e-02,
      2.31702775e-02, -9.62972790e-02,  1.08853690e-02,  3.31265926e-02,
     -1.22479446e-01, -4.53323275e-02, -6.48580771e-03,  1.86511770e-01,
     -4.01124321e-02, -3.80056351e-02,  1.80485606e-01,  4.21522520e-02,
     -1.25692442e-01,  4.26428355e-02, -3.65151614e-02,  2.37538755e-01,
      2.43660599e-01,  9.46232602e-02,  2.16111876e-02, -7.63924718e-02,
      8.86106640e-02, -2.31042743e-01,  1.12985276e-01,  1.88004851e-01,
      9.78572965e-02,  1.29169047e-01,  8.78251567e-02, -1.17875651e-01,
      6.47547543e-02,  1.34579882e-01, -1.89067379e-01,  1.79654155e-02,
     -2.04601996e-02, -1.07527092e-01,  6.69555552e-03, -2.09217574e-02,
      1.25626385e-01,  1.18705645e-01, -6.49905577e-02, -1.14510834e-01,
      1.69617102e-01, -1.15009055e-01, -8.06217343e-02,  9.47106071e-03,
     -1.06643319e-01, -1.41750485e-01, -2.59348154e-01,  2.85650846e-02,
      3.53699714e-01,  1.22421354e-01, -2.37807542e-01,  2.14618072e-03,
     -1.14982933e-01, -1.06856585e-01,  2.72826552e-02,  2.93514766e-02,
     -6.31333664e-02, -7.60509595e-02, -1.12680361e-01, -1.43936723e-02,
      1.58955827e-01, -1.77538600e-02, -1.35961827e-03,  1.60439938e-01,
     -3.55376489e-03,  1.64712630e-02,  7.72328302e-02,  2.40266994e-02,
     -1.15281515e-01,  6.49038255e-02, -1.58196956e-01, -1.09264910e-01,
      6.59492612e-02, -1.52538687e-01, -2.91352905e-02,  3.32798883e-02,
     -2.33941197e-01,  2.14188188e-01,  5.02633415e-02, -3.62857021e-02,
      8.78258348e-02,  1.65613908e-02, -1.04529910e-01, -3.52109149e-02,
      2.60774076e-01, -2.42391914e-01,  2.14160234e-01,  2.67838150e-01,
      3.08285467e-02,  1.64190412e-01,  1.02699265e-01,  1.74490958e-01,
     -2.73696482e-02, -2.40529403e-02, -1.68477818e-01, -7.69579336e-02,
     -4.31553572e-02,  9.20310691e-02, -1.32388296e-02,  8.49268064e-02]
r_tree = RTree()
print(r_tree.search(q, 3))