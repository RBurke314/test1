
# import from parent directory
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import DynamicObjectV2
Obj = DynamicObjectV2.Class

fromSource = [
    "FaceRecDet"
]

fromClass = [
]

tests = Obj({
  "Color-Detect": ["Color-Detect"],
  "Servo-1": ["Servo-1"],
  "Sound": ["Sound", "Voice"],
  "GUI-Item-Detect": ["GUI", "Item-Detect"],
  "GUI-Face-Detect": ["GUI", "Face-Detect"],
  "GUI-Color-Detect": ["GUI", "Color-Detect"]
})
