import csv

def delete_z_columns(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        data = [row for row in reader]
    
    new_header = [col for col in header if not col.endswith("Z") and col not in ["FrameNumber", "HandsPresent"]]
    new_data = []
    for row in data:
        new_row = [row[header.index(col)] for col in new_header]
        new_data.append(new_row)
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(new_header)
        writer.writerows(new_data)

# Example usage
delete_z_columns("/Users/by12/Braille/FingerTracker/output_logs/coords_2023-03-22_23-03-05-145722.csv")
