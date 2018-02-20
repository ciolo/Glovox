from pyo import *
from Effects import (NoEFF, DistortionEFF, AutoWahEFF, ChordsEFF, SineEFF, BlitEFF, SuperSawEFF, PhasorEFF, RCOscEFF, LFOEff, ReverbEFF, DelayEFF)
import numpy as np
import threading
import atexit

# The Model

class Glovox():
	""" Class that implements the model. It handles the comunication with audio drivers and keeps track of processing chain.
        
        Attributes:
            input     input used for no Effect
            input2	  input used for Distortion and Auto-wah effect
            input3	  input used for Harmonizer effect
            input4	  input used to compute a gate signal and its frequency
            gated	  gated signal of input4, it is used to gate inpu4 so that not to listen to it, if it is under a threshold
            freq      frequency of the input4, it is used as an input parameter of signal generators effect
            input5    input used to initialize Reverb and Delay effect
            t     	  TO COMMENT - Ciolo
            arr 	  ...
            lock 	  ...
            stop  	  ...
    """
	def __init__(self):
		""" Init Method """
		self.server = Server(nchnls=1)
		self.server.boot()

		# setting microphones as input
		# more inputs are used because calling stop() on just a single input disables all the pedals' output 
		self.input = Input(chnl=0)

		self.input2 = Input(chnl=0)

		self.input3 = Input(chnl=0)

		self.input4 = Input(chnl=0)
		self.gated = Gate(self.input4, thresh=-40, outputAmp=True)
		self.freq = Yin(self.input4, cutoff=3000)

		self.input5 = Input(chnl=0)

		self.createPedals()

		#TO COMMENT - Ciolo 
		# Create a table of length `buffer size` and read it in loop.
		self.t = DataTable(size=self.server.getBufferSize())
		# Share the table's memory with a numpy array.
		self.arr = np.asarray(self.t.getBuffer())
		# callback necessary for waveform
		self.server.setCallback(self.process)

		self.lock = threading.Lock()
		self.stop = False
		"""This class runs in a thread. 
		So to make sure it stops correctly, a call to atexit is registered at startup"""
		atexit.register(self.close)

		self.start()

	def close(self):
		""" Method to stop the server and reset the table containing information for the waveform """
		with self.lock:
			self.stop = True
		self.t.reset()
		self.server.stop()

	def start(self):
		""" Method to start the server and set the active effect as the clean input """
		self.server.start()
		self.switchToNoEff()

	def createPedals(self):
		""" Method to create all the available effect """
		self.noEffect = NoEFF(self.input)
		self.distortion = DistortionEFF(self.input2)
		self.wah = AutoWahEFF(self.input2)
		self.chords = ChordsEFF(self.input3)
		self.sine = SineEFF(self.gated, self.freq)
		self.blit = BlitEFF(self.gated, self.freq)
		self.superSaw = SuperSawEFF(self.gated, self.freq)
		self.phasor = PhasorEFF(self.gated, self.freq)
		self.rc = RCOscEFF(self.gated, self.freq)
		self.lfo = LFOEff(self.gated, self.freq)
		self.reverb = ReverbEFF(self.input5)
		self.delay = DelayEFF(self.input5)

	def getNoEffect(self):
		""" Method to get NoEffect signal """
		return self.noEffect

	def switchToNoEff(self):
		""" Method to switch to no effect """
		if self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.noEffect.enable()
		self.rec = TableFill(self.noEffect.getSignal(), self.t)

	def getDistortion(self):
		""" Method to get Distortion signal """
		return self.distortion

	def switchToDistortion(self):
		""" Method to switch to Distortion effect """
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.distortion.reset()
		self.distortion.enable()
		self.rec = TableFill(self.distortion.getSignal(), self.t)

	def getWah(self):
		""" Method to get Auto-Wah signal """
		return self.wah

	def switchToWah(self):
		""" Method to switch to Auto-Wah effect """
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.wah.enable()
		self.rec = TableFill(self.wah.getSignal(), self.t)

	def getChords(self):
		""" Method to get Harmonizer signal """
		return self.chords

	def switchToChords(self):
		""" Method to switch to Harmonizer effect """
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.chords.reset()
		self.chords.enable()
		self.rec = TableFill(self.chords.getSignal(), self.t)

	def updateTableChords(self):
		""" Method to update the wavefrm table, when the user change the chord of harmonizer """
		self.rec = TableFill(self.chords.getSignal(), self.t)

	def getSine(self):
		""" Method to get the Sine signal """
		return self.sine

	def switchToSine(self):
		""" Method to switch to the Sine effect """
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.sine.enable()
		self.rec = TableFill(self.sine.getSignal(), self.t)

	def getBlit(self):
		""" Method to get the BLIT signal """
		return self.blit

	def switchToBlit(self):
		""" Method to switch to the BLIT effect """
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.blit.enable()
		self.rec = TableFill(self.blit.getSignal(), self.t)

	def getSuperSaw(self):
		""" Method to get the Super Saw signal """
		return self.superSaw

	def switchToSuperSaw(self):
		""" Method to switch to the Super Saw Effect """
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.superSaw.enable()
		self.rec = TableFill(self.superSaw.getSignal(), self.t)

	def getPhasor(self):
		""" Method to get the Phasor signal """
		return self.phasor

	def switchToPhasor(self):
		""" Method to switch to the Phasor Effect """
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.rc.isOutputting():
			self.rc.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.phasor.enable()
		self.rec = TableFill(self.phasor.getSignal(), self.t)

	def getRC(self):
		""" Method to get the RC Osc signal """
		return self.rc

	def switchToRC(self):
		""" Method to switch to the RC Osc Effect """
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.lfo.isOutputting():
			self.lfo.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.rc.enable()
		self.rec = TableFill(self.rc.getSignal(), self.t)

	def getLFO(self):
		""" Method to get the LFO signal """
		return self.lfo

	def switchToLFO(self):
		""" Method to switch to the LFO effect """
		if self.noEffect.isOutputting():
			self.noEffect.disable()
		elif self.distortion.isOutputting():
			self.distortion.disable()
		elif self.wah.isOutputting():
			self.wah.disable()
		elif self.chords.isOutputting():
			self.chords.disable()
		elif self.sine.isOutputting():
			self.sine.disable()
		elif self.blit.isOutputting():
			self.blit.disable()
		elif self.superSaw.isOutputting():
			self.superSaw.disable()
		elif self.phasor.isOutputting():
			self.phasor.disable()
		elif self.rc.isOutputting():
			self.rc.disable()

		self.disableReverb()
		self.reverb.reset()
		self.disableDelay()
		self.delay.reset()
		self.lfo.reset()
		self.lfo.enable()
		self.rec = TableFill(self.lfo.getSignal(), self.t)

	def getReverb(self):
		""" Method to get the Reverb signal """
		return self.reverb

	def enableReverb(self):
		""" Method to enable the Reverb on the active effect """
		if self.noEffect.isOutputting():
			self.reverb.enable(self.noEffect.getSignal())
		elif self.distortion.isOutputting():
			self.reverb.enable(self.distortion.getSignal())
		elif self.wah.isOutputting():
			self.reverb.enable(self.wah.getSignal())
		elif self.chords.isOutputting():
			self.reverb.enable(self.chords.getSignal())
		elif self.sine.isOutputting():
			self.reverb.enable(self.sine.getSignal())
		elif self.blit.isOutputting():
			self.reverb.enable(self.blit.getSignal())
		elif self.superSaw.isOutputting():
			self.reverb.enable(self.superSaw.getSignal())
		elif self.phasor.isOutputting():
			self.reverb.enable(self.phasor.getSignal())
		elif self.rc.isOutputting():
			self.reverb.enable(self.rc.getSignal())
		elif self.lfo.isOutputting():
			self.reverb.enable(self.lfo.getSignal())

	def disableReverb(self):
		""" Method to disable the Reverb """
		self.reverb.disable()

	def getDelay(self):
		""" Method to get the Delay signal """
		return self.delay

	def enableDelay(self):
		""" Method to enable the Delay on the active effect """
		if self.noEffect.isOutputting():
			self.delay.enable(self.noEffect.getSignal())
		elif self.distortion.isOutputting():
			self.delay.enable(self.distortion.getSignal())
		elif self.wah.isOutputting():
			self.delay.enable(self.wah.getSignal())
		elif self.chords.isOutputting():
			self.delay.enable(self.chords.getSignal())
		elif self.sine.isOutputting():
			self.delay.enable(self.sine.getSignal())
		elif self.blit.isOutputting():
			self.delay.enable(self.blit.getSignal())
		elif self.superSaw.isOutputting():
			self.delay.enable(self.superSaw.getSignal())
		elif self.phasor.isOutputting():
			self.delay.enable(self.phasor.getSignal())
		elif self.rc.isOutputting():
			self.delay.enable(self.rc.getSignal())
		elif self.lfo.isOutputting():
			self.delay.enable(self.lfo.getSignal())

	def disableDelay(self):
		""" Method to disable the Delay """
		self.delay.disable()

	def process(self):
		"""Fill the array with last samples of current input or current effect."""
		self.samples = self.t.getTable()
		with self.lock:
			self.arr[1:] = self.arr[:-1]
			self.arr[0] = self.samples[-1]
			if self.stop:
				return None
		return None

	def getFrames(self):
		"""Get array of samples"""
		with self.lock:
			return self.arr
