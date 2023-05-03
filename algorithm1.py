import cv2 as cv
import numpy as np

def e(grad_X, grad_Y, i, j):
	return abs(grad_X[i, j, 0]) + abs(grad_Y[i, j, 0])
	+ abs(grad_X[i, j, 1]) + abs(grad_Y[i, j, 1])
	+ abs(grad_X[i, j, 2]) + abs(grad_Y[i, j, 2])

def matrix_m(img):
	shape = img.shape
	rows = shape[0]
	cols = shape[1]
	gradient_X = cv.Sobel(img, cv.CV_64F, 1, 0, ksize=3)
	gradient_Y = cv.Sobel(img, cv.CV_64F, 0, 1, ksize=3)

	energy = np.zeros((rows, cols))

	for i in range(rows):
		for j in range(cols):
			energy[i, j] = e(gradient_X, gradient_Y, i, j) 

	M = np.zeros((rows, cols))


	for j in range(0, cols):
		M[0, j] = energy[0, j]

	for i in range(1, rows):
		M[i, 0] = energy[i, 0] + min(M[i-1, 0], M[i-1, 1])
		for j in range(1, cols - 1):
			M[i][j] = energy[i, j] + min(min(M[i-1, j-1], M[i-1, j]), M[i-1, j+1])
		M[i, cols - 1] = energy[i, j] + min(M[i-1, j-1], M[i-1, j])	
	
	return M
	
def remove_horizontal_seam(img):
	shape = img.shape
	rows = shape[0]
	cols = shape[1]
	
	M = matrix_m(img)
	
	seam = np.zeros(cols).astype(int)

	m = 0
	for i in range(1, rows):
		if M[i, cols - 1] < M[m, cols - 1]:
			m = i
		
	seam[cols - 1] = m
##	print(vertical_seam[rows - 1])
	## bactrack to the previous row
	for j in reversed(range(0, cols - 1)):
		## find the min among the three options
		_min = seam[j]
		if _min == rows - 1:
			seam[j] = _min if (M[_min, j] < M[_min - 1, j]) else _min - 1
		elif _min == 0:
			seam[j] = _min if (M[_min, j] < M[_min + 1, j]) else _min + 1
		else:
			x = min(M[_min, j], min(M[_min - 1, j], M[_min + 1, j]))
			if x == M[_min, j]:
				seam[j] = _min
			elif x == M[_min - 1, j]:
				seam[j] = _min - 1
			else:
				seam[j] = _min + 1
			
##	for i in range(0, rows):
##		img[i, vertical_seam[i]] = [0, 0, 0]
	new_image = np.zeros((rows - 1, cols, 3), np.uint8)
	for j in range(cols):
		x = seam[j]
		for i in range(x):
			new_image[i, j] = img[i, j]
		for i in range(x + 1, rows):
			new_image[i - 1, j] = img[i, j]
	return new_image

def remove_horizontal_seams(img, counter):
	new_image = img
	for i in range(counter):
		new_image = remove_horizontal_seam(new_image)
	return new_image
		
def remove_vertical_seams(img, counter):
	new_image = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
	for i in range(counter):
		new_image = remove_horizontal_seam(new_image)
	return cv.rotate(new_image, cv.ROTATE_90_CLOCKWISE)


img = cv.imread('nature1.jpg')
assert img is not None, "file could not be read, check with os.path.exists()"

shape = img.shape

rows = shape[0]
cols = shape[1]

print(rows)
print(cols)

## for i in range(0, rows):
##	for j in range(0, cols):
##		print(img[i][j])

h = int(input("Enter target height: "))
w = int(input("Enter target width: "))

img = remove_vertical_seams(img, cols - w)
img = remove_horizontal_seams(img, rows - h)

cv.imwrite('nature1_seam.jpg', img)

##cv.imshow('photo', img)
cv.waitKey(0)
cv.destroyAllWindows()

