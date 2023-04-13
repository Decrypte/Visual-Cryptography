from PIL import Image


def combine_shares(share1, share2):
    w, h = share1.size
    res = Image.new("1", (w // 2, h))
    pixels = res.load()
    for x in range(0, w, 2):
        for y in range(h):
            if share1.getpixel((x, y)) == 0 and share1.getpixel((x+1, y)) == 1 and share2.getpixel((x, y)) == 1 and share2.getpixel((x+1, y)) == 0:
                pixels[x // 2, y] = 0
            else:
                pixels[x // 2, y] = 1
    return res


name = input()
share1 = Image.open("output/share1/"+name+"-1.jpg").convert("1")
share2 = Image.open("output/share2/"+name+"-2.jpg").convert("1")
white_image = combine_shares(share1, share2)
input_image = Image.open("input/"+name+".jpg")

width, height = input_image.size
result = Image.new("RGB", (width, height))
pixels = result.load()
for x in range(width):
    for y in range(height):
        white_pixel = white_image.getpixel((x, y))
        colored_pixel = input_image.getpixel((x, y))
        pixels[x, y] = tuple([colored_pixel[i] if (white_pixel >> i) & 1 == 0 else (white_pixel >> i) & 1 for i in range(3)])

result.save("output/recovered/"+name+"-new.jpg")


