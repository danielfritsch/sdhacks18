import dlib


def get_face_points(face):
    predictor_path = "DlibDetectors/shape_predictor_68_face_landmarks.dat"
    recognizer_path = "DlibDetectors/dlib_face_recognition_resnet_model_v1.dat"

    face_detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictor_path)
    recognizer = dlib.face_recognition_model_v1(recognizer_path)

    bounding_rects = face_detector(face)

    if len(bounding_rects) > 0:
        bounding_rect = bounding_rects[0]
    else:
        return None
    shape = predictor(face, bounding_rect)
    descriptor = recognizer.compute_face_descriptor(face, shape)

    return descriptor

