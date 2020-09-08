#!/usr/bin/env python3

import os
import urllib

import numpy as np


# to keep track of printing download progress
last_percent_printed = None


def format_bytes(nbytes):
    """
    Format a number in bytes with a prefix

    :param int nbytes: number of bytes (>0)
    :return: number of MB/GB etc (float), unit (MB/GB etc) (str)
    """
    # prefixes up to exabyte
    prefix_letters = ' kMGTPE'

    if nbytes < 1:
        # special case, because log10(nbytes) < 0 for nbytes < 1
        prefix_tier = 0
    else:
        prefix_tier = int(np.log10(nbytes) / 3)  # 3 = log10(1000)

    try:
        letter = prefix_letters[prefix_tier]
        scaling = 1000 ** prefix_tier
    except IndexError:
        # unlikely to run into files over 1000 exabytes, but we wouldn't want an unexplained
        # IndexError when someone puts in a very large number
        letter = prefix_letters[-1]
        scaling = 1000 ** (len(prefix_letters) - 1)
    # do the scaling
    return nbytes / scaling, letter + 'B'


def print_progress(nblock, nbyte_per_block, nbyte_total, step=5):
    """
    Print download progress of urllib.request.urlretrieve command

    :param nblock:
    :param nbyte_per_block:
    :param total_bytes:
    :param int step: progress is only printed if the percentage is a multiple of step
    """
    global last_percent_printed
    nbyte_done = nblock * nbyte_per_block
    percent_done = int(100 * nbyte_done / nbyte_total)

    # print only if not done already and multiple of step
    if last_percent_printed != percent_done and int(percent_done % step) == 0:
        # get scaled value prefix to use for output (kB, MB etc)
        done_scaled, done_unit = format_bytes(nbyte_done)
        total_scaled, total_unit = format_bytes(nbyte_total)

        print(f"{done_scaled:.0f} {done_unit} / {total_scaled:.0f} {total_unit} ({percent_done:.0f}%)")
        last_percent_printed = percent_done

    return


def download_url(url, output_folder=None, verbose=False):
    """
    Download file at given url using
    :param url: URL to download file from
    :param str output_folder: Output folder (Default: current directory)
    :param bool verbose: Print download progress
    """
    # get full path to output file
    if output_folder is not None:
        output_file = os.path.join(output_folder, os.path.basename(url))
    else:
        output_file = os.path.basename(url)
    # set report hook if verbose output
    if verbose:
        hook = print_progress
    else:
        hook = None
    # download the file
    try:
        urllib.request.urlretrieve(url, filename=output_file, reporthook=hook)
    except urllib.error.HTTPError as e:
        # add filename to error message
        e.msg = f"URL not found: {url}"
        raise
    return


def download_irods(path, output_folder=None):
    """
    Download file
    :param path: Path to file on iRODS server
    :param str output_folder: Output folder (Default: current directory)
    """
    raise NotImplementedError("iRODS download not available")
