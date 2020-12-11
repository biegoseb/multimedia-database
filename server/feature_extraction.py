import face_recognition
import os
from os.path import join
import math

root = './data3/'
ext = '.jpg'

face_encodings = {}
def extract_features():
  c = 0
  for base, dirs, files in os.walk(root):
    for file in files:
      img = join(base, file)
      #images = []
      c += 1
      print(c,img)
      if img.endswith(ext):    
        picture = face_recognition.load_image_file(img)
        try:
          encoding = face_recognition.face_encodings(picture)[0] # feature vector
        except IndexError as e:
          print(e)
        face_encodings[img] = encoding
  #print(face_encodings)
  return face_encodings


print(extract_features())