import cv2
import face_recognition
import os
import numpy as np
import time

from config import (
    KNOWN_FACES_DIR,
    TARGET_PEOPLE,
    PROCESS_EVERY,
    FACE_DISTANCE_THRESHOLD,
    FRAME_SCALE,
    CAMERA_INDEX,
    USE_GPU,
)

from pip_control import hide_pip


known_faces = {}


def load_known_faces():

    if not os.path.exists(KNOWN_FACES_DIR):

        os.makedirs(KNOWN_FACES_DIR)

        print(
            f"Created '{KNOWN_FACES_DIR}/'"
        )

        print(
            "Create a folder for each person and "
            "put their photos inside."
        )

        return

    for person_name in sorted(
        os.listdir(KNOWN_FACES_DIR)
    ):

        person_dir = os.path.join(
            KNOWN_FACES_DIR,
            person_name
        )

        if not os.path.isdir(person_dir):
            continue

        encodings = []

        print()
        print(
            f"Loading person: {person_name}"
        )

        for filename in sorted(
            os.listdir(person_dir)
        ):

            if not filename.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            ):
                continue

            path = os.path.join(
                person_dir,
                filename
            )

            print(
                f"  Loading {filename}..."
            )

            try:

                image = (
                    face_recognition
                    .load_image_file(path)
                )

                face_locations = (
                    face_recognition.face_locations(
                        image
                    )
                )

                if not face_locations:

                    print(
                        f"    WARNING: No face found "
                        f"in {filename}"
                    )

                    continue

                if len(face_locations) > 1:

                    print(
                        f"    WARNING: Multiple faces "
                        f"found in {filename}"
                    )

                    print(
                        "    Using the first face."
                    )

                image_encodings = (
                    face_recognition.face_encodings(
                        image,
                        face_locations
                    )
                )

                if not image_encodings:

                    print(
                        f"    WARNING: Could not encode "
                        f"face in {filename}"
                    )

                    continue

                encodings.append(
                    image_encodings[0]
                )

                print(
                    "    OK"
                )

            except Exception as e:

                print(
                    f"    ERROR: {e}"
                )

        if encodings:

            known_faces[person_name] = encodings

            print(
                f"  Registered {person_name}: "
                f"{len(encodings)} photos"
            )

        else:

            print(
                f"  WARNING: No usable photos "
                f"for {person_name}"
            )


def recognize_faces(frame):

    small_frame = cv2.resize(
        frame,
        (0, 0),
        fx=FRAME_SCALE,
        fy=FRAME_SCALE
    )

    rgb_frame = cv2.cvtColor(
        small_frame,
        cv2.COLOR_BGR2RGB
    )

    detection_model = "cnn" if USE_GPU else "hog"

    face_locations = (
        face_recognition.face_locations(
            rgb_frame,
            model=detection_model
        )
    )

    face_encodings = (
        face_recognition.face_encodings(
            rgb_frame,
            face_locations
        )
    )

    results = []

    for face_encoding, location in zip(
        face_encodings,
        face_locations
    ):

        best_name = "Unknown"
        best_distance = float("inf")

        for person_name, person_encodings in (
            known_faces.items()
        ):

            distances = face_recognition.face_distance(
                person_encodings,
                face_encoding
            )

            person_best_distance = np.min(
                distances
            )

            if person_best_distance < best_distance:

                best_distance = (
                    person_best_distance
                )

                best_name = person_name

        if best_distance > FACE_DISTANCE_THRESHOLD:

            best_name = "Unknown"

        top, right, bottom, left = location

        top = int(top / FRAME_SCALE)
        right = int(right / FRAME_SCALE)
        bottom = int(bottom / FRAME_SCALE)
        left = int(left / FRAME_SCALE)

        results.append(
            (
                best_name,
                best_distance,
                (top, right, bottom, left)
            )
        )

    return results


def main():

    print()
    print(
        "=========================================="
    )
    print(
        "       Offline Face Recognition"
    )
    print(
        "=========================================="
    )

    print()
    print(
        f"Detection mode: "
        f"{'GPU/CNN' if USE_GPU else 'CPU/HOG'}"
    )

    load_known_faces()

    print()
    print(
        f"Registered people: {len(known_faces)}"
    )

    if not known_faces:

        print()
        print(
            "No usable faces found."
        )

        return

    print()
    print(
        "Target people:"
    )

    for person in TARGET_PEOPLE:

        if person in known_faces:

            print(
                f"  [OK] {person}"
            )

        else:

            print(
                f"  [WARNING] {person} "
                f"has no registered photos"
            )

    print()
    print(
        "Starting camera..."
    )

    cap = cv2.VideoCapture(
        CAMERA_INDEX
    )

    if not cap.isOpened():

        print(
            "ERROR: Could not open camera."
        )

        return

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )

    frame_count = 0
    recognized_faces = []
    pip_hidden = False

    fps = 0

    last_time = time.time()
    frame_counter = 0

    print()
    print(
        "Running."
    )
    print(
        "Press Q to quit."
    )
    print()

    while True:

        ret, frame = cap.read()

        if not ret:

            print(
                "ERROR: Could not read frame."
            )

            break

        frame_count += 1
        frame_counter += 1

        if frame_count % PROCESS_EVERY == 0:

            recognized_faces = (
                recognize_faces(frame)
            )

            detected_targets = {
                name
                for name, distance, location
                in recognized_faces
                if name in TARGET_PEOPLE
            }

            if detected_targets:

                if not pip_hidden:

                    print(
                        "[TARGET DETECTED] "
                        + ", ".join(
                            sorted(detected_targets)
                        )
                    )

                    if hide_pip():

                        print(
                            "[PiP] Hidden"
                        )

                        pip_hidden = True

                    else:

                        print(
                            "[PiP] Not found"
                        )

            else:

                if pip_hidden:

                    print(
                        "[TARGET LEFT]"
                    )

                pip_hidden = False

        for (
            name,
            distance,
            (top, right, bottom, left)
        ) in recognized_faces:

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

            label = (
                f"{name} "
                f"{distance:.2f}"
            )

            cv2.rectangle(
                frame,
                (left, bottom - 35),
                (right, bottom),
                (0, 255, 0),
                cv2.FILLED
            )

            cv2.putText(
                frame,
                label,
                (left + 6, bottom - 8),
                cv2.FONT_HERSHEY_DUPLEX,
                0.7,
                (0, 0, 0),
                1
            )

        now = time.time()

        elapsed = now - last_time

        if elapsed >= 1.0:

            fps = (
                frame_counter /
                elapsed
            )

            frame_counter = 0
            last_time = now

        cv2.putText(
            frame,
            f"Camera: {fps:.1f} FPS",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            (
                f"Recognition: "
                f"1/{PROCESS_EVERY} frames"
            ),
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        pip_status = (
            "PiP: hidden"
            if pip_hidden
            else "PiP: normal"
        )

        cv2.putText(
            frame,
            pip_status,
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Offline Face Recognition",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()