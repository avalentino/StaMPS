#!/usr/bin/env python3
"""Extract phase for PS candidates from complex interferograms."""

import io
import sys
import logging
import argparse

import numpy as np


LOGFMT = "%(message)s"
SUN_RASTER_MAGIC = 0x59a66a95.to_bytes(4, 'little')


def load_param_file(filename):
    with open(filename) as paramfile:
        width = int(paramfile.readline().strip())
        ifgfiles = [name.rstrip() for name in paramfile]
    return width, ifgfiles


def get_offset_and_size(fd, header=SUN_RASTER_MAGIC):
    pos = fd.tell()
    fd.seek(0, io.SEEK_END)
    size = fd.tell()
    fd.seek(0)
    header_size = len(header)
    data = fd.read(header_size)
    offset = header_size if data == header else 0
    if offset != 0:
        logging.getLogger(__name__).info("sun raster file - skipping header")
    fd.seek(pos)
    return offset, size - offset


def get_memmap(fd, width, dtype=np.complex64):
    offset, size = get_offset_and_size(fd)
    linesize = width * np.dtype(dtype).type().nbytes
    height = (size - offset) // linesize
    assert height == (size - offset) / linesize
    shape = (height, width)
    return np.memmap(fd, dtype=dtype, mode='r', offset=offset, shape=shape)


def pscphase(paramfile, psfile, pscands_ps):
    log = logging.getLogger(__name__)

    width, ifgfiles = load_param_file(paramfile)
    log.info("width = %d", width)
    log.info("number of interferograms = %d", len(ifgfiles))

    ps = np.loadtxt(psfile, dtype=int)
    y = ps[:, 1]
    x = ps[:, 2]
    buffer = np.empty(len(ps), dtype=np.complex64)

    with open(pscands_ps, 'wb') as out_fd:
        for idx, filename in enumerate(ifgfiles):
            log.info("opening %s ...", filename)
            with open(filename, 'rb') as fd:
                mmap = get_memmap(fd, width=width)
                buffer[:] = mmap[y, x]
                del mmap
            out_fd.write(buffer.tobytes())
            log.info(
                "%d  of %d interferograms processed", idx + 1, len(ifgfiles))


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "paramfile",
        help="path to the parameter file containing the width of the "
             "interferogram files (range bins) and the list of paths to "
             "interferogram files (containing complex floats stored as "
             "binaty data)")
    parser.add_argument(
        "psfile", default="pscands.1.ij",
        help="path to the text file containing the location (image "
             "candidiates) of permanent scatterer (default: '%(default)s')")
    parser.add_argument(
        "pscands_ph", default="pscands.1.ph",
        help="output file containing the phase of the permanent scatterer "
             "candidates stored in binary format (default: '%(default)s')")

    return parser


def parse_args(args=None, namespace=None, parser=None):
    if parser is None:
        parser = get_parser()

    args = parser.parse_args(args, namespace)

    return args


def main(*argv):
    logging.basicConfig(format=LOGFMT, level=logging.INFO, stream=sys.stdout)
    logging.captureWarnings(True)

    args = parse_args(argv if argv else None)
    return pscphase(args.paramfile, args.psfile, args.pscands_ph)


if __name__ == "__main__":
    sys.exit(main())