import kivy
kivy.require('1.0.8')

from kivy.core.window import Window
from kivy.uix.widget import Widget
from pygame import midi
from midiutil.MidiFile3 import MIDIFile

class MyKeyboardListener(Widget):

    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


    row1 = [49,50,51,52,53,54,55,56,57,48,45,61] #1234567890-=
    row2 = [113,119,101,114,116,121,117,105,111,112,91,93,92]#qwertyuiop[]\
    row3 = [97,115,100,102,103,104,106,107,108,59,39]#asdfghjkl;'
    row4 = [122,120,99,118,98,110,109,44,46,47]#zxcvbnm,./

    # global keys
    # keys = dict()
    # num = 48 #goes til 83
    # for key in row4:
    #     keys[key] = num
    #     num += 1
    # for key in row3:
    #     keys[key] = num
    #     num += 1
    # for key in row2:
    #     keys[key] = num
    #     num += 1
    # keys[49] = 82
    # keys[50] = 83

    global keys
    keys = dict()
    bass = [48, 50, 52, 53, 55, 57, 59, 60]
    for i in range(8):
        keys[row4[i]] = bass[i]
        keys[row3[i]] = bass[i] + 12
        keys[row2[i]] = bass[i] + 24
        keys[row1[i]] = bass[i] + 36

    global active
    active = set()

    midi.init()
    global player
    player = midi.Output(0)
    # player.set_instrument(48,1)
    player.set_instrument(1,1)

    global tempo
    tempo = 120 # make dynamic later
    track = 0
    channel = 0
    pitch = 60
    time = 0
    duration = 1
    volume = 100

    global MyMIDI
    MyMIDI = MIDIFile(1)
    MyMIDI.addTrackName(track,time,"Recording")
    MyMIDI.addTempo(track,time,tempo)

    #MyMIDI.addNote(track,channel,pitch,time,duration,volume)

    global noteinfo
    noteinfo = dict()

    # timeMIDI = tempo / 60000 * time
    # durationMIDI = tempo / 60000 * time_difference

    global initial
    initial = True
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        global initial
        if initial:
            initial = False
            midi.init()
        if keycode[1] == 'escape':
            keyboard.release()

            binfile = open("output" + str(midi.time()) + ".mid",'wb')
            MyMIDI.writeFile(binfile)
            binfile.close()
        if keycode[0] in keys.keys() and keycode[0] not in active:
            player.note_on(keys[keycode[0]],127,1)
            active.add(keycode[0])


            noteinfo[keycode[0],'time'] = tempo / 60000 * midi.time()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True
    def _on_keyboard_up(self,keyboard,keycode):
        if keycode[0] in active and keycode[0] in keys.keys():
            player.note_off(keys[keycode[0]],127,1)
            active.remove(keycode[0])

            time = noteinfo[keycode[0],'time']
            MyMIDI.addNote(0,0,keys[keycode[0]],time,(tempo / 60000 * midi.time())-time,100)

if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MyKeyboardListener())