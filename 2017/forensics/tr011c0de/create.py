import Image

image = Image.open("lol.jpg").convert('RGBA')
pixeldata = list(image.getdata())
pixeldata = pixeldata[:]
flagString = 'hackgt{iM_w0ke_aF}'
alternator = 250
counter = 0
for i in range(0, len(flagString)):
	for j in range(0, ord(flagString[i])):
		pixeldata[12345 + counter] = list(pixeldata[12345 + counter])
		pixeldata[12345 + counter][3] = alternator
		pixeldata[12345 + counter] = tuple(pixeldata[12345 + counter])
		counter += 1
	alternator = 250 if alternator == 251 else 251
image.putdata(pixeldata)
image.save("lolcopter.png")
