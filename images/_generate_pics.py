import os

from glob import glob

from PIL import Image
import numpy as np


def generate_pic(filename):
    top = 5
    height = 272
    left = 5
    width = 315

    im = Image.open(filename)
    d = np.asarray(im)
    d = d[top:height, left:width]

    return Image.fromarray(d)


for f in glob('*.png'):
    if f.endswith('_gray.png') or f.endswith('_pic.png'):
        continue

    filename = f.replace('.png', '_pic.png')
    if os.path.isfile(filename):
        continue

    pic = generate_pic(f)
    pic.show()

    pic.save(filename)



