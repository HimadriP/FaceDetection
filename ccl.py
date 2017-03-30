from myhdl import *

def connected_components(i_img, i_clk, o_img):


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
				if img[i][j] == 1:
					print("geit")
				img[i][j] = -img[i][j]
		for i in range(len(img)):
			for j in range(len(img[0])):
				if img[i][j] == -1:
					img = flood_fill(img, i, j, nc)
					nc = nc + 1
		print("nc"+str(nc))
		return img

	@always(i_clk.posedge)
	def run():
		delay(400)
		img = [ [ None for j in range(len(i_img[0])) ] for i in range(len(i_img)) ]
		for i in range(len(i_img)):
			for j in range(len(i_img[0])):
				img[i][j] = int(i_img[i][j])
		img = ccl(img)
		for i in range(len(i_img)):
			for j in range(len(i_img[0])):
				p = img[i][j]
				o_img[i][j].next = Signal(intbv(p)[8:0])
				if p!=0:
					print(o_img[i][j].next)

	return run