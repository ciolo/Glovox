# Glovox
![logo.png](/Images/logo.png)

## Assignment
Build a musical instruments (consisting of a glove with a microphone) that let the user use his voice as a musical instrument.
The users must be able to select an effect from an application and apply it to his voice, which is captured by the **Glovox**.
The idea comes from one of the Primiata Forneria Marconi’s singer, Bernardo Lanzetti.

## Goals
 - Find a way to convert the audio input in a digital signal.
 - Real-Time processing of the digital signal, so that to modify it with the application.
 - Implement a GUI application that allow the user to manage the effects desired.
 - Build the physical instrument, consisting of a glove and a microphones.

## Technologies
 - Real-time audio Processing is done using a Python free library called **Pyo**.
 - The interface is developed with the PyQt Framework using Python. 
 - Waveform of audio signal is done using NumPy package.
 - The glove has been created using a mini-jack microphone and a glove of synthetic fabric.

## Realization
### Analog to Digital Conversion
The ideal device should have brought **portability** and **low latency** to the system.
Because of the sampling capacity and the delay a compromise was found.
**Focusrite Saffire** audio card has been used to output the signal and the computer itself to convert the input.

### Model-View-Controller
**MVC** pattern has been used to create the control GUI application that the user uses to manage the available effects. In particular, we used Pyo to realize the model. 

###Pyo
Real-Time Digital Signal Processing (RT DSP) has been realized using Python and Python’s module called **Pyo**.
Pyo contain classes for a wide variety of audio signal processing.
With Pyo, the user will be able to include signal processing chains directly in Python scripts or projects, and to manipulate them in real-time through the interpreter.

Pyo offers primitives, like mathematical operations on audio signals, basic signal processing (filters, delay, synthesis generators, etc), but also complex algorithms to create audio manipulations.
Pyo also supports the MIDI protocol for generating sound events and controlling process parameters.

### Glovox (The Model)
This class is used to keep track of the references of every effect: so, the View/Controller communicates just with this class and delegates to it the management of the effects.
It is responsible of starting **Pyo’s Server**.
Contains methods to get, enable and disable the effects, and some methods, based on **Pyo’s Tables**, to create the waveform of the currently selected signal.

### Effects
Effects can be divided in **Pyo’s special effects** and **Pyo’s signal generator**.
The first one use a signal generator called Input. This generator is used to get the microphone’s signal in Real-Time. With Input we can create some effects like Distortion, Harmonizer, Auto-Wah, Reverb and Delay.
The other effects consist in some synthesized sounds. This sounds are obtained using signal generators and they are created based on a frequency range which is computed using a Gate on the input signal. We included the following effects: Super Saw, Blit, Phasor, Sinusoidal Oscillator, RC Oscillator and Low Filter Oscillator.

### Interface
The GUI of Glovox has been realized using **PyQt5**. At startup the application will present itself with a simple interface.
Initially, no effect is activated, but only the original signal from the microphone is processed.
![Interface3.png](/Images/Interface3.png)

The GUI provide a list to choose the effect and three boxes to vary parameters of Reverb, Delay and the chosen effect.
Also, it’s present a box to show the waveform of every effect.
It is possible to get a brief description of the effect and its parameters.
![Interface4.png](/Images/Interface4.png)
![Interface5.png](/Images/Interface5.png)

### Glove
The Glove has been created using a mini-jack microphone and a glove of synthetic fabric. 
The microphone has then been sewn inside the glove in such a way to put the sensors exactly halfway between the thumb and the forefinger.
![glove.jpg](/Images/glove.jpg)

The Glove could be finally used, connecting the jack to the computer, the computer to the audio card, launching the application and singing with the glove put under the throat.
![reo.png](/Images/reo.png)

## Usability Test
To test the usability of the Glovox, we choose a SEQ test composed by twelve questions, that can be evaluated from 1 to 7.
The test took place in a comfortable room, with two surrounding speakers and the microphone’s input volume lowered to the minimum possible, due to the unpleasant effect created by the feedback of the speakers.
Before starting the test, we gave a brief explanation of what Glovox is and does.

### Tasks
Tasks:
 - Put the Glove under your throat. 
 - Now, take confidence with your voice and try to sing some notes.
 - Try to enable the Harmonizer effect and enjoy using it!
 - Try to vary between all the available chords. 
 - Try to enable Reverb and to vary its parameters, as you want.
 - Now, change effect and enable Super Saw.
 - Vary its parameters, as you want.
 - If you want, enable Delay and/or Reverb and vary their parameters.
 - Now you’re free! Enjoy Glovox doing whatever you want!

### SEQ
We examined a population of thirteen interviewees.
Before making global consideration overall the answers, we used the twelfth question to divide the population between musicians and non-musicians.
For a rate greater than 4, we considered the interviewee a musician, otherwise we considered him a non-musician. 
Each question has been evaluated with the average and the standard deviation of the collected rates.

**Musicians**
![Res.png](/Images/Res.png)

**Non Musicians**
![Res2.png](/Images/Res2.png)

**Globa Evaluation**
![Res3.png](/Images/Res3.png)

## Conclusion
 - The results of the Usability tests highlighted the potential of Glovox.
 - A problem of Glovox has been the amount of noise, while the sound latency has not been very considerable, despite our previsions. 
 - An improvement concerns the possibility of using a jack directly connected to the audio card removing the latency that we encountered at the first steps of the project.
 - We should also consider the idea of making a portable version of Glovox, for example using a device with an LCD screen and potentiometers - or touch screen displaying the GUI - instead of the computer and the audio card.
