import warnings
warnings.simplefilter("ignore", UserWarning)

import cv2
import numpy as np
import face_detection



# load DSFD model
detector = face_detection.build_detector(
    "DSFDDetector", confidence_threshold=0.5, nms_iou_threshold=0.3)

# im = cv2.imread("input3.jpg")

# detections = detector.detect(im)

# h, w = im.shape[:2]
# kernel_width = (w // 7) | 1
# kernel_height = (h // 7) | 1


# open video file
cap = cv2.VideoCapture("part1000-3000.mp4")
# get fps of video
fps = int(cap.get(cv2.CAP_PROP_FPS))
# create VideoWriter object to write output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps,
                               (int(cap.get(3)),
                                int(cap.get(4))))


# loop through frames of video
frame_index = 0
while True:
    print(frame_index)
    frame_index += 1

    # read frame
    ret, frame = cap.read()
    # check if frame is read
    if not ret:
        break


    # get frame h, w and prepare gaussian blur kernel size
    h, w = frame.shape[:2]
    kernel_width = (w // 7) | 1
    kernel_height = (h // 7) | 1


    # perform inference and get results
    detections = detector.detect(frame)

          
    

    if detections.shape[0]:
        for i in range(0, detections.shape[0]):
            conf = detections[i, 4]
            if conf < 0.4:
                continue
            box = detections[i, 0:4]
            start_x, start_y, end_x, end_y = box.astype(np.int64)
            start_x, start_y, end_x, end_y = max(0, start_x), max(0, start_y), max(0, end_x), max(0, end_y)            

            # cv2.rectangle(im, (start_x, start_y), (end_x, end_y), color=(255,0,0),
            #               thickness=2)

            # get face image
            face = frame[start_y:end_y, start_x:end_x]
            
            try:
                # apply gaussian blur to face
                face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
                # apply blur to original frame
                frame[start_y:end_y, start_x:end_x] = face
            except:
                print(face)
                print(detections.shape[0])
                print(detections[i])
                print(box)
                print(start_x, start_y, end_x, end_y)
                print(h, w)
            

    # cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break
    output_video.write(frame)


# close all opencv windows
cv2.destroyAllWindows()
# release video capture and output video objects
cap.release()
output_video.release()
