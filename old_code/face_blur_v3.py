import cv2
import mediapipe as mp
import numpy as np


mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture("part1000-3000.mp4")
with mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5) as face_detection:
    i = 0
    while cap.isOpened():
        i += 1
        ret, image = cap.read()
        if not ret:
            break

        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        annotated_image = image.copy()

        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(annotated_image, detection)
            cv2.imwrite("frame" + str(i) + ".png", annotated_image)
        #cv2.imshow("annotated image", annotated_image)

cap.release()


# # load face mesh and create object
# mp_face_mesh = mp.solutions.face_mesh
# face_mesh = mp_face_mesh.FaceMesh()


# # use rgb
# image = cv2.imread("im.png")
# rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# result = face_mesh.process(rgb_image)


# height, width = image.shape[:2]

# for facial_landmarks in result.multi_face_landmarks:
#     for i in range(0, 468):
#         pt1 = facial_landmarks.landmark[i]
#         x = int(pt1.x * width)
#         y = int(pt1.y * height)

#         cv2.circle(image, (x, y), 5, (100, 100, 0), -1)


# cv2.imshow("image", image)
