from myhdl import *

def skin_threshold(i_y, i_cb, i_cr, i_clk, o_s):

	skin_pixel = Signal(intbv(0)[1:])

	@always(i_clk.posedge)
	def run():
		delay(6)
		if 72 <= i_cb and i_cb <=122 and  127 <= i_cr and i_cr <= 168:
			skin_pixel.next = 1
			# print("skin")
		else: 
			skin_pixel.next = 0
		#print(skin_pixel.next)

	@always_comb
	def outputs():
		o_s.next = skin_pixel.next

	return run, outputs
