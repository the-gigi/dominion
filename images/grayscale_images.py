import os

from PIL import Image, ImageOps

from glob import glob


for f in glob('*.jpg'):
    if f.endswith('_gray.jpg'):
        continue

    img = Image.open(f).convert('LA')
    new_filename = f.replace('.jpg', '_gray.jpg')
    if os.path.exists(new_filename):\
        continue
    img2 = ImageOps.grayscale(img)
    img2.show()
    img2.save(new_filename)