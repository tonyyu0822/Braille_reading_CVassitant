# Braille Finger Tracker
This is source code for a finger-tracking system that will be used for a larger research project on braille reading, 
This project utlizes computer vision and machine learning to track the movement of fingertips on a Braille page, and determining which fingers are in contact with which character(s) at a given point in time. This integrated software-hardware aims to assist evidence-based research into how braille is best taught and learned.
The output is a combined video displaying the live finger tip detection information and touch detections.

## Input

1. Video recording of Braille reading(recorded in 29fps(default of the system. If the recording is proceeded in 60fps, change the corresponding fps in code files))
2. Monitor recording txt file (finger coordinates output from the monitor)

## Functionality

1. Perform four-point transform on the input video to align the Braille page.(Video_PreProcessing.py)
2. Detect both hands' fingertip locations using a machine learning model (MediaPipe) and save the extracted and normalized coordinates data in a CSV file.(Braille_Finger_tracker.py)
3. Make predictions on which finger is touching the Braille page based on time frames by comparing fingertip locations and Braille character positions.(predict.py)
4. Maps finger-tip coordinates to corresponding braille character on the given brf file.(Braille_2_coord.py & Map_Braille_character.py)
5. Display the combined video showing the live predictions.(Displays.py)

## Steps to run the project

1. Install the required libraries by running:
   
`pip install -r requirements.txt`


2. Run the scripts in the following order:
- Trim and remove audio from the original recording. Using a video editor, mandually trim the recorded video to start exactly when the first frame of the red flash appears and remove the audio from the recording. 

- Run Video_PreProcessing.py: To preform four point transform to transform the skewed view of the recorded video to a flat view for proceeding processing. 
After running the code, a freezed frame will show up for you to manually identify the four corners of the screen(which should be taped in blue, not the four corners of the braille page). Select the four points in this order(left bottom, right bottom, left top, right top, after selecting four corners in this order, hit enter and the video frame window should display the transformed view with the title(Transformed Video). Please wait until the video render finishes.

- Run Braille_finger_tracker.py: To detect fingertip locations and save them in a CSV file that will be labeled with data and time:

- Run Convert_tzt_2_csv.py: To convert the monitor recording txt file to a CSV file that is compatible with format of the CV detected CSV from previous step.
- Run predict.py: To make predictions on which finger is touching the Braille page.
- RunDisplay.py: To display the combined video showing the live predictions.
- Run Map_Braille_character.py. Maps finger-tip coordinates to corresponding braille character on the given brf file. i.e. The character at position ({x_pos}, {y_pos}) is '{character}' and is located at row {row} and column {column}.

3. The output video file will be saved as 'Combined_output_video.mp4' in the project directory.

## Libraries and dependencies

- OpenCV (cv2): To process and display video files
- MediaPipe: To detect fingertip locations in the video
- NumPy: For numerical calculations
- Pandas: To process and manipulate CSV files
- CSV and datetime libraries: Part of the Python standard library, used for file processing and time calculations

Please make sure to install the required libraries and dependencies before running the project.
