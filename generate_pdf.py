#!/usr/bin/env python2

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Scantron:
    def __init__(self, filename):
        self._fontSize = 0.15*inch

        self._canvas = canvas.Canvas(filename, pagesize=letter)
        self._canvas.setFontSize(self._fontSize)


    def _y(self, y):
        return 11*inch - y


    def drawBox(self, x, y, label='', length=0.4*inch):
        offset = (length - self._fontSize) / 2
        self._canvas.drawCentredString(x + length / 2, self._y(y), label)
        self._canvas.rect(x, self._y(y + offset), length, length, stroke=1, 
                fill=0)


    def drawText(self, x, y, text=''):
        self._canvas.drawString(x, self._y(y), text)


    def drawBoolean(self, x, y, label="UNKNOWN", spacing=0.4):
        x = x * inch
        y = y * inch

        yes_x = x + 2*inch
        yes_y = y

        no_x = x + (2.0 + spacing) * inch
        no_y = y

        self.drawText(x, y, label)
        self.drawBox(yes_x, yes_y, label='Y')
        self.drawBox(no_x, no_y, label='N')


    def drawInteger(self, x, y, label="UNKNOWN", spacing=0.4):
        x = x * inch
        y = y * inch

        self.drawText(x, y, label)

        for i in range(10):
            self.drawBox(x + (2 + i * spacing) * inch, y, label='%d' % i)


    def save(self):
        self._canvas.save()


scantron = Scantron('form.pdf')
scantron.drawBoolean(1, 2, 'Broke Down')
scantron.drawBoolean(1, 2+0.2, 'Disqualified')
scantron.drawInteger(1, 2+0.4, 'Pyramid')
scantron.save()
