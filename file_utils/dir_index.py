import os
import logging
from .hash_index import stats_from_file
import json


class DirectoryIndexer:

    index = {}
    processed = False
    directory_name = None
    subdirs = []
    subdir_index = {}

    def __init__(self, directory_name, datadir=None):
        if not os.path.isdir(directory_name):
            logging.warn("{0} is not a directory".format(directory_name))
            exit()
        self.datadir = datadir
        self.directory_name = directory_name
        self._build_index()

    def _build_index(self):
        # Read the directory
        # for every file, generate the index
        self._load_data()

        if self.processed:
            logging.warn(
                "Attempted to re-index {0} - skipped".format(self.directory_name)
            )
            return
        
        filelist = os.listdir(self.directory_name)
        logging.warn(
            "Starting to index {0} files in {1}".format(
                len(filelist), self.directory_name
            )
        )
        for file in filelist:
            filepath = os.path.join(self.directory_name, file)
            if os.path.isfile(filepath):
                stats = stats_from_file(filepath)
                if stats:
                    self.index.update({os.path.basename(file): stats})
            elif os.path.isdir(filepath):
                self.subdirs.append(filepath)
        
        self._index_subdirs()
        self.processed = True
        return

    def get_subdir_indexers(self):
        """
        Return the subdir indexers
        """
        res = {}
        for index_name, idx in self.subdir_index.items():
            res.update({index_name, idx})
            res.update(idx.get_subdir_indexers())

        return res

    def _index_subdirs(self):
        """
        Generate the same index for the subdirs

        """
        for dirname in self.subdirs:
            path = os.path.join(self.directory_name, dirname)
            idx = DirectoryIndexer(path)
            self.subdir_index.update({path: idx})
            

    def refresh_index(self):
        self.processed = False
        # Remove the cached file
        if self.datadir:
            filename = "{0}.json".format(self._generate_filename())
            path = os.path.join(self.datadir, filename)
            if os.path.isfile(path):
                os.remove(path)
        
        self._build_index()

    def _generate_filename(self):
        return self.directory_name.replace("/", " ").strip().replace(" ", "_")

    def _store_data(self):
        if not self.datadir:
            return
        
        filename = "{0}.json".format(self._generate_filename())
        output_path = os.path.join(self.datadir, filename)
        fp = open(output_path, "w")
        fp.write(self.index)
        fp.close()

    def _load_data(self):
        if not self.datadir:
            return
        
        filename = "{0}.json".format(self._generate_filename())
        path = os.path.join(self.datadir, filename)
        if not os.path.isfile(path):
            return

        fp = open(path, "r")
        self.index = json.load(fp)
        fp.close()
        self.processed = True