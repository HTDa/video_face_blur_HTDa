import cv2

file = "original_video.mp4"
parts = [(1000, 3000)]



cap = cv2.VideoCapture(file)
ret, frame = cap.read()
h, w, _ = frame.shape

fourcc = cv2.VideoWriter_fourcc(*"XVID")
writers = [cv2.VideoWriter(f"part{start}-{end}.mp4", fourcc, 20.0, (w, h)) for start, end in parts]

end = parts[-1][-1]

f = 0
while ret and f < end+1:
    f += 1
    for i, part in enumerate(parts):
        start, end = part
        if start <= f <= end:
            writers[i].write(frame)
    ret, frame = cap.read()
    print(f)

for writer in writers:
    writer.release()

print(end)

cap.release()
