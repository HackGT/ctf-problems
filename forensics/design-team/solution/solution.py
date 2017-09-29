from PIL import Image
import numpy

height = 851
width = 315
f = open('asset.png').readlines()
img = Image.new("RGB", (height, width), "white")
img_data = []
counter = 0
for line in f:
  a = line.split('+')
  b = [x.split('x')[0].strip() for x in a]
  poly = numpy.poly1d(b)
  img_data.append(tuple(int(round(r)) for r in poly.r)[::-1])
  counter += 1
  print counter
img.putdata(img_data)
img.save('flag.png')