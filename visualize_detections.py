"""
Visualize detections from a .pickle file on the source video.
Usage:
    python visualize_detections.py -i input_video.mp4 -p detections.pickle -o output_video.mp4
"""

import os
import sys
import cv2
import pickle
import argparse
import numpy as np

# Class ID -> Name mapping
CATEGORIES = {
    0: "Hatchback",
    1: "Sedan",
    2: "SUV",
    3: "MUV",
    4: "Bus",
    5: "Truck",
    6: "Three-wheeler",
    7: "Two-wheeler",
    8: "LCV",
    9: "Mini-bus",
    10: "Tempo-traveller",
    11: "Bicycle",
    12: "Van",
}

# Distinct colors per class (BGR)
COLORS = {
    0:  (255, 128,   0),   # Hatchback - orange
    1:  (  0, 212, 255),   # Sedan - gold
    2:  ( 80, 175,  76),   # SUV - green
    3:  (230,  50, 240),   # MUV - magenta
    4:  (  0,   0, 220),   # Bus - red
    5:  (180, 105, 255),   # Truck - pink
    6:  (255, 255,   0),   # Three-wheeler - cyan
    7:  ( 50, 210, 255),   # Two-wheeler - yellow
    8:  (200, 150,  80),   # LCV - steel blue
    9:  (100, 100, 255),   # Mini-bus - salmon
    10: (147, 200, 100),   # Tempo-traveller - teal
    11: (  0, 255, 127),   # Bicycle - spring green
    12: (255, 190, 128),   # Van - light blue
}


def draw_detections(frame, detections):
    """Draw bounding boxes and labels on a single frame."""
    if detections is None:
        return frame

    h, w = frame.shape[:2]
    # Scale font/thickness to frame resolution
    scale = max(w, h) / 1920.0
    font_scale = max(0.35, 0.45 * scale)
    box_thick = max(1, int(2 * scale))
    txt_thick = max(1, int(1.2 * scale))
    font = cv2.FONT_HERSHEY_SIMPLEX

    for det in detections:
        x1, y1, x2, y2, score, cls_id = det
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cls_id = int(cls_id)
        cls_name = CATEGORIES.get(cls_id, f"cls_{cls_id}")
        color = COLORS.get(cls_id, (200, 200, 200))

        # Draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, box_thick)

        # Label text
        label = f"{cls_name} {score:.2f}"
        (tw, th), baseline = cv2.getTextSize(label, font, font_scale, txt_thick)

        # Label background — place above the box, fall inside if at top edge
        label_y = y1 - 4 if y1 - th - 6 > 0 else y1 + th + 6
        bg_y1 = label_y - th - 4
        bg_y2 = label_y + 4

        # Semi-transparent background
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, bg_y1), (x1 + tw + 6, bg_y2), color, -1)
        cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

        # Text
        cv2.putText(frame, label, (x1 + 3, label_y), font, font_scale, (255, 255, 255), txt_thick, cv2.LINE_AA)

    return frame


def main():
    parser = argparse.ArgumentParser(description="Visualize pickle detections on video")
    parser.add_argument("-i", "--input", type=str, required=True, help="Path to source video")
    parser.add_argument("-p", "--pickle", type=str, required=True, help="Path to detections .pickle file")
    parser.add_argument("-o", "--output", type=str, default="output_vis.mp4", help="Path to output video")
    parser.add_argument("--codec", type=str, default="mp4v", help="FourCC codec (default: mp4v)")
    args = parser.parse_args()

    # Load detections
    with open(args.pickle, "rb") as f:
        data = pickle.load(f)

    # The pickle structure is {video_name: {frame_id: detections}}
    # Grab the first (and typically only) video key
    video_name = list(data.keys())[0]
    detections = data[video_name]
    print(f"Loaded detections for '{video_name}' — {len(detections)} frames with entries.")

    # Open source video
    cap = cv2.VideoCapture(args.input)
    if not cap.isOpened():
        print(f"Error: cannot open video '{args.input}'")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video: {w}x{h} @ {fps:.1f} fps, {total} frames")

    fourcc = cv2.VideoWriter_fourcc(*args.codec)
    out = cv2.VideoWriter(args.output, fourcc, fps, (w, h))

    frame_id = 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        dets = detections.get(frame_id, None)
        frame = draw_detections(frame, dets)

        # Small HUD in top-left corner
        hud = f"Frame {frame_id}/{total}"
        cv2.putText(frame, hud, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(frame, hud, (8, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        out.write(frame)
        frame_id += 1

        if frame_id % 500 == 0:
            print(f"  Rendered {frame_id}/{total} frames...")

    cap.release()
    out.release()
    print(f"Done — saved to '{args.output}'")


if __name__ == "__main__":
    main()