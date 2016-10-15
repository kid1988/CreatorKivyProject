# -*- coding: utf-8 -*-
#
# license.py
#
# Выводит окно с текстом лицензии.
#

import os

from kivy.clock import Clock
from kivy.uix.rst import RstDocument

from libs.uix.dialogs import dialog, card


class ShowLicense(object):
    def show_license(self, *args):
        def choice_language_license(on_language):
            window = dialog(text=self.data.string_lang_wait, title=self.title)
            Clock.schedule_once(
                lambda *args: show_license(window, on_language), 0
            )
            choice_dialog.dismiss()

        def show_license(dialog, on_language):
            path_to_license = '{}/license/license_{}.rst'.format(
                self.directory, self.data.dict_language[on_language]
            )
            if not os.path.exists(path_to_license):
                dialog(text=self.data.string_lang_not_license, title=self.title)
                dialog.dismiss()

                return

            text_license = open(path_to_license).read()
            widget_license = RstDocument(
                text=text_license, background_color=self.data.alpha,
                underline_color=self.data.underline_rst_color
            )
            card(widget_license, size=(.9, .8))
            dialog.dismiss()

        choice_dialog = dialog(
            text=self.data.string_lang_prev_license, title=self.title,
            buttons=[
                [self.data.string_lang_on_russian,
                 lambda *x: choice_language_license(self.data.string_lang_on_russian)],
                [self.data.string_lang_on_english,
                 lambda *x: choice_language_license(self.data.string_lang_on_english)]
            ]
        )

