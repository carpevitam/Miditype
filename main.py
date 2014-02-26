from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

import touchapp
from touchapp import MyKeyboardListener

class Keyboard(Widget):
	pass

class MiditypeApp(App):
	def build(self):
		midi = MyKeyboardListener()
		Clock.schedule_interval(midi.update, 1.0 / 60.0)
		return midi

if __name__ == '__main__':
	MiditypeApp().run();