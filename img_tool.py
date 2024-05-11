import time
import cv2
import os
from PIL import Image
from alive_progress import alive_bar


def progress_bar(func):
    def wrapper(*args, **kwargs):
        with alive_bar(total=len(args[0]), force_tty=True, theme="smooth") as bar:
            for result in func(*args, **kwargs):
                print(result)
                bar()

    return wrapper


def compress(path, percent):
    output = r"\compressed"
    if not os.path.exists(path + output):
        os.mkdir(path + output)
    for filename in os.listdir(path):
        # Check if the file is a JPEG image
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            # Open the image
            img = Image.open(os.path.join(path, filename))

            # Reduce the quality of the image
            img.save(os.path.join(path + output, filename), "JPEG", optimize=True, quality=int(percent))


@progress_bar
def convert(path):
    output = r"\converted"
    if not os.path.exists(path + output):
        os.mkdir(path + output)

    for filename in os.listdir(path):
        if filename.endswith(".png") and (filename[:-4] + ".jpg") not in os.listdir(path + output):
            png_img = cv2.imread(os.path.join(path, filename))

            new_file = os.path.join(path + output, f'{filename.strip(".png")}.jpg')

            cv2.imwrite(new_file, png_img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

            time.sleep(0.01)

            yield


def resize(path, size):
    output = r"\resized"
    if not os.path.exists(path + output):
        os.mkdir(path + output)

    for filename in os.listdir(path):
        if not filename.endswith('.jpg') and not filename.endswith('.jpeg') and not filename.endswith('.png'):
            continue

        with Image.open(os.path.join(path, filename)) as img:
            img = img.resize(size)
            img.save(os.path.join(path + output, filename))


if __name__ == '__main__':
    match input("1- Compress\n2- Convert\n3- Resize\nChoose Option: "):
        case '1':
            compress(input("Path: "), input("Percent: "))
        case '2':
            convert(input("Path: "))  # C:\Users\alice\Downloads
        case '3':
            resize(input("Path: "), tuple(input("Size: ").split(',')))
        case _:
            pass
