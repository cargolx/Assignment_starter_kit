# Starter Kit — Detection Reference Data

This repository contains frame-level detection outputs from our best-performing model on a sample traffic CCTV video, along with a visualization script.

## Contents

```
├── Traffic_congestion_in_Delhi_due_to_Metro_construction_work_1080P.pickle        # Frame-level detections (you will add this)
├── visualize_detections.py  # Script to overlay detections on the source video
└── README.md
```

## Pickle Format

The `.pickle` file contains a nested dictionary:

```python
{
    "video_name": {
        frame_id (int): [
            [x1, y1, x2, y2, confidence_score, class_id],
            [x1, y1, x2, y2, confidence_score, class_id],
            ...
        ],
        ...
    }
}
```

- **Outer key:** video filename (string)
- **Inner key:** 1-indexed frame number (int)
- **Value:** list of detections, each a 6-element list `[x1, y1, x2, y2, score, class_id]`
  - `x1, y1, x2, y2` — bounding box coordinates in pixels (absolute, not normalized)
  - `score` — confidence score (float, 0–1)
  - `class_id` — integer class label (see mapping below)

### Class Mapping

| ID | Class |
|----|-------|
| 0 | Hatchback |
| 1 | Sedan |
| 2 | SUV |
| 3 | MUV |
| 4 | Bus |
| 5 | Truck |
| 6 | Three-wheeler |
| 7 | Two-wheeler |
| 8 | LCV |
| 9 | Mini-bus |
| 10 | Tempo-traveller |
| 11 | Bicycle |
| 12 | Van |

## Loading the Pickle

```python
import pickle

with open("detections.pickle", "rb") as f:
    data = pickle.load(f)

video_name = list(data.keys())[0]
detections = data[video_name]

# Get detections for frame 1
frame_1_dets = detections.get(1, [])
for det in frame_1_dets:
    x1, y1, x2, y2, score, cls_id = det
    print(f"Class {int(cls_id)}, Score {score:.2f}, Box [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")
```

## Visualization

```bash
python visualize_detections.py -i <source_video.mp4> -p detections.pickle -o output.mp4
```

### Requirements

```
opencv-python
numpy
```