import face_recognition
from rtree import index
from os.path import join
import sys, os
import math
import heapq 
import numpy as np

PATH = './data/'
EXT = '.jpg'

id_person = {}
face_encodings = {}

def clear_files():
  for base, dirs, files in os.walk('./'):
    if '128d.data' in files:
      os.remove('128d.data')
    if '128d.index' in files:
      os.remove('128d.index')

def euclidian_distance(query_encoding, known_encoding):
  sum = 0
  for i in range(len(query_encoding)): #D=128
      sum += math.pow((query_encoding[i] - known_encoding[i]), 2)
  return math.sqrt(sum)

def sequential_knn(query, k_results):
  result = []
  for person, encodings in face_encodings.items(): # O(N x D)
    for encoding in encodings:
      dist = euclidian_distance(query, encoding)
      result.append((person, dist))
  result.sort(key=lambda tup:tup[1]) # O(N x logN)
  return result[:k_results]

def get_img_vector(img):
  picture = face_recognition.load_image_file(img)
  try:
    encoding = face_recognition.face_encodings(picture)[0] # feature vector
    return encoding
  except IndexError as e:
    print(e, "No face detected")


class RTree:
  idx = None
  def __init__(self):
    p = index.Property()
    p.dimension = 128 #D
    p.buffering_capacity = 10 #M
    p.dat_extension = 'data'
    p.idx_extension = 'index'
    self.idx = index.Index('128d', properties=p)
    self.extract_features()
    self.insert_all()
  
  def extract_features(self):
    i = -1
    for base, dirs, files in os.walk(PATH):
      i += 1
      encodings = []
      for file in files:
        img = join(base, file)
        if img.endswith(EXT):    
          picture = face_recognition.load_image_file(img)
          if len(face_recognition.face_encodings(picture)) > 0:
            encoding = face_recognition.face_encodings(picture)[0] # feature vector
            encodings.append(encoding)
        face_encodings[base.replace('./data/','')] = encodings
      #if i >= 1:
      #  print(i, base)
    #print(face_encodings)
  
  def insert_all(self):   
    id = 0
    for person, encodings in face_encodings.items():
      for encoding in encodings:
        point = tuple(encoding)
        point += point
        id_person[id] = (person,encoding)
        self.idx.insert(id, point)
        id += 1

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

  def priority_knn(self, query, k_results):
    heap = []
    min_distance = sys.float_info.max
    leaf_region = None
    for leaf in self.idx.leaves():
      print('hola')
      if self.mindist(query, leaf[2]) < min_distance: # leaf[2] -> region bounds
        min_distance = self.mindist(query, leaf[2])
        leaf_region = leaf
    for point in leaf_region[1]: # leaf_region[1] -> points
      person = id_person[point][0]
      encoding = id_person[point][1]
      distance = euclidian_distance(query, encoding)
      if len(heap) < k_results:
        heapq.heappush(heap, (-distance, person))
      else:
        r = heap[0] # front
        if distance <= -r[0]:
          heapq.heappush(heap, (-distance, person))
          heapq.heappop(heap)
    heap = [(person, -dist) for dist, person in heap]
    heap.sort(key=lambda tup:tup[1]) # O(k_results x log(k_results))
    return heap

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

# Sagasti
sagasti = [-0.04388325,  0.08636447,  0.00740112, -0.11340982, -0.07251073,  0.06708346,
           -0.00214581, -0.05114206,  0.14976943,  0.00068636,  0.1698042 , -0.03777033,
           -0.26229391,  0.04498326, -0.05950817,  0.07186246, -0.22964758,  0.01412559,
           -0.22676213, -0.15868887, -0.02888724,  0.15669826,  0.09247879,  0.00218791,
           -0.09244427, -0.27623978, -0.07943413, -0.13096462,  0.10875303, -0.11547134,
            0.04305288, -0.02516632, -0.20949079, -0.07785788,  0.06227748, -0.0361296,
           -0.07694005, -0.09169348,  0.13331431,  0.02937641, -0.06195091,  0.02420534,
            0.09387225,  0.22266592,  0.18958504,  0.08399098, -0.00851541, -0.11568355,
            0.07180073, -0.28698865,  0.17485631,  0.10737325,  0.10871355,  0.07405763,
            0.16998234, -0.17623222,  0.00128484,  0.13433544, -0.08543238,  0.13344043,
            0.07027915,  0.00834422, -0.02108626, -0.04548386,  0.10838822,  0.073659,
           -0.07993541, -0.17658746,  0.09692895, -0.14512962, -0.04623122,  0.09002209,
           -0.05711326, -0.15257491, -0.2654441 ,  0.05597412,  0.48137558,  0.18501423,
           -0.19346209, -0.0175518 , -0.12415781, -0.04067444,  0.08482124,  0.04761392,
           -0.09880095, -0.10778631, -0.05232498,  0.03266819,  0.16248484, -0.06929194,
           -0.11913073,  0.18797506, -0.00497043, -0.0391056 ,  0.01995035, -0.00416033,
           -0.15566687, -0.01692763, -0.07490887, -0.02968643,  0.02580032, -0.069192,
           -0.05955453,  0.09933162, -0.16125791,  0.1779259 ,  0.01008272, -0.13790442,
            0.03126442,  0.01375106, -0.08122745, -0.01843515,  0.20970128, -0.30781066,
            0.21092011,  0.19706464, -0.00336648,  0.18440998,  0.0130247 ,  0.13745371,
            0.05147406,  0.09820212, -0.10302395, -0.14900856,  0.00138092,  0.00886786,
           -0.01493349,  0.0097323]

'''
clear_files()
r_tree = RTree()
print("Priority KNN  : ", r_tree.priority_knn(q, 3))
print("Sequential KNN: ", sequential_knn(q, 3))
#v = get_img_vector('data/Adam_Scott/Adam_Scott_0001.jpg')
#print(v)
'''