#! /usr/bin/python3.4
# -*- coding: utf-8 -*-
#
# main.py
#
# Точка входа в приложение. Запускает основной программный код program.py.
# В случае ошибки, выводит на экран окно с ее текстом.
#

import os
import sys
import shutil
import argparse

try:
    from kivy.logger import Logger
except Exception:
    import traceback
    raise(traceback.format_exc())

__version__ = '0.1.1'

if len(sys.argv) <= 1:
    Logger.warning('''
Используйте скрипт со строковыми аргументами:

'name' - Имя проекта
'path' - Директория проекта
'repo' - Адресс репозитория на GitHub (необязательный параметр)
'autor' - Имя автора проекта (необязательный параметр)
'mail' - Почта автора проекта (необязательный параметр)
''')
    sys.exit(0)

prog_path = os.path.split(os.path.abspath(sys.argv[0]))[0]
# sys.dont_write_bytecode = True

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, help='Имя проекта')
parser.add_argument('path', type=str, help='Директория проекта')
parser.add_argument('-repo', type=str, help='Адресс репозитория на GitHub')
parser.add_argument('-autor', type=str, help='Имя автора проекта')
parser.add_argument('-mail', type=str, help='Почта автора проекта')

name_project = parser.parse_args().name
dir_project = parser.parse_args().path
repo_project = parser.parse_args().repo
name_autor = parser.parse_args().autor
address_mail = parser.parse_args().mail

full_path_to_project = '{}/{}'.format(dir_project, name_project)
dir_language = '{}/data/language'.format(full_path_to_project)
dir_settings = '{}/data/settings'.format(full_path_to_project)
dir_license = '{}/license'.format(full_path_to_project)

Logger.info('Creator Kivy Project version {} ...\n'.format(__version__))

if os.path.exists(full_path_to_project):
    Logger.error('Проект {} уже существует!'.format(name_project))
    sys.exit(0)

try:
    for directory in [full_path_to_project, dir_language, dir_settings]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            Logger.info('Создана директория проекта {} ...'.format(directory))
except FileNotFoundError:
    Logger.error('Указанная директория {} не существует!'.format(dir_project))
except PermissionError:
    Logger.error(
        'У вас нет прав для создания проекта в директории {}!'.format(
            dir_project
        )
    )
try:
    Logger.info('Создание точки входа main.py ...')
    open('{}/main.py'.format(full_path_to_project), 'w').write(
        open('{}/data/files/main'.format(prog_path)).read() % repo_project)

    Logger.info('Создание файла языковой локализации russian.txt ...')
    open('{}/russian.txt'.format(dir_language), 'w').write(
        open('{}/data/files/russian'.format(prog_path)).read().format(
            NAME_PROJECT=name_project,
            REPOSITORY=repo_project,
            MAIL=address_mail
        )
    )

    Logger.info('Создание файла README.md ...')
    open('{}/README.md'.format(full_path_to_project), 'w').write('')

    data = {
        '{}/program.py'.format(full_path_to_project):
            'Создание файла программного кода program.py ...',
        '{}/data/settings/general.json'.format(full_path_to_project):
            'Создание файла настроек general.json ...'
    }
    for file in data.keys():
        Logger.info(data[file])
        open(file, 'w').write(open('{}/data/files/{}'.format(
            prog_path, os.path.splitext(os.path.split(file)[1])[0])).read())

    Logger.info('Копирование файлов проекта ...')
    for directory in ['{}/libs', '{}/data/images', '{}/data/themes']:
        shutil.copytree(directory.format(prog_path),
                        directory.format(full_path_to_project))

    Logger.info('Создание файлов лицензии ...')
    os.mkdir(dir_license)
    for file_license in ['license_english.rst', 'license_russian.rst']:
        open('{}/license/{}'.format(
            full_path_to_project, file_license),'w').write(
            open('{}/data/files/{}'.format(
                prog_path, file_license)).read().format(COPYRIGHT=name_autor))
    shutil.copy(
        '{}/data/files/open-source-logo.png'.format(prog_path),
        '{}/open-source-logo.png'.format(dir_license)
    )

    Logger.info('Создание файла README.rst для плагина button ...')
    open('{}/libs/plugins/button/README.rst'.format(full_path_to_project),
         'w').write(
        open('{}/data/files/README.rst'.format(prog_path)).read()
    )
except FileNotFoundError as exc:
    Logger.error('Не могу найти файл проекта - {}'.format(exc))
    shutil.rmtree(full_path_to_project)
    sys.exit(0)
except Exception as exc:
    Logger.error('Неизвестная ошибка - {}'.format(exc))
    shutil.rmtree(full_path_to_project)
    sys.exit(0)

Logger.info('')
Logger.info('Проект {} успешно создан!'.format(name_project))
