'''
Copyright (c) 2018-2019 p4a-build-spaces team and others, see AUTHORS.md

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import json
import os

class SettingsStore(object):
    UNSPECIFIED_DEFAULT = object()

    @staticmethod
    def settings_folder():
        folder_path = os.path.join(
            os.path.expanduser("~"),
            ".local", "share", "p4a-build-spaces")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path

    def get_store(self):
        settings_file = os.path.join(
            self.__class__.settings_folder(),
            "settings.json")
        if not os.path.exists(settings_file):
            return dict()
        with open(settings_file, "r", encoding="utf-8") as f:
            return json.loads(f.read().strip())

    def set_store(self, dictionary):
        settings_file = os.path.join(
            self.__class__.settings_folder(),
            "settings.json")
        serialized = json.dumps(dictionary)
        with open(settings_file, "w", encoding="utf-8") as f:
            f.write(serialized)

    def get(self, value, default=UNSPECIFIED_DEFAULT,
            type=object):
        store = self.get_store()
        if type == dict and default == self.__class__.UNSPECIFIED_DEFAULT:
            default = dict()
        elif type == float and default == self.__class__.UNSPECIFIED_DEFAULT:
            default = 0.0
        elif type == int and default == self.__class__.UNSPECIFIED_DEFAULT:
            default = 0
        elif default == self.__class__.UNSPECIFIED_DEFAULT:
            default = None
        if value in store:
            return store[value]
        return default

    def set(self, value_name, value):
        store = self.get_store()
        store[value_name] = value
        self.set_store(store)

settings = SettingsStore()


