import Image

image = Image.open("lolcopter.png")
pixeldata = list(image.getdata())
lolBool = False
counter = -1
for pixel in pixeldata:
	if not lolBool and pixel[3] in (250,251):
		lolBool = True
		alternator = pixel[3]
	if lolBool and pixel[3] in (250,251):
		counter += 1
		if pixel[3] != alternator:
			print chr(counter),
			alternator = pixel[3]
			
			counter = 0
image.close()

