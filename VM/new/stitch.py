from PIL import Image

def merge_images(file1, file2):
    image1 = Image.open(file1)
    image2 = Image.open(file2)

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    width1 = int((1 - 448/1700 * 2) * width1 - 3)

    result_width = width1 + width2
    result_height = max(height1, height2)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    result.save('out.png')

merge_images("p1.png", "p2.png")
