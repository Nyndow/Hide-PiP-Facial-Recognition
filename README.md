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

### Linux

Install the required system packages according to your distribution.

**Ubuntu / Debian**

```bash
sudo apt install python3-pip python3-venv cmake build-essential wmctrl
```

**Arch / EndeavourOS**

```bash
sudo pacman -S python-pip python-virtualenv cmake base-devel wmctrl
```

**Fedora**

```bash
sudo dnf install python3-pip python3-virtualenv cmake gcc gcc-c++ make wmctrl
```

**openSUSE**

```bash
sudo zypper install python3-pip python3-virtualenv cmake gcc gcc-c++ make wmctrl
```

Then create the virtual environment and install the Python dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Windows

Install Python 3 and CMake, then in PowerShell:

```powershell
python -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### macOS

Install Python 3 and CMake with Homebrew:

```bash
brew install python cmake
```

Then:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

`wmctrl` is Linux-specific. The PiP control implementation in `pip_control.py` may need to be changed for Windows or macOS.

### Running

```bash
python main.py
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
USE_GPU = False
```

| Variable                  | Description                                        |
| ------------------------- | -------------------------------------------------- |
| `KNOWN_FACES_DIR`         | Directory containing reference photos              |
| `TARGET_PEOPLE`           | People who trigger PiP hiding                      |
| `PROCESS_EVERY`           | Run recognition every N frames                     |
| `FACE_DISTANCE_THRESHOLD` | Recognition strictness. Lower = stricter           |
| `FRAME_SCALE`             | Image size used for recognition. Lower = faster    |
| `CAMERA_INDEX`            | Camera index (`0` = default camera)                |
| `USE_GPU`                 | `True` uses the `cnn` detector, `False` uses `hog` |

## Running

```bash
source venv/bin/activate
python main.py
```

Press `Q` to exit.

## Troubleshooting

**Error: `Please install face_recognition_models with this command...`**

`face_recognition` prints this for *any* failure while importing
`face_recognition_models`, so it is usually not a missing package. Check the
real error with:

```bash
python -c "import face_recognition_models"
```

If it reports `No module named 'pkg_resources'`, setuptools is too new —
`pkg_resources` was removed in setuptools 81. Reinstall the pin:

```bash
pip install "setuptools<81"
```

**`USE_GPU = True` fails or is slow**

The `cnn` detector needs dlib built with CUDA. Verify with:

```bash
python -c "import dlib; print(dlib.DLIB_USE_CUDA)"
```

If that prints `False`, keep `USE_GPU = False`.

## PiP Control

`pip_control.py` controls what happens to the PiP when a target person is detected.

You can edit this file to decide how the PiP should be handled by the system:

* Hide the PiP
* Close the PiP
* Kill the PiP process
* Use another method

The face-recognition system only detects the target and calls `pip_control.py`. The actual PiP handling is up to your implementation.

