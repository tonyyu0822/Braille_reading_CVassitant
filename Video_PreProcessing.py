

# Define the path to the input video file here:
video_file_name = '/Users/by12/Braille/FingerTracker/data/video/4x.mp4'

import cv2
import numpy as np

# Mouse callback function to capture corner points
def mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(params['points']) < 4:
            params['points'].append((x, y))
            cv2.circle(params['img'], (x, y), 5, (0, 255, 0), -1)
            cv2.imshow('Select Corners', params['img'])

# Read input video
cap = cv2.VideoCapture(video_file_name)

# Get first frame to select corners
ret, frame = cap.read()
if not ret:
    print('Error reading video file')
    exit()

# Display the first frame for corner selection
cv2.namedWindow('Select Corners', cv2.WINDOW_NORMAL)
cv2.imshow('Select Corners', frame)
corner_points = []
cv2.setMouseCallback('Select Corners', mouse_callback, {'img': frame, 'points': corner_points})
cv2.waitKey(0)

# Close the window after corner selection
cv2.destroyAllWindows()

# Define source and destination points for the perspective transform
src = np.float32(corner_points)
dst = np.float32([[0, 0], [1024, 0], [0, 768], [1024, 768]])

# Compute perspective transform matrix
M = cv2.getPerspectiveTransform(src, dst)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('./transformed_video.mp4', fourcc, 29, (1024,768))  


# Loop through all frames of the video
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Apply the perspective transform to the current frame
    transformed_frame = cv2.warpPerspective(frame, M, (1024, 768))
    transformed_frame = cv2.flip(transformed_frame,1)
    out.write(transformed_frame)

    # Display the transformed frame
    cv2.imshow('Transformed Video', transformed_frame)

 

    # Exit if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
