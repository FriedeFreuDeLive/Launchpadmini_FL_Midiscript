#name=launchpadmini
import transport
import midi
import patterns
import device
import channels

PadsW = 8
PadsH = 8

class Tlaunchpadmini():
    def OnInit(self):
        device.setHasMeters()
        self.gridStatus = [0,0,0,0,0,0,0,0,
                           0,0,0,0,0,0,0,0,
                           0,0,0,0,0,0,0,0,
                           0,0,0,0,0,0,0,0,
                           0,0,0,0,0,0,0,0,
                           0,0,0,0,0,0,0,0,
                           0,0,0,0,0,0,0,0,
                           0,0,0,0,0,0,0,0]
        self.step = 0
        self.buttons = [81, 82, 83, 84, 85, 86, 87, 88,
                        71, 72, 73, 74, 75, 76, 77, 78,
                        61, 62, 63, 64, 65, 66, 67, 68,
                        51, 52, 53, 54, 55, 56, 57, 58,
                        41, 42, 43, 44, 45, 46, 47, 48,
                        31, 32, 33, 34, 35, 36, 37, 38,
                        21, 22, 23, 24, 25, 26, 27, 28,
                        11, 12, 13, 14, 15, 16, 17, 18]
    def __init__(self):
        self.BtnMap = [[0 for x in range(PadsW)] for y in range(PadsH + 1)]
    def LedOn(self, iButton, iColor):
        device.midiOutMsg(midi.MIDI_NOTEON + ((0 * 3) + self.buttons[iButton] << 8) + (iColor << 16))
    def OnRefresh(self, flags):
        self.uu = channels.selectedChannel
        self.c = channels.getChannelColor(channels.selectedChannel(0))
        self.d = round(self.c/256/256/2, 0)
        self.e = int(self.d)
        self.f = self.e*-1
        for y in range(64):
            if channels.getGridBit(channels.selectedChannel(0), y) != 1:
                LedOn(y, 0x01)
            else:
                LedOn(y, self.e*-1+4)
    def OnControlChange(self, event):
        print(event.data1)
        print(event.data2)
        if event.data1 == 91 and event.data2 == 127:
            for y in range(64):
                channels.setGridBit(channels.selectedChannel(0), y, 0)
        if event.data1 == 89 and event.data2 == 127:
            #each
            for y in range(64):
                channels.setGridBit(channels.selectedChannel(0), y, 1)
        if event.data1 == 79 and event.data2 == 127:
            #each 2
            for y in range(64):
                if y % 2 == 0: 
                    channels.setGridBit(channels.selectedChannel(0), y, 1)
                else:
                    channels.setGridBit(channels.selectedChannel(0), y, 0)
        if event.data1 == 69 and event.data2 == 127:
            #each 4
            for y in range(64):
                if y % 4 == 0: 
                    channels.setGridBit(channels.selectedChannel(0), y, 1)
                else:
                    channels.setGridBit(channels.selectedChannel(0), y, 0)
        if event.data1 == 59 and event.data2 == 127:
            #each 8
            for y in range(64):
                if y % 8 == 0: 
                    channels.setGridBit(channels.selectedChannel(0), y, 1)
                else:
                    channels.setGridBit(channels.selectedChannel(0), y, 0)
        if event.data1 == 49 and event.data2 == 127:
            #each 16
            for y in range(64):
                if y % 16 == 0: 
                    channels.setGridBit(channels.selectedChannel(0), y, 1)
                else:
                    channels.setGridBit(channels.selectedChannel(0), y, 0)
        if event.data1 == 39 and event.data2 == 127:
            #snare standard
            for y in range(64):
                if (y-4) % 8 == 0: 
                    channels.setGridBit(channels.selectedChannel(0), y, 1)
                else:
                    channels.setGridBit(channels.selectedChannel(0), y, 0)
        if event.data1 == 29 and event.data2 == 127:
            #offhat
            for y in range(64):
                if (y-2) % 4 == 0: 
                    channels.setGridBit(channels.selectedChannel(0), y, 1)
                else:
                    channels.setGridBit(channels.selectedChannel(0), y, 0)
        if event.data1 == 19 and event.data2 == 127:
            #offhat
            for y in range(64):
                if y % 2 != 0: 
                    channels.setGridBit(channels.selectedChannel(0), y, 1)
                else:
                    channels.setGridBit(channels.selectedChannel(0), y, 0)
        if event.data1 == 93 and event.data2 == 127:
            #rotate left
            for y in range(64):
                self.gridStatus[y] = channels.getGridBit(channels.selectedChannel(0), y)
            for y in range(64):
                if y < 63:
                    channels.setGridBit(channels.selectedChannel(0), y, self.gridStatus[y+1])
                else:
                    channels.setGridBit(channels.selectedChannel(0), y, self.gridStatus[0])
        if event.data1 == 94 and event.data2 == 127:
            #rotate right
            for y in range(64):
                self.gridStatus[y] = channels.getGridBit(channels.selectedChannel(0), y)
            for y in range(64):
                if y > 0:
                    channels.setGridBit(channels.selectedChannel(0), y, self.gridStatus[y-1])
                else:
                    channels.setGridBit(channels.selectedChannel(0), y, self.gridStatus[63])
    def OnNoteOn(self, event):
        #print(event.data1)
        if event.data2 == 127:
            self.pressed=-1
            if event.data1 >= 81 and event.data1 <= 88:
                self.pressed = event.data1-81
            if event.data1 >= 71 and event.data1 <= 78:
                self.pressed = event.data1-63
            if event.data1 >= 61 and event.data1 <= 68:
                self.pressed = event.data1-45
            if event.data1 >= 51 and event.data1 <= 58:
                self.pressed = event.data1-27
            if event.data1 >= 41 and event.data1 <= 48:
                self.pressed = event.data1-9
            if event.data1 >= 31 and event.data1 <= 38:
                self.pressed = event.data1+9
            if event.data1 >= 21 and event.data1 <= 28:
                self.pressed = event.data1+27
            if event.data1 >= 11 and event.data1 <= 18:
                self.pressed = event.data1+45
            if self.pressed != -1:
                if channels.getGridBit(channels.selectedChannel(0), self.pressed) != 0:
                    channels.setGridBit(channels.selectedChannel(0), self.pressed, 0)
                else:
                    channels.setGridBit(channels.selectedChannel(0), self.pressed, 1)
launchpadmini = Tlaunchpadmini()
def LedOn(iButton, iColor):
	launchpadmini.LedOn(iButton, iColor)
def OnInit():
    launchpadmini.OnInit()
def OnRefresh(flags):
    launchpadmini.OnRefresh(flags)
def OnControlChange(event):
    launchpadmini.OnControlChange(event)
def OnNoteOn(event):
    launchpadmini.OnNoteOn(event)