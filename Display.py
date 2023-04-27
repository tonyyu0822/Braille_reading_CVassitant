import pandas as pd
import cv2

class FingerPredictor:
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def get_predicted_finger_at_time(self, time):
        row = self.data.loc[self.data['Time'] < time].tail(1)
        if row.empty:
            return None, None
        return row['PredictedFinger'].values[0], row['Time'].values[0]

# Define the path to the input video file and CSV file
video_file_name = './Detected_output_video.mp4'
csv_file = '/Users/by12/Braille/FingerTracker/output_logs/predicted_touching_fingers.csv'

# Initialize the FingerPredictor
finger_predictor = FingerPredictor(csv_file)

# Start reading the video from the file
cap = cv2.VideoCapture(video_file_name)

fps_input = int(cap.get(cv2.CAP_PROP_FPS))
print(fps_input)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Output video
output_video_file = './Combined_output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_file, fourcc, 29, (frame_width, frame_height))

frame_no = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Finished analyzing video")
        break

    elapsed_time = frame_no / fps_input

    predicted_finger, finger_time = finger_predictor.get_predicted_finger_at_time(elapsed_time)
    if predicted_finger is not None:
        cv2.putText(frame, f"Time: {finger_time:.2f} Predicted Finger: {predicted_finger}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    # Write the frame to the output video
    out.write(frame)

    # Display the video
    cv2.imshow('Combined Video', frame)
    delay = int(1000 / fps_input)
    if cv2.waitKey(delay) & 0xFF == ord('q'):  # Exit the video playback by pressing the Q key.
        break

    frame_no += 1

cap.release()
out.release()
cv2.destroyAllWindows()
