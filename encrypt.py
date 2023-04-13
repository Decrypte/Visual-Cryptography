from PIL import Image


def generate_shares(input_image):

    width, height = input_image.size
    share1 = Image.new("1", (width * 2, height))
    share2 = Image.new("1", (width * 2, height))
    pixels1 = share1.load()
    pixels2 = share2.load()
    for x in range(width):
        for y in range(height):
            pixel = input_image.getpixel((x, y))
            if pixel == 0:
                pixels1[x*2, y] = 0
                pixels1[x*2+1, y] = 1
                pixels2[x*2, y] = 1
                pixels2[x*2+1, y] = 0
            else:
                pixels1[x*2, y] = 1
                pixels1[x*2+1, y] = 0
                pixels2[x*2, y] = 0
                pixels2[x*2+1, y] = 1
    return share1, share2

v = input()
direc = "input/" + v + ".jpg"
input_image = Image.open(direc).convert("1")
share1, share2 = generate_shares(input_image)
share1.save("output/share1/"+ v +"-1.jpg")
share2.save("output/share2/"+ v +"-2.jpg")


