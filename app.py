from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import insert_new_face
import compare_face
import numpy as np
import dlib
import get_face_points
from imageio import imread
import io
import base64
import ast

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    return "...listening..."


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
    return response


app.after_request(add_cors_headers)


@app.route('/face_recognition', methods=['GET', 'POST'])
@cross_origin()
def face_recognition():
    if request.method == 'POST':
        print(request.data)
        req = ast.literal_eval(request.data.decode("utf-8"))
        image_base64 = bytes(req["image"], 'utf-8')

        with open("temp.jpg", 'wb') as file:
            image_bytes = base64.decodebytes(image_base64)
            file.write(image_bytes)

        image = dlib.load_rgb_image("temp.jpg")

        full_array = insert_new_face.read("data.txt")

        descriptor = [i[2] for i in full_array]
        descriptor = np.array(descriptor)
        match = compare_face.closest_match(get_face_points.get_face_points(image), descriptor)
        print(match)

        if match:
            return str(full_array[match][:2]) + str(match)
        else:
            return str(None)

    else:
        return "Waiting for image"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
