import os
from glob import glob

from PIL import Image
import numpy as np


def generate_pic(filename):
    top = 5
    bottom = 272
    left = 5
    width = 315

    top2 = 440
    bottom2 = 500

    im = Image.open(filename)
    d = np.asarray(im)
    d1 = d[top:bottom, left:width]
    d2 = d[top2:bottom2, left:width]
    dd = np.vstack((d1, d2))
    return Image.fromarray(dd)


def main():
    files = glob('*.jpg')
    for f in files:
        if f.endswith('_gray.jpg') or f.endswith('_pic.jpg'):
            continue

        filename = f.replace('.jpg', '_pic.jpg')
        if os.path.isfile(filename):
            continue

        pic = generate_pic(f)
        pic.show()

        pic.save(filename)


def show_pics():
    for f in glob('*_pic.jpg'):
        im = Image.open(f)
        im.show()


def convert_png_to_jpg():
    files = glob('*.png')
    for f in files:
        im = Image.open(f)
        im.load()
        background = Image.new("RGB", im.size, (255, 255, 255))
        try:
            background.paste(im, mask=im.split()[3])  # 3 is the alpha channel
        except:
            background = im
            background.convert('RGB')
        background.save(f.replace('.png', '.jpg'), 'JPEG', quality=80)

if __name__ == '__main__':
    #show_pics()
    #convert_png_to_jpg()
    main()
