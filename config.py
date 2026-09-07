KNOWN_FACES_DIR = "known_faces"

TARGET_PEOPLE = {
    "antsa",
    "alice",
}

PROCESS_EVERY = 10
FACE_DISTANCE_THRESHOLD = 0.50
FRAME_SCALE = 0.25
CAMERA_INDEX = 0

# "cnn" detection model when True, "hog" when False.
# Requires dlib built with CUDA (dlib.DLIB_USE_CUDA).
USE_GPU = False
