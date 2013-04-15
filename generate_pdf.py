#!/usr/bin/env python2

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def ty(y):
    return 11*inch - y

def drawBox(c, x, y, label='', length=0.4*inch):
    offset = (length - fontSize) / 2
    c.drawCentredString(x + length / 2, ty(y), label)
    c.rect(x, ty(y + offset), length, length, stroke=1, fill=0)

def drawBoolean(c, x, y, label="UNKNOWN", spacing=0.4):
    x = x * inch
    y = y * inch

    yes_x = x + 2*inch
    yes_y = y

    no_x = x + (2.0 + spacing) * inch
    no_y = y

    c.drawString(x, ty(y), label)

    drawBox(c, yes_x, yes_y, label='Y')
    drawBox(c, no_x, no_y, label='N')

def drawInteger(c, x, y, label="UNKNOWN", spacing=0.4):
    x = x * inch
    y = y * inch

    c.drawString(x, ty(y), label)

    for i in range(10):
        drawBox(c, x + (2 + i * spacing) * inch, y, label='%d' % i)

fontSize = 0.15 * inch

canvas = canvas.Canvas('form.pdf', pagesize=letter)
canvas.setFontSize(fontSize)

drawBoolean(canvas, 1, 2, 'Broke Down')
drawBoolean(canvas, 1, 2+0.2, 'Disqualified')
drawInteger(canvas, 1, 2+0.4, 'Pyramid')

canvas.save()
