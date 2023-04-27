import pandas as pd
import numpy as np

def find_closest_time_pair(time1, time2):
    time_diff = abs(time1 - time2)
    return time_diff.idxmin()

def l1_norm(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

def l2_norm(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def main():
    coord_file = "/Users/by12/Braille/FingerTracker/output_logs/monitor_data/test_acc.csv"
    no_z_file = "/Users/by12/Braille/FingerTracker/output_logs/coords_2023-04-20_00-27-28-429140.csv"

    coord_df = pd.read_csv(coord_file)
    no_z_df = pd.read_csv(no_z_file)
    no_z_df.iloc[:, 0] += 0.5

    print(no_z_df.head())
    coord_df['PredictedFinger'] = ""

    for index, row in coord_df.iterrows():
        closest_time_index = find_closest_time_pair(row['Time'], no_z_df['Time'])

        # Get the reference coordinates from index_coord_without_coordinate.csv
        ref_coords = []
        for col_name in coord_df.columns:
            if '_X' in col_name:
                ref_coords.append((row[col_name], row[coord_df.columns[coord_df.columns.get_loc(col_name) + 1]]))

        # Get the finger coordinates from no_z.csv
        finger_coords = [
            ('LeftThumb', (no_z_df.loc[closest_time_index, 'LeftThumbX'], no_z_df.loc[closest_time_index, 'LeftThumbY'])),
            ('LeftIndex', (no_z_df.loc[closest_time_index, 'LeftIndexX'], no_z_df.loc[closest_time_index, 'LeftIndexY'])),
            ('LeftMiddle', (no_z_df.loc[closest_time_index, 'LeftMiddleX'], no_z_df.loc[closest_time_index, 'LeftMiddleY'])),
            ('LeftRing', (no_z_df.loc[closest_time_index, 'LeftRingX'], no_z_df.loc[closest_time_index, 'LeftRingY'])),
            ('LeftPinky', (no_z_df.loc[closest_time_index, 'LeftPinkyX'], no_z_df.loc[closest_time_index, 'LeftPinkyY'])),
            ('RightThumb', (no_z_df.loc[closest_time_index, 'RightThumbX'], no_z_df.loc[closest_time_index, 'RightThumbY'])),
            ('RightIndex', (no_z_df.loc[closest_time_index, 'RightIndexX'], no_z_df.loc[closest_time_index, 'RightIndexY'])),
            ('RightMiddle', (no_z_df.loc[closest_time_index, 'RightMiddleX'], no_z_df.loc[closest_time_index, 'RightMiddleY'])),
            ('RightRing', (no_z_df.loc[closest_time_index, 'RightRingX'], no_z_df.loc[closest_time_index, 'RightRingY'])),
            ('RightPinky', (no_z_df.loc[closest_time_index, 'RightPinkyX'], no_z_df.loc[closest_time_index, 'RightPinkyY'])),
        ]

        # Find the closest finger
        predicted_fingers = []
        for ref_coord in ref_coords:
            if not pd.isna(ref_coord[0]) and not pd.isna(ref_coord[1]):
                min_distance = float('inf')
                closest_finger = None
                for finger, finger_coord in finger_coords:
                    distance = l2_norm(finger_coord, ref_coord)
                    
                    #Add a penalty factor to Ring and Pinky fingers
                    if  finger.endswith('Pinky') or  finger.endswith('Ring'):
                        penalty_factor = 10
                        distance *= penalty_factor

                    if distance < min_distance:
                        min_distance = distance
                        closest_finger = finger
                if closest_finger is not None:
                    predicted_fingers.append(closest_finger)


        # Update the predicted touching finger
        coord_df.loc[index, 'PredictedFinger'] = ', '.join(predicted_fingers)

    coord_df.to_csv('/Users/by12/Braille/FingerTracker/output_logs/predicted_touching_fingers.csv', index=False)


if __name__ == '__main__':
    main()






