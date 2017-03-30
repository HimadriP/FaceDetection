from scipy.misc import imread, imsave, imresize
import numpy as np
# import Queue as Q
import matplotlib.pyplot as plt
import face
import detect, brightness_increement, contrast_correction, rgb_to_ycbcr, skin_threshold, morphological
import pygame
import pygame.camera

pygame.camera.init()

cam = pygame.camera.Camera('/dev/video0', (640, 480))

cam.start()

img = cam.get_image()

pygame.image.save(img, 'image.jpg')

img = imread('image.jpg')
width = 480
ar = 1.0*len(img[0])/len(img)
img = imresize(img, (int(width/ar), width))

cam.stop()

print(img[0][0])
detect.start(img)

# img = face.recognize(img)