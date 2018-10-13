import numpy as np
import insert_new_face
import compare_face
from get_face_points import *
import sys


full_array = insert_new_face.read("students.txt")

descriptor = [i[2] for i in full_array]
descriptor = np.array(descriptor)

new_face_path = sys.argv[1]
new_face = dlib.load_rgb_image(new_face_path)
new_points = get_face_points(new_face)

index = compare_face.closest_match(new_points, descriptor)
if index:
    print(full_array[index])
else:
    print("none found")

