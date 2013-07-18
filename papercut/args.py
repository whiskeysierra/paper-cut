from __future__ import unicode_literals


class Arguments(object):
    def __init__(self):
        self.dryrun = False
        self.size = 'A4'
        self.orientation = 'portrait'
        self.overwrite = True
        self.input = None
        self.output = None
