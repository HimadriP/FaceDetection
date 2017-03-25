from myhdl import *

def contrast_correction(i_r, i_g, i_b, i_clk, o_r, o_g, o_b):

	red = Signal(intbv(0)[8:])
	gre = Signal(intbv(0)[8:])
	blu = Signal(intbv(0)[8:])

	def contrast_correct(p):
		if p<26:
			return 0
		if p>226:
			return 255
		return (p+(p>>2))-32

	@always_comb
	def run():
		red.next = contrast_correct(i_r)
		gre.next = contrast_correct(i_g)
		blu.next = contrast_correct(i_b)

	@always_comb
	def outputs():
		o_r.next = red.next
		o_g.next = gre.next
		o_b.next = blu.next
                print o_r.next,o_g.next,o_b.next 
	return run, outputs
