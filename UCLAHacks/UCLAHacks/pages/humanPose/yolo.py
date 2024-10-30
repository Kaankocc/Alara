from ultralytics import YOLO
import time
import cv2

model = YOLO('yolov8n-pose.pt')

cap=cv2.VideoCapture(0)
ret, frame = cap.read()

startTime = time.time()
while(ret):
    results = model(source=frame, show=True, conf=0.3, save=False)
    
    left_shoulder_x = [result.keypoints.xy[0][5][0] for result in results]
    left_shoulder = [result.keypoints.xy[0][5] for result in results] # left shoulder:6
    left_hip = [result.keypoints.xy[0][11] for result in results] # left hip:12
    left_knee = [result.keypoints.xy[0][13] for result in results] # left knee:14
    left_ankle = [result.keypoints.xy[0][15] for result in results] # left ankle:16

    print(left_ankle)
    print(left_hip)
    ret, frame = cap.read()
    
    if(time.time()-startTime >= 10):
        break