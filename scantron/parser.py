#!/usr/bin/env python2

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
