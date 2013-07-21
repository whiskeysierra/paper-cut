from __future__ import unicode_literals

import os

from clint.textui import colored, indent, puts

from glob import glob
from wand.image import Image

sizes = {
    'A0': (841.0, 1189.0),
    'A1': (594.0, 841.0),
    'A2': (420.0, 594.0),
    'A3': (297.0, 420.0),
    'A4': (210.0, 297.0),
    'A5': (148.0, 210.0),
    'A6': (105.0, 148.0),
    'A7': (74.0, 105.0),
    'A8': (52.0, 74.0),
    'A9': (37.0, 52.0),
    'A10': (26.0, 37.0),
    'Letter': (215.9, 279.4),
    'Legal': (215.9, 355.6),
    'Ledger': (2.0, 279.0),
    'Tabloid': (9.0, 432.0),
}

orientations = {
    'portrait': lambda (w, h): h / w,
    'landscape': lambda (w, h): w / h,
}

# TODO make image extensions more dynamic, versatile or configurable
extensions = ['bmp', 'gif', 'jpeg', 'jpg', 'png', 'tiff']


def exists(target):
    return os.path.exists(target) or glob('%s-*%s' % os.path.splitext(target))


def run(args):
    size = sizes[args.size]
    ratio = orientations[args.orientation](size)

    for root, _, _ in os.walk(args.input):
        puts(root)
        with indent(4):
            for extension in extensions:
                files = glob(os.path.join(root, '*.%s' % extension))
                for source in files:
                    with Image(filename=source) as original:
                        with original.clone() as img:
                            width, height = img.size

                            if width < height:
                                height = int(width * ratio)
                            else:
                                width = int(height / ratio)

                            dimension = '%sx%s' % (width, height)

                            relative = os.path.relpath(source, args.input)
                            target = os.path.join(args.output, relative)
                            directory = os.path.dirname(target)

                            if not args.dryrun:
                                if not os.path.exists(directory):
                                    os.makedirs(directory)

                                if not args.overwrite and exists(target):
                                    puts('[%s] %s' % (colored.yellow('exists'), relative))
                                else:
                                    img.transform(crop=dimension)
                                    img.save(filename=target)
                                    puts('[%s] %s' % (colored.green('done'), relative))