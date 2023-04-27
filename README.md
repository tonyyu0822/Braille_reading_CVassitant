# Braille Finger Tracker

This project aims to track the fingertip locations of both hands while reading Braille and predict which finger is touching the Braille page at specific time frames. The output is a combined video displaying the live predictions.

## Input

1. Video recording of Braille reading
2. Monitor recording txt file (output from a monitoring tool)

## Functionality

1. Perform four-point transform on the input video to align the Braille page.
2. Detect both hands' fingertip locations using a machine learning model (MediaPipe) and save the extracted and normalized coordinates data in a CSV file.
3. Make predictions on which finger is touching the Braille page based on time frames by comparing fingertip locations and Braille character positions.
4. Display the combined video showing the live predictions.

## Steps to run the project

1. Install the required libraries by running:
   
`pip install -r requirements.txt`


2. Run the scripts in the following order:

- Braille_finger_tracker.py: To detect fingertip locations and save them in a CSV file.
- Convert_tzt_2_csv.py: To convert the monitor recording txt file to a CSV file compatible with the project.
- predict.py: To make predictions on which finger is touching the Braille page.
- Display.py: To display the combined video showing the live predictions.

3. The output video file will be saved as 'Combined_output_video.mp4' in the project directory.

## Libraries and dependencies

- OpenCV (cv2): To process and display video files
- MediaPipe: To detect fingertip locations in the video
- NumPy: For numerical calculations
- Pandas: To process and manipulate CSV files
- CSV and datetime libraries: Part of the Python standard library, used for file processing and time calculations

Please make sure to install the required libraries and dependencies before running the project.
