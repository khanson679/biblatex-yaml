#!/usr/bin/env python

import sys

try:
    import yaml
except ImportError as e:
    print(e)
    print("Please install 'pyyaml' with `pip install pyyaml`")
    sys.exit(1)

try:
    import pybtex.database
except ImportError as e:
    print(e)
    print("Please install 'pybtex' with `pip install pybtex`")
    sys.exit(1)


if not len(sys.argv) == 3:
    print("usage: python yaml2bib.py <infile> <outfile>")
    sys.exit(1)
INFILENAME = sys.argv[1]
OUTFILENAME = sys.argv[2]


#
# preprocess source database
#

with open(INFILENAME) as infile:
    srcdata = yaml.load(infile)

# delete unsupported fields in person entries
for person in srcdata['people'].itervalues():
    for field in ['ids', 'url']:
        if person.has_key(field):
            del person[field]

for section in srcdata['xdata'].itervalues():
    for entry in section.itervalues():
        to_remove = 'xdatatype'
        if entry.has_key(to_remove):
            del entry[to_remove]

# merge XDATA entries into main section
for section in srcdata['xdata'].itervalues():
    srcdata['entries'].update(section)


#
# convert to BIB format
#

bibdb = pybtex.database.parse_string(unicode(yaml.dump(srcdata)), "yaml")
bibdb.to_file(OUTFILENAME)
