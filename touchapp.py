import kivy
kivy.require('1.0.8')

from kivy.core.window import Window
from kivy.uix.widget import Widget
from pygame import midi

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

    key = 0
    midi.init()
    global player
    player = midi.Output(0)
    player.set_instrument(48,1)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'have been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        global key
        key = keycode[0] - 52
        if modifiers:
            key += 12
        if key > 44 and key < 100:
            player.note_on(key,127,1)
        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True
    def _on_keyboard_up(self,keyboard,keycode):
        global key
        player.note_off(key,127,1)

if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MyKeyboardListener())