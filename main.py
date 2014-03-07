from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

import touchapp
from touchapp import MyKeyboardListener

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class Keyboard(Widget):
	pass



class MiditypeApp(App):
	midi = MyKeyboardListener()
	# layout = GridLayout(cols = 2)
	# layout.add_widget(midi)
	# layout.add_widget(Button(text='World 1',width =100))
	# layout.add_widget(Button(text='Hello 2'))
	# layout.add_widget(Button(text='World 3',width=100))


	layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)
	b = Button(text='Hello 1', size_hint_x=None, width=100)

	def callback(instance,value):
		print(str(instance) + " " + str(value))
	b.bind(on_press=callback)
	layout.add_widget(b)
	layout.add_widget(Button(text='World 1'))
	layout.add_widget(Button(text='Hello 2', size_hint_x=None, width=100))
	layout.add_widget(Button(text='World 2'))
	layout.add_widget(midi)

	global layout
	#Clock.schedule_interval(midi.update, 1.0 / 60.0)
	def build(self):
		midi = MyKeyboardListener()
		# layout = GridLayout(cols = 2)
		# layout.add_widget(midi)
		# layout.add_widget(Button(text='World 1'))
		# layout.add_widget(Button(text='Hello 2'))
		# layout.add_widget(Button(text='World 2'))
		#Clock.schedule_interval(midi.update, 1.0 / 60.0)
		
		# return layout
		return midi

if __name__ == '__main__':
	MiditypeApp().run();