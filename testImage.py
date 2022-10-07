from PIL import Image
from numpy import asarray

def get_num_pixels(filepath):
    image = Image.open(filepath)
    width, height = image.size
    return width, height

def resize_image(filepath, width, height):
    image = Image.open(filepath)
    image = image.resize((height, width), Image.ANTIALIAS)
    image.save(f'{filepath[:-4]}_resized.png')

print(get_num_pixels("./image/LogoName.jpg"))
resize_image("./image/LogoName.jpg", 512, 384)
print(get_num_pixels("./image/LogoName_resized.png"))

image = Image.open("./image/LogoName_resized.png")
arr = asarray(image)
print(arr.shape)

# count repeated numbers on arr array
counter = 0
allelements = 0
for element in arr:
    for i in element[:, 0]:
        allelements = allelements + 1
        if i == 255:
            counter = counter + 1
        else:
            print(i)
print(counter)
print(allelements)
