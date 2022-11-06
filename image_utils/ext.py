import logging


def has_valid_extension(filename):
    extension = filename.split(".").pop().lower()
    if extension in ["jpg", "heic"]:
        return True
    logging.warn("{0} is not a valid extension".format(extension))
    return False
