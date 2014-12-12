#!/usr/bin/python

class SLMSettings(object):
	def __init__(self):
		self.window = {
			'size': 500,
			'xpos': 5,
			'ypos': 5,
			'scale': 4.0,
			'screenid': 1,
			'fullscreen': False,
			'xoffset': 0,
			'yoffset': 0
		}
		self.blazed_grating = {
			'enabled': False,
			'lines': 100,
			'coverage': 0.9
		}
		self.intensity_map = {
			'enabled': False,
			'P1': 0.005,
			'P2': 0.35
		}
		self.LG = [
			[0., 0., 0., 0., 0., 0.],
			[0., 0., 0., 0., 0., 0.],
			[0., 0., 0., 0., 0., 0.],
			[0., 0., 0., 1., 0., 0.],
			[0., 0., 0., 0., 0., 0.],
			[0., 0., 0., 0., 0., 0.]
		]
