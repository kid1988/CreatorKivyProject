#! /usr/bin/python3.4
# -*- coding: utf-8 -*-

'''
loadplugin.py
+++++++++++++++++++++++++++++++++++

Класс, описывающий манифест загружаемого плагина.

:Автор: Virtuos86

'''

__version__ = '0.0.1'


class Manifest(object):
    def __init__(self, filename=None):
        self.fields = {}
        if filename is not None:
            self.load(filename)

    def parse(self, data):
        lines = data.splitlines()
        lines.reverse()
        self.fields = {}

        while True:
            try:
                ln = lines.pop()
            except IndexError:
                break
            try:
                p = ln.index(':')
            except ValueError:
                raise ValueError('mangled manifest file')
            name = ln[:p].strip().title()
            value = []
            vln = ln[(p + 1):].strip()

            while vln.endswith('\\'):
                value.append(vln[:-1].strip())
                try:
                    ln = lines.pop()
                except IndexError:
                    break
                vln = ln.strip()
            else:
                value.append(vln)

            if name in self.fields:
                raise ValueError('manifest field defined twice')
            self.fields[name] = '\r\n'.join(value)

    def dump(self):
        lines = []
        for (name, value,) in self.fields.items():
            lines.append(('%s: %s\r\n' % (
                name.title(), '\\\r\n'.join(value.split('\n')))))

        # return ''.join(lines).encode('utf8')
        return ''.join(lines)

    def load(self, filename):
        f = open(filename, 'r')
        try:
            self.parse(f.read())
        finally:
            f.close()

    def save(self, filename):
        f = open(filename, 'w')
        try:
            f.write(self.dump())
        finally:
            f.close()

    def get(self, name, default=None):
        return self.fields.get(name.title(), default)

    def keys(self):
        return self.fields.keys()

    def items(self):
        return self.fields.items()

    def values(self):
        return self.fields.values()

    def clear(self):
        self.fields = {}

    def __getitem__(self, name):
        return self.fields[name.title()]

    def __setitem__(self, name, value):
        self.fields[name.title()] = value

    def __delitem__(self, name):
        del self.fields[name.title()]

    def __len__(self):
        return len(self.fields)

    def __contains__(self, name):
        return name.title() in self.fields
