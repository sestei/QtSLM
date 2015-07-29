#!/usr/bin/python

import sys
import uiMainWindow
import uiSLMDialog 
from PyQt4 import QtGui
from PyQt4 import QtCore
import gen_pattern as gp
from SLMSettings import SLMSettings


class SLMWindow(QtGui.QMainWindow, uiMainWindow.Ui_MainWindow):
	def __init__(self, parent=None):
		super(SLMWindow, self).__init__(parent)
		self.setupUi(self)
		self.settings = SLMSettings()
		self.SLM = uiSLMDialog.SLMDialog(self)
		self.updateUi()
		self.updatePhaseMap()

		self.statusBar.showMessage('QtSLM driver application, S. Steinlechner (2014)')

	def updateUi(self):
		self.winSize.setText(str(self.settings.window['size']))
		self.winXPos.setText(str(self.settings.window['xpos']))
		self.winYPos.setText(str(self.settings.window['ypos']))
		self.winScale.setText(str(self.settings.window['scale']))
		self.winScreenID.setMaximum(QtGui.QApplication.desktop().screenCount()-1)
		self.winScreenID.setValue(self.settings.window['screenid'])
		self.winFullscreen.setCheckState(self.settings.window['fullscreen'])

		self.bgrEnable.setCheckState(self.settings.blazed_grating['enabled'])
		self.bgrLines.setText(str(self.settings.blazed_grating['lines']))
		self.bgrCoverage.setText(str(self.settings.blazed_grating['coverage']))

		self.imEnable.setCheckState(self.settings.intensity_map['enabled'])
		self.imP1.setText(str(self.settings.intensity_map['P1']))
		self.imP2.setText(str(self.settings.intensity_map['P2']))

		self.tabLG.blockSignals(True)
		for row in range(len(self.settings.LG)):
			for col in range(len(self.settings.LG[row])):
				item = QtGui.QTableWidgetItem(str(self.settings.LG[row][col]))
				item.setTextAlignment(QtCore.Qt.AlignRight)
				self.tabLG.setItem(row, col, item)
		self.tabLG.blockSignals(False)

	def calculatePhaseMap(self, size=-1):
		if size < 0:
			size = self.settings.window['size']

		aux_mat = gp.prepare_aux_matrices(size,
										  self.settings.window['xoffset'],
										  self.settings.window['yoffset'])
		p_lg = gp.gen_lg_pattern(0,0, aux_mat,
								 self.settings.window['scale']) * self.settings.LG[0][0]
		
		for row in range(len(self.settings.LG)):
			for col in range(len(self.settings.LG[row])):
				if col == row == 0:
					continue # we already had this, above
				if self.settings.LG[row][col] == 0.0:
					continue # nothing to calculate here
				p_lg_add = gp.gen_lg_pattern(row, col, aux_mat,
										  	 self.settings.window['scale'])
				p_lg += p_lg_add * self.settings.LG[row][col]
		
		if self.settings.blazed_grating['enabled']:
			p_g = gp.gen_blaze_grating(self.settings.blazed_grating['lines'],
									   aux_mat,
									   self.settings.blazed_grating['coverage'])
			p_lg += p_g

		if self.settings.intensity_map['enabled']:
			im = gp.create_beziermap(self.settings.intensity_map['P1'],
									 self.settings.intensity_map['P2'])
			pm = gp.phasemap(p_lg, im)
		else:
			pm = gp.phasemap(p_lg)

		return pm

	def updatePhaseMap(self):
		size = -1
		if self.settings.window['fullscreen']:
			geom = QtGui.QApplication.desktop().screenGeometry(
						self.settings.window['screenid'])
			size = min(geom.width(), geom.height())
			if not (self.SLM.windowState() & QtCore.Qt.WindowFullScreen):
				# if we're already full screen, don't update geometry
				#TODO: this prevents switching fullscreen between displays directly
				#self.SLM.setGeometry(geom)
				#self.SLM.showFullScreen()
				pass
		else:
			size = (self.settings.window['size']/2)*2
			self.SLM.setGeometry(self.settings.window['xpos'],
								 self.settings.window['ypos'],
		 						 size-1,
		 						 size-1)
		pm = self.calculatePhaseMap(size)
		self.SLM.imshow(pm)
		self.SLM.show()
		

	# ===== SLOTS =====

	@QtCore.pyqtSlot()
	def on_winSize_editingFinished(self):
		self.settings.window['size'] = int(self.winSize.text())
		self.updatePhaseMap()

	@QtCore.pyqtSlot()
	def on_winXPos_editingFinished(self): 
		self.settings.window['xpos'] = int(self.winXPos.text())
		self.updatePhaseMap()

	@QtCore.pyqtSlot()
	def on_winYPos_editingFinished(self): 
		self.settings.window['ypos'] = int(self.winYPos.text())
		self.updatePhaseMap()
	
	@QtCore.pyqtSlot()
	def on_winScale_editingFinished(self): 
		self.settings.window['scale'] = float(self.winScale.text())
		self.updatePhaseMap()

	@QtCore.pyqtSlot('int')
	def on_winScreenID_valueChanged(self, value):
		self.settings.window['screenid'] = value

	@QtCore.pyqtSlot('int')
	def on_winFullscreen_stateChanged(self, state):
		state = state > 0
		self.settings.window['fullscreen'] = state
		self.winXPos.setEnabled(not state)
		self.winYPos.setEnabled(not state)
		self.winSize.setEnabled(not state)
		self.winScreenID.setEnabled(state)
		self.updatePhaseMap()

	@QtCore.pyqtSlot('int')
	def on_winXOffset_valueChanged(self, value):
		self.settings.window['xoffset'] = value
		self.updatePhaseMap()
	
	@QtCore.pyqtSlot('int')
	def on_winYOffset_valueChanged(self, value):
		self.settings.window['yoffset'] = value
		self.updatePhaseMap()
	
	@QtCore.pyqtSlot('int')
	def on_bgrEnable_stateChanged(self, state):
		state = state>0
		self.settings.blazed_grating['enabled'] = state
		self.bgrLines.setEnabled(state)
		self.bgrCoverage.setEnabled(state)
		self.updatePhaseMap()
	
	@QtCore.pyqtSlot()
	def on_bgrLines_editingFinished(self): 
		self.settings.blazed_grating['lines'] = int(self.bgrLines.text())
		self.updatePhaseMap()
	
	@QtCore.pyqtSlot()
	def on_bgrCoverage_editingFinished(self): 
		self.settings.blazed_grating['coverage'] = float(self.bgrCoverage.text())
		self.updatePhaseMap()

	@QtCore.pyqtSlot('int')
	def on_imEnable_stateChanged(self, state):
		state = state > 0
		self.settings.intensity_map['enabled'] = state
		self.imP1.setEnabled(state)
		self.imP2.setEnabled(state)
		self.updatePhaseMap()
	
	@QtCore.pyqtSlot()
	def on_imP1_editingFinished(self): 
		self.settings.intensity_map['P1'] = float(self.imP1.text())
		self.updatePhaseMap()
	
	@QtCore.pyqtSlot()
	def on_imP2_editingFinished(self): 
		self.settings.intensity_map['P2'] = float(self.imP2.text())
		self.updatePhaseMap()

	@QtCore.pyqtSlot('int', 'int')
	def on_tabLG_cellChanged(self, row, col):
		self.settings.LG[row][col] = float(self.tabLG.item(row, col).text())
		self.updatePhaseMap()


if __name__ == '__main__':
	qApp = QtGui.QApplication(sys.argv) 
	SLM = SLMWindow()
	SLM.show()
	qApp.exec_()
