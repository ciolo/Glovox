import json
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QListWidgetItem, QFrame, QSlider, QListWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QCheckBox, QGroupBox, QDesktopWidget)
from MyWidgets import (EffectWidget, MainEffectLayout, ReverbLayout, DelayLayout, WaveformWidget)

### THE GUI

class MainWindow(QWidget):
	""" Class that implements the view and the controller
        
        Attributes:
            model         reference to the model
            size          dimension of the computer screen
            effectsFile   contains descriptions of each effect
    """
	def __init__(self, model, size):
		""" Init Method """
		super().__init__()

		self.model = model
		self.size = size
		self.effectsFile = json.load(open('effects.json'))

		self.init_ui()
		self.centerOnScreen()

	def init_ui(self):
		""" Method to initialize the user interface """

		#Title
		self.setWindowTitle("Glovox")
		self.setStyleSheet("""QToolTip { 
		                           background-color: black; 
		                           color: white; 
		                           border: white solid 3px
		                           }""")

		#GUI ELEMENTS

		# List containing the available effects
		self.effectList = QListWidget()
		self.typeFont = QFont(".Lucida Grande UI", 18)
		self.effectList.setFont(self.typeFont)

		noEff = QListWidgetItem('No Effect')
		noEff.setToolTip(self.effectsFile["effects"][0]["NoEffects"])

		dist = QListWidgetItem('Distortion')
		dist.setToolTip(self.effectsFile["effects"][1]["Distortion"])

		wah = QListWidgetItem('Auto-Wah')
		wah.setToolTip(self.effectsFile["effects"][2]["Auto-Wah"])

		chords = QListWidgetItem('Harmonizer')
		chords.setToolTip(self.effectsFile["effects"][3]["Chords"])

		sine = QListWidgetItem('Sine Oscillator')
		sine.setToolTip(self.effectsFile["effects"][4]["Sine Oscillator"])

		blit = QListWidgetItem('BLIT')
		blit.setToolTip(self.effectsFile["effects"][5]["BLIT"])

		superSaw = QListWidgetItem('Super Saw')
		superSaw.setToolTip(self.effectsFile["effects"][6]["Super Saw"])

		phasor = QListWidgetItem('Phasor')
		phasor.setToolTip(self.effectsFile["effects"][7]["Phasor"])

		rc = QListWidgetItem('RC Oscillator')
		rc.setToolTip(self.effectsFile["effects"][8]["RC Oscillator"])

		lfo = QListWidgetItem('LF Oscillator')
		lfo.setToolTip(self.effectsFile["effects"][9]["LF Oscillator"])

		self.effectList.addItem(noEff)
		self.effectList.addItem(dist)
		self.effectList.addItem(wah)
		self.effectList.addItem(chords)
		self.effectList.addItem(sine)
		self.effectList.addItem(blit)
		self.effectList.addItem(superSaw)
		self.effectList.addItem(phasor)
		self.effectList.addItem(rc)
		self.effectList.addItem(lfo)
		self.effectList.setCurrentItem(self.effectList.item(0))

		effectListLayout = QVBoxLayout()
		effectListLayout.addWidget(self.effectList)

		effectListBox = QGroupBox('Effects')
		effectListBox.setMaximumWidth(300)
		effectListBox.setMinimumWidth(150)
		effectListBox.setLayout(effectListLayout)

		#Box displaying the waveform of the active effect
		self.waveform = WaveformWidget(self.model)
		analyzerLayout = QVBoxLayout()
		analyzerLayout.addWidget(self.waveform)
		analyzerBox = QGroupBox('Waveform')
		analyzerBox.setMinimumHeight(350)
		analyzerBox.setMaximumHeight(500)
		analyzerBox.setLayout(analyzerLayout)

		effectParameterLayout = QHBoxLayout()

		#Boxes containing the parameters that can be used to modify the active effect, Rever and Delay
		self.effect = EffectWidget('Effect', MainEffectLayout(self.model))
		self.rev = EffectWidget('Reverb', ReverbLayout(self.model))
		self.delay = EffectWidget('Delay', DelayLayout(self.model))

		self.effect.setMinimumWidth(250)
		self.rev.setMinimumWidth(275)
		self.delay.setMinimumWidth(275)

		self.effect.setMaximumWidth(300)
		self.rev.setMaximumWidth(375)
		self.delay.setMaximumWidth(300)

		self.effect.setMinimumHeight(250)
		self.rev.setMinimumHeight(250)
		self.delay.setMinimumHeight(250)

		self.effect.setMinimumHeight(275)
		self.rev.setMinimumHeight(275)
		self.delay.setMinimumHeight(275)


		effectParameterLayout.addWidget(self.effect)
		effectParameterLayout.addWidget(self.rev)
		effectParameterLayout.addWidget(self.delay)

		effectParameterBox = QWidget()
		effectParameterBox.setLayout(effectParameterLayout)

		effectManagementLayout = QVBoxLayout()
		effectManagementLayout.addWidget(analyzerBox)
		effectManagementLayout.addWidget(effectParameterBox)

		effectManagementWidget = QWidget()
		effectManagementWidget.setLayout(effectManagementLayout)

		mainLayout = QHBoxLayout()
		mainLayout.addWidget(effectListBox)
		mainLayout.addWidget(effectManagementWidget)
		self.setLayout(mainLayout)
		self.setMinimumSize(self.size.width()*0.925, self.size.height()*0.875)

		self.show()

		#Connecting widgets
		self.effectList.itemSelectionChanged.connect(self.changeEffect)

	def centerOnScreen(self):
		""" Method to center the GUI on the user screen """
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

	def closeEvent(self, event):
		""" Overloading of close event. Overloading has been necessary to stop Pyo's Server """
		self.model.switchToNoEff()# Necessary, because sometimes the app doesn't stop when we close it
		self.model.close()

	def changeEffect(self):
		""" Method to change the effect"""
		if self.effectList.currentItem().text() == 'No Effect':
			self.effect.getLayout().changeEffect('No Effect')
			self.model.switchToNoEff()
		elif self.effectList.currentItem().text() == 'Distortion':
			self.effect.getLayout().changeEffect('Distortion')
			self.effect.getLayout().currentWidget().reset()
			self.model.switchToDistortion()

		elif self.effectList.currentItem().text() == 'Auto-Wah':
			self.effect.getLayout().changeEffect('Auto-Wah')
			self.model.switchToWah()

		elif self.effectList.currentItem().text() == 'Harmonizer':
			self.effect.getLayout().changeEffect('Harmonizer')
			self.effect.getLayout().currentWidget().reset()
			self.model.switchToChords()

		elif self.effectList.currentItem().text() == 'Sine Oscillator':
			self.effect.getLayout().changeEffect('Sine Oscillator')
			self.effect.getLayout().currentWidget().reset()
			self.model.switchToSine()
		elif self.effectList.currentItem().text() == 'BLIT':
			self.effect.getLayout().changeEffect('BLIT')
			self.effect.getLayout().currentWidget().reset()
			self.model.switchToBlit()
		elif self.effectList.currentItem().text() == 'Super Saw':
			self.effect.getLayout().changeEffect('Super Saw')
			self.effect.getLayout().currentWidget().reset()
			self.model.switchToSuperSaw()
		elif self.effectList.currentItem().text() == 'Phasor':
			self.effect.getLayout().changeEffect('Phasor')
			self.effect.getLayout().currentWidget().reset()
			self.model.switchToPhasor()
		elif self.effectList.currentItem().text() == 'RC Oscillator':
			self.effect.getLayout().changeEffect('RC Oscillator')
			self.effect.getLayout().currentWidget().reset()
			self.model.switchToRC()
		elif self.effectList.currentItem().text() == 'LF Oscillator':
			self.effect.getLayout().changeEffect('LF Oscillator')
			self.effect.getLayout().currentWidget().reset()
			self.model.switchToLFO()

		self.rev.getLayout().reset()
		self.delay.getLayout().reset()