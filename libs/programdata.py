# -*- coding: utf-8 -*-
#
# programdata.py
#

import os
import sys
import traceback

from kivy.config import ConfigParser
from kivy.logger import PY2
from kivy.utils import get_color_from_hex

if PY2:
    select_locale = {u'Русский': 'russian', 'English': 'english'}
else:
    select_locale = {'Русский': 'russian', 'English': 'english'}

prog_path = os.path.split(os.path.abspath(sys.argv[0]))[0]

# Если файл настроек отсутствует.
if not os.path.exists('{}/program.ini'.format(prog_path)):
    if PY2:
        language = u'Русский'
    else:
        language = 'Русский'
    theme = 'default'
else:
    config = ConfigParser()
    config.read('{}/program.ini'.format(prog_path))
    theme = config.get('General', 'theme')
    language = config.get('General', 'language')
    # языковая локализация

old_language = language
language = select_locale[language]

# -----------------------УСТАНОВКА ЦВЕТОВОЙ ТЕМЫ---------------------------
config_theme = ConfigParser()
config_theme.read('{}/data/themes/{theme}/{theme}.ini'.format(
    prog_path, theme=theme))

alpha = \
    get_color_from_hex(config_theme.get('color', 'alpha'))
color_action_bar = \
    get_color_from_hex(config_theme.get('color', 'color_action_bar'))
color_body_program = \
    get_color_from_hex(config_theme.get('color', 'color_body_program'))
list_color = \
    get_color_from_hex(config_theme.get('color', 'list_color'))

text_color = config_theme.get('color', 'text_color')
underline_rst_color = config_theme.get('color', 'underline_rst_color')
text_key_color = config_theme.get('color', 'text_key_color')
text_link_color = config_theme.get('color', 'text_link_color')

try:  # устанавливаем языковую локализацию
    if not PY2:
        exec(
            open('{}/data/language/{}.txt'.format(
                prog_path, language), encoding='utf-8-sig').read()
        )
    else:
        exec(
            open('{}/data/language/{}.txt'.format(prog_path, language)).read()
        )
except Exception:
    raise Exception(traceback.format_exc())

dict_language = {
    string_lang_on_russian: 'russian',
    string_lang_on_english: 'english'
}
