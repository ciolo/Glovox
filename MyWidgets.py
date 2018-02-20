import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QWidget, QStackedLayout, QVBoxLayout, QHBoxLayout, QCheckBox, QGroupBox, QSlider, QLabel, QListWidget, QListWidgetItem)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

np.seterr(divide='ignore', invalid='ignore')

# MY WIDGETS

class mySlider(QWidget):
	""" Custom Slider composed by a label showing the name of the parameter, the current value of the slider and a QSlider.
		It is used to vary the value of parameters of a certain effect.
		
		Attributes:
			parameter    label describing the name of the parameter
			value 	     float value of the parameter
	"""
	def __init__(self, label, value):
		""" Init Method """
		super().__init__()

		layout = QVBoxLayout()

		self.parameter = QLabel(label)
		self.parameter.setAlignment(Qt.AlignHCenter)
		self.value = QLabel(str(value))
		self.value.setAlignment(Qt.AlignHCenter)

		layout.addWidget(self.parameter)
		layout.addWidget(self.value)

		self.slider = QSlider(Qt.Vertical)
		if label == 'Depth':
			self.slider.setMinimum(1)
			self.slider.setMaximum(1000)
			self.slider.setValue(value*200)
			self.slider.setTickInterval(1)
			layout.addWidget(self.slider)
		elif label == 'Harmonics':
			self.slider.setMinimum(1)
			self.slider.setMaximum(1000)
			self.slider.setValue(value*10)
			self.slider.setTickInterval(1)
			layout.addWidget(self.slider)
		elif label == 'Intensity':
			self.slider.setMinimum(1000)
			self.slider.setMaximum(5000)
			self.slider.setValue(value * 1000)
			self.slider.setTickInterval(1)
			layout.addWidget(self.slider)
		elif label == 'Cutoff':
			self.slider.setMinimum(1)
			self.slider.setMaximum(10000)
			self.slider.setValue(value)
			self.slider.setTickInterval(1)
			layout.addWidget(self.slider)
		elif label == 'Room':
			self.slider.setMinimum(250)
			self.slider.setMaximum(4000)
			self.slider.setValue(value*1000)
			self.slider.setTickInterval(1)
			layout.addWidget(self.slider)
		else:
			self.slider.setMinimum(1)
			self.slider.setMaximum(1000)
			self.slider.setValue(value*1000)
			self.slider.setTickInterval(1)
			layout.addWidget(self.slider)

		layout.setAlignment(self.slider, Qt.AlignHCenter)
		self.setLayout(layout)

	def getSlider(self):
		""" Method to get the QSlider """
		return self.slider

	def updateValue(self, newValue):
		""" Method to update the value displayed by the custom slider, according to the QSlider """
		self.value.setText(str(newValue))

class EffectWidget(QGroupBox):
	""" GroupBox where active effect, reverb or delay parameters will be displayed.
		
		Attributes:
			effectLayout    reference to a layout between mainEffectLayout, ReverbLayout and DelayLayout
	"""
	def __init__(self, title, effect): #Effect must be a Layout
		""" Init Method """
		
		super().__init__()

		self.setTitle(title)

		self.effectLayout = effect

		self.setMaximumHeight(250)

		self.setLayout(self.effectLayout)

	def getLayout(self):
		""" Method to get the effect, Reverb or delay layout. """
		return self.effectLayout

class MainEffectLayout(QStackedLayout):
	""" Custom Layout used to switch between the available effects.

		Attribute:
			model           reference to the model
			noEffWidget     reference to no Effect widget
			distWidget      reference to Distortion widget
			wahWidget       reference to Auto-wah widget
			chordsWidget    reference to Harmonizer widget
			sineWidget      reference to Sine OSC widget
			blitWidget      reference to BLIT widget
			superSawWidget  reference to Super Saw widget
			phasorWidget    reference to Phasor Widget
			rcWidget        reference to RC OSC widget
			lfoWidget       reference to LF OSC widget
	"""
	def __init__(self, model):
		""" Init Method"""
		super().__init__()

		self.model = model

		self.noEffWidget = NoEffectWidget(self.model)
		self.distWidget = DistortionWidget(self.model)
		self.wahWidget = WahWidget(self.model)
		self.chordsWidget = ChordsWidget(self.model)
		self.sineWidget = SineWidget(self.model)
		self.blitWidget = BlitWidget(self.model)
		self.superSawWidget = SuperSawWidget(self.model)
		self.phasorWidget = PhasorWidget(self.model)
		self.rcWidget = RCOscWidget(self.model)
		self.lfoWidget = LFOWidget(self.model)

		self.addWidget(self.noEffWidget)
		self.addWidget(self.distWidget)
		self.addWidget(self.wahWidget)
		self.addWidget(self.chordsWidget)
		self.addWidget(self.sineWidget)
		self.addWidget(self.blitWidget)
		self.addWidget(self.superSawWidget)
		self.addWidget(self.phasorWidget)
		self.addWidget(self.rcWidget)
		self.addWidget(self.lfoWidget)

	def changeEffect(self, effect):
		""" Method to change the effect displayed in the EffectBox """
		if effect == 'No Effect':
			self.setCurrentWidget(self.noEffWidget)
		elif effect == 'Distortion':
			self.setCurrentWidget(self.distWidget)
		elif effect == 'Auto-Wah':
			self.setCurrentWidget(self.wahWidget)
		elif effect == 'Harmonizer':
			self.setCurrentWidget(self.chordsWidget)
		elif effect == 'Sine Oscillator':
			self.setCurrentWidget(self.sineWidget)
		elif effect == 'BLIT':
			self.setCurrentWidget(self.blitWidget)
		elif effect == 'Super Saw':
			self.setCurrentWidget(self.superSawWidget)
		elif effect == 'Phasor':
			self.setCurrentWidget(self.phasorWidget)
		elif effect == 'RC Oscillator':
			self.setCurrentWidget(self.rcWidget)
		elif effect == 'LF Oscillator':
			self.setCurrentWidget(self.lfoWidget)

	def getEffect(self):
		""" Method to get the active effectm shown in the EffectBox """
		return self.currentWidget()

class NoEffectWidget(QWidget):
	""" Custom Widget related to the clean signal. """
	def __init__(self, model):
		""" Init Method """
		super().__init__()

class DistortionWidget(QWidget):
	""" Custom Widget related to the effect 'Distortion'.
		
		Attributes:
			model      reference to the model
			distDrive  slider for Drive parameter
			LPFSlope   slider for slope parameter

	"""
	def __init__(self, model):
		""" Init method """
		super().__init__()

		self.model = model

		layout = QVBoxLayout()
		invisibleLabel = QLabel('')
		layout.addWidget(invisibleLabel)

		paramLayout = QHBoxLayout()

		self.distDrive = mySlider('Drive', 0.75)
		paramLayout.addWidget(self.distDrive)

		self.LPFSlope = mySlider('LPF Slope', 0.5)
		paramLayout.addWidget(self.LPFSlope)

		paramWidget = QWidget()
		paramWidget.setLayout(paramLayout)
		
		layout.addWidget(paramWidget)

		self.distDrive.getSlider().valueChanged.connect(self.setDrive)
		self.LPFSlope.getSlider().valueChanged.connect(self.setLPFSlope)

		self.setLayout(layout)

	def setDrive(self):
		""" Method to set Drive parameter in the model """
		self.model.getDistortion().setDrive(self.distDrive.getSlider().value()/1000)
		self.distDrive.updateValue(round(self.model.getDistortion().getDrive(),2))

	def setLPFSlope(self):
		""" Method to set Slope parameter in the model  """
		self.model.getDistortion().setSlope(self.LPFSlope.getSlider().value()/1000)
		self.LPFSlope.updateValue(round(self.model.getDistortion().getSlope(),2))

	def reset(self):
		""" Method to set the parameters at the initial state in the model """
		self.distDrive.getSlider().setValue(750)
		self.LPFSlope.getSlider().setValue(500)

		self.distDrive.updateValue(round(self.model.getDistortion().getDrive(),2))
		self.LPFSlope.updateValue(round(self.model.getDistortion().getSlope(),2))

class WahWidget(QWidget):
	""" Custom Widget related to the effect 'Auto-Wah'. """
	def __init__(self, model):
		""" Init Method """
		super().__init__()

class ChordsWidget(QWidget):
	""" Custom Widget related to the effect 'Harmonizer'. 

		Attributes:
			model       reference to the model
			chordsList  list of available chords

	"""
	def __init__(self, model):
		super().__init__()

		self.model = model

		layout = QVBoxLayout()

		self.chordsList = QListWidget()
		self.chordsList.addItem(QListWidgetItem('Major'))
		self.chordsList.addItem(QListWidgetItem('Major 7th'))
		self.chordsList.addItem(QListWidgetItem('Major 7th-Maj'))
		self.chordsList.addItem(QListWidgetItem('Minor'))
		self.chordsList.addItem(QListWidgetItem('Minor 7th'))
		self.chordsList.addItem(QListWidgetItem('Minor 7th-Maj'))
		self.chordsList.addItem(QListWidgetItem('Diminished'))
		self.chordsList.setCurrentItem(self.chordsList.item(0))

		typeFont = QFont(".Lucida Grande UI", 18)
		self.chordsList.setFont(typeFont)

		layout.addWidget(self.chordsList)

		self.setLayout(layout)

		self.chordsList.itemSelectionChanged.connect(self.changeChords)

	def changeChords(self):
		""" Method to change the chords in the model """
		if self.chordsList.currentItem().text() == 'Major':
			self.model.getChords().setMajor()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Major 7th':
			self.model.getChords().setMajor7th()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Major 7th-Maj':
			self.model.getChords().setMajor7thMaj()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Minor':
			self.model.getChords().setMinor()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Minor 7th':
			self.model.getChords().setMinor7th()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Minor 7th-Maj':
			self.model.getChords().setMinor7thMaj()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())

		elif self.chordsList.currentItem().text() == 'Diminished':
			self.model.getChords().setDiminished()
			self.model.updateTableChords()
			self.model.getReverb().setInput(self.model.getChords().getSignal())
			self.model.getDelay().setInput(self.model.getChords().getSignal())
			
	def reset(self):
		""" Method to reset the active chord """
		self.chordsList.setCurrentItem(self.chordsList.item(0))

class SineWidget(QWidget):
	""" Custom Widget related to the effect 'Sinusoidal Oscillator'. 

		Attributes:
			model       reference to the model
			sinePhase   slider for Phase parameter
	"""

	def __init__(self, model):
		""" Inith Method """
		super().__init__()

		self.model = model

		layout = QVBoxLayout()
		invisibleLabel = QLabel('')
		layout.addWidget(invisibleLabel)

		paramLayout = QHBoxLayout()

		self.sinePhase = mySlider('Phase', 0.0)
		paramLayout.addWidget(self.sinePhase)

		paramWidget = QWidget()
		paramWidget.setLayout(paramLayout)
		
		layout.addWidget(paramWidget)

		self.sinePhase.getSlider().valueChanged.connect(self.setPhase)

		self.setLayout(layout)

	def setPhase(self):
		""" Method to set the parameter Phase in the model """
		self.model.getSine().setPhase(self.sinePhase.getSlider().value()/1000)
		self.sinePhase.updateValue(round(self.model.getSine().getPhase(),2))

	def reset(self):
		""" Method to set the parameters at the initial state in the model """
		self.sinePhase.getSlider().setValue(0)
		self.sinePhase.updateValue(round(self.model.getSine().getPhase(), 2))

class BlitWidget(QWidget):
	""" Custom Widget related to the effect 'BLIT'. 

		Attributes:
			model       reference to the model
			blitHarm    slider for harm parameter
	"""
	def __init__(self, model):
		""" Init Method """
		super().__init__()

		self.model = model

		layout = QVBoxLayout()
		invisibleLabel = QLabel('')
		layout.addWidget(invisibleLabel)

		paramLayout = QHBoxLayout()

		self.blitHarm = mySlider('Harmonics', 0.0)
		paramLayout.addWidget(self.blitHarm)

		paramWidget = QWidget()
		paramWidget.setLayout(paramLayout)
		
		layout.addWidget(paramWidget)

		self.blitHarm.getSlider().valueChanged.connect(self.setHarms)

		self.setLayout(layout)

	def setHarms(self):
		""" Method to set the parameter Harms in the model """
		self.model.getBlit().setHarms(self.blitHarm.getSlider().value()/10)
		self.blitHarm.updateValue(round(self.model.getBlit().getHarms(),2))

	def reset(self):
		""" Method to set the parameters at the initial state in the model """

		self.blitHarm.getSlider().setValue(400)
		self.blitHarm.updateValue(round(self.model.getBlit().getHarms(), 2))

class SuperSawWidget(QWidget):
	""" Custom Widget related to the effect 'Super Saw'. 

		Attributes:
			model       reference to the model
			ssDetune    slider for Detune parameter
			ssBal		slider for Balance parameter
	"""
	def __init__(self, model):
		""" Init Method """
		super().__init__()

		self.model = model

		layout = QVBoxLayout()
		invisibleLabel = QLabel('')
		layout.addWidget(invisibleLabel)

		paramLayout = QHBoxLayout()

		self.ssDetune = mySlider('Detune', 0.5)
		self.ssBal = mySlider('Balance', 0.7)
		paramLayout.addWidget(self.ssDetune)
		paramLayout.addWidget(self.ssBal)

		paramWidget = QWidget()
		paramWidget.setLayout(paramLayout)
		
		layout.addWidget(paramWidget)

		self.ssDetune.getSlider().valueChanged.connect(self.setDetune)
		self.ssBal.getSlider().valueChanged.connect(self.setBal)

		self.setLayout(layout)

	def setDetune(self):
		""" Method to set the parameter Detune in the model """
		self.model.getSuperSaw().setDetune(self.ssDetune.getSlider().value()/1000)
		self.ssDetune.updateValue(round(self.model.getSuperSaw().getDetune(),2))

	def setBal(self):
		""" Method to set the parameter Balance in the model """
		self.model.getSuperSaw().setBal(self.ssBal.getSlider().value()/1000)
		self.ssBal.updateValue(round(self.model.getSuperSaw().getBal(),2))

	def reset(self):
		""" Method to set the parameters at the initial state in the model """
		self.ssDetune.getSlider().setValue(500)
		self.ssBal.getSlider().setValue(700)
		self.ssDetune.updateValue(round(self.model.getSuperSaw().getDetune(), 2))
		self.ssBal.updateValue(round(self.model.getSuperSaw().getBal(), 2))

class PhasorWidget(QWidget):
	""" Custom Widget related to the effect 'Phasor'. 

		Attributes:
			model       reference to the model
			phase       slider for phase parameter
	"""
	def __init__(self, model):
		""" Init Method """
		super().__init__()

		self.model = model

		layout = QVBoxLayout()
		invisibleLabel = QLabel('')
		layout.addWidget(invisibleLabel)

		paramLayout = QHBoxLayout()

		self.phase = mySlider('Phase', 0.0)
		paramLayout.addWidget(self.phase)

		paramWidget = QWidget()
		paramWidget.setLayout(paramLayout)
		
		layout.addWidget(paramWidget)

		self.phase.getSlider().valueChanged.connect(self.setPhase)

		self.setLayout(layout)

	def setPhase(self):
		""" Method to set the parameter Phase in the model """
		self.model.getPhasor().setPhase(self.phase.getSlider().value()/1000)
		self.phase.updateValue(round(self.model.getPhasor().getPhase(),2))

	def reset(self):
		""" Method to set the parameters at the initial state in the model """
		self.phase.getSlider().setValue(0)
		self.phase.updateValue(round(self.model.getPhasor().getPhase(), 2))

class RCOscWidget(QWidget):
	""" Custom Widget related to the effect 'RC Oscillator'. 

		Attributes:
			model       reference to the model
			rcSharp     slider for Sharp parameter
	"""
	def __init__(self, model):
		""" Init Method """
		super().__init__()

		self.model = model

		layout = QVBoxLayout()
		invisibleLabel = QLabel('')
		layout.addWidget(invisibleLabel)

		paramLayout = QHBoxLayout()

		self.rcSharp = mySlider('Sharpness', 0.25)
		paramLayout.addWidget(self.rcSharp)

		paramWidget = QWidget()
		paramWidget.setLayout(paramLayout)
		
		layout.addWidget(paramWidget)

		self.rcSharp.getSlider().valueChanged.connect(self.setSharp)

		self.setLayout(layout)

	def setSharp(self):
		""" Method to set the parameter Sharp in the model """
		self.model.getRC().setSharp(self.rcSharp.getSlider().value()/1000)
		self.rcSharp.updateValue(round(self.model.getRC().getSharp(),2))

	def reset(self):
		""" Method to set the parameters at the initial state in the model """
		self.rcSharp.getSlider().setValue(250)
		self.rcSharp.updateValue(round(self.model.getRC().getSharp(), 2))

class LFOWidget(QWidget):
	""" Custom Widget related to the effect 'LF Oscillator'. 

		Attributes:
			model       reference to the model
			lfoWf       list of available waveforms

	"""
	def __init__(self, model):
		""" Init method """
		super().__init__()

		self.model = model

		layout = QVBoxLayout()

		self.lfoWf = QListWidget()
		self.lfoWf.addItem(QListWidgetItem('Saw Up'))
		self.lfoWf.addItem(QListWidgetItem('Saw Down'))
		self.lfoWf.addItem(QListWidgetItem('Square'))
		self.lfoWf.addItem(QListWidgetItem('Triangle'))
		self.lfoWf.addItem(QListWidgetItem('Pulse'))
		self.lfoWf.addItem(QListWidgetItem('Bipolar Pulse'))
		self.lfoWf.addItem(QListWidgetItem('Sample & Hold'))
		self.lfoWf.addItem(QListWidgetItem('Modulated Sine'))
		self.lfoWf.setCurrentItem(self.lfoWf.item(0))
		layout.addWidget(self.lfoWf)

		typeFont = QFont(".Lucida Grande UI", 18)
		self.lfoWf.setFont(typeFont)

		self.setLayout(layout)

		self.lfoWf.itemSelectionChanged.connect(self.changeWaveform)

	def changeWaveform(self):
		""" Method to change the waveform in the model """
		if self.lfoWf.currentItem().text() == 'Saw Up':
			self.model.getLFO().setSawUp()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Saw Down':
			self.model.getLFO().setSawDown()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Square':
			self.model.getLFO().setSquare()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Triangle':
			self.model.getLFO().setTriangle()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Pulse':
			self.model.getLFO().setPulse()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Bipolar Pulse':
			self.model.getLFO().setBipolarPulse()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Sample & Hold':
			self.model.getLFO().setSnH()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())

		elif self.lfoWf.currentItem().text() == 'Modulated Sine':
			self.model.getLFO().setModSine()
			self.model.getReverb().setInput(self.model.getLFO().getSignal())
			self.model.getDelay().setInput(self.model.getLFO().getSignal())
			
	def reset(self):
		""" Method to reset the active waveform """
		self.lfoWf.setCurrentItem(self.lfoWf.item(0))

class ReverbLayout(QVBoxLayout):
	""" Custom Layout used to manage Reverb effect.

		Attribute:
			model           reference to the model
			enableReverb    Check box to enable and disable Reverb
			revTime    		slider for parameter RevTime
			revCutoff		slider for parameter Cutoff
			roomSize 		slider for parameter Roomsize
			revBalance 		slider for parameter revBalance
	"""
	def __init__(self, model):
		""" Init mehtod """
		super().__init__()

		self.model = model

		self.enableReverb = QCheckBox('Enable')
		self.addWidget(self.enableReverb)

		paramLayout = QHBoxLayout()

		self.revTime = mySlider('Intensity', 1.00)
		paramLayout.addWidget(self.revTime)

		self.revCutoff = mySlider('Cutoff', 5000)
		paramLayout.addWidget(self.revCutoff)

		self.roomSize = mySlider('Room', 0.25)
		paramLayout.addWidget(self.roomSize)

		self.revBalance = mySlider('Balance', 0.5)
		paramLayout.addWidget(self.revBalance)

		paramWidget = QWidget()
		paramWidget.setLayout(paramLayout)
		
		self.addWidget(paramWidget)

		self.enableReverb.stateChanged.connect(self.toggleReverbMode)
		self.revTime.getSlider().valueChanged.connect(self.setRevtime)
		self.revCutoff.getSlider().valueChanged.connect(self.setCutoff)
		self.roomSize.getSlider().valueChanged.connect(self.setRoomSize)
		self.revBalance.getSlider().valueChanged.connect(self.setRevBalance)

	def toggleReverbMode(self, activate):
		""" Method to toggle Reverb Effect """
		if activate == Qt.Checked:
			self.enableReverb.setText('Disable')
			self.model.enableReverb()
		else:
			self.enableReverb.setText('Enable')
			self.model.disableReverb()

	def setRevtime(self):
		""" Method to set the parameter Revtime in the model """
		self.model.getReverb().setRevTime(self.revTime.getSlider().value()/1000)
		self.revTime.updateValue(round(self.model.getReverb().getRevTime(),2))

	def setCutoff(self):
		""" Method to set the parameter Cutoff in the model """
		self.model.getReverb().setCutoff(self.revCutoff.getSlider().value())
		self.revCutoff.updateValue(round(self.model.getReverb().getCutoff(),2))

	def setRoomSize(self):
		""" Method to set the parameter RoomSize in the model """
		self.model.getReverb().setRoomSize(4.25 - self.roomSize.getSlider().value()/1000)
		self.roomSize.updateValue(round(4.25 - self.model.getReverb().getRoomSize(),2))

	def setRevBalance(self):
		""" Method to set the parameter Bal in the model """
		self.model.getReverb().setBal(self.revBalance.getSlider().value()/1000)
		self.revBalance.updateValue(round(self.model.getReverb().getBal(),2))

	def reset(self):
		""" Method to set the parameters at the initial state in the model """
		self.revTime.getSlider().setValue(1000)
		self.revCutoff.getSlider().setValue(5000)
		self.roomSize.getSlider().setValue(250)
		self.revBalance.getSlider().setValue(500)
		self.enableReverb.setText('Enable')
		self.enableReverb.setCheckState(Qt.Unchecked)


class DelayLayout(QVBoxLayout):
	""" Custom Layout used to manage Reverb effect.

		Attribute:
			model           reference to the model
			enableDelay     Check box to enable and disable Delay
			delayAmount    	slider for parameter Delay
			delayFeedback	slider for parameter Feedback
	"""
	def __init__(self, model):
		""" Init Method """
		super().__init__()

		self.model = model

		self.enableDelay = QCheckBox('Enable')
		self.addWidget(self.enableDelay)

		paramLayout = QHBoxLayout()

		self.delayAmount = mySlider('Delay', 0.25)
		paramLayout.addWidget(self.delayAmount)

		self.delayFeedback = mySlider('Feedback', 0.0)
		paramLayout.addWidget(self.delayFeedback)

		paramWidget = QWidget()
		paramWidget.setLayout(paramLayout)
		
		self.addWidget(paramWidget)

		self.enableDelay.stateChanged.connect(self.toggleDelayMode)
		self.delayAmount.getSlider().valueChanged.connect(self.setAmountDelay)
		self.delayFeedback.getSlider().valueChanged.connect(self.setFeedback)

	def toggleDelayMode(self, activate):
		""" Method to toggle Delay Effect """
		if activate == Qt.Checked:
			self.enableDelay.setText('Disable')
			self.model.enableDelay()
		else:
			self.enableDelay.setText('Enable')
			self.model.disableDelay()

	def setAmountDelay(self):
		""" Method to set the parameter Delay in the model """
		self.model.getDelay().setDelayAmount(self.delayAmount.getSlider().value()/1000)
		self.delayAmount.updateValue(round(self.model.getDelay().getDelayAmount(),2))

	def setFeedback(self):
		""" Method to set the parameter Feedback in the model """
		self.model.getDelay().setFeedback(self.delayFeedback.getSlider().value()/1000)
		self.delayFeedback.updateValue(round(self.model.getDelay().getFeedback(),2))

	def reset(self):
		""" Method to set the parameters at the initial state in the model """
		self.delayAmount.getSlider().setValue(250)
		self.delayFeedback.getSlider().setValue(0)
		self.enableDelay.setText('Enable')
		self.enableDelay.setCheckState(Qt.Unchecked)


class MplFigure(object):
	""" Custom widget used to plot waveform.

		Attribute:
			figure     figure to plot waveform
			canvas     canvas necessary for figure of matplotlib
	"""
	def __init__(self, parent):
		"""Init method"""
		self.figure = plt.figure(figsize=(6, 9), dpi=100, facecolor='#31363B')
		self.canvas = FigureCanvas(self.figure)


class WaveformWidget(QWidget):
	""" Custom widget used to represent waveform.

		Attribute:
			mainFigure     reference to MplFigure Class
			timer          used to refresh waveform
			model		   reference to the model
			freqVect       Discrete Fourier Transform sample frequencies
			timeVect       time signal
	"""
	def __init__(self, model):
		""" Init method """
		super().__init__()

		self.initUI()

		self.initData(model)

		self.initWaveform()

	def initUI(self):
		"""Init UI"""
		vbox = QVBoxLayout()

		# mpl figure
		self.mainFigure = MplFigure(self)
		vbox.addWidget(self.mainFigure.canvas)

		self.setLayout(vbox)

		"""The refreshing part of the app is handled with a QTimer that gets called 10 times a second and 
		refreshes the gui at that time by calling the handleNewData function. 
		That function gets the latest frame from the microphone, plots the time series, 
		computes the Fourier transform and plots its modulus."""
		timer = QTimer()
		timer.timeout.connect(self.handleNewData)
		timer.start(100)
		
		self.timer = timer

	def initData(self, model):
		"""Init method to set model, frequencies, and time"""
		self.model = model

		# computes the parameters that will be used during plotting
		self.freqVect = np.fft.rfftfreq(self.model.server.getBufferSize(), 1./ (self.model.server.getSamplingRate()/10))
		self.timeVect = np.arange(self.model.server.getBufferSize(), dtype=np.float32) / self.model.server.getSamplingRate() * 100

	def initWaveform(self):
		"""creates initial matplotlib plots in the main window and keeps 
		references for further use"""

		self.axTop = self.mainFigure.figure.add_subplot(111)
		self.axTop.set_ylim(-2000, 2000)
		self.axTop.set_xlim(0, self.timeVect.max())
		self.axTop.set_xlabel(u'time (ms)', fontsize=8, color='white')
		self.axTop.set_facecolor('#18465d')
		self.axTop.tick_params(axis='x', colors='white')
		self.axTop.tick_params(axis='y', colors='white')

		# line objects        
		self.lineTop, = self.axTop.plot(self.timeVect, np.ones_like(self.timeVect), color='white')

	def handleNewData(self):
		""" handles the asynchroneously collected sound chunks """
		streams = self.model.getFrames()
		
		if len(streams) > 0:
			
			# plots the time signal
			self.lineTop.set_data(self.timeVect, streams*1000)

			# refreshes the plots
			self.mainFigure.canvas.draw()
