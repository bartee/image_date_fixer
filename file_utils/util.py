import os


def ensure_dir(dirname):
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
