# Offline Face Recognition + PiP Control

A local Python application that uses a webcam to recognize configured people and hide a Firefox Picture-in-Picture window when they are detected.

## Project Structure

```text
project/
├── main.py
├── config.py
├── pip_control.py
├── known_faces/
│   ├── antsa/
│   │   ├── 01.jpg
│   │   └── 02.jpg
│   └── alice/
│       ├── 01.jpg
│       └── 02.jpg
└── README.md
```

Each folder inside `known_faces/` represents one person.

## Installation

```bash
sudo apt install python3-pip python3-venv cmake build-essential wmctrl

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Configuration

All settings are in `config.py`:

```python
KNOWN_FACES_DIR = "known_faces"

TARGET_PEOPLE = {
    "antsa",
    "alice",
}

PROCESS_EVERY = 10
FACE_DISTANCE_THRESHOLD = 0.50
FRAME_SCALE = 0.25
CAMERA_INDEX = 0
```

| Variable                  | Description                                     |
| ------------------------- | ----------------------------------------------- |
| `KNOWN_FACES_DIR`         | Directory containing reference photos           |
| `TARGET_PEOPLE`           | People who trigger PiP hiding                   |
| `PROCESS_EVERY`           | Run recognition every N frames                  |
| `FACE_DISTANCE_THRESHOLD` | Recognition strictness. Lower = stricter        |
| `FRAME_SCALE`             | Image size used for recognition. Lower = faster |
| `CAMERA_INDEX`            | Camera index (`0` = default camera)             |

## Running

```bash
source venv/bin/activate
python main.py
```

Press `Q` to exit.
::

## PiP Control

`pip_control.py` controls what happens to the PiP when a target person is detected.

You can edit this file to decide how the PiP should be handled by the system:

* Hide the PiP
* Close the PiP
* Kill the PiP process
* Use another method

The face-recognition system only detects the target and calls `pip_control.py`. The actual PiP handling is up to your implementation.

