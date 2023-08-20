from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage
import os


def find_seams(image, target_width, K):
    current_width = image.size[0]
    current_height = image.size[1]
    K = target_width - current_width
    image = np.array(image).astype(np.float32)
    seam = np.zeros([current_height, K]).astype(int)
    k = 0
    
    while k != K:
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
        
        # racunamo trenutnu traku
        m = 0
        for j in range(1, current_width):
            if M[current_height - 1, 0] > M[current_height - 1, j]:
                m = j
            seam[current_height - 1, k] = m
        
        for i in reversed(range(1, current_height)):
            j = seam[i, k]
            if j == 0:
                # posmatramo samo desnog suseda
                if M[i - 1, j] < M[i - 1, j + 1]:
                    seam[i - 1, k] = j
                else:
                    seam[i - 1, k] = j + 1
            elif j == current_width - 1:
                # posmatramo samo levog suseda
                if M[i - 1, j] < M[i - 1, j - 1]:
                    seam[i - 1, k] = j
                else:
                    seam[i - 1, k] = j - 1
            else:
                # posmatramo oba suseda
                m = min(M[i - 1, j - 1], min(M[i - 1, j], M[i - 1, j + 1]))
                if m == M[i - 1, j - 1]:
                    seam[i - 1, k] = j - 1
                elif m == M[i - 1, j]:
                    seam[i - 1, k] = j
                else:
                    seam[i - 1, k] = j + 1
        
        new_image = np.zeros([current_height, current_width - 1, 3]).astype(np.float32)
        for i in range(current_height):
            for j in range(current_width):
                if j < seam[i, k]:
                    new_image[i, j] = image[i, j]
                elif j > seam[i, k]:
                    new_image[i, j - 1] = image[i, j]
                else:
                    continue
                    
        image = new_image
        current_width -= 1
        k += 1
        
    return seam

def return_seam(x1, x2):
    if x2 < x1:
        return x2
    else:
        return x2 + 1

def return_seams(seams, K, height):
    for i in range(height):
        # unazad imitiramo vracanje jedne po jedne trake
        for k in range(1, K):
            for j in reversed(range(k, K)):
                seams[i, j] = return_seam(seams[i, j - k], seams[i, j])
    return seams


def seam_carving_enlarge(image, target_width):
    K = target_width - image.size[0]
    current_height = image.size[1]
    current_width = image.size[0]
    seams = find_seams(image, target_width, K)
    seams = return_seams(seams, K, current_height)
    
    for i in range(image.size[1]):
        seams[i].sort()


    new_image = np.zeros([current_height, current_width + K, 3]).astype(np.float32)
    image = np.array(image).astype(np.float32)
    
    for i in range(current_height):
    # idemo od 0 do seams[i, 0], pa do seams[i, 1]...
        for j in range(seams[i, 0] + 1):
            new_image[i, j] = image[i, j]
       
        if seams[i, 0] == 0:
            new_image[i, seams[i, 0] + 1] = image[i, seams[i, 0]] / 2
        else:
            new_image[i, seams[i, 0] + 1] = (image[i, seams[i, 0] - 1] + image[i, seams[i, 0] + 1]) / 2
    
        for k in range(K - 1):
            for j in range(seams[i, k] + k + 2, seams[i, k + 1] + k + 2):
                new_image[i, j] = image[i, j - k - 1]
            
            if seams[i, k + 1] == current_width - 1:
                new_image[i, seams[i, k + 1] + k + 2] = image[i, current_width - 1] / 2
            else:
                new_image[i, seams[i, k + 1] + k + 2] = (image[i, seams[i, k + 1] - 1] + image[i, seams[i, k + 1] + 1]) / 2
        
        for j in range(seams[i, K - 1] + K + 1, current_width + K):
            new_image[i, j] = image[i, j - K - 2]
        
    return new_image
    
    
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
    print(file_path)
    image = Image.open('assets/' + file_path)
    img = seam_carving_enlarge(image, image.size[0] + 30)
    img = (img * 255 / np.max(img)).astype(np.uint8)
    image = Image.fromarray(img)
    image.save('rezultati_uvecavanje2/' + file_path)
    image = 0
    
    
    
    
    
    
    
    
    







