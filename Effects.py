from pyo import *

#EFFECTS
"""Each effect has the related signal as attribute, getter and setter methods for each effect's parameters, 
enabling, disabling and resetting method. A description of each effect can be found in effects.json file."""

class NoEFF():
	""" Class that implements the clean signal effect.
        
        Attributes:
            signal     clean signal
    """

	def __init__(self, cleanS):
		""" Init Methdod """
		self.signal = cleanS

	def enable(self):
		""" Method to output the clean signal """
		self.signal.out()

	def disable(self):
		""" Method to stop outputting the clean signal """
		self.signal.stop()

	def isOutputting(self):
		""" Method to get if the clean signal is outputting or not """
		return self.signal.isOutputting()

	def getSignal(self):
		""" Method to get the clean signal """
		return self.signal

class DistortionEFF():
	""" Class that implements the distortion effect.
        
        Attributes:
            dist     distortion effect signal
    """
	def __init__(self, cleanS):
		""" Init Methdod """
		self.dist = Disto(cleanS, drive = 0.75, slope = 0.5)

	def setDrive(self, drive):
		""" Method to set Disto's drive """
		self.dist.setDrive(drive)

	def getDrive(self):
		""" Method to get Disto's drive """
		return self.dist.drive

	def setSlope(self, slope):
		""" Method to set Disto's slope """
		self.dist.setSlope(slope)

	def getSlope(self):
		""" Method to get Disto's slope """
		return self.dist.slope

	def reset(self):
		""" Method to reset the parameters of distortion effect """
		self.setDrive(0.75)
		self.setSlope(0.5)

	def enable(self):
		""" Method to output the distortion effect signal """
		self.dist.out()

	def disable(self):
		""" Method to stop outputting the distortion effect signal """
		self.dist.stop()

	def isOutputting(self):
		""" Method to get if the distortion effect signal is outputting or not """
		return self.dist.isOutputting()

	def getSignal(self):
		""" Method to get the distortion effect signal """
		return self.dist

class AutoWahEFF():
	""" Class that implements the Auto-wah effect.
        
        Attributes:
            wah     auto-wah effect signal
    """
	def __init__(self, cleanS):
		""" Init Methdod """
		fol = Follower(cleanS, freq=30, mul=4000, add=40)
		self.wah = Biquad(cleanS, freq=fol, q=5, type=2)

	def enable(self):
		""" Method to output the auto-wah effect signal """
		self.wah.out()

	def disable(self):
		""" Method to stop outputting the Autowah effect signal """
		self.wah.stop()

	def isOutputting(self):
		""" Method to get if the Auto-wah signal is outputting or not """
		return self.wah.isOutputting()

	def getSignal(self):
		""" Method to get the Auto-wah effect signal """
		return self.wah

class ChordsEFF():
	""" Class that implements the Harmonizer effect.
        
        Attributes:
            first      clean signal, representing the first of the chord
            third      clean signal, representing the third of the chord
            fifth	   clean signal, representing the fifth of the chord
            lastNote   clean signal, representing the last note of the chord
            chords     chord signal
    """
	def __init__(self, cleanS):
		""" Init Methdod """
		self.first = cleanS

		self.third = Harmonizer(self.first, transpo = 4)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 5) #Default major chords

		self.chords = self.first + self.third + self.fifth + self.lastNote

	def setMajor(self):
		""" Method to set Major Chords """
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 4)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 5)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setMajor7th(self):
		""" Method to set Major 7th Chords """
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 4)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 3)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setMajor7thMaj(self):
		""" Method to set Major 7thMaj Chords """
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 4)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 4)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setMinor(self):
		""" Method to set minor Chords """
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 3)
		self.fifth = Harmonizer(self.third, transpo = 4)
		self.lastNote = Harmonizer(self.fifth, transpo = 5)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setMinor7th(self):
		""" Method to set Minor 7th Chords """
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 3)
		self.fifth = Harmonizer(self.third, transpo = 4)
		self.lastNote = Harmonizer(self.fifth, transpo = 3)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setMinor7thMaj(self):
		""" Method to set Minor 7thMaj Chords """
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 3)
		self.fifth = Harmonizer(self.third, transpo = 4)
		self.lastNote = Harmonizer(self.fifth, transpo = 4)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def setDiminished(self):
		""" Method to set Diminished Chords """
		self.chords.stop()

		self.third = Harmonizer(self.first, transpo = 3)
		self.fifth = Harmonizer(self.third, transpo = 3)
		self.lastNote = Harmonizer(self.fifth, transpo = 3)

		self.chords = self.first + self.third + self.fifth + self.lastNote
		self.chords.out()

	def reset(self):
		""" Method to reset the output chord of Harmonizer effect """
		self.setMajor()

	def enable(self):
		""" Method to output the Harmonizer effect signal """
		self.chords.out()
		
	def disable(self):
		""" Method to stop outputting the Harmonizer effect signal """
		self.chords.stop()

	def isOutputting(self):
		""" Method to get if the Harmonizer effect signal is outputting or not """
		return self.chords.isOutputting()

	def getSignal(self):
		""" Method to get the Harmonizer effect signal """
		return self.chords

class SineEFF():
	""" Class that implements the Sinusoidal Oscillator effect.
        
        Attributes:
            sine     sine effect signal
    """
	def __init__(self, gatedS, freqS):
		""" Init Methdod """
		self.sine = Sine(freqS, phase = 0, mul = 0.2*gatedS)

	def setPhase(self, phase):
		""" Method to set Sine's phase """
		self.sine.setPhase(phase)

	def getPhase(self):
		""" Method to get Sine's phase """
		return self.sine.phase

	def reset(self):
		""" Method to reset the parameters of Sinusoidal Oscillator effect """
		self.setPhase(0)

	def enable(self):
		""" Method to output the Sinusoidal Oscillator effect signal """
		self.sine.out()

	def disable(self):
		""" Method to stop outputting the Sinusoidal Oscillator effect signal """
		self.sine.stop()

	def isOutputting(self):
		""" Method to get if the Sinusoidal Oscillator effect signal is outputting or not """
		return self.sine.isOutputting()

	def getSignal(self):
		""" Method to get the Sinusoidal Oscillator effect signal """
		return self.sine

class BlitEFF():
	""" Class that implements the BLIT effect.
        
        Attributes:
            blit     blit effect signal
    """
	def __init__(self, gatedS, freqS):
		""" Init Methdod """
		self.blit = Blit(freqS, harms=40, mul=0.2*gatedS)

	def setHarms(self, harms):
		""" Method to set Blit's harms """
		self.blit.setHarms(harms)

	def getHarms(self):
		""" Method to get Blit's harms """
		return self.blit.harms

	def reset(self):
		""" Method to reset the parameters of Blit effect """
		self.setHarms(40)

	def enable(self):
		""" Method to output the Blit effect signal """
		self.blit.out()

	def disable(self):
		""" Method to stop outputting the Blit effect signal """
		self.blit.stop()

	def isOutputting(self):
		""" Method to get if the Blit effect signal is outputting or not """
		return self.blit.isOutputting()

	def getSignal(self):
		""" Method to get the Blitn effect signal """
		return self.blit

class SuperSawEFF():
	""" Class that implements the Super Saw effect.
        
        Attributes:
            supersaw     super saw effect signal
    """
	def __init__(self, gatedS, freqS):
		""" Init Methdod """
		self.superSaw = SuperSaw(freqS, detune = 0.5, bal = 0.7, mul = 0.2*gatedS)

	def setDetune(self, detune):
		""" Method to set SuperSaw's detune """
		self.superSaw.setDetune(detune)

	def getDetune(self):
		""" Method to get SuperSaw's detune """
		return self.superSaw.detune

	def setBal(self, bal):
		""" Method to set SuperSaw's Bal """
		self.superSaw.setBal(bal)

	def getBal(self):
		""" Method to get SuperSaw's Bal """
		return self.superSaw.bal

	def reset(self):
		""" Method to reset the parameters of Super Saw effect """
		self.setDetune(0.5)
		self.setBal(0.7)

	def enable(self):
		""" Method to output the Super Saw effect signal """
		self.superSaw.out()

	def disable(self):
		""" Method to stop outputting the Super Saw effect signal """
		self.superSaw.stop()

	def isOutputting(self):
		""" Method to get if the Super Saw effect signal is outputting or not """
		return self.superSaw.isOutputting()

	def getSignal(self):
		""" Method to get the SuperSaw effect signal """
		return self.superSaw

class PhasorEFF():
	""" Class that implements the Phasor effect.
        
        Attributes:
            phasor     phasor effect signal
    """
	def __init__(self, gatedS, freqS):
		""" Init Methdod """
		self.phasor = Phasor(freqS, phase = 0, mul = 0.2*gatedS)

	def setPhase(self, phase):
		""" Method to set Phasor's phase """
		self.phasor.setPhase(phase)

	def getPhase(self):
		""" Method to get Phasor's phase """
		return self.phasor.phase

	def reset(self):
		""" Method to reset the parameters of Phasor effect """
		self.setPhase(0.0)

	def enable(self):
		""" Method to output the Phasor effect signal """
		self.phasor.out()

	def disable(self):
		""" Method to stop outputting the Phasor effect signal """
		self.phasor.stop()

	def isOutputting(self):
		""" Method to get if the Phasor effect signal is outputting or not """
		return self.phasor.isOutputting()

	def getSignal(self):
		""" Method to get the Phasor effect signal """
		return self.phasor

class RCOscEFF():
	""" Class that implements the Rc oscillator effect.
        
        Attributes:
            rc     rc oscillator effect signal
    """
	def __init__(self, gatedS, freqS):
		""" Init Methdod """
		self.rc = RCOsc(freqS, sharp = 0.25, mul = 0.2*gatedS)

	def setSharp(self, sharp):
		""" Method to set RCOsc's sharp """
		self.rc.setSharp(sharp)

	def getSharp(self):
		""" Method to get RCOsc's sharp """
		return self.rc.sharp

	def reset(self):
		""" Method to reset the parameters of RC Oscillator effect """
		self.setSharp(0.25)

	def enable(self):
		""" Method to output the RC Oscillator effect signal """
		self.rc.out()

	def disable(self):
		""" Method to stop outputting the RC Oscillator effect signal """
		self.rc.stop()

	def isOutputting(self):
		""" Method to get if the RC Oscillator effect signal is outputting or not """
		return self.rc.isOutputting()

	def getSignal(self):
		""" Method to get the RC Oscillator effect signal """
		return self.rc

class LFOEff():
	""" Class that implements the LF oscillator effect.
        
        Attributes:
            lfo     lf oscillator effect signal
    """
	def __init__(self, gatedS, freqS):
		""" Init Methdod """
		self.lfo = LFO(freqS, type = 0, mul = 0.2*gatedS)

	def setSawUp(self):
		""" Method to set saw up waveform """
		self.lfo.setType(0)

	def setSawDown(self):
		""" Method to set saw down waveform """
		self.lfo.setType(1)

	def setSquare(self):
		""" Method to set Square waveform """
		self.lfo.setType(2)

	def setTriangle(self):
		""" Method to set triangle waveform """
		self.lfo.setType(3)

	def setPulse(self):
		""" Method to set pulse waveform """
		self.lfo.setType(4)

	def setBipolarPulse(self):
		""" Method to set bipolar pulse waveform """
		self.lfo.setType(5)

	def setSnH(self):
		""" Method to set sample and hold waveform """
		self.lfo.setType(6)

	def setModSine(self):
		""" Method to set modulateed Sine waveform """
		self.lfo.setType(7)

	def reset(self):
		""" Method to reset the waveform of the output of LF OScillator effect """
		self.setSawUp()

	def enable(self):
		""" Method to output the LF Oscillator effect signal """
		self.lfo.out()

	def disable(self):
		""" Method to stop outputting the LF Oscillator effect signal """
		self.lfo.stop()

	def isOutputting(self):
		""" Method to get if the LF Oscillator effect signal is outputting or not """
		return self.lfo.isOutputting()

	def getSignal(self):
		""" Method to get the LF Oscillator effect signal """
		return self.lfo

class ReverbEFF():
	""" Class that implements the Reverb effect.
        
        Attributes:
            stereoRev     reverb effect signal
    """
	def __init__(self, cleanS):
		""" Init Methdod """
		self.stereoRev = STRev(cleanS, revtime = 1.0, cutoff = 5000, roomSize = 1.0, bal = 0.5)

	def setRevTime(self, revTime):
		""" Method to set STRev's revtime """
		self.stereoRev.setRevtime(revTime)

	def getRevTime(self):
		""" Method to get STRev's revtime """
		return self.stereoRev.revtime

	def setCutoff(self, cutoff):
		""" Method to set STRev's cutoff """
		self.stereoRev.setCutoff(cutoff)

	def getCutoff(self):
		""" Method to get STRev's cutoff """
		return self.stereoRev.cutoff

	def setRoomSize(self, roomSize):
		""" Method to set STRev's roomSize """
		self.stereoRev.setRoomSize(roomSize)

	def getRoomSize(self):
		""" Method to get STRev's roomSize """
		return self.stereoRev.roomSize

	def setBal(self, bal):
		""" Method to set STRev's bal """
		self.stereoRev.setBal(bal)

	def getBal(self):
		""" Method to get STRev's bal """
		return self.stereoRev.bal

	def reset(self):
		""" Method to reset the parameters of Reverb effect """
		self.setRevTime(1)
		self.setCutoff(5000)
		self.setRoomSize(1.0)
		self.setBal(0.5)

	def enable(self, output):
		""" Method to output the Reverb effect signal """
		self.stereoRev.setInput(output)
		self.stereoRev.out()

	def disable(self):
		""" Method to stop outputting the Reverb effect signal """
		self.stereoRev.reset()
		self.stereoRev.stop()

	def setInput(self, x):
		""" Method to set Reverb input """
		self.stereoRev.setInput(x)


class DelayEFF():
	""" Class that implements the Delay effect.
        
        Attributes:
            d     delay effect signal
    """
	def __init__(self, cleanS):
		""" Init Methdod """
		self.d = Delay(cleanS, delay = 0.25, feedback = 0)

	def setDelayAmount(self, delayAmount):
		""" Method to set Delay's delay """
		self.d.setDelay(delayAmount)

	def getDelayAmount(self):
		""" Method to get Delay's delay """
		return self.d.delay

	def setFeedback(self, feedback):
		""" Method to set Delay's feedback """
		self.d.setFeedback(feedback)

	def getFeedback(self):
		""" Method to get Delay's feedback """
		return self.d.feedback

	def reset(self):
		""" Method to reset the parameters of Delay effect """
		self.setDelayAmount(0.25)
		self.setFeedback(0.0)

	def enable(self, output):
		""" Method to output the Delay effect signal """
		self.d.setInput(output)
		self.d.out()

	def disable(self):
		""" Method to stop outputting the Delay effect signal """
		self.d.reset()# this reset is Pyo's reset function, not our custom one
		self.d.stop()

	def setInput(self, x):
		""" Method to set Delay input """
		self.d.setInput(x)
