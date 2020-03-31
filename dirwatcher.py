#!/usr/bin/env python
# -*- coding: utf-8 -*-

'__author__' == 'Sean Bailey'

import os
import argparse
import time
import datetime
import logging
import logging.handlers
import signal

# exit_flag - False
logger = logging.getLogger(__file__)


def watch_directory(args):
    watching_files = {}
    logger.info('Watching directory: {}, File Extension: {}, Polling Interval: {}, Magic Text: {}'.format(
        args.path, args.extension, args.interval, args.magic
    ))

    # Keys are the actual filename and values are where to begin searching
    # Look at directory and get list of files from it.
    # Put files into watching files dictionary IF they're not already in it.
    # Log it as a new file.
    # Look through watching_files dictionary and compare to list of files that is in directory.
    # IF file is not in dictionary anymore, you have to log the file and remove it from dictionary.
    # Iterate through dictionary, open each file at last line you read from.
    # Start reading from that point looking for any "magic" text.
    # Update the last position you read from in dictionary.
    # Add gitignore for log files, vs code files
    # Will want to add a ReadMe

    while True:
        try:
            logger.info('Inside Watch Loop')
            time.sleep(args.interval)
        except KeyboardInterrupt:
            break


def find_magic(filename, starting_line, magic_word):
    pass


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--ext', type=str, default='.txt',
                        help='Text file extension to watch')
    parser.add_argument('-i', '--interval', type=float,
                        default=1.0, help='Number of seconds between polling')
    parser.add_argument('path', help='Directory path to watch')
    parser.add_argument('magic', help='String to watch for')
    return parser


def main():
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s [%(threadName)-12s] %(message)s',
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
    watch_directory(args)
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
    main()
