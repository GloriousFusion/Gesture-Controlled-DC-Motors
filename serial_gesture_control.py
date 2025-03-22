import cv2
import mediapipe as mp

import serial
import struct
import time

#   Change default port accordingly
default_port = 'COM5'
arduino = serial.Serial(port=default_port, baudrate=9600, timeout=1)

#   Camera width & height
cam_width, cam_height = 640, 480

#   Set camera id accordingly
cam_id = 0
cam = cv2.VideoCapture(cam_id)

cam.set(3, cam_width)
cam.set(4, cam_height)

x1 = y1 = x2 = y2 = 0
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

#   Modified lesson code to write a float type value
def write_read(value):
    arduino.write(struct.pack('f', value))
    time.sleep(0.05)
    data = arduino.readline()
    return data

#   Gesture control guide: https://www.youtube.com/watch?v=nPzde1YG4ko
while True:
    _, image = cam.read()
    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                #   Reference image to modify id (hand landmarks): https://ai.google.dev/static/mediapipe/images/solutions/hand-landmarks.png
                if id == 8:
                    cv2.circle(img=image, center=(x,y), radius=8, color=(0,255,255), thickness=3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img=image, center=(x,y), radius=8, color=(0,0,255), thickness=3)
                    x2 = x
                    y2 = y

        #   Distance formula (from gesture control guide): https://youtu.be/nPzde1YG4ko?si=eyJOrv-gBx96O_pe&t=1390
        distance = ((x2-x1)**2 + (y2-y1)**2) ** 0.5 // 4

        distance_value = write_read(distance)
        print(distance_value)
        cv2.line(image,(x1,y1), (x2,y2), (0,255,0), 5)

    cv2.imshow("Gesture control interface", image)

    key = cv2.waitKey(10)
    if key == 27: # ESC key
        break

cam.release()
cv2.destroyAllWindows()