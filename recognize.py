from __future__ import print_function
from datetime import datetime as dt
import cv2
import numpy as np
from crop import crop
from scan import scan
import pytesseract
from PIL import Image
import argparse
from test_accuracy import test_accuracy


def recognize(imgname='photos\\tough6.jpg', output='output.txt', desired='texts\\chom_tough.txt',
              show_intermediate_results=False):
    scan(imgname, show_intermediate_results)
    img = cv2.imread('deskewed.jpg')
    img = cv2.dilate(img, np.ones((2, 2)))
    newimgname = 'no_noise.jpg'
    cv2.imwrite(newimgname, img)
    crop(newimgname, "scan_res.jpg", show_intermediate_results)
    a = pytesseract.image_to_string(Image.open('scan_res.jpg'), config="config")
    f = open(output, 'w+')
    print(a, file=f)
    f.flush()
    f.close()
    print('Accuracy: ' + str(test_accuracy(scan_res=output, desired=desired)))


def recognize_many(img_names_file,
                   out='output/' + str(dt.now()).replace(':', '-')[:16]):
    with open(out + img_names_file) as f:
        names = f.readlines()
    names = [x.strip() for x in names]
    for name in names:
        output = name + 'output.txt'
        desired = 'chom.txt'
        if 'tough' in name:
            desired = 'chom_tough.txt'
        elif 'bad' in name:
            desired = 'bad.txt'
        elif 'ital' in name:
            desired = 'ital.txt'
        elif 'font1' in name:
            desired = 'font1.txt'
        elif 'font2' in name:
            desired = 'font2.txt'
        desired = 'texts\\' + desired
        print('\n' + name)
        recognize(name, output, desired)


# recognize_many('photos.txt')
# recognize('photos\\tough6.jpg')

if __name__ == '__main__':
    # example usage:
    #python .\recognize.py -i photos\chom4.jpg -c texts\chom.txt -o output.txt
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="Path to the image to be scanned")
    ap.add_argument("-o", "--output", required=True,
                    help="Path for the output text file")
    ap.add_argument("-c", "--check", required=True,
                    help="Path to the file with reference text")
    ap.add_argument("-s", "--show", required=False,
                    help="Show intermediate results", dest='show', action='store_true')
    args = vars(ap.parse_args())
    recognize(imgname=args['image'],
              output=args['output'],
              desired=args['check'],
              show_intermediate_results=args['show'])
