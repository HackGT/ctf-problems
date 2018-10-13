import struct

def conv(r, g, b):
    r /= 255.0
    g /= 255.0
    b /= 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    if delta == 0:
        h = 0
    elif cmax == r:
        h = int(60 * (((g - b) / delta) % 6))
    elif cmax == g:
        h = int(60 * (((b - r) / delta) + 2))
    else:
        h = int(60 * (((r - g) / delta) + 4))

    if cmax == 0:
        s = 0
    else:
        s = delta / cmax

    v = cmax

    h = int(h * 255 / 360)
    s = int(s * 255)
    v = int(v * 255)
    return (h, s, v)



def main():
    from PIL import Image
    import colorsys
    im = Image.open('test.jpg')
    hdat = []
    sdat = []
    vdat = []
    for px in im.getdata():
        data = conv(*px)
        data = (data[0] / 360, data[1] / 255, data[2] / 255)
        print(px)
        print(data)
        print(colorsys.rgb_to_hsv(data[0] / 255, data[1] / 255, data[2] / 255))

def foo(r, g, b):
    r, g, b = m[(r, g, b)]
    print("b'\\x{}\\x{}\\x{}'".format(hex(r)[2:], hex(g)[2:], hex(b)[2:]))


if __name__ == '__main__':
    main()
else:
    m = {}
    for r in range(256):
        print(r)
        for g in range(256):
            for b in range(256):
                m[(r, g, b)] = conv(r, g, b)
