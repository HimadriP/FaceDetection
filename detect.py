from myhdl import *
from brightness_increement import *
from contrast_correction import *
from rgb_to_ycbcr import *
from skin_threshold import *
from median_filter import *
from morphological import *
from ccl import *
from scipy.misc import imread, imsave, imresize
import numpy as np
# import Queue as Q
import matplotlib.pyplot as plt

def start(img):

    def clkDriver(clk):
        halfPeriod = delay(10)
        @always(halfPeriod)

        def driverclk():
            clk.next = not clk

        return driverclk



    clk = Signal(intbv(0)[8:])
    clkin = clkDriver(clk)


    BRIGHTNESS = Signal(intbv(20)[8:])

    # Convert img to Singal intbv
    img_o = None
    img_b = None
    img_c = None
    img_y = None
    img_s = None
    img_m = None
    img_l = None

    # Convert img to Singal intbv
    img_o = [ [ [ Signal(intbv(0)[8:]) for k in range(3) ] for i in range(len(img[0]))] for j in range(len(img))]
    img_b = [ [ [ Signal(intbv(0)[8:]) for k in range(3) ] for i in range(len(img[0]))] for j in range(len(img))]
    img_c = [ [ [ Signal(intbv(0)[8:]) for k in range(3) ] for i in range(len(img[0]))] for j in range(len(img))]
    img_y = [ [ [ Signal(intbv(0)[8:]) for k in range(3) ] for i in range(len(img[0]))] for j in range(len(img))]
    img_s = [ [   Signal(intbv(0)[1:]) for i in range(len(img[0]))] for j in range(len(img))]
    img_m = [ [   Signal(intbv(0)[1:]) for i in range(len(img[0]))] for j in range(len(img))]
    img_l = [ [   Signal(intbv(0)[1:]) for i in range(len(img[0]))] for j in range(len(img))]

    for i in range(len(img)):
        for j in range(len(img[0])):
            for k in range(3):
                img_o[i][j][k] = Signal(intbv(int(img[i][j][k]))[8:])
                

    def channel_in(clk):
        brightness_channel = [[None for i in range(len(img[0]))] for j in range(len(img))]
        contrast_channel   = [[None for i in range(len(img[0]))] for j in range(len(img))]
        ycbcr_channel      = [[None for i in range(len(img[0]))] for j in range(len(img))]
        skin_channel       = [[None for i in range(len(img[0]))] for j in range(len(img))]
        for i in range(len(img)):
            for j in range(len(img[0])):
                brightness_channel[i][j] = brightness_increement(img_o[i][j][0], img_o[i][j][1], img_o[i][j][2], BRIGHTNESS, clk, img_b[i][j][0], img_b[i][j][1], img_b[i][j][2])
                contrast_channel[i][j]   = contrast_correction  (img_b[i][j][0], img_b[i][j][1], img_b[i][j][2], clk, img_c[i][j][0], img_c[i][j][1], img_c[i][j][2])
                ycbcr_channel[i][j]      = rgb_to_ycbcr         (img_c[i][j][0], img_c[i][j][1], img_c[i][j][2], clk, img_y[i][j][0], img_y[i][j][1], img_y[i][j][2])
                skin_channel[i][j]       = skin_threshold       (img_y[i][j][0], img_y[i][j][1], img_y[i][j][2], clk, img_s[i][j])
        return instances()

    # def init(imgh):
    cin = channel_in(clk)
    sim = Simulation(clkin,cin)
    sim.run(200)

    morphological_channel = morphological_closing(img_s, clk, img_m)
    sim1 = Simulation(clkin, morphological_channel)
    sim1.run(200)
    print("donee")

    final = [[ 0 for i in range(len(img[0]))] for j in range(len(img))]
    for i in range(len(img)):
        for j in range(len(img[0])):
            final[i][j] = int(img_m[i][j])
            # print(final[i][j])

    # print(final)

    plt.imshow(final, cmap='gray')
    plt.show()

# img = imread('../faces3.jpg')
# width = 64
# ar = 1.0*len(img[0])/len(img)
# img = imresize(img, (int(width/ar), width))

# start(img)

#Converting to VHDL

# clkD = toVHDL(clkDriver,clk)
# BI = toVHDL(brightness_increement,img_o[0][0][0], img_o[0][0][1], img_o[0][0][2], BRIGHTNESS, clk, img_b[0][0][0], img_b[0][0][1], img_b[0][0][2])
# cc = toVHDL(contrast_correction,img_b[0][0][0], img_b[0][0][1], img_b[0][0][2], clk, img_c[0][0][0], img_c[0][0][1], img_c[0][0][2])
# ycbcr = toVHDL(rgb_to_ycbcr,img_c[0][0][0], img_c[0][0][1], img_c[0][0][2], clk, img_y[0][0][0], img_y[0][0][1], img_y[0][0][2])
# skin = toVHDL(skin_threshold,img_y[0][0][0], img_y[0][0][1], img_y[0][0][2], clk, img_s[0][0])
