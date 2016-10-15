# -*- coding: utf-8 -*-
#
# about.py
#
# Выводит окно с информацией о приложении.
#

from libs.uix.dialogs import dialog


class ShowAbout(object):
    def show_about(self):
        dialog(
            text=self.data.string_lang_about.format(
                LINK_COLOR=self.data.text_link_color),
            title=self.title, ref_callback=self.events_callback
        )

    def events_callback(self, instance, text_link):
        print(instance, text_link)

