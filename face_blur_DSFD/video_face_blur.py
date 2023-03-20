import warnings
warnings.simplefilter("ignore", UserWarning)

import cv2
import numpy as np
import face_detection


def videoFaceBlur(path):

    detector = face_detection.build_detector(
        "DSFDDetector", confidence_threshold=0.5, nms_iou_threshold=0.3)

    cap = cv2.VideoCapture(path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')