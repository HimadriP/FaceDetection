from myhdl import *

def morphological_closing(i_img, i_clk, o_img):

	window = Signal(intbv(0)[8:])
	img = Signal(intbv(0)[8:0])[8:0]

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

	def init():

		window = Signal(intbv(0)[8:])
		img = Signal(intbv(0)[8:0])[8:0]

		win = 0
		for i in range(7):
			for j in range(7):
				win += i_img[i][j]
		window = Signal(intbv(win)[8:])

		return window

                        
	def get_column(i, j, i_img):
		x = 0
		for k in range(7):
			if i+k < len(i_img):
				x += i_img[i+k][j]
		return x;

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
				if img[_i][_j]:
					n = n + int(img[_i][_j])*s[_si][_sj]
		return n

	def check(img, i, j):
		n = get_n(img, i, j)
		if n == N:
			return FIT
		if n == 0:
			return MIS
		return HIT

	def dilate(img):
		dil = [ [ 0 for j in range(len(i_img[0])) ] for i in range(len(i_img)) ]
		for i in range(len(img)):
			for j in range(len(img[0])):
				r = check(img, i, j)
				if r != MIS:
					dil[i][j] = 1
		return dil

	def erode(img):
		ero = [ [ 0 for j in range(len(i_img[0])) ] for i in range(len(i_img)) ]	
		for i in range(len(img)):
			for j in range(len(img[0])):
				r = check(img, i, j)
				if r == FIT:
					ero[i][j] = 1
		return ero


	def morph_closing(img):
		img = dilate(img)
		# plot(img, 1)
		img = erode(img)
		return img


	dx = [ 0, -1, 1, 0]
	dy = [-1,  0, 0, 1]

	def flood_fill(img, i, j, l):
		global dx, dy
		q = []
		q.append((i, j))
		c = img[i][j]
		while not len(q):
			x, y = q.pop(0)
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
					q.append((_i, _j))
		return img

	def ccl(img):
		nc = 1
		for i in range(len(i_img)):
			for j in range(len(i_img[0])):
				img[i][j] = -img[i][j]
		for i in range(len(img)):
			for j in range(len(img[0])):
				if img[i][j] == 1:
					img = flood_fill(img, i, j, nc)
					nc = nc + 1
		print("nc"+str(nc))
		return img

	@always(i_clk.posedge)
	def morphological():
		delay(10)
		window = init()
		img = [ [ 0 for j in range(len(i_img[0])) ] for i in range(len(i_img)) ]
		# for i in range(2, len(i_img)-2):
		# 	for  j in range(2, len(i_img[0])-2):
		# 		window = window - get_column(i-2, j, i_img) + get_column(i+3, j, i_img)
		# 		if window > (7*7)>>2:
		# 			img[i][j] = 1
		# 		else:
		# 			img[i][j] = 0
		# 		i_img[i][j] = Signal(intbv(img[i][j])[8:])
		# print("asdf")
		for i in range(len(i_img)):
			for j in range(len(i_img[0])):
				img[i][j] = int(i_img[i][j])
		img = med_filter(img)
		img = morph_closing(img)
		img = ccl(img)
		for i in range(len(i_img)):
			for j in range(len(i_img[0])):
				p = img[i][j]
				if not p:
					p = 0
				o_img[i][j].next = Signal(intbv(p)[1:])
				# print((o_img[i][j].next, p))

	return morphological