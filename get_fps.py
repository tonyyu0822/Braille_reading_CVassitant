import cv2
import mediapipe as mp
import numpy as np
import csv
import datetime
from time import time

video_file_name = '/Users/by12/Braille/FingerTracker/data/video/4x.mp4'
cap = cv2.VideoCapture(video_file_name)

fps = int(cap.get(cv2.CAP_PROP_FPS))
print(fps)
