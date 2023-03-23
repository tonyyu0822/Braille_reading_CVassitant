# Import the BraillePage class
from Braille_2_coord import BraillePage

# Create an instance of BraillePage with the path to a .brf file
braille_page = BraillePage("/Users/by12/Braille/FingerTracker/data/video/brf/full cells.brf")

# Call the position2Char method with x_pos and y_pos as arguments
x_pos = 5.0
y_pos = 3.0
character, row, column = braille_page.position2Char(x_pos, y_pos)

# Print the result
print(f"The character at position ({x_pos}, {y_pos}) is '{character}' and is located at row {row} and column {column}.")
