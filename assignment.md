# Why Does Detector Fail on Small Objects?

In CCTV footage, most vehicles appear small — the camera is mounted high and far from the road. Standard object detectors are known to struggle with small objects, yet this is exactly where accurate detection matters most for traffic analytics. Your task is to **investigate, understand, and address** this problem.

For reference:
- Original clip — https://www.youtube.com/watch?v=9o9TVsCUZzM&list=PLZy_yosa6uXT-X47I4RwDYTMXgh53p7g8&index=5
- Our best detector model output — https://drive.google.com/file/d/1RcTyZWUJoH-ADuQ6gEsSWEXOreWu9qSz/view?usp=sharing
- Starter repo — [Github](https://github.com/cargolx/Assignment_starter_kit.git) (contains frame-level detections from our best model on the above clip, with a visualization script)

Dataset Link - https://huggingface.co/datasets/iisc-aim/UVH-26

**Duration:** 1 Week

## Steps:

1. Download a working subset of UVH-26. Explore and understand the data. What are your observations for detection?

2. Fine-tune a detection model on UVH-26 (You can use Google Colab or Kaggle GPU). Evaluate and analyze how performance varies across different object sizes.

3. Propose and experiment with approaches to **improve small object detection**. You may try as many strategies as you like.

4. **(Optional)** Can your improved detector maintain its gains when used as part of a **multi-object tracking** pipeline on a traffic video?

## Submission

1. Provide a Github repository with a detailed README documenting everything you did from scratch. Modular, scalable and clean code will be a bonus.
 
2. Present a unified analysis of what you tried, what worked and what are the tradeoffs, what didn't, and your understanding of **why**.
 
3. Provide your fine-tuned model weights with properly documented instructions to reproduce your results.
 
4. Include qualitative examples — visualize where your model succeeds and where it still fails.
