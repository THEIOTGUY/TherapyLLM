import time
import cv2 as cv
import mediapipe as mp
import numpy as np
import httpx
import json
import os
import asyncio
url = 'http://localhost:8011/A2F/SetSettings'
text="{\"a2f_instance\": \"/World/audio2face/CoreFullface\",\"settings\": {\"left_eye_rot_y_offset\":10.0,\"right_eye_rot_y_offset\":10.0,\"left_eye_rot_x_offset\":10.0,\"right_eye_rot_x_offset\":10.0}}"
async def make_request():
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=text)
        return response
def map_range(value, from_min, from_max, to_min, to_max):
    # First, normalize the input value to the range [0, 1]
    normalized_value = (value - from_min) / (from_max - from_min)
    
    # Then, scale it to the desired range [to_min, to_max]
    mapped_value = normalized_value * (to_max - to_min) + to_min
    
    return mapped_value
mp_face_detection = mp.solutions.face_detection
cap = cv.VideoCapture(0)
with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detector:
    frame_counter = 0
    fonts = cv.FONT_HERSHEY_PLAIN
    start_time = time.time()
    while True:
        frame_counter += 1
        ret, frame = cap.read()
        if ret is False:
            break
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        results = face_detector.process(rgb_frame)
        frame_height, frame_width, c = frame.shape
        if results.detections:
            for face in results.detections:
                face_react = np.multiply(
                    [
                        face.location_data.relative_bounding_box.xmin,
                        face.location_data.relative_bounding_box.ymin,
                        face.location_data.relative_bounding_box.width,
                        face.location_data.relative_bounding_box.height,
                    ],
                    [frame_width, frame_height, frame_width, frame_height]).astype(int)
                
                cv.rectangle(frame, face_react, color=(255, 255, 255), thickness=2)
                key_points = np.array([(p.x, p.y) for p in face.location_data.relative_keypoints])
                y = key_points[1][1]
                x = key_points[0][0]
                mapped_value_x = map_range(x, 0, 1, -10,10 )
                mapped_value_y = map_range(y, 0, 1, -10, 10)
                x = float(mapped_value_x)
                y = float(mapped_value_y)
                x = -x
                y = y
                print(x)
                print(y)
                text = json.loads(text)
                print(type(text))
                text["settings"]["right_eye_rot_y_offset"] = x
                text["settings"]["left_eye_rot_y_offset"] = x
                text["settings"]["right_eye_rot_x_offset"] = y
                text["settings"]["left_eye_rot_x_offset"] = y
                text = json.dumps(text)
                text1 = text.replace("\"", "\\\"")
                print("sending values")
                wholetext = "curl -X \"POST\" \"http://localhost:8011/A2F/SetSettings\" \ -H \"accept: application/json\" \ -H \"Content-Type: application/json\" \ -d \"{}\"".format(text1)
                print("whole text :",wholetext)
                os.system(wholetext)
                print(x)
                key_points_coords = np.multiply(key_points,[frame_width,frame_height]).astype(int)
                for p in key_points_coords:
                    cv.circle(frame, p, 4, (255, 255, 255), 2)
                    cv.circle(frame, p, 2, (0, 0, 0), -1)
        
        fps = frame_counter / (time.time() - start_time)
        cv.putText(frame,f"FPS: {fps:.2f}",(30, 30),cv.FONT_HERSHEY_DUPLEX,0.7,(0, 255, 255),2,)
        cv.imshow("frame", frame)
        key = cv.waitKey(1)
        if key == ord("q"):
            break
    cap.release()
    cv.destroyAllWindows() 
