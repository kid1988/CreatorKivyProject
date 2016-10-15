# -*- coding: utf-8 -*-
#
# Пример простого плагина. Добавляет кнопку в actionbar.
#

from kivy.clock import Clock


def test_plugin(interval):
    app.screen.ids.action_bar.right_action_items = [
        ['shopping-cart', lambda x: None], ['more-vert', lambda x: None]
    ]


Clock.schedule_once(test_plugin, 5)
