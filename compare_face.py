import sys
import numpy as np


def dlibVect_to_numpyNDArray(vector):
    array = np.zeros(shape=128)
    for i in range(0, len(vector)):
        array[i] = vector[i]
    return array


def closest_match(face, descriptors):
    if not face:
        return None

    minimum = 5
    min_index = 0
    for index, known_face in enumerate(descriptors):
        current = np.linalg.norm(face - known_face, axis=0)
        if current < minimum and current < .4:
            minimum = current
            min_index = index

    if minimum > 3:
        return None
    else:
        return min_index


def compare_face(face_vector_known, face_vector_new):

    points_1 = dlibVect_to_numpyNDArray(face_vector_known)
    points_2 = dlibVect_to_numpyNDArray(face_vector_new)
    return np.linalg.norm(points_1 - points_2, axis=0)






