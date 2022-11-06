import os
import argparse
import logging
from file_utils import DirectoryIndexer, ensure_dir
import json

logging.basicConfig(level=logging.INFO)

description = """ This utility can compare the content of directories based on 
filenames, lastmod dates, hashed content and filesizes
"""

parser = argparse.ArgumentParser(description=description)
parser.add_argument(
    "--dirs",
    "-d",
    type=str,
    nargs="+",
    action="append",
    help="Path to the original content dir",
)

args = parser.parse_args()

if not args.dirs or len(args.dirs) <= 1:
    logging.error(
        "You need to specify at least 2 dirs (argument -d) in order to compare their content"
    )
    exit(1)

# Create data dir for storing tmp result, create output dir for endresult
DATA_DIR = os.path.abspath(os.path.join(os.getcwd(), "data"))
OUTPUT_DIR = os.path.abspath(os.path.join(os.getcwd(), "output"))
ensure_dir(DATA_DIR)
ensure_dir(OUTPUT_DIR)

# Create indexes
indexes = {}
first_index = args.dirs[0]
for dirname in args.dirs:
    idx = DirectoryIndexer(dirname, DATA_DIR)
    sub_indexes = idx.get_subdir_indexers()
    indexes.update({dirname: idx})
    indexes.update(sub_indexes)

# Use the first index to compare all else with
found_files = {}
result = {}
source_directory_indexer = indexes.get(first_index)
source_files = source_directory_indexer.index

for filename, source_stat in source_files.items():
    resultset = {}
    equals_in = []
    for target, idx in indexes.items():
        if target == first_index:
            continue

        found = idx.index.get(filename, "Not found")
        if found:
            # check for hash
            if source_stat.get('hash') == found.get('hash') and source_stat.get("filesize") == found.get("filesize"):
                equals_in.append(target)
        resultset.update({target, found})
    resultset.update({"equals_in": equals_in})
    if len(equals_in) > 1:
        found_files.update({filename, equals_in})
    result.update({filename: resultset})

# Store the output
print("RESULT: comparing dirs:")
for name in args.dirs:
    print(name)

print("-----------------------------------")
for filename, found in found_files:
    print("{0}:   {1}".format(filename, ", ".join(found)))

print("-----------------------------------")

all_dir_names = "_".join(args.dirs).replace("/"," ").split().replace(" ","_")

output_file = os.path.join(OUTPUT_DIR, "{0}.json".format(all_dir_names))
fp = open(output_file, "w")
json.dump(result, fp)
fp.close()