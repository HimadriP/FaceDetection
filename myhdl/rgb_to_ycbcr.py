from myhdl import *

def rgb_to_ycbcr(i_r, i_g, i_g, i_clk, o_r, o_g, o_b):

	red = Signal(intbv(0)[8:])
	gre = Signal(intbv(0)[8:])
	blu = Signal(intbv(0)[8:])

	@always(i_clk.posedge)
	def run():
		red.next = (r + r<<1 + r<<2 + r<<8 + g<<9 + g<<2 + b<<6 + b<<5 + b<<2)>>10 + 16
		#red.next =  0.257*r + 0.504*g + 0.098*b + 16
		gre.next = (-(r<<7 + r<<4 + r<<2 + r<<1 + r) - (g<<8 + g<<5 + g<<3 + g<<1) + b<<8 + b<<7 + b<<6 + b<<1)>>10 + 128
		#gre.next = -0.148*r - 0.291*g + 0.439*b + 128
		blu.next = (r<<8 + r<<7 + r<<6 + r<<1 - (g<<8 + g<<6 + g<<5 + g<<4 + g<<3 + g) - (b<<6 + b<<3 + b))>>10 + 128
		#blu.next =  0.439*r - 0.368*g - 0.071*b + 128

	@always_comb
	def outputs():
		o_r.next = red.next
		o_g.next = gre.next
		o_b.next = blu.next

	return run, outputs
