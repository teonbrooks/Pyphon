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
from matplotlib import axis, pyplot


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
    intervals1 = {}
    intervals2 = {}
    #Creates a triple where 1:index, 2:start time, 3:end time.
    for j, i in enumerate(tier1):
        intervals1[j] = (i.split('\n')[2][1:], i.split('\n')[0],i.split('\n')[1])
    for j, i in enumerate(tier2):
        intervals2[j] = (i.split('\n')[2][1:], i.split('\n')[0],i.split('\n')[1])
    return intervals1, intervals2

# Read wavfile, return data in NumPy array along with useful information:
def wav(soundfile):
    rate, data = read(soundfile)
    x = range(len(data))
    return [x,data,rate]

# Basic waveform plotting function:
def waveform(data,rate):
	x = range(len(data))
	plot(x,data,color='black',linewidth=0.2)

# Basic spectrogram plotting function:
def spectrogram(data,rate,window_length=20):
	nfft = int(float((window_length*rate))/1000)
	specgram(data,NFFT=nfft,noverlap=0,cmap=binary)
# wondering if we can use the non-plot part of the output of specgram to get dynamic range and such. I haven't looked at what type of object it's returning, but we might be able to assign it to something, then apply a threshold, then plot the results of that?

# Function which combines previous ones to give Praat-style waveform+spectrogram+textgrid plot
# plot waveform + spectrogram + transcription
#time is given in sec units
def soundplot(sound, transcription, window_length = 20):
    # read in soundfile:
    a = wav(sound)
    # read in textgrid:
    b = textgrid(transcription)
    # plot waveform
    subplot(3,1,1)
    waveform(a[1],a[2])
    # plot spectrogram
    subplot(3,1,2)
    spectrogram1(a[1], a[2], window_length)
    # add transcription:
    subplot(3,1,3)
    for word in b[0]:
    	#plots the interval for each phone
	    pyplot.axvspan(float(b[0][word][1]), float(b[0][word][2]), facecolor = 'b')
	    # actually plot words:
	    pyplot.annotate(b[0][word][0], xy =((float(b[0][word][1])+float(b[0][word][2]))/2, .5), color= 'y')
    axis([0,max(a[0]),0,2])
	
# define class 'Sound' (check to make sure this isn't overwriting anything else)
# definitely not the right syntax yet
class Sound:
    def __init__(self,soundfile,transcription):
        self.rate, self.data = read(soundfile)
        self.x = range(len(self.data))
        for i, r in enumerate(self.x): self.x[i] = float(r)/self.rate
        self.intervals1, self.intervals2 = textgrid(transcription)

    #make waveform plot
    def waveform(self):
        plot(self.x,self.data,color='black',linewidth=0.2)
    
    # make spectrogram plot
    def spectrogram(self,window_length=20,noverlap=0,cmap=binary):
        nfft = int(float((window_length*self.rate))/1000)
        specgram(self.data,NFFT=nfft,noverlap=noverlap,cmap=binary)
        

    # Make transcription plot
#    def self.transcription(args):






# plot transcription
#subplot(3,1,3)
#axis([0,max(a[0]),0,2])
#plots the interval
#for word in intervals1:
#    matplotlib.pyplot.axvspan(float(b[0][word][1]), float(b[0][word][2]), facecolor = 'b')
#    #plots word
#    annotate(word, xy =((float(b[0][word][1])+float(b[0][word][2]))/2, .5), color= 'y')




