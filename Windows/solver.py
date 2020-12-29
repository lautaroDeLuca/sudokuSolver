import cv2
from imutils import contours
import pytesseract as pt
import numpy as np
import glob
from sudokuSolver import solve
from sudokuSolver import printSudoku
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # your path may be different

def processImage():
    custom_config = r'--psm 6 -c tessedit_char_whitelist=123456789'

    route = r'sudoku3.png'
    image = cv2.imread(route)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,57,5)

    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < 1500:
            cv2.drawContours(thresh, [c], -1, (0,0,0), -1)

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, vertical_kernel, iterations=9)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,1))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, horizontal_kernel, iterations=4)

    invert = 255 - thresh
    cnts = cv2.findContours(invert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    (cnts, _) = contours.sort_contours(cnts, method="top-to-bottom")

    sudoku_rows = []
    row = []
    matrix = []
    ok = '123456789 '
    for (i, c) in enumerate(cnts, 1):
        area = cv2.contourArea(c)
        if area < 50000:
            row.append(c)
            if i % 9 == 0:  
                (cnts, _) = contours.sort_contours(row, method="left-to-right")
                sudoku_rows.append(cnts)
                row = []

    for row in sudoku_rows:
        for c in row:
            mask = np.zeros(image.shape, dtype=np.uint8)
            cv2.drawContours(mask, [c], -1, (255,255,255), -1)
            result = cv2.bitwise_and(image, mask)
            result[mask==0] = 255
            box = pt.image_to_string(result, config=custom_config)
            box = split(box)
            if box[0] == 'A':
                box[0] = '4'
            if all(c in ok for c in box[0]):
                matrix.append(int(box[0]))
            else:
                matrix.append(int(0))
    return matrix

def matrix2sudoku(mat):
    npmat = np.array(mat)
    sudoku = npmat.reshape(9,9)
    realSudoku = sudoku.tolist()
    return realSudoku

def split(word):
    return [char for char in word]

rawMatrix = processImage()
sudoku = matrix2sudoku(rawMatrix)
printSudoku(sudoku)
solve(sudoku)
print('______________________')
printSudoku(sudoku)
