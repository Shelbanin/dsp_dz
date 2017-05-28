# coding: utf-8

from __future__ import unicode_literals

import platform

import cv2
import numpy as np
import tkFileDialog

from Tkconstants import ACTIVE, BOTH, DISABLED
from Tkinter import Button, Frame, Tk


class ImageCorrelationWindow(Tk):

    def __init__(self):
        Tk.__init__(self)

        self.title('Image Correlation')
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
            'command': self.image_correlation,
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
            'initialdir': 'D:\\' if platform.system() == 'Windows' else '~',
            'title': 'Выберите исходное изображение'
        }
        setattr(self, img_type, tkFileDialog.askopenfilename(**file_options))
        self.try_to_activate_correlation_btn()

    def image_correlation(self):
        ImageCorrelationProcessor(self.base_img, self.sub_img)

    def try_to_activate_correlation_btn(self):
        try:
            self.base_img
            self.sub_img
        except AttributeError:
            pass
        else:
            self.correlation_btn.config(state=ACTIVE)

    @property
    def correlation_btn(self):
        return filter(lambda x: 'correlation_btn' in x.winfo_name(), self.winfo_children())[0]


class ImageCorrelationProcessor:

    NAME = 'Images correlation'

    IS_COLOR_IMG = False
    H_POS = 0
    W_POS = 1

    def __init__(self, base_img_path, sub_img_path, process_now=True):
        self.base_img_path, self.sub_img_path = base_img_path, sub_img_path

        if process_now:
            self.process_images()

    def process_images(self):
        base_img_path, sub_img_path = self.base_img_path, self.sub_img_path

        base_img = cv2.imread(base_img_path, self.IS_COLOR_IMG)
        base_img_height = base_img.shape[self.H_POS]
        base_img_width = base_img.shape[self.W_POS]

        sub_img = cv2.imread(sub_img_path, self.IS_COLOR_IMG)
        sub_img_height = sub_img.shape[self.H_POS]
        sub_img_width = sub_img.shape[self.W_POS]

        height_delta = base_img_height - sub_img_height
        width_delta = base_img_width - sub_img_width

        values = np.zeros((height_delta, width_delta))

        for h in range(height_delta):
            for w in range(width_delta):
                corr = values[h][w]
                for i in range(sub_img_height):
                    for j in range(sub_img_width):
                        h_offset = h + i
                        w_offset = w + j
                        corr = corr + (sub_img[i][j] - base_img[h_offset][w_offset]) ** 2

                values[h][w] = corr

        left_top_point = cv2.minMaxLoc(values)[2]
        bottom_right = left_top_point[0] + sub_img_width, left_top_point[1] + sub_img_height
        cv2.rectangle(base_img, left_top_point, bottom_right, (255, 0, 0))

        cv2.namedWindow(self.NAME, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.NAME, base_img_width, base_img_height)
        cv2.imshow(self.NAME, base_img)
        cv2.waitKey()


if __name__ == '__main__':
    ImageCorrelationWindow()
