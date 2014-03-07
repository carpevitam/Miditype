import kivy
kivy.require('1.0.8')

from kivy.core.window import Window
from kivy.uix.widget import Widget
from pygame import midi
from midiutil.MidiFile3 import MIDIFile

from kivy.properties import NumericProperty, ObjectProperty

from kivy.uix.boxlayout import BoxLayout



# TEST LAYOUT
class Lay(BoxLayout):
    pass


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

    # KEY SETUP
    global keys
    keys = dict()

    try:
        f = open('keyconfig','r+')
    except:
        #default
        f = open('keyconfig-default','r+')
        pass
    for line in f:
        if line.startswith('###') or line.startswith('\n'):
            pass
        else:
            keys[ord(line[:-1].split(' ')[0])] = int(line[:-1].split(' ')[1])
    print(keys)

    # INITIALIZE MIDI INFORMATION
    ###################################################################################
    global active
    active = set()

    midi.init()
    global player
    player = midi.Output(0)
    # player.set_instrument(48,1)
    player.set_instrument(1,1)

    global start_time
    start_time = 0
    te = NumericProperty(23);
    global tempo
    tempo = 60 # make dynamic later
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
    noteVAL = NumericProperty(0)
    def update(self,dt):
        noteVAL = NumericProperty(0)
        if (active):
            noteVAL = list(active)[0]
    global initial
    initial = True
    ###################################################################################
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        global initial
        global start_time
        
        if keycode[1] == 'escape':
            keyboard.release()

            binfile = open("output" + str(midi.time()) + ".mid",'wb')
            MyMIDI.writeFile(binfile)
            binfile.close()
        if keycode[0] in keys.keys() and keycode[0] not in active:
            if initial:
                initial = False
                start_time = midi.time()

            player.note_on(keys[keycode[0]],127,1)
            active.add(keycode[0])

            noteinfo[keycode[0],'time'] = tempo / 60000 * (midi.time()-start_time)

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def _on_keyboard_up(self,keyboard,keycode):
        if keycode[0] in active and keycode[0] in keys.keys():
            player.note_off(keys[keycode[0]],127,1)
            active.remove(keycode[0])

            time = noteinfo[keycode[0],'time']
            MyMIDI.addNote(0,0,keys[keycode[0]],time,(tempo / 60000 * (midi.time()-start_time))-time,100)

    def on_touch_up(self,touch): 
        print(self.width)
        print(self.height)

        partition = self.width / 10;
        tempDict = {}
        if touch.y < self.height / 2:
            temp = [122,120,99,118,98,  97,115,100,102,103] 
        else:
            temp = [110,109,44,46,47,104,106,107,108,59,39]
        for i in range(10):
            tempDict[i] = temp[i]
            # tempDict[i] = keys.keys()[i]
        if int(touch.x*10/self.width) in tempDict.keys() and tempDict[int(touch.x*10/self.width)] in active:
            note = tempDict[int(touch.x*10/self.width)]
            player.note_off(keys[note],127,1)
            active.remove(note)


            time = noteinfo[note,'time']
            MyMIDI.addNote(0,0,keys[note],time,(tempo / 60000 * (midi.time()-start_time))-time,100)
            # noteinfo[tempDict[int(touch.x*10/self.width)],'time'] = tempo / 60000 * (midi.time()-start_time)


    def on_touch_down(self,touch): # need to implement gliss

        partition = self.width / 10;
        tempDict = {}
        if touch.y < self.height / 2:
            temp = [122,120,99,118,98,  97,115,100,102,103] 
        else:
            temp = [110,109,44,46,47,104,106,107,108,59,39]
        for i in range(10):
            tempDict[i] = temp[i]
            # tempDict[i] = keys.keys()[i]
        if int(touch.x*10/self.width) in tempDict.keys() and tempDict[int(touch.x*10/self.width)] not in active:
            note = tempDict[int(touch.x*10/self.width)]
            player.note_on(keys[note],127,1)
            active.add(note)
            noteinfo[note,'time'] = tempo / 60000 * (midi.time()-start_time)
        # if keycode[0] in keys.keys() and keycode[0] not in active:

        #     player.note_on(keys[keycode[0]],127,1)
        #     active.add(keycode[0])

        #     noteinfo[keycode[0],'time'] = tempo / 60000 * (midi.time()-start_time)



        if touch.x > 400:
            player.note_off(60,127,1)
    def precision_algorithm():
        pass

if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MyKeyboardListener())