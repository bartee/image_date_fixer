from datetime import datetime
import time
import exifread
import os
import logging


def image_modification_date_from_exif(imagename):
    """
    Set the modification/creation date of the image to its EXIF data.

    :param imagename: name of the image to handle
    """
    if os.path.exists(imagename):
        logging.debug("Parsing {0}...".format(imagename))
        filestream = open(imagename, "rb")
        tags = exifread.process_file(filestream)
        start_time = tags.get("EXIF DateTimeOriginal", None)
        if start_time:
            timestamp = datetime.strptime(start_time.values, "%Y:%m:%d %H:%M:%S")
            mt = int(time.mktime(timestamp.timetuple()))
            os.utime(imagename, (mt, mt))
            return timestamp
        else:
            logging.warn(tags)

    return None
