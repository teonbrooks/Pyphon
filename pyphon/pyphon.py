"""
Module with a number of functions useful for working with the output of the Penn Forced Aligner (CITATION, WEBSITE).
Eventual goal is to provide a set of functions for phonetic analysis similar in function to Praat (Boersma & Weenink, 2004+).

Depends on several functions from SciPy and Pylab/MatPlotLib.

"""
import string
from scipy.io.wavfile import read
from pylab import plot, show, subplot, specgram
from matplotlib import axis, pyplot as plt, cm

# Define a class

class Sound:
    def __init__(self, soundfile, transcription):
        self.x, self.rate, self.data = wav(soundfile)
        self.interval1, self.interval2 = textgrid(transcription)
        self.soundfile = soundfile
        self.soundplot = SoundFigure
#        self.waveform = plot(self.x, self.data, color='black', linewidth=0.2)

    # assigns spectrogram as a method
    def spectrogram(self, window_length=20, noverlap=0, cmap=cm.binary):
        return spectrogram(self.data, self.rate, window_length=window_length, noverlap=noverlap, cmap=cmap)

    # assigns transcript as a method
    def transcript(self):
        return transcript(self.interval1)

    # assigns soundplot as a method
    def soundplot(self):
        return soundplot(self.x, self.data, self.rate, self.interval1, self.interval2)


class SoundFigure:
    """
    Parent class for Pyphon figures.

    In order to subclass:

     - find desired figure properties and then use them to initialize
       the SoundFigure superclass; then use the
       :py:attr:`SoundFigure.figure` and :py:attr:`SoundFigure.canvas` attributes.

    """
    def __init__(self, title="SoundFigure", **fig_kwargs):
        frame = mpl_figure(**fig_kwargs)
        # store attributes
        self._frame = frame
        self.figure = frame.figure
        self.canvas = frame.canvas
        self.canvas.mpl_connect('button_press_event', self.onclick)

    def onclick(self, event):
        self.xdata = event.xdata

    """the goal of the SoundFigure class is to do the functionality below with some user interface"""
    # Function which combines previous ones to give Praat-style waveform+spectrogram+textgrid plot
    # plot waveform + spectrogram + transcription
    #time is given in sec units
    def soundplot(x, data, rate, interval1, interval2, window_length=20):
        # plot waveform
        subplot(3, 1, 1)
        waveform(x, data)
        # plot spectrogram
        subplot(3, 1, 2)
        spectrogram(data, rate, window_length)
        # add transcription:
        subplot(3, 1, 3)
        transcript(interval1)

def waveform(x, data):
    """ Basic waveform plotting function """
    #x = range(len(data))
    plot(x, data, color='black', linewidth=0.2)

# Basic spectrogram plotting function:
def spectrogram(data, rate, window_length=20, noverlap=0, cmap=cm.binary):
    nfft = int(float((window_length * rate)) / 1000)
    specgram(data, NFFT=nfft, noverlap=noverlap, cmap=cmap)
# wondering if we can use the non-plot part of the output of specgram to get dynamic range and such. I haven't looked at what type of object it's returning, but we might be able to assign it to something, then apply a threshold, then plot the results of that?

class mpl_figure:
    def __init__(self, **fig_kwargs):
        "creates self.figure and self.canvas attributes and returns the figure"
        self.figure = plt.figure(**fig_kwargs)
        self.canvas = self.figure.canvas

    def Close(self):
        plt.close(self.figure)

    def SetStatusText(self, text):
        pass

    def redraw(self, axes=[], artists=[]):
        "Adapted duplicate of mpl_canvas.FigureCanvasPanel"
        self.canvas.restore_region(self._background)
        for ax in axes:
            ax.draw_artist(ax)
            extent = ax.get_window_extent()
            self.canvas.blit(extent)
        for artist in artists:
            ax = artist.get_axes()
            ax.draw_artist(ax)
            extent = ax.get_window_extent()
            self.canvas.blit(extent)

    def store_canvas(self):
        self._background = self.canvas.copy_from_bbox(self.figure.bbox)

# Define functions:

# This function takes as input a Praat textgrid and returns a dictionary for each tier which contains the list [label,start,end] for each interval.
def textgrid(fname):
    #reads textgrid
    textgrid = open(fname, 'r').read()
    #splits into tiers
    tiers = textgrid.split('"IntervalTier"\n')
    #Removes trailing whitespace and the phone information from the tier.
    tier1 = '\n'.join(string.rstrip(tiers[1]).split('\n')[4:]).split('"\n')
    #This is done to remove the phone information from the tier.
    tier2 = '\n'.join(string.rstrip(tiers[2]).split('\n')[4:]).split('"\n')
    #Creates empty dictionaries
    interval1 = {}
    interval2 = {}
    #Creates a triple where 1:index, 2:start time, 3:end time.
    for j, i in enumerate(tier1):
        interval1[j] = (i.split('\n')[2][1:], i.split('\n')[0], i.split('\n')[1])
    for j, i in enumerate(tier2):
        interval2[j] = (i.split('\n')[2][1:], i.split('\n')[0], i.split('\n')[1])
    return interval1, interval2


# Read wavfile, return data in NumPy array along with useful information:
def wav(soundfile):
    rate, data = read(soundfile)
    x = [float(r) / rate for r in range(len(data))]
    #for i, r in enumerate(x): x[i] = float(r)/rate
    return [x, rate, data]


# Basic transcription of the file from Penn Forced Aligner
def transcript(interval1):
    for word in interval1:
        #plots the interval for each phone
        pyplot.axvspan(float(interval1[word][1]), float(interval1[word][2]), facecolor='b')
        # actually plot words:
        pyplot.annotate(interval1[word][0], xy=((float(interval1[word][1]) + float(interval1[word][2])) / 2, .5), color='y')



