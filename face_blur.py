import cv2
import numpy as np

# Load the cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



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
output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps, (int(video_capture.get(3)), int(video_capture.get(4))))

# Loop through the frames of the video
i = 0
while True:
    # Read a frame from the video
    ret, frame = video_capture.read()
    print('frame: ', i)

    # Check if the frame was successfully read
    if not ret:
        break

    # get width and height of frame
    h, w = frame.shape[:2]
    # gaussian blur kernel size depends on w and h of original image
    kernel_width = (w // 7) | 1
    kernel_height = (h // 7) | 1

    # preprocess image: resize to (300, 300) and performs mean subtraction
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # set the image into the input of the neural network
    model.setInput(blob)
    # perform inference and get result
    output = np.squeeze(model.forward())

    
    for i in range(0, output.shape[0]):
        # get confidence
        conf = output[i, 2]
        # if confidence > 0.5 then draw box
        if conf > 0.4:
            # get box coords and upscale to original img size
            box = output[i, 3:7] * np.array([w, h, w, h])
            # convert to int
            start_x, start_y, end_x, end_y = box.astype(np.int)
            # get face image
            face = frame[start_y: end_y, start_x: end_x]
            # apply gaussian blur to face
            face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)
            frame[start_y:end_y, start_x:end_x] = face
    
    
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Loop through the detected faces and blur them
    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        face_blur = cv2.GaussianBlur(face_roi, (51, 51), 0)
        frame[y:y+h, x:x+w] = face_blur

    # Write the modified frame to the output video
    output_video.write(frame)
    i+=1

# Release the video capture and output video objects
video_capture.release()
output_video.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
