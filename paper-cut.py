#!/usr/bin/env python

from __future__ import unicode_literals

import argparse
import argcomplete
import papercut.args
import papercut.core

parser = argparse.ArgumentParser(description='Cuts pictures into paper-sized chunks to allow easy printing.')
args = papercut.args.Arguments()

parser.add_argument('-d', '--dry-run', dest='dryrun', action='store_true', default=args.dryrun,
                    help='Does not do anything, put prints what it does. Implies verbose')
parser.add_argument('-s', '--size', dest='size', choices=sorted(papercut.core.sizes.keys()),
                    default=args.size, help='The output paper size.')
parser.add_argument('-o', '--orientation', dest='orientation', choices=papercut.core.orientations.keys(),
                    default=args.orientation, help='The output paper orientation.')
parser.add_argument('-n', '--no-overwrite', dest='overwrite', action='store_false',
                    default=args.overwrite, help='Don\'t overwrite existing target files')
parser.add_argument('input', help='The input directory')
parser.add_argument('output', help='The output directory')

argcomplete.autocomplete(parser)
parser.parse_args(namespace=args)
papercut.core.run(args)
