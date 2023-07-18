import math

import cv2
import pyautogui
import mediapipe as mp
import pyaudio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Получение списка аудиоустройств
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Получение текущей громкости
current_volume = volume.GetMasterVolumeLevel()

print(current_volume)

cap = cv2.VideoCapture(0)

hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

mpDraw = mp.solutions.drawing_utils

while True:
    _, img = cap.read()
    res = hands.process(img)
    if res.multi_hand_landmarks:
        for hand_landmarks in res.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            x1, y1 = int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].x * img.shape[1]), \
                int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y * img.shape[0])
            x2, y2 = int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].x * img.shape[1]), \
                int(hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP].y * img.shape[0])
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 2 - 70
            if distance <= -65.25:
                distance = -65.25
            elif distance >= 0:
                distance = 0
            print("Расстояние между пальцами: {:.2f}".format(distance))
            volume.SetMasterVolumeLevel(distance, None)
    cv2.imshow('Hand tracking', img)
    cv2.waitKey(1)