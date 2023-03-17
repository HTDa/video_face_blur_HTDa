import cv2
import numpy as np
import sys


# caffe model
prototxt_path = "caffe_weights/deploy.prototxt.txt"
model_path = "caffe_weights/res10_300x300_ssd_iter_140000_fp16.caffemodel"
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)


# Open the video file
video_capture = cv2.VideoCapture('part1000-3000.mp4')
# Get the frames per second (fps) of the video
fps = int(video_capture.get(cv2.CAP_PROP_FPS))
# Create a VideoWriter object to write the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps,
                               (int(video_capture.get(3)),
                                int(video_capture.get(4))))


# loop through frames of video
while True:

    # read frame
    ret, frame = video_capture.read()

    # check if frame is read
    if not ret:
        break

    # get frame h, w
    h, w = frame.shape[:2]
    # gaussian blur kernel size depends on w and h of original frame
    kernel_width = (w // 7) | 1
    kernel_height = (h // 7) | 1

    # preprocess frame: resize to (300, 300) and performs mean subtraction
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # set the image into the input of the neural network
    model.setInput(blob)
    # perform inference and get result
    output = np.squeeze(model.forward())


    for i in range(0, output.shape[0]):
        # get conf
        conf = output[i, 2]
        # if conf is above 0.4, then blur bounding box
        if conf > 0.4:
            # get box coords and upscale to original h, w
            box = output[i, 3:7] * np.array([w, h, w, h])
            # convert to int
            start_x, start_y, end_x, end_y = box.astype(np.int64)

            # draw rectangle
            cv2.rectangle(frame, (start_x, start_y), (end_x, end_y), color=(255, 0, 0), thickness=2)
            
            # get face image
            face = frame[start_y:end_y, start_x:end_x]
            # apply gaussian blur to face
            face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
            # apply to original frame
            frame[start_y:end_y, start_x:end_x] = face

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == ord("q"):
        break

    output_video.write(frame)


# close all opencv windows
cv2.destroyAllWindows()

# release video capture and output video objects
video_capture.release()
output_video.release()
    
