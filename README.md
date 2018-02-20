# Glovox
![Glovox logo.png](/Images/Glovox logo.png)

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

### Pyo
Real-Time Digital Signal Processing (RT DSP) has been realized using Python and Python’s module called **Pyo**.
Pyo contain classes for a wide variety of audio signal processing.
With Pyo, the user will be able to include signal processing chains directly in Python scripts or projects, and to manipulate them in real-time through the interpreter.

Pyo offers primitives, like mathematical operations on audio signals, basic signal processing (filters, delay, synthesis generators, etc), but also complex algorithms to create audio manipulations.
Pyo also supports the MIDI protocol for generating sound events and controlling process parameters.

### Glovox (The Model)
This class is used to keep track of the references of every effect: so, the View/Controller communicates just with this class and delegates to it the management of the effects.
It is responsible of starting **Pyo’s Server**.
Contains methods to get, enable and disable the effects, and some methods, based on **Pyo’s Tables**, to create the waveform of the currently selected signal.

