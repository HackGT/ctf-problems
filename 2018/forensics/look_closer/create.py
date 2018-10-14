#!/usr/bin/env python3

import copy
import struct
import zipfile
from zlib import compress

INJECT_LOCATION = 1
FLAG = compress(b"hackgt{zYHSDZkblWNPnt53}")


def main():
    with open("look_closer_orig.docx", "rb") as infile, open(
        "look_closer.docx", "wb"
    ) as outfile:
        with zipfile.ZipFile(infile, "r") as inzip, zipfile.ZipFile(
            outfile, "w"
        ) as outzip:
            for i, zi in enumerate(inzip.infolist()):
                ziout = copy.deepcopy(zi)
                ziout.header_offset = outfile.tell()

                infile.seek(zi.header_offset)
                lheader = struct.unpack(
                    zipfile.structFileHeader, infile.read(zipfile.sizeFileHeader)
                )
                tocopy = (
                    zipfile.sizeFileHeader
                    + lheader[zipfile._FH_COMPRESSED_SIZE]
                    + lheader[zipfile._FH_FILENAME_LENGTH]
                    + lheader[zipfile._FH_EXTRA_FIELD_LENGTH]
                )

                infile.seek(zi.header_offset)
                while tocopy:
                    data = infile.read(min(tocopy, 4096))
                    outfile.write(data)
                    tocopy -= len(data)

                outzip.filelist.append(ziout)

                if i == INJECT_LOCATION:
                    outfile.write(FLAG)

                outzip.start_dir = outfile.tell()


if __name__ == "__main__":
    main()
