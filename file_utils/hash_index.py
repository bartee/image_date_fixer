import logging
import os
import hashlib


def stats_from_file(filename):
    """
    Read all stats from a certain file:
     - hashed file content
     - filesize
     - lastmod timestamp
    """
    if not os.path.isfile(os.path.abspath(filename)):
        logging.warn("{0} is not a file".format(filename))
        return False

    hash = hashfile(filename)
    filesize = os.path.getsize(filename)
    lastmod = os.path.getmtime(filename)

    return {"hash": hash, "filesize": filesize, "lastmod": lastmod}


def hashfile(file):
    # An arbitrary (but fixed) buffer
    # size (change accordingly)
    # 65536 = 65536 bytes = 64 kilobytes
    BUF_SIZE = 65536

    # Initializing the sha256() method
    sha256 = hashlib.sha256()

    # Opening the file provided as
    # the first commandline argument
    with open(file, "rb") as f:

        while True:

            # reading data = BUF_SIZE from
            # the file and saving it in a
            # variable
            data = f.read(BUF_SIZE)

            # True if eof = 1
            if not data:
                break

            # Passing that data to that sh256 hash
            # function (updating the function with
            # that data)
            sha256.update(data)

    f.close()
    # sha256.hexdigest() hashes all the input
    # data passed to the sha256() via sha256.update()
    # Acts as a finalize method, after which
    # all the input data gets hashed hexdigest()
    # hashes the data, and returns the output
    # in hexadecimal format
    return sha256.hexdigest()
