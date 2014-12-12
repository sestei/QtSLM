#!/usr/bin/python

import sys 
from PyQt4 import QtGui 

import numpy as np

class SLMDialog(QtGui.QDialog):
	def __init__(self, parent=None):
		super(SLMDialog, self).__init__(parent)
		
		data = (np.random.rand(100,100)*255).astype(np.uint8)
		image = QtGui.QImage(data)
		self.lbl = QtGui.QLabel()
		self.lbl.setPixmap(image)		
		layout = QtGui.QHBoxLayout()
		layout.addWidget(self.lbl)
		self.setLayout(layout)
		
if __name__ == '__main__':
	import gen_pattern as gp

	qApp = QtGui.QApplication(sys.argv) 
	SLM = SLMDialog()
	SLM.show()
	sys.exit(qApp.exec_()) 