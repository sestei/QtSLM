#!/usr/bin/python

import numpy as np
from scipy.special import genlaguerre
from scipy import fftpack

def theta(x):
	"""
	Heaviside function (unit step function)
	"""
	return (np.sign(x)+1) * 0.5

def create_beziermap(P1, P2, imin, imax):
	"""
	Creates a four-point bezier curve starting at 0 and ending at 1,
	with control points P1 at 1/3 and P2 at 2/3, for use as an
	intensity map.
	"""
	a = 1.0 - 3*P2 + 3*P1
	b = 3*P2 - 6*P1
	c = 3*P1

	return lambda t: np.minimum(imax, np.maximum(imin, a*t**3 + b*t**2 + c*t))

def phasemap(phase, intensitymap = None):
	"""
	Wrap phase between 0 and 2pi, convert to 0..1
	"""
	if not intensitymap:
		intensitymap = lambda t: t
	minphase = np.floor(np.min(phase) / np.pi)
	phase += minphase * np.pi
	phase %= 2*np.pi
	return intensitymap(phase / (2*np.pi))

def fourier_image(phasemap):
	p_z = exp(1j*gp.phasemap(p_swirl)*2*pi)
	return fftpack.fftshift(abs(fftpack.fft2(p_z)))

def prepare_aux_matrices(size, xoffset=0, yoffset=0):
	"""
	Prepare auxiliary matrices used by the pattern generators.
	"""
	size = np.floor(size/2)
	x = np.arange(-size, size)
	xx, yy = np.meshgrid(x+xoffset, x+yoffset)
	rr = np.sqrt(xx**2 + yy**2) / size
	return (xx, yy, rr)

def gen_lg_pattern(l, p, aux_mat, scale):
	"""
	Generate phase pattern for LG_{lp} modes, returns a matrix
	with dimension size x size.
	The width is assumed to be ''scale''*2 waist radii. 
	"""
	if l == p == 0:
		return np.zeros_like(aux_mat[0])
	rr = aux_mat[2] * scale
	phi = np.arctan2(aux_mat[0],aux_mat[1])
	L = genlaguerre(p, l)
	return -l*phi + np.pi*theta(-L(2*rr**2))

def gen_blaze_grating(lines, aux_mat, coverage = 1.0):
	lw = np.floor(len(aux_mat[0]) / lines)
	grating = (aux_mat[0] % lw) / lw * 2*np.pi

	# mask out elements that are outside coverage area
	np.putmask(grating, aux_mat[2] > coverage, 0.0)
	return grating

def gen_swirl_pattern(aux_mat, twist=0, dz=1):
	rr = aux_mat[2]
	phi = np.arctan2(aux_mat[0], aux_mat[1])
	return 2*np.pi*(rr**2 * dz + aux_mat[0] + aux_mat[1]) + twist*phi

def gen_hg_pattern(size, m=1, n=1):
	print "Sorry, this probably does not work correctly"
	size = int(np.floor(size/2)*2)
	pm = np.zeros((size, size))
	m_strides = size / (m+1)
	n_strides = size / (n+1)
	for ii in range(m+2):
		for jj in range(n+2):
			pm[ii*m_strides:(ii+1)*m_strides, jj*n_strides:(jj+1)*n_strides] = ii+jj	
	return (pm % 2) * np.pi

if __name__ == '__main__':
	from pylab import *	
	p_lg = gen_lg_pattern(768,3,3,4)
	p_g = gen_blaze_grating(768,50, 0.9)
	pm = phasemap(p_lg + p_g)
	close(1)
	figure(1)
	imshow(pm, cmap=get_cmap('binary'))
	show()

