#!/usr/bin/python

from pylab import *
import numpy as np
from scipy import fftpack
import gen_pattern as gp

def fft_test():
	aux_mat = gp.prepare_aux_matrices(512)
	#p_lg = gp.gen_lg_pattern(1,10,aux_mat,5)
	#p_bg = gp.gen_blaze_grating(50,aux_mat)
	#p_swirl = gp.gen_swirl_pattern(aux_mat, dz=10, twist=10)
	#p_hg = gp.gen_hg_pattern(512, m=1, n=2)
	p_z = exp(1j*gp.phasemap(p_hg+p_bg)*2*pi)
	#imshow(gp.phasemap(p_swirl), cmap=get_cmap('binary'))
	#figure(2)
	imshow(fftpack.fftshift(abs(fftpack.fft2(p_z))), cmap=get_cmap('binary'))
	show()

if __name__ == '__main__':
	fft_test()