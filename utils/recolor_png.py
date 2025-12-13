from PIL import Image

def recolor_png(image_path, new_color):
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()

    new_data = []
    for item in data:
        if item[3] > 0:
            new_data.append((new_color[0], new_color[1], new_color[2], item[3]))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img