import numpy as np


def insert(file_path, name, student_id, points):
    point_string = ""
    for point in points:
        point_string += ",{0}".format(point)

    string = "{0},{1}{2}\n".format(name, student_id, point_string)

    with open(file_path, 'a') as file:
        file.write(string)


def read(file_path):
    with open(file_path) as file:
        full_list = []
        for line in file:
            line = line[:-1]
            lst = line.split(',')

            name = lst[0]
            student_id = lst[1]
            points = []
            for item in lst[2:]:
                points.append(float(item))

            full_list.append([name, student_id, np.array(points)])

        return full_list
