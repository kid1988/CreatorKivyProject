#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# bug_reporter.py
#
# Окно для визуализации ошибок запуска приложения.
# Модуль взят и переработан из программы Kivy Designer -
# графическом строителе интерфейсов для фреймворка Kivy.
#
#
# MIT license
#
# Copyright (c) 2010-2015 Kivy Team and other contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Март, 2016
# Луганск
# Автор переработанного сценария: Иванов Юрий aka HeaTTheatR
#
# Email: gorodage@gmail.com
#

import os
import sys


from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty


class BugReporter(FloatLayout):
    title = 'Bug reporter'
    label_info_for_user = StringProperty('Sorry, an error occurred in the '
                                         'program!')
    info_for_user = StringProperty('You can report this bug using'
                                   'the button bellow, helping us to fix it.')
    txt_report = StringProperty('')

    callback_clipboard = ObjectProperty(None)
    """Функция копирования баг-репорта в буфер обмена"""

    callback_report = ObjectProperty(None)
    """Функция отправки баг-репорта"""

    report_readonly = BooleanProperty(False)
    """Запрещено ли редактировать текст ошибки"""

    icon_background = StringProperty('data/logo/kivy-icon-256.png')
    """Фоновое изображение окна"""

    txt_button_clipboard = StringProperty('Copy Bug')
    txt_button_report = StringProperty('Report Bug')
    txt_button_close = StringProperty('Close')
    """Подписи кнопок"""

    Builder.load_file('{}/libs/uix/kv/bugreporter.kv'.format(
        os.path.split(os.path.abspath(sys.argv[0]))[0].split("/libs/uix")[0]))
    """Макет интерфейса"""

    def __init__(self, **kwargs):
        super(BugReporter, self).__init__(**kwargs)

        if not os.path.exists(self.icon_background):
            self.icon_background = 'data/logo/kivy-icon-256.png'

        name_funcs_buttons = {
            self.txt_button_clipboard: self.callback_clipboard,
            self.txt_button_report: self.callback_report}

        for name_button in name_funcs_buttons.keys():
            if callable(name_funcs_buttons[name_button]):
                self.ids.box_layout.add_widget(
                    Button(text=name_button,
                           on_press=name_funcs_buttons[name_button]))

    def on_close(self, *args):
        from kivy.app import App
        App.get_running_app().stop()
