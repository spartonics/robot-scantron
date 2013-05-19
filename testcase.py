#!/usr/bin/env python2

from scantron import *
import PythonMagick
from pyPdf import PdfFileReader
from PIL import Image

data = [
    Field('foo', 'Foo foo foo', int),
    Field('bar', 'Bar bar bar', int),
    Field('baz', 'Baz baz baz', int),
    Field('laber', 'Laber laber', bool),
]

# Generate PDF
st = Scantron('test.pdf')
st.set_box_sizes(box_size=0.2*inch, box_spacing=0.3*inch)
st.populate(data, matches=1, collate='no')
st.save()

# Convert PDF to a series of pictures
pages = []

pdf = PdfFileReader(file('test.pdf', 'rb'))

for page in range(pdf.getNumPages()):
    #page += 1
    name = 'test_image_%d.png' % page

    im = PythonMagick.Image()
    im.density('200')
    im.read('test.pdf[%d]' % page)
    im.write(name)

    pages.append(name)

# Create a series of transformations to apply
transformations = [
    lambda x: x.rotate(10, expand=False),
    lambda x: x.rotate(-10, expand=False),
]

tf = 0

# Take all pictures and modify them in different ways
for page in pages:
    im = Image.open(page).convert('L')
    im = transformations[tf](im)
    im.save(page)

    tf = (tf + 1) % len(transformations)
