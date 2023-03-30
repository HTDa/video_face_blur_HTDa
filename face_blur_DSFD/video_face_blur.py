import warnings
warnings.simplefilter("ignore", UserWarning)

import cv2
import numpy as np
import face_detection
import sys
import torch


detector = face_detection.build_detector(
        "DSFDDetector", confidence_threshold=0.5, nms_iou_threshold=0.3)



def progressBar(count_value, total, suffix=''):
    bar_length = 100
    filled_up_Length = int(round(bar_length* count_value / float(total)))
    percentage = round(100.0 * count_value/float(total),1)
    bar = '=' * filled_up_Length + '-' * (bar_length - filled_up_Length)
    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
    sys.stdout.flush()


def videoFaceBlur(path, output_folder):

    global detector

    print()
    print(torch.cuda.get_device_properties(torch.cuda.current_device()))

    cap = cv2.VideoCapture(path)
    video_name = path.split('/')[-1].split('.')[0]

    print("\nVideo name: " + video_name)
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_folder + "/" + video_name + "_output.mp4",
                                    fourcc, fps,
                                    (int(cap.get(3)),
                                    int(cap.get(4))))


    frame_index = 0
    while True:
        
        # print(frame_index)
        frame_index += 1
        progressBar(frame_index, video_length+1)

        ret, frame = cap.read()
        if not ret:
            print()
            break


        h, w = frame.shape[:2]
        kernel_width = (w // 7) | 1
        kernel_height = (h // 7) | 1


        detections = detector.detect(frame)

        if detections.shape[0]:
            for i in range(0, detections.shape[0]):
                conf = detections[i, 4]
                if conf < 0.4:
                    continue
                box = detections[i, 0:4]
                start_x, start_y, end_x, end_y = box.astype(np.int64)
                start_x, start_y, end_x, end_y = max(0, start_x), max(0, start_y), min(w, end_x), min(h, end_y)


                face = frame[start_y:end_y, start_x:end_x]

                try:
                    face = cv2.GaussianBlur(face, (kernel_width, kernel_height), 0)

                    frame[start_y:end_y, start_x:end_x] = face
                except:
                    print(face)
                    print(box)
                    print(detections[i])
                    print(start_x, start_y, end_x, end_y)
                    print(h, w)


        if cv2.waitKey(1) == ord("q"):
            break
        output_video.write(frame)


    cv2.destroyAllWindows()
    # release video capture and output video objects
    cap.release()
    output_video.release()
    return