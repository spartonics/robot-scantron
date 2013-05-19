#!/usr/bin/env python2

from scantron import ScantronGenerator, ScantronField, inch
import PythonMagick
from pyPdf import PdfFileReader
from PIL import Image

test_data = [
    ScantronField('foo', 'Foo foo foo', int),
    ScantronField('bar', 'Bar bar bar', int),
    ScantronField('baz', 'Baz baz baz', int),
    ScantronField('laber', 'Laber laber', bool),
]

# Generate scantron PDF
pdf = ScantronGenerator('test.pdf')
pdf.set_box_sizes(box_size=0.2*inch, box_spacing=0.3*inch)
pdf.populate(test_data, matches=1, collate='no')
pdf.save()

# Convert PDF to a series of pictures
pages = []

pdf = PdfFileReader(file('test.pdf', 'rb'))
num_pages = pdf.getNumPages()

for page in range(num_pages):
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
