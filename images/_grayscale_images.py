import os

from PIL import Image, ImageOps

from glob import glob

for ext in 'png jpg'.split():
    for f in glob(f'*.{ext}'):
        if f.endswith(f'_gray.{ext}'):
            continue

        img = Image.open(f).convert('LA')
        new_filename = f.replace(f'.{ext}', f'_gray.{ext}')
        if os.path.exists(new_filename):
            continue
        img2 = ImageOps.grayscale(img)
        img2.show()
        img2.save(new_filename)