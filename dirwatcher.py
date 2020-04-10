#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import signal
import logging
import datetime
import time
import argparse
import os
import sys
'__author__' == 'Sean Bailey, Koren, Chris, Stew, Piero, MikeA'
'   and mobcoding walkthrough'

# import logging.handlers

exit_flag = False
logger = logging.getLogger(__name__)
files_found = []
magic_word_position = {}


def watch_directory(magic_word, extension, polling, dir_path):
    # watch directory for file changes

    file_dictionary = {}
    while not exit_flag:
        logger.debug("Still watching")
        # Add files
        for filename in os.listdir(dir_path):
            if filename.endswith(extension) and filename\
                    not in file_dictionary:
                logger.info(f"{filename} added")
                file_dictionary[filename] = 0
        # Remove files
        for filename in list(file_dictionary):
            if filename not in os.listdir(dir_path):
                file_dictionary.pop(filename)
                logger.info(f"{filename} removed")
        # Scan rest of files
        for filename in file_dictionary:
            broad_path = os.path.join(dir_path, filename)
            file_dictionary[filename] = find_magic(
                broad_path, magic_word, file_dictionary[filename]
            )
        time.sleep(polling)


def find_magic(filename, starting_line, magic_word):
    """ Look for magic word in filename searching line by line.
     Keep record of most recent line searched"""
    with open(filename, "r") as f:
        search_index = 0
        for search_index, line in enumerate(f):
            if search_index >= starting_line:
                if magic_word in line:
                    logger.info(f"Magic word is {magic_word} in {filename} "
                                f"on line {search_index + 1}"
                                )
        return search_index + 1


def signal_handler(sig_num, frame):
    """ Toogles exit_flag when finds SIGINT and SIGTERM signals"""
    global exit_flag
    # log signal name both python 2 and python 3 ways
    signames = dict((k, v) for v, k in reversed(sorted(
        signal.__dict__.items()))
        if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received sig: ' + signames[sig_num])
    if sig_num == signal.SIGINT or signal.SIGTERM:
        global exit_flag
        exit_flag = True


def create_parser():
    """ Creates parser. Sets up command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-e', '--ext',
        type=str,
        default='.txt',
        help='Text file extension to watch')
    parser.add_argument(
        '-i', '--interval',
        type=float,
        default=1,
        help='Number of seconds between polling')
    parser.add_argument(
        'path',
        help='Directory path to watch')
    parser.add_argument(
        'magic',
        help='String to watch for')
    return parser


def main(args):
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s '
        '[%(threadName)-12s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)
    app_start_time = datetime.datetime.now()
    logger.info(
        '\n'
        '-----------------------------------------------------------------\n'
        '   Running {0}\n'
        '   Started on {1}\n'
        '-----------------------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )
    parser = create_parser()
    args = parser.parse_args()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info(
        f"Searching in {args.path} for {args.ext}"
        f" files with {args.magic}"
    )

    while not exit_flag:
        try:
            watch_directory(args.ext, args.interval, args.path, args.magic)
        except FileNotFoundError:
            logger.error(args.path + " directory does not exist")
        except Exception:
            logger.exception("Unhandled exception")
        finally:
            logger.info("Program Interrupted")
        time.sleep(3.0)

    # watch_directory(args)
    # watch_directory()
    uptime = datetime.datetime.now()-app_start_time
    logger.info(
        '\n'
        '-----------------------------------------------------------------\n'
        '   Stopped {0}\n'
        '   Uptime was {1}\n'
        '-----------------------------------------------------------------\n'
        .format(__file__, str(uptime))
    )
    logging.shutdown


if __name__ == '__main__':
    main(sys.argv[1:])
