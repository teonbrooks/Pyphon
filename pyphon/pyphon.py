# Module with a number of functions useful for working with the output of the Penn Forced Aligner (CITATION, WEBSITE).
# Eventual goal is to provide a set of functions for phonetic analysis similar in function to Praat (Boersma & Weenink, 2004+).

# Depends on several functions from SciPy and Pylab/MatPlotLib.

# Import string for text manipulation (needed for textgrid manipulation.
import string
# Import necessary functions from SciPy and Pylab
from scipy.io.wavfile import read
from pylab import plot, show, subplot, specgram
# skip this line and remove cmap=binary from the code below if you want non-greyscale spectrograms
from matplotlib.cm import binary
from matplotlib import axis, pyplot, cm
from __future__ import division

# Define functions:

# This function takes as input a Praat textgrid and returns a dictionary for each tier which contains the list [label,start,end] for each interval.
def textgrid(file):
    #reads textgrid
    textgrid = open(file, 'r').read()
    #splits into tiers
    tiers = textgrid.split('"IntervalTier"\n')
    #The first four elements correspond to the number of sound segments listed in phone
    phone = tiers[1].split('\n')[:4]
    #Removes trailing whitespace and the phone information from the tier.
    tier1 = '\n'.join(string.rstrip(tiers[1]).split('\n')[4:]).split('"\n')
    #This is done to remove the phone information from the tier.
    tier2 = '\n'.join(string.rstrip(tiers[2]).split('\n')[4:]).split('"\n')
    #Creates empty dictionaries
    interval1 = {}
    interval2 = {}
    #Creates a triple where 1:index, 2:start time, 3:end time.
    for j, i in enumerate(tier1):
        interval1[j] = (i.split('\n')[2][1:], i.split('\n')[0],i.split('\n')[1])
    for j, i in enumerate(tier2):
        interval2[j] = (i.split('\n')[2][1:], i.split('\n')[0],i.split('\n')[1])
    return interval1, interval2

# Read wavfile, return data in NumPy array along with useful information:
def wav(soundfile):
    rate, data = read(soundfile)
    x = [float(r)/rate for r in range(len(data))]
    #for i, r in enumerate(x): x[i] = float(r)/rate
    return [x,rate, data]

# Basic waveform plotting function:
def waveform(x, data):
	#x = range(len(data))
	plot(x,data,color='black',linewidth=0.2)

# Basic spectrogram plotting function:
def spectrogram(data,rate,window_length=20, noverlap = 0, cmap=cm.binary):
	nfft = int(float((window_length*rate))/1000)
	specgram(data,NFFT=nfft,noverlap=noverlap,cmap=cmap)
# wondering if we can use the non-plot part of the output of specgram to get dynamic range and such. I haven't looked at what type of object it's returning, but we might be able to assign it to something, then apply a threshold, then plot the results of that?

# Basic transcription of the file from Penn Forced Aligner
def transcript(interval1):
    for word in interval1:
        #plots the interval for each phone
        pyplot.axvspan(float(interval1[word][1]), float(interval1[word][2]), facecolor = 'b')
        # actually plot words:
        pyplot.annotate(interval1[word][0], xy =((float(interval1[word][1])+float(interval1[word][2]))/2, .5), color= 'y')   


# Function which combines previous ones to give Praat-style waveform+spectrogram+textgrid plot
# plot waveform + spectrogram + transcription
#time is given in sec units
def soundplot(x, data, rate, interval1, interval2, window_length = 20):
    # plot waveform
    subplot(3,1,1)
    waveform(x,data)
    # plot spectrogram
    subplot(3,1,2)
    spectrogram(data, rate, window_length)
    # add transcription:
    subplot(3,1,3)
    transcript(interval1)


# Define a class

class Sound:
    def __init__(self,soundfile,transcription):
        self.x, self.rate, self.data = wav(soundfile)
        self.interval1, self.interval2 = textgrid(transcription)
        self.soundfile = soundfile

    # assigns waveform as a method
    def waveform(self):
        plot(self.x,self.data,color='black',linewidth=0.2)
    
    # assigns spectrogram as a method
    def spectrogram(self,window_length=20,noverlap=0,cmap=cm.binary):
        return spectrogram(self.data, self.rate, window_length=window_length, noverlap = noverlap, cmap=cmap)
    
    # assigns transcript as a method
    def transcript(self):
        return transcript(self.interval1)
    
    # assigns soundplot as a method
    def soundplot(self):
        return soundplot(self.x, self.data, self.rate, self.interval1, self.interval2)
