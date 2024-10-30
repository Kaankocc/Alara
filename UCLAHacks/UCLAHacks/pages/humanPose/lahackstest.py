
import cv2 as cv
import numpy as np

BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

width = 368
height = 368
inWidth = width
inHeight = height

net = cv.dnn.readNetFromTensorflow("../UCLAHacks/UCLAHacks/pages/humanPose/graph_opt.pb")
thr = 0.2

def poseDetector(frame):
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]

    net.setInput(cv.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]  # MobileNet output [1, 57, -1, -1], we only need the first 19 elements

    assert(len(BODY_PARTS) == out.shape[1])

    points = []
    for i in range(len(BODY_PARTS)):
        # Slice heatmap of corresponging body's part.
        heatMap = out[0, i, :, :]



        # pointx = point[0] + i
        _, conf, _, point = cv.minMaxLoc(heatMap)
        point_x =  point[0]

        if(i == 2):
            for i in range(10):
              heatMap_value_at_point = heatMap[point[1], point[0] - i]
              if heatMap_value_at_point < 0.1:
                point_x = point[0] - i * 0.1
                break

        if(i == 5):
            for i in range(10):
              heatMap_value_at_point = heatMap[point[1], point[0] + i]
              if heatMap_value_at_point < 0.1:
                point_x = point[0] + i * 0.35
                break

        if(i == 11):
            for i in range(10):
              heatMap_value_at_point = heatMap[point[1], point[0] + i]
              if heatMap_value_at_point < 0.3:
                point_x = point[0] + i * 0.5
                break

        if(i == 8):
            for i in range(10):
              heatMap_value_at_point = heatMap[point[1], point[0] - i]
              if heatMap_value_at_point < 0.3:
                point_x = point[0] - i * 0.25
                break



        x = (frameWidth * point_x)  / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        points.append((int(x), int(y)) if conf > thr else None)

    for pair in POSE_PAIRS:
        partFrom = pair[0]
        partTo = pair[1]
        assert(partFrom in BODY_PARTS)
        assert(partTo in BODY_PARTS)

        idFrom = BODY_PARTS[partFrom]
        idTo = BODY_PARTS[partTo]

        if points[idFrom] and points[idTo]:
            cv.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)
            cv.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv.FILLED)

    t, _ = net.getPerfProfile()
    return frame, points


import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Define the path to your image file
image_path = '../UCLAHacks/UCLAHacks/pages/humanPose/Pics/Person.jpeg'  # Adjust the path accordingly if the image is in a different folder

# Open and display the image
img = mpimg.imread(image_path)
plt.imshow(img)
plt.axis('off')  # Turn off axis
plt.show()

input = cv.imread(image_path)
output, points = poseDetector(input)


Rshoulder_x, Rshoulder_y = points[BODY_PARTS["RShoulder"]]
Lshoulder_x, Lshoulder_y = points[BODY_PARTS["LShoulder"]]

if points[BODY_PARTS["LHip"]] is not None:
  RHip_x, RHip_y = points[BODY_PARTS["RHip"]]
  LHip_x, LHip_y = points[BODY_PARTS["LHip"]]


print("Xcord: " + str(Rshoulder_x) + " Ycord: " + str(Rshoulder_y))
print("Xcord: " + str(Lshoulder_x) + " Ycord: " + str(Lshoulder_y))

import csv
import os

def write_to_csv(filename, data_point, right, left):
    # Define the field names
    fieldnames = ['dataPoint', 'x', 'y']
    
    # Check if the file already exists and contains data
    file_exists = os.path.exists(filename)
    file_has_data = file_exists and os.path.getsize(filename) > 0

    # Open the file in append mode ('a') if it exists and contains data, otherwise open in write mode ('w')
    mode = 'a' if file_has_data else 'w'

    # Write data to the CSV file
    with open(filename, mode=mode, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # Write the header if the file is newly created or contains no data
        if not file_has_data:
            writer.writeheader()

        # Write the data
        writer.writerow({'dataPoint': data_point, 'x': right, 'y': left})



def clear_csv(filename):
    # Open the CSV file in write mode, which truncates the file
    with open(filename, mode='w', newline='') as file:
        # Write nothing to the file, effectively clearing it
        pass

# Example usage
clear_csv('../UCLAHacks/UCLAHacks/data.csv')
write_to_csv('../UCLAHacks/UCLAHacks/data.csv', "RightShoulder", Rshoulder_x, Rshoulder_y)
write_to_csv('../UCLAHacks/UCLAHacks/data.csv', "LeftShoulder", Lshoulder_x, Lshoulder_y)
if points[BODY_PARTS["LHip"]] is not None:
  write_to_csv('../UCLAHacks/UCLAHacks/data.csv', "RightHip", RHip_x, RHip_y)
  write_to_csv('../UCLAHacks/UCLAHacks/data.csv', "LeftHip", LHip_x, LHip_y)



