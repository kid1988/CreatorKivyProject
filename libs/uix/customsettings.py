# -*- coding: utf-8 -*-
#
# customsettings.py
#

import os

from kivy.uix.settings import (
    SettingOptions, SettingNumeric, SettingPath, SettingString,
    InterfaceWithNoMenu, Settings
)
from kivy.lang import Builder

from libs.programdata import string_lang_yes, string_lang_cancel, string_lang_title
from libs.uix.dialogs import card, input_dialog, file_dialog
from libs.uix.lists import Lists


TEXT_INPUT = 'Enter value'  # подпись окна для ввода значений
BACKGROUND_SECTIONS = [47 / 255., 167 / 255., 212 / 255., 1]  # фоновый цвет активного раздела настроек
COLOR_TEXT_INPUT = [.9, .9, .9, 1]  # цвет текста описания пункта настроек
BACKGROUND_IMAGE_TITLE = ''  # фоновое изображение описания пункта настроек
BACKGROUND_COLOR_TITLE = [.15, .15, .15, .5]  # цвет описания пункта настроек
BACKGROUND_IMAGE_ITEM = ''  # фоновое изображение пункта настроек
BACKGROUND_COLOR_ITEM = [47 / 255., 167 / 255., 212 / 255., 0]  # цвет пункта настроек
BACKGROUND_COLOR = [1, 1, 1, 0]  # фоновый цвет настроек
SEPARATOR_COLOR = [0.12156862745098039, 0.8901960784313725, 0.2, 0.011764705882352941]
SETTINGS_INTERFACE = InterfaceWithNoMenu

title_item = '''
<SettingSidebarLabel>:
    canvas.before:
        Color:
            rgba: [{background_sections}, int(self.selected)]
        Rectangle:
            pos: self.pos
            size: self.size

<SettingTitle>:
    color: {color_text_title}
    canvas.before:
        Color:
            rgba: {background_color_title}
        Rectangle:
            source: '{background_image_title}'
            pos: self.x, self.y + 2
            size: self.width, self.height - 2
        Color:
            rgba: {separator_color}
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1

<SettingItem>:
    canvas:
        Color:
            rgba: {background_color_item}
        Rectangle:
            source: '{background_image_item}'
            pos: self.x, self.y + 1
            size: self.size
        Color:
            rgba: {separator_color}
        Rectangle:
            pos: self.x, self.y - 2
            size: self.width, 1'''


Builder.load_string("""
<-CustomSettings>:
    interface_cls: 'SettingsInterface'

    canvas:
        Color:
            rgba: 0, 0, 0, .9
        Rectangle:
            size: self.size
            pos: self.pos
""")


class SettingsInterface(SETTINGS_INTERFACE):
    pass


class CustomSettings(Settings):
    '''Кастомные диалоговые окна для экрана настроек.'''

    def __init__(self, **kvargs):
        super(CustomSettings, self).__init__(**kvargs)
        Builder.load_string(
            title_item.format(
                background_color_title=BACKGROUND_COLOR_TITLE,
                background_image_title=BACKGROUND_IMAGE_TITLE,
                background_color_item=BACKGROUND_COLOR_ITEM,
                background_image_item=BACKGROUND_IMAGE_ITEM,
                background_sections=', '.join(
                    [str(value) for value in BACKGROUND_SECTIONS[:-1]]),
                separator_color=SEPARATOR_COLOR,
                color_text_title=COLOR_TEXT_INPUT
            )
        )
        SettingOptions._create_popup = self.options_popup
        SettingNumeric._create_popup = self.input_popup
        SettingString._create_popup = self.input_popup
        SettingPath._create_popup = self.path_popup

    def options_popup(self, options_instance):
        def on_select(value):
            options_instance.value = value
            dialog.dismiss()

        options_list = []
        for options in options_instance.options:
            options_list.append(options)

        options_list = Lists(
            list_items=options_list, flag='single_list',
            events_callback=on_select
        )
        dialog = card(options_list)

    def input_popup(self, input_instance):
        def on_select(value):
            dialog.dismiss()
            if not value or value.isspace():
                return
            input_instance.value = value

        dialog = input_dialog(
            title=string_lang_title, hint_text=TEXT_INPUT,
            text_button_ok=string_lang_yes, events_callback=on_select,
            text_button_cancel=string_lang_cancel)

    def path_popup(self, path_instance):
        def on_select(file_or_directory):
            dialog.dismiss()
            path_instance.value = file_or_directory

        if os.path.isfile(path_instance.value):
            path = os.path.split(path_instance.value)[0]
        else:
            path = path_instance.value

        dialog, file_manager = file_dialog(
            path=path, events_callback=on_select
        )
