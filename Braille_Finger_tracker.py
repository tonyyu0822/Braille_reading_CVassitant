"""
added flip so that the exported data is correct dirrection adn in sync with the monitor data
"""
import cv2
import mediapipe as mp
import numpy as np
import csv
import datetime
from time import time

mp_drawing = mp.solutions.drawing_utils  # Drawing helpers
# mp_holistic = mp.solutions.holistic # Mediapipe Solutions - unused
mp_hands = mp.solutions.hands

###
# INPUTS:

# Define the path to the input video file here:
video_file_name = './downsampled.mp4'



# Choose whether or not to see video as it is being analyzed:
display_annotated_video = True

t = time()  # Set a timer for later to see how long code takes to run
now = datetime.datetime.now()
# format the date and time for use in the file name
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
filename = f"coords_{timestamp}.csv"
    

# folder to store the csv file
folder = "./output_logs/"

# creating the csv file in the folder
with open(folder + filename, 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

# Generate names of column headers for csv
landmarks = ["Time", 'FrameNumber', 'HandsPresent']
for side in ["Left", "Right"]:
    for fgr in ["Thumb", "Index", "Middle", "Ring", "Pinky"]:
        for dim in ["X", "Y", "Z"]:
            landmarks += [side + fgr + dim]



#Initialize the csv
with open(folder + filename, mode='w', newline='') as f:
    csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(landmarks)

# Start reading the video from the file
cap = cv2.VideoCapture(video_file_name)


frame_no = 0
with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.4) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame,-1)
        elapsed_time = time() - t
        print(elapsed_time)
        if frame is None:
            print("Finished analyzing video")
            break

        # Preprocess image for hands detection
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # BGR 2 RGB 
        image = cv2.flip(image, 1)  # Flip on horizontal since hands face down
        # image = cv2.flip(image, 0)
        image.flags.writeable = False

        # Perform detection of all 21 landmarks (fingers, joints, etc.) of a hand.
        results = hands.process(image)

        # Revert image after hands detection
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # RGB 2 BGR

        # pose is a list whose ith entry is the data for the ith hand detected
        # (ideally two hands are detected if two hands are in the video...)
        pose = results.multi_hand_landmarks
        # handedness_results is a list whose ith entry is handedness (left or right)
        # of the ith hand.
        handedness_results = results.multi_handedness

        # Reformat data for writing into csv
        if pose:  # (if pose exists/is not None)
            row_partials = {}
            for hand_idx, hand in enumerate(pose):
                # Within pose, hand_idx is the index of which hand is detected (should be 0 or 1...)
                # and hand is the coordinate data for all 21 possible joints in the hand
                # For more info about mp_hands:
                # https://google.github.io/mediapipe/solutions/hands.html#multi_hand_landmarks

                handedness = handedness_results[hand_idx].classification[0].label

                # Retrieve fingertip coordinates
                Thumb = hand.landmark[mp_hands.HandLandmark.THUMB_TIP]
                Index = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                Middle = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                Ring = hand.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                Pinky = hand.landmark[mp_hands.HandLandmark.PINKY_TIP]

                # Reformat fingertip coordinates as lists
                T = list(
                    np.array([[Thumb.x, Thumb.y, Thumb.z] for landmark in pose])[0].flatten())
                I = list(
                    np.array([[Index.x, Index.y, Index.z] for landmark in pose])[0].flatten())
                M = list(
                    np.array([[Middle.x, Middle.y, Middle.z] for landmark in pose])[0].flatten())
                R = list(
                    np.array([[Ring.x, Ring.y, Ring.z] for landmark in pose])[0].flatten())
                P = list(
                    np.array([[Pinky.x, Pinky.y, Pinky.z] for landmark in pose])[0].flatten())

                # Concatenate rows
                row_partials[handedness] = T + I + M + R + P
                print(row_partials[handedness])

                if display_annotated_video:
                    # Draw the skeleton with dots on the joints for this hand
                    mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                              mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2,
                                                                     circle_radius=2),
                                              )

            # Fill in any missing handed data with None.
            if ("Left" in row_partials) and ("Right" in row_partials):
                present_hands = "Both"
            # If one of the two hands isn't detected, then make all of its finger location entries be None.
            elif ("Left" not in row_partials) and ("Right" in row_partials):
                present_hands = "Right"
                row_partials["Left"] = [None] * 15  # for 5 fingers * 3 x,y,z coords to be rendered null
            elif ("Left" in row_partials) and ("Right" not in row_partials):
                present_hands = "Left"
                row_partials["Right"] = [None] * 15
            else:
                # The no-hands case should only occur if pose was None (i.e. outside this if condition);
                # leaving this here in case that assumption is violated
                print("NOHANDS ERROR")

            # Generate row to write into csv
            row = [elapsed_time, frame_no, present_hands] + row_partials["Left"] + row_partials["Right"]

        else:  # If no hands were detected (pose is None), just write 30 Nones (2 hands * 5 fingers * 3 x,y,z, coords) to the data.
            row = [elapsed_time, frame_no, "NoHands"] + [None] * 30

        # Write this frame's data to the csv
        with open(folder + filename, mode='a', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(row)



        frame_no += 1

        if display_annotated_video:
            cv2.imshow('Video from ' + video_file_name, cv2.flip(image, 1))
            if cv2.waitKey(10) & 0xFF == ord('q'):  # Exit the video playback by pressing the Q key.
                break

print("Analysis concluded in " + str((time() - t)) + " seconds. Results recorded in " + folder+filename)

cap.release()
cv2.destroyAllWindows()