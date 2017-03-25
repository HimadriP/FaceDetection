from myhdl import *
def brightness_increement(i_r, i_g, i_b, i_brightness, i_clk, o_r, o_g, o_b):

	red = Signal(intbv(0)[8:])
	gre = Signal(intbv(0)[8:])
	blu = Signal(intbv(0)[8:])

	def truncate(x):
		if x>255:
			x = 255
		return x

	@always(i_clk.posedge)
	def run():
		red.next = truncate(i_r + i_brightness)
		gre.next = truncate(i_g + i_brightness)
		blu.next = truncate(i_b + i_brightness)

	@always_comb
	def outputs():
		o_r.next = red.next
		o_g.next = gre.next
		o_b.next = blu.next
                print o_r.next,o_g.next,o_b.next
	return run, outputs
