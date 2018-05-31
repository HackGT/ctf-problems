from PIL import Image

import numpy

img = Image.open('lmao.png')

pix = img.load()
width = img.size[0]
height = img.size[1]
for i in range(0, height):
  for j in range(0, width):
    arr = pix[j, i][:-1]
    poly = numpy.poly1d(arr, True)
    print "{0}x^3 + {1}x^2 + {2}x + {3}".format(poly[3], poly[2], poly[1], poly[0])