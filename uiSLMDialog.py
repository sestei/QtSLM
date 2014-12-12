#!/usr/bin/python

import sys 
from PyQt4 import QtGui 

import numpy as np
from matplotlib.cm import get_cmap
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qt4agg \
	import FigureCanvasQTAgg as FigureCanvas 

class SLMDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		super(SLMDialog, self).__init__(parent)
		self.fig = Figure()
		self.fc = FigureCanvas(self.fig) 
		self.axes = self.fig.add_axes([0,0,1,1])
		
		layout = QtGui.QHBoxLayout()
		layout.addWidget(self.fc)
		layout.setMargin(0)
		self.setLayout(layout)
		
	def imshow(self, img):
		self.axes.clear()
		self.axes.axis('off')
		self.axes.imshow(img, cmap=get_cmap('binary'))
		self.fc.draw()

if __name__ == '__main__':
	import gen_pattern as gp

	qApp = QtGui.QApplication(sys.argv) 
	SLM = SLMDialog()

	aux_mat = gp.prepare_aux_matrices(512)
	p_lg = gp.gen_lg_pattern(3,3,aux_mat,4)
	p_g = gp.gen_blaze_grating(50, aux_mat)
	pm = gp.phasemap(p_lg + p_g)
	#pm = gp.phasemap(p_lg)

	SLM.imshow(pm)
	SLM.show()

	sys.exit(qApp.exec_()) 

