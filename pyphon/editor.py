#----------------------------------------------------------------------

import pyphon
import matplotlib
import  os
import  wx
from wx.lib.splitter import MultiSplitterWindow

#----------------------------------------------------------------------






#This brings up a file dialog to import files.
#This happens at launch. If no files are selected, RaiseError 
#---------------------------------------------------------------------------

# This is how you pre-establish a file filter so that the dialog
# only shows the extension(s) you want it to.
wildcard = "Wavefile (*.wav)|"     \
           "TextGrid (*.TextGrid)|" \
           "All files (*.*)|*.*"

#---------------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Create and Show an OPEN FileDialog", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

        b = wx.Button(self, -1, "Create and Show a SAVE FileDialog", (50,90))
        self.Bind(wx.EVT_BUTTON, self.OnButton2, b)


    def OnButton(self, evt):
        self.log.WriteText("CWD: %s\n" % os.getcwd())

        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'open' dialog, and allows multitple
        # file selections as well.
        #
        # Finally, if the directory is changed in the process of getting files, this
        # dialog is set up to change the current working directory to the path chosen.
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()

            self.log.WriteText('You selected %d files:' % len(paths))

            for path in paths:
                self.log.WriteText('           %s\n' % path)

        # Compare this with the debug above; did we change working dirs?
        self.log.WriteText("CWD: %s\n" % os.getcwd())

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()



    def OnButton2(self, evt):
        self.log.WriteText("CWD: %s\n" % os.getcwd())

        # Create the dialog. In this case the current directory is forced as the starting
        # directory for the dialog, and no default file name is forced. This can easilly
        # be changed in your program. This is an 'save' dialog.
        #
        # Unlike the 'open dialog' example found elsewhere, this example does NOT
        # force the current working directory to change if the user chooses a different
        # directory than the one initially set.
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )

        # This sets the default filter that the user will initially see. Otherwise,
        # the first filter in the list will be used by default.
        dlg.SetFilterIndex(2)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.log.WriteText('You selected "%s"' % path)

            # Normally, at this point you would save your data using the file and path
            # data that the user provided to you, but since we didn't actually start
            # with any data to work with, that would be difficult.
            # 
            # The code to do so would be similar to this, assuming 'data' contains
            # the data you want to save:
            #
            # fp = file(path, 'w') # Create file anew
            # fp.write(data)
            # fp.close()
            #
            # You might want to add some error checking :-)
            #

        # Note that the current working dir didn't change. This is good since
        # that's the way we set it up.
        self.log.WriteText("CWD: %s\n" % os.getcwd())

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()

        

#---------------------------------------------------------------------------


def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#---------------------------------------------------------------------------


overview = """\
This class provides the file selection dialog. It incorporates OS-native features
depending on the OS in use, and can be used both for open and save operations. 
The files displayed can be filtered by setting up a wildcard filter, multiple files
can be selected (open only), and files can be forced in a read-only mode.

There are two ways to get the results back from the dialog. GetFiles() returns only
the file names themselves, in a Python list. GetPaths() returns the full path and 
filenames combined as a Python list.

"""


if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])















#This is for the MultiSplitter Window. This comes from the wxpython demo and it has been modified to have a default horizontal orientation.
#----------------------------------------------------------------------

class SamplePane(wx.Panel):
    """
    Just a simple test window to put into the splitter.
    """
    def __init__(self, parent, colour, label):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)
        self.SetBackgroundColour(colour)
        wx.StaticText(self, -1, label, (5,5))

    def SetOtherLabel(self, label):
        wx.StaticText(self, -1, label, (5, 30))



class ControlPane(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        hvBox = wx.RadioBox(self, -1, "Orientation",
                            choices=["Horizontal", "Vertical"],
                            style=wx.RA_SPECIFY_COLS,
                            majorDimension=1)
        hvBox.SetSelection(0)
        self.Bind(wx.EVT_RADIOBOX, self.OnSetHV, hvBox)
        
        luCheck = wx.CheckBox(self, -1, "Live Update")
        luCheck.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, self.OnSetLiveUpdate, luCheck)

        btn = wx.Button(self, -1, "Swap 2 && 4")
        self.Bind(wx.EVT_BUTTON, self.OnSwapButton, btn)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hvBox)
        sizer.Add(luCheck, 0, wx.TOP, 5)
        sizer.Add(btn, 0, wx.TOP, 5)
        border = wx.BoxSizer()
        border.Add(sizer, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(border)


    def OnSetHV(self, evt):
        rb = evt.GetEventObject()
        self.GetParent().SetOrientation(rb.GetSelection())
        

    def OnSetLiveUpdate(self, evt):
        check = evt.GetEventObject()
        self.GetParent().SetLiveUpdate(check.GetValue())


    def OnSwapButton(self, evt):
        self.GetParent().Swap2and4()
        


class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        cp = ControlPane(self)
        
        splitter = MultiSplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.splitter = splitter
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(cp)
        sizer.Add(splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)


        p1 = SamplePane(splitter, "pink", "Panel One")
        p1.SetOtherLabel(
            "There are two sash\n"
            "drag modes. Try\n"
            "dragging with and\n"
            "without the Shift\n"
            "key held down."
            )
        splitter.AppendWindow(p1, 140)

        p2 = SamplePane(splitter, "sky blue", "Panel Two")
        p2.SetOtherLabel("This window\nhas a\nminsize.")
        p2.SetMinSize(p2.GetBestSize())
        splitter.AppendWindow(p2, 150)

        p3 = SamplePane(splitter, "yellow", "Panel Three")
        splitter.AppendWindow(p3, 125)

        p4 = SamplePane(splitter, "Lime Green", "Panel Four")
        splitter.AppendWindow(p4)

        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnChanged)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnChanging)


    def OnChanging(self, evt):
        self.log.write( "Changing sash:%d  %s\n" %
                        (evt.GetSashIdx(), evt.GetSashPosition()))
        # This is one way to control the sash limits
        #if evt.GetSashPosition() < 50:
        #    evt.Veto()

        # Or you can reset the sash position to whatever you want
        #if evt.GetSashPosition() < 5:
        #    evt.SetSashPosition(25)


    def OnChanged(self, evt):
        self.log.write( "Changed sash:%d  %s\n" %
                        (evt.GetSashIdx(), evt.GetSashPosition()))

            
    def SetOrientation(self, value=0):
        if value:
            self.splitter.SetOrientation(wx.VERTICAL)
        else:
            self.splitter.SetOrientation(wx.HORIZONTAL)
        self.splitter.SizeWindows()

            
    def SetLiveUpdate(self, enable):
        if enable:
            self.splitter.SetWindowStyle(wx.SP_LIVE_UPDATE)
        else:
            self.splitter.SetWindowStyle(0)
            

    def Swap2and4(self):
        win2 = self.splitter.GetWindow(1)
        win4 = self.splitter.GetWindow(3)
        self.splitter.ExchangeWindows(win2, win4)

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>MultiSplitterWindow</center></h2>

This class is very similar to wx.SplitterWindow except that it
allows for more than two windows and more than one sash.  Many of
the same styles, constants, and methods behave the same as in
wx.SplitterWindow.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
















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
    
