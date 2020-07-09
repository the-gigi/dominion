import os
from glob import glob

from PIL import Image
import numpy as np


def crop(filename):
    im = Image.open(filename)
    d = np.asarray(im)

    n_rows, n_cols = d.shape[:2]
    print(n_rows, n_cols)

    rows = [[x[:3] for x in d[i]] for i in range(n_rows)]
    cols = [[x[:3] for x in d[:, i]] for i in range(n_cols)]

    row_averages = [sum(sum(x) for x in row) for row in rows]
    col_averages = [sum(sum(x) for x in col) for col in cols]

    threshold_value = 10
    row_threshold = threshold_value * 3 * n_cols
    col_threshold = threshold_value * 3 * n_rows

    first_row = 0
    while row_averages[first_row] > row_threshold:
        first_row += 1

    last_row = n_rows - 1
    while row_averages[last_row] > row_threshold:
        last_row -= 1

    first_col = 0
    while col_averages[first_col] > col_threshold:
        first_col += 1

    last_col = n_cols - 1
    while col_averages[last_col] > col_threshold:
        last_col -= 1

    new_d = d[first_row:last_row, first_col:last_col]
    return Image.fromarray(new_d)


def main():
    """ """
    for f in glob('*_screenshot.png'):
        filename = f.replace('_screenshot', '')
        if os.path.isfile(filename):
            continue
        im = crop(f)
        im.show()
        im.save(filename)

    print('done.')


if __name__ == '__main__':
    main()
