# coding: utf-8

from __future__ import unicode_literals

import platform

import cv2
import tkFileDialog

from Tkconstants import ACTIVE, BOTH, DISABLED
from Tkinter import Button, Frame, Tk


class ImageCorrelationWindow(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.title('Image Correlation')
        self.iconbitmap('')
        ImageCorrelationFrame()

        self.mainloop()


class ImageCorrelationFrame(Frame):

    def __init__(self):
        Frame.__init__(self)

        buttons_config = [{
            'text': 'Выбрать исходное изображение',
            'command': lambda: self.get_img_name('base_img')
        }, {
            'text': 'Выбрать изображение для поиска',
            'command': lambda: self.get_img_name('sub_img')
        }, {
            'text': 'Поиск',
            'command': lambda: self.image_correlation,
            'name': 'correlation_btn',
            'state': DISABLED
        }]

        for cfg in buttons_config:
            Button(self, **cfg).pack(fill=BOTH, padx=5, pady=5)

        self.pack()

    def get_img_name(self, img_type):
        file_options = {
            'defaultextension': '.jpg',
            'filetypes': [('jpg files', '.jpg'), ('PNG files', '.png')],
            'initialdir': 'C:\\' if platform.system() == 'Windows' else '~',
            'title': 'Выберите исходное изображение'
        }
        setattr(self, img_type, tkFileDialog.askopenfilename(**file_options))
        self.try_to_activate_correlation_btn()

    def image_correlation(self):
        pass

    def try_to_activate_correlation_btn(self):
        try:
            base_img = self.base_img
            sub_img = self.sub_img
        except AttributeError:
            pass
        else:
            self.correlation_btn.config(state=ACTIVE)

    @property
    def correlation_btn(self):
        return filter(lambda x: 'correlation_btn' in x.winfo_name(), self.winfo_children())[0]


if __name__ == '__main__':
    ImageCorrelationWindow()
