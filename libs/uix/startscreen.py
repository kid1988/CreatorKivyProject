# -*- coding: utf-8 -*-
#
# startscreen.py
#

from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty


class StartScreen(BoxLayout):
    events_callback = ObjectProperty(None)
    '''Функция обработки сигналов экрана.'''

    def __init__(self, **kvargs):
        super(StartScreen, self).__init__(**kvargs)
