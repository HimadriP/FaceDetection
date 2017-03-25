from scipy.misc import imread, imsave, imresize
import numpy as np
import Queue as Q
import matplotlib.pyplot as plt

def plot(img, v=0):
	if v == 1:
		plt.imshow(img, cmap='gray')
	else:
		plt.imshow(img)
	plt.show()

# Color correction

BRIGHTNESS = 0

def brightness_increement(img, brightness):
	img = img + brightness
	of = img>255
	img = of*255 + (1-of)*img
	return img

def contrast_correction(img):
	for i in range(len(img)):
		for j in range(len(img[i])):
			for k in range(len(img[i][j])):
				p = img[i][j][k]
				if p<26:
					p = 0
				elif p>229:
					p = 255
				else:
					p = (p + (p>>2)) - 32
				img[i][j][k] = p
	return img

def to_ycbcr(img):
	for i in range(len(img)):
		for j in range(len(img[i])):
			r  = img[i][j][0]
			g  = img[i][j][1]
			b  = img[i][j][2]
			y  =  0.257*r + 0.504*g + 0.098*b + 16
			cb = -0.148*r - 0.291*g + 0.439*b + 128
			cr =  0.439*r - 0.368*g - 0.071*b + 128
			img[i][j][0] = y
			img[i][j][1] = cb
			img[i][j][2] = cr
	return img

def to_skin_pixels(img):
	skin = np.zeros((len(img), len(img[0])))
	for i in range(len(img)):
		for j in range(len(img[0])):
			cb = img[i][j][1]
			cr = img[i][j][2]
			if 72<=cb and cb<=122 and 127<=cr and cr<=168:
				skin[i][j] = 1
	return skin

# Noise Filter : Window Space ( 7 X 7 )

limit = (7*7) / 2

def init_space(img,row_s,column_s=0):
        medval = 0
        for i in range(row_s,row_s+7):
                for j in range(column_s,column_s + 7):
                        medval += img[i][j]
        return medval

def check_limit(medval,limit):
        if (medval>limit):
                return 1
        else:
                return 0

def med_filter(img):
        
        for i in range(len(img)-6):

                #Initial median value for every new row
                medval = init_space(img,i)
                img[i+3][3] = check_limit(medval,limit)
                
                for j in range(1,len(img[0])-6):
                        for k in range(7):
                                medval = medval + img[i+k][j+6] - img[i+k][j-1]

                        img[i+3][j+3] = check_limit(medval,limit)
        return img
    
# Morphological filtering

# s = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
s = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
N   = 9
MIS = 0 
HIT = 1
FIT = 2

def get_n(img, x, y):
	d = [-1, 0, 1]
	n = 0
	for i in range(3):
		for j in range(3):
			_i  = x + d[i]
			_j  = y + d[j]
			_si = 1 + d[i]
			_sj = 1 + d[j]
			if _i<0 or _i>=len(img):
				continue
			if _j<0 or _j>=len(img[0]):
				continue
			n = n + img[_i][_j]&s[_si][_sj]
	return n

def check(img, i, j):
	n = get_n(img, i, j)
	if n == N:
		return FIT
	if n == 0:
		return MIS
	return HIT

def dilate(img):
	dil = np.zeros((len(img), len(img[0])))
	for i in range(len(img)):
		for j in range(len(img[0])):
			r = check(img, i, j)
			if r != MIS:
				dil[i][j] = 1
	return dil

def erode(img):
	ero = np.zeros((len(img), len(img[0])))
	for i in range(len(img)):
		for j in range(len(img[0])):
			r = check(img, i, j)
			if r == FIT:
				ero[i][j] = 1
	return ero


def morph_closing(img):
	img = dilate(img)
	plot(img, 1)
	img = erode(img)
	return img

# Connected components labelling

dx = [ 0, -1, 1, 0]
dy = [-1,  0, 0, 1]

def flood_fill(img, i, j, l):
	global dx, dy
	q = Q.Queue()
	q.put((i, j))
	c = img[i][j]
	while not q.empty():
		x, y = q.get()
		if img[x][y] != c:
			continue
		img[x][y] = l
		for k in range(4):
			_i = x + dx[k]
			_j = y + dy[k]
			if _i < 0 or _i >= len(img):
				continue
			if _j < 0 or _j >= len(img[0]):
				continue
			if c == img[_i][_j]:
				q.put((_i, _j))

def ccl(img):
	nc = 1
	img = -img
	for i in range(len(img)):
		for j in range(len(img[0])):
			if img[i][j] == -1:
				flood_fill(img, i, j, nc)
				nc = nc + 1
	return img

# Face Recognition

def recognize(img):
	img = brightness_increement(img, BRIGHTNESS)
	plot(img)
	img = contrast_correction(img)
	plot(img)
	img = to_ycbcr(img)
	plot(img, 0)
	img = to_skin_pixels(img)
	plot(img, 1)
        img = med_filter(img)
        plot(img, 1)
        img = morph_closing(img)
	plot(img, 1)
	img = ccl(img)
	plot(img, 1)
	return img

img = imread('faces3.jpg')
width = 64
ar = 1.0*len(img[0])/len(img)
img = imresize(img, (int(width/ar), width))

img = recognize(img)
