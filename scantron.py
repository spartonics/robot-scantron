#!/usr/bin/env python2

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Scantron:
    def __init__(self, filename, spacing=0.3*inch):
        self._fontSize = 0.15*inch

        self._canvas = canvas.Canvas(filename, pagesize=letter)
        self._canvas.setFontSize(self._fontSize)

        self._y = 1 * inch
        self._spacing = spacing
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
        self._canvas.rect(x, self._to_y(y), size, size, stroke=1, 
                fill=int(filled))


    def draw_text(self, x, y, text=''):
        self._canvas.drawString(x, self._to_y(y), text)


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


    def draw_qr(self, x, y, data):
        pass


    def adjust_y(self, delta_y):
        self._y += delta_y


    def set_box_sizes(self, box_size, box_spacing):
        self._bsize = box_size
        self._bspacing = box_spacing


    def populate(self, data):
        # Draw boxes for determining boundaries
        self.draw_box(1*inch, 1*inch, size=0.4*inch, filled=True)
        self.draw_box((7-0.4)*inch, (10-0.4)*inch, size=0.4*inch, filled=True)

        # Draw a sheet title
        self.draw_text(2*inch, 1*inch, 'Spartonics 1503')
        self.draw_text(2*inch, 1.4*inch, 'Scouting Sheet')
        self.adjust_y(1.0*inch)

        # Create the bubbles for the team number
        self.draw_integer('1000')
        self.draw_integer('100')
        self.draw_integer('10')
        self.draw_integer('1')

        # Create the remainder of the sheet
        for field in data:
            if field.fieldType == int:
                self.draw_integer(field.label)
            elif field.fieldType == bool:
                self.draw_boolean(field.label)


    def save(self):
        self._canvas.save()


class Field:
    def __init__(self, name, label, fieldType):
        self.name = name
        self.label = label
        self.fieldType = fieldType
