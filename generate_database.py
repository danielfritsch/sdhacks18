import dlib
from os import listdir
from os.path import isfile, join
import insert_new_face
from get_face_points import *


onlyfiles = [f for f in listdir("TestImages")]

for num, file_path in enumerate(onlyfiles):
    face = dlib.load_rgb_image("TestImages/" + file_path)
    points = get_face_points(face)
    insert_new_face.insert("data.txt", "{0}".format(file_path[:-3]), num, points)
