import cv2 as cv
import numpy as np

def F_v1(i, j, K, img):
	return np.linalg.norm(img[i, j + K] - img[i, j - 1])
	+ np.linalg.norm(img[i - 1, j + K - 1] - img[i, j - 1])
	
def F_v2(i, j, K, img):
	return np.linalg.norm(img[i, j + K] - img[i, j - 1])

def F_v3(i, j, K, img):
	return np.linalg.norm(img[i, j + K] - img[i, j - 1])
	+ np.linalg.norm(img[i - 1, j] - img[i, j + K])

def energy(img):
	rows = img.shape[0]
	cols = img.shape[1]
	gradX = np.gradient(img, axis = 0)
	gradY = np.gradient(img, axis = 1)
	return [[np.linalg.norm(gradX[i, j]) + np.linalg.norm(gradY[i, j]) for j in range (cols)] for i in range(rows)]
	

def matrix_M(img, K):
	rows = img.shape[0]
	cols = img.shape[1]
	
	E = energy(img)
	
	M = np.zeros((rows, cols - K))
	
	e = 0
	
	for j in range(0, K):
		e += E[0][j]
	
	M[0, 0] = e
	e -= E[0][0]
	e += E[0][K]
	
	for j in range(1, cols - K - 1):
		M[0, j] = e
		e -= E[0][j - 1]
		e += E[0][j + K + 1]
		
	M[0, cols - K - 1] = e
	
	for i in range(1, rows):
		e = 0
		for j in range(0, K):
			e += E[i][j]
		
		M[i, 0] = e + min(M[i - 1, 0] + F_v2(i, j, K, img), M[i - 1, 1] + F_v3(i, j, K, img))
		e -= E[i][0]
		e += E[i][K]
			
		for j in range(1 , cols - K - 2):
			M[i, j] = e + min(min(M[i - 1, j - 1] + F_v1(i, j, K, img), M[i - 1, j] + F_v2(i, j, K, img)), M[i - 1, j + 1] + F_v3(i, j, K, img))
			e -= E[i][j - 1]
			e += E[i][j + K]
			
		M[i, cols - K - 2] = e
		e -= E[i][cols - K - 2]
		e += E[i][cols - 1]
		
		M[i, cols - K - 1] = e + min(M[i - 1, j - 1] + F_v1(i, j, K, img), M[i - 1, j] + F_v2(i, j, K, img))
	
	return M
	
def batch_seam(img, K):
	rows = img.shape[0]
	cols = img.shape[1]
	
	M = matrix_M(img, K)
	
	## find the minimum in the last row of M
	m = 0
	for j in range(1, cols - K):
		if M[rows - 1, j] < M[rows - 1, m]:
			m = j
	
	seam = np.zeros(rows).astype(int)
	
	seam[rows - 1] = m
	
	for i in reversed(range(rows - 1)):
		_min = seam[i + 1]
		if _min == cols - K - 1:
			seam[i] = (_min if (M[i, _min] < M[i, _min - 1]) else _min - 1)
		elif _min == 0:
			seam[j] = (_min if (M[i, _min] < M[i, _min + 1]) else _min + 1)
		else:
			x = min(M[i, _min - 1], min(M[i, _min], M[i, _min + 1]))
			if x == M[i, _min]:
				seam[i] = _min
			elif x == M[i, _min - 1]:
				seam[i] = _min - 1
			else:
				seam[i] = _min + 1
	
	return seam

def seam_carving_vertical(img, K, w):
	rows = img.shape[0]
	cols = img.shape[1]
	tmp = img
	
	while cols > w:
		if cols - w < K:
			K = cols - w
		
		seam = batch_seam(tmp, K)
	
		## now delete the seam from the image
		new_img = np.zeros((rows, cols - K, 3), np.uint8)
		for i in range(rows):
			for j in range(seam[i]):
				new_img[i, j] = tmp[i, j]
			
			for j in range(seam[i], cols - K):
				new_img[i, j] = tmp[i, j + K]
		
		tmp = new_img
		rows = tmp.shape[0]
		cols = tmp.shape[1]
	
	return new_img
	
def colour_seam(img, K):
	rows = img.shape[0]
	cols = img.shape[1]
	seam = batch_seam(img, K)
	
	for i in range(rows):
		for j in range(K):
			img[i, j + seam[i]] = [0, 255, 0]
	cv.imwrite('batch_colouring.png', img)

if __name__ == '__main__':
	
	image = input("Path to the image: ")
	img = cv.imread(image)
	assert img is not None, "file could not be read, check with os.path.exists()"

	shape = img.shape

	rows = shape[0]
	cols = shape[1]

	print(rows)
	print(cols)

	h = int(input("Enter target height: "))
	w = int(input("Enter target width: "))
	K = int(input("Enter desired K: "))

#	new_img = seam_carving_vertical(img, K, w)

#	cv.imwrite("batch_seam_" + image, new_img)
	
	colour_seam(img, K)

	##cv.imshow('photo', img)
	cv.waitKey(0)
	cv.destroyAllWindows()

