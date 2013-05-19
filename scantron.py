#!/usr/bin/env python2

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from qrcode import *

import numpy as np
import scipy as sp
from scipy import ndimage
from PIL import Image, ImageDraw
import math


class ScantronParser:
    def __init__(self):
        pass


    def scan(self, data, path):
        img = Image.open(path).convert('RGB')
        im = sp.misc.fromimage(img, flatten=True)
        im = np.where(im > 128, 0, 1)
        label_im, num = ndimage.label(im, structure=np.ones((3, 3)).tolist())
        centroids = ndimage.measurements.center_of_mass(im, label_im, xrange(1, 
                num+1))
        slices = ndimage.find_objects(label_im)

        squares = []

        for i in range(len(slices)):
            sub_img = np.where(label_im[slices[i]] == i + 1, 1, 0)
            num_ones = np.sum(sub_img)
            num_all = sub_img.size
            shape = sub_img.shape

            ratio = float(shape[0]) / float(shape[1])
            darkness = float(num_ones)/float(num_all)

            if darkness > 0.95 and abs(ratio - 1.0) < 0.1 and shape[0] > 14:
                x1, x2 = slices[i][1].start, slices[i][1].stop
                y1, y2 = slices[i][0].start, slices[i][0].stop

                draw = ImageDraw.Draw(img)
                draw.rectangle([x1, y1, x2, y2], outline='blue')
                del draw

                squares.append(i)

        if len(squares) != 3:
            print('Could not uniquely identify the three page markers.')
            raise Exception

        squares = zip(squares, map(lambda s: sum(centroids[s]), squares))
        squares = sorted(squares, key=lambda x: x[1])

        for s in squares:
            print('square ' + str(s))

        tl = centroids[squares[0][0]]
        bl = centroids[squares[1][0]]
        br = centroids[squares[2][0]]

        rotation = math.atan2(bl[1] - tl[1], bl[0] - tl[0])
        print('rotation: ' + str(rotation))


class Scantron:
    def __init__(self, filename, spacing=0.3*inch):
        self._fontSize = 0.15*inch

        self._canvas = canvas.Canvas(filename, pagesize=letter)
        self._canvas.setFontSize(self._fontSize)
        self._reset_values()
        self._spacing = spacing


    def _reset_values(self):
        self._y = 1 * inch
        self._bsize = 0.2*inch
        self._bspacing = 0.3*inch


    def _to_y(self, y):
        return 11*inch - y


    def draw_box(self, x, y, size=0, label='', filled=False):
        if size == 0:
            size = self._bsize

        offset = (size - self._fontSize) / 2

        if label != '':
            self._canvas.drawCentredString(x + size / 2, self._to_y(y), label)

        y += offset
        if filled:
            self._canvas.rect(x, self._to_y(y), size, size, stroke=0, fill=1)
        else:
            self._canvas.rect(x, self._to_y(y), size, size, stroke=1, fill=0)


    def draw_text(self, x, y, text='', size=0):
        if size != 0:
            self._canvas.setFontSize(size)

        self._canvas.drawString(x, self._to_y(y), text)
        self._canvas.setFontSize(self._fontSize)


    def draw_boolean(self, label="UNKNOWN", x=1*inch):
        x = x
        y = self._y

        self.draw_text(x, y, label)
        self.draw_box(x + 2*inch, y, label='Y')
        self.draw_box(x + 2*inch + self._bspacing, y, label='N')

        self._y += self._spacing


    def draw_integer(self, label="UNKNOWN", x=1*inch):
        y = self._y

        self.draw_text(x, y, label)
        x += 2 * inch

        for i in range(10):
            self.draw_box(x, y, label='%d' % i)
            x += self._bspacing

        self._y += self._spacing


    def draw_qr(self, x, y, data, unit_size=0.03*inch):
        qr = QRCode(version=2, error_correction=ERROR_CORRECT_L)
        qr.add_data(data)
        qr.make()

        qr_x = x
        qr_y = y

        for row in qr.modules:
            for col in row:
                if col:
                    self.draw_box(qr_x, qr_y, size=unit_size, filled=True)
                qr_x += unit_size

            qr_x = x
            qr_y += unit_size


    def adjust_y(self, delta_y):
        self._y += delta_y


    def set_box_sizes(self, box_size, box_spacing):
        self._bsize = box_size
        self._bspacing = box_spacing


    def add_sheet(self, data, match=1, position=1):
        # Draw boxes for determining boundaries
        self.draw_box(1*inch, 1.2*inch, size=0.4*inch, filled=True)
        self.draw_box(1*inch, (10.2-0.4)*inch, size=0.4*inch, filled=True)
        self.draw_box((7.5-0.4)*inch, (10.2-0.4)*inch, size=0.4*inch, 
                filled=True)

        # Draw the QR code containing match and position
        self.draw_qr(6.5*inch, 1.1*inch, '%d:%d' % (match, position))

        # Draw a sheet title
        position_str = [
            'Red 1',
            'Red 2',
            'Red 3',
            'Blue 1',
            'Blue 2',
            'Blue 3',
        ][position - 1]
        self.draw_text(2*inch, 1.2*inch, 'Spartonics 1503', size=0.3*inch)
        self.draw_text(2*inch, 1.6*inch, 'Scouting Sheet', size=0.3*inch)
        self.draw_text(1*inch, 2.0*inch, 'Team ___________')
        self.draw_text(3*inch, 2.0*inch, 'Match %d %s' % (match, position_str))
        self.adjust_y(1.5*inch)

        # Create the bubbles for the team number
        self.draw_integer('1000')
        self.draw_integer('100')
        self.draw_integer('10')
        self.draw_integer('1')
        self.adjust_y(0.2*inch)

        # Create the remainder of the sheet
        for field in data:
            if field.fieldType == int:
                self.draw_integer(field.label)
            elif field.fieldType == bool:
                self.draw_boolean(field.label)


    def populate(self, data, matches=1, collate='on'):
        if collate == 'on':
            for match in range(1, matches + 1):
                for position in range(1, 7):
                    self.add_sheet(data, match, position)
                    self._canvas.showPage()
                    self._reset_values()
        else:
            for position in range(1, 7):
                for match in range(1, matches + 1):
                    self.add_sheet(data, match, position)
                    self._canvas.showPage()
                    self._reset_values()


    def save(self):
        self._canvas.save()


class Field:
    def __init__(self, name, label, fieldType):
        self.name = name
        self.label = label
        self.fieldType = fieldType
