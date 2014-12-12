#!/usr/bin/python

import sys 
from PyQt4 import QtGui 

import numpy as np
from matplotlib.cm import get_cmap
from matplotlib.figure import Figure 
from matplotlib.backends.backend_qt4agg \
	import FigureCanvasQTAgg as FigureCanvas 

class SLM_Dialog(QtGui.QDialog):
	def __init__(self, parent=None):
		super(SLM_Dialog, self).__init__(parent)
		self.fig = Figure()
		self.fc = FigureCanvas(self.fig) 
		
		layout = QtGui.QHBoxLayout()
		layout.addWidget(self.fc)
		layout.setMargin(0)
		self.setLayout(layout)
		self.setGeometry(1681, 1050-768, 768, 768)
		
		self.fc.mpl_connect('button_press_event', self.close_on_click)
	
	def close_on_click(self, event):
		self.close()

	def imshow(self, img):
		axes = self.fig.add_axes([0,0,1,1])
		axes.axis('off')
		axes.imshow(img, cmap=get_cmap('binary'))

if __name__ == '__main__':
	import gen_pattern as gp

	qApp = QtGui.QApplication(sys.argv) 
	SLM = SLM_Dialog()

	p_lg = gp.gen_lg_pattern(768,3,3,4)
	p_g = gp.gen_blaze_grating(768,50, 0.9)
	pm = gp.phasemap(p_lg + p_g)
	#pm = gp.phasemap(p_lg)

	SLM.imshow(pm)
	SLM.show()

	sys.exit(qApp.exec_()) 

