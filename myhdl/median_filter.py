from myhdl import *

def median_filter(i_img, i_clk, o_img):

	window = Signal(intbv(0)[8:])
	img = Signal(intbv(0)[8:0])[8:0]

	def init():
		global i_img
		for i in range(7):
			for j in range(7):
				window += i_img[i][j]

	def get_column(i, j):
		global i_img
		x = 0
		for k in range(7):
			x += i_img[i+k][j]
		return x;

	@always(i_clk.posedge)
	def median_filter():
		global i_img, o_img
		for i in range(2, len(i_img)-2):
			for  j in range(2, len(i_img[0])-2):
				window = window - get_column(i-2) + get_column(i+3)
				if window > (7*7)>>2:
					img.next[i][j] = 1
				else
					img.next[i][j] = 0

	@always_comb
	def outputs():
		o_imig = img

	return median_filter