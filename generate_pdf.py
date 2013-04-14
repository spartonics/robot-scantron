#!/usr/bin/env python2

from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def ty(y):
    return 11*inch - y

def drawBoolean(c, x, y, label="UNKNOWN"):
    x = x * inch
    y = y * inch

    yes_x = x + 2*inch
    yes_y = y

    no_x = x + 2.2*inch
    no_y = y

    box_length = 0.2*inch

    c.drawString(x, ty(y), label)
    c.drawString(yes_x, ty(yes_y), 'Y')
    c.drawString(no_x, ty(no_y), 'N')

    c.rect(yes_x, ty(yes_y), box_length, box_length, stroke=1, fill=0)

canvas = canvas.Canvas('form.pdf', pagesize=letter)

drawBoolean(canvas, 2, 2, 'Broke Down')
drawBoolean(canvas, 2, 2+0.2, 'Disqualified')

canvas.save()
