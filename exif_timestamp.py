"""Update image file modification timestamp."""
from datetime import datetime
import time
import exifread
import os
import argparse


def image_modification_date_from_exif(imagename):
    """
    Set the modification/creation date of the image to its EXIF data.

    :param imagename: name of the image to handle
    """
    if os.path.exists(imagename):
        print("Parsing {0}...".format(imagename))
        filestream = open(imagename, 'rb')
        tags = exifread.process_file(filestream)
        start_time = tags.get('EXIF DateTimeOriginal')
        print(start_time)
        timestamp = datetime.strptime(start_time.values, "%Y:%m:%d %H:%M:%S")
        mt = int(time.mktime(timestamp.timetuple()))
        os.utime(imagename, (mt, mt))
        return timestamp
    return None

description = """ When you copy files to your computer from your iPhone,
                  the dates to the individual files are set to the current
                  date.
                  With this utility, you can restore the date to the original.
                  You can do it with individual files, or with a
                  complete directory.
                  Mind you, the script is limited to .jpg-images """

parser = argparse.ArgumentParser(description=description)
parser.add_argument('--path', type=str, required=False,
                    help='Path to the dir containing the images to handle.')
parser.add_argument('--image', type=str, required=False,
                    help='Path to a single image to handle. Non-recursive!')

args = parser.parse_args()

handled = False
if args.path:
    # Handle a full directory.
    print ("Handling {0}...\n".format(args.path))
    if os.path.exists(args.path):
        files = os.listdir(args.path)
        images = [img for img in files if '.jpg' in img.lower()]
        print("Found {0} images in {1}".format(len(images), args.path))
        succeeded = 0

        for image in images:
            imagepath = os.path.abspath(os.path.join(args.path, image))
            print("Handling {0}...\n".format(imagepath))
            res = image_modification_date_from_exif(imagepath)
            succeeded += 1
        if succeeded > 0:
            print("Handled {0} images. \n".format(succeeded))
            handled = True
    else:
        print("Invalid path: {0} \n".format(args.path))

if args.image:
    # Handle an individual image.
    if os.path.exists(args.image):
        res = image_modification_date_from_exif(args.image)
        print("Set the date of {0} to {1}".format(args.image, res.isoformat()))
        handled = True
    else:
        print("Image {0} not found!".format(args.image))

if not handled:
    print (parser.print_help())
    print ("")
    print ("Nothing was done; did you specify image or a path? Do they exist? ")
