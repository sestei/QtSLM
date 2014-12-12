#!/usr/bin/python

import sys
from uiSLMWindow import SLMWindow
from PyQt4 import QtGui

qApp = QtGui.QApplication(sys.argv) 
SLM = SLMWindow()
SLM.show()
qApp.exec_()