from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
from scipy import ndimage
import os


def seam_carving(image, target_width):
    current_width = image.size[0]
    current_height = image.size[1]
    image = np.array(image).astype(np.uint8)
    
    while current_width > target_width:
        sx = ndimage.sobel(image, axis = 0, mode='constant')
        sy = ndimage.sobel(image, axis = 1, mode='constant')
        sobel = np.absolute(sx) + np.absolute(sy)
        energy = sobel.sum(axis = 2)
        
        M = np.zeros([current_height, current_width])
        # prvi red je energija piksela iz prvog reda
        M[0] = energy[0]
        for i in range(1, current_height):
            M[i, 0] = energy[i, 0] + min(M[i - 1, 0], M[i - 1, 1])
            M[i, current_width - 1] = energy[i, current_width - 1] + min(M[i - 1, current_width - 1], M[i - 1, current_width - 2])
            for j in range(1, current_width - 1):
                M[i, j] = energy[i, j] + min(M[i - 1, j - 1], min(M[i - 1, j], M[i - 1, j + 1]))
        seam = np.zeros([current_height]).astype(int)
        m = 0
        for j in range(1, current_width):
            if M[current_height - 1, 0] > M[current_height - 1, j]:
                m = j
            seam[current_height - 1] = m
        
        for i in reversed(range(1, current_height)):
            j = seam[i]
            if j == 0:
                # posmatramo samo desnog suseda
                if M[i - 1, j] < M[i - 1, j + 1]:
                    seam[i - 1] = j
                else:
                    seam[i - 1] = j + 1
            elif j == current_width - 1:
                # posmatramo samo levog suseda
                if M[i - 1, j] < M[i - 1, j - 1]:
                    seam[i - 1] = j
                else:
                    seam[i - 1] = j - 1
            else:
                # posmatramo oba suseda
                m = min(M[i - 1, j - 1], min(M[i - 1, j], M[i - 1, j + 1]))
                if m == M[i - 1, j - 1]:
                    seam[i - 1] = j - 1
                elif m == M[i - 1, j]:
                    seam[i - 1] = j
                else:
                    seam[i - 1] = j + 1
        
        new_image = np.zeros([current_height, current_width - 1, 3]).astype(np.uint8)
        for i in range(current_height):
            for j in range(current_width):
                if j < seam[i]:
                    new_image[i, j] = image[i, j]
                elif j > seam[i]:
                    new_image[i, j - 1] = image[i, j]
                else:
                    continue
                    
        image = new_image
        current_width -= 1
        
    return image
    

dir_path = r'assets'

# list to store files
res = []

# Iterate directory
for file_path in os.listdir(dir_path):
    # check if current file_path is a file
    if os.path.isfile(os.path.join(dir_path, file_path)):
        # add filename to list
        res.append(file_path)
print(res)

for file_path in res:
    image = Image.open('assets/' + file_path)
    img = seam_carving(image, image.size[0] - 50)
    image = Image.fromarray(img)
    image.save('rezultati_skracivanje/' + file_path)


