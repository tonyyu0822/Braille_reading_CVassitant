import numpy as np

class BraillePage:
    """
    Class representing a page of braille. Position of finger is measured from top right corner.
    """
    # number of rows and columns of Braille characters on printed Braille sheet
    numRows = 26
    numColumns = 42

    ### NOTE: might want to change page/margin dimensions to inputs? not sure if this is necessary feature
    # Braille sheet dimensions (in inches)
    pageWidth = 11.5 # originally 11.5625, but should be 11.5? double check measurements later
    pageHeight = 11
    leftMargin = 0.875
    rightMargin = 0.75
    topMargin = 0.5
    botMargin = 0.625

    def __init__(self, brf_file_path):
        """
        initialize page of Braille
        :param brf_file_path: path to .brf file of Braille to load in
        """
        # load in file at input path
        fileStr = self.loadBrf(brf_file_path)

        # convert input Braille file into a matrix
        self.charMatrix = self.assignCharGridCoords(fileStr)
    
    # Converts .brf file into text string
    def loadBrf(self, brf_file_path):
        """
        Loads in Braille .brf file into a String
        :param brf_file_path: path to .brf file of Braille to load in 
        :return: text string read from file at input path
        """
        with open(brf_file_path, 'r') as fh:
            fileStr = fh.read()
        return fileStr
        
    def assignCharGridCoords(self, textFile):
        """
        :param textFile: test string obtained from text file of braille printout
        :return: np matrix where each character is allocated a grid position on the page
        ex. reference 3rd row, 5th character by calling assignCharGridCoords(textFile,numRows,numColumns)[5][3]
        """
        charCoords = np.empty((self.numRows, self.numColumns), str)
        charCount = 0
        for row in range(self.numRows):
            for column in range(self.numColumns):
                char = textFile[charCount]
                charCount += 1
                if char == '\n':
                    break
                charCoords[row][column] = char
        print('done')
        return charCoords

    def position2GridCoord(self, x_pos, y_pos):
        """
        Translates the x and y postions (continuous) of the finger into discrete row, column coordinates on Braille sheet

        SOMETIMES OFF BY 1 ROW OR COLUMN, POSSIBLY DUE TO EMBOSSER INACCURACY
        """
        x_coord = int(self.numColumns * (x_pos - self.leftMargin) / (self.pageWidth - self.leftMargin - self.rightMargin))
        y_coord = int(self.numRows * (y_pos - self.topMargin) / (self.pageHeight - self.topMargin - self.botMargin))
        return x_coord, y_coord
        
    def position2Char(self, x_pos, y_pos):
        """
        :returns: the character at the given x, y positions (continuous) measured from top left of Braille sheet. Also returns the row and column the character is located at.
        """
        # check if x, y finger position is with page margins
        if (x_pos >= self.leftMargin and x_pos < self.pageWidth - self.rightMargin and y_pos >= self.topMargin and y_pos < self.pageHeight - self.botMargin):
            gridCoords = self.position2GridCoord(x_pos, y_pos)
            row = gridCoords[0]
            column = gridCoords[1]
            return self.charMatrix[column][row], row, column
        else:
            #returns char = ' ' and row/column = -1 if finger outside margins
            return ' ', -1, -1
        
if __name__ == '__main__':
    test = BraillePage('/Users/by12/Braille/FingerTracker/data/video/brf/full cells.brf')