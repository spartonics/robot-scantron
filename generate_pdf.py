#!/usr/bin/env python2

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Scantron:
    def __init__(self, filename, spacing=0.2):
        self._fontSize = 0.15*inch

        self._canvas = canvas.Canvas(filename, pagesize=letter)
        self._canvas.setFontSize(self._fontSize)

        self._y = 1 * inch
        self._spacing = spacing * inch

    def _to_y(self, y):
        return 11*inch - y


    def drawBox(self, x, y, label='', length=0.4*inch):
        offset = (length - self._fontSize) / 2
        self._canvas.drawCentredString(x + length / 2, self._to_y(y), label)
        self._canvas.rect(x, self._to_y(y + offset), length, length, stroke=1, 
                fill=0)


    def drawText(self, x, y, text=''):
        self._canvas.drawString(x, self._to_y(self._y), text)


    def drawBoolean(self, x, label="UNKNOWN", spacing=0.4):
        x = x * inch
        y = self._y

        yes_x = x + 2*inch
        yes_y = y

        no_x = x + (2.0 + spacing) * inch
        no_y = y

        self.drawText(x, y, label)
        self.drawBox(yes_x, yes_y, label='Y')
        self.drawBox(no_x, no_y, label='N')

        self._y += self._spacing


    def drawInteger(self, x, label="UNKNOWN", spacing=0.4):
        x = x * inch
        y = self._y

        self.drawText(x, y, label)

        for i in range(10):
            self.drawBox(x + (2 + i * spacing) * inch, y, label='%d' % i)

        self._y += self._spacing


    def drawQR(self, x, y, data):
        pass


    def moveBy(self, inches):
        self._y += inches * inch


    def save(self):
        self._canvas.save()


class Field:
    def __init__(self, name, label, fieldType):
        self.name = name
        self.label = label
        self.fieldType = fieldType

data = [
        Field('auton_high', 'Auton High', int),
        Field('auton_mid', 'Auton Mid', int),
        Field('auton_low', 'Auton Low', int),
        Field('high', 'High', int),
        Field('mid', 'Mid', int),
        Field('low', 'Low', int),
        Field('pyramid', 'Pyramid', int),
        Field('missed', 'Missed', int),
        Field('fouls', 'Fouls', int),
        Field('tech_fouls', 'Tech fouls', int),
        Field('defense', 'Defense', bool),
        Field('pickup', 'Pickup', bool),
        Field('noshow', 'Noshow', bool),
        Field('brokedown', 'Brokedown', bool),
        Field('dq', 'DQ', bool),
]


scantron = Scantron('form.pdf', spacing=0.5)
scantron.drawText(1*inch, 1*inch, 'Scouting Sheet')
scantron.moveBy(0.5)
scantron.drawInteger(1, '1000')
scantron.drawInteger(1, '100')
scantron.drawInteger(1, '10')
scantron.drawInteger(1, '1')
for field in data:
    if field.fieldType == int:
        scantron.drawInteger(1, field.label)
    elif field.fieldType == bool:
        scantron.drawBoolean(1, field.label)
scantron.save()
