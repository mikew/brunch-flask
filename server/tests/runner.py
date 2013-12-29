#!/usr/bin/env python

import os
import sys
import nose


def relative_path(*parts):
    dirname, realpath, join_path = (os.path.dirname,
                                    os.path.realpath,
                                    os.path.join)

    cwd = dirname(realpath(__file__))
    return realpath(join_path(cwd, '..', *parts))


def safe_add_import_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)


main_dir = relative_path('..')
vendor_dir = relative_path('tests', 'vendor')

# Easily import things in tests/vendor/ directory.
safe_add_import_path(vendor_dir)
# Easily import things in root directory.
safe_add_import_path(main_dir)

import spec

files = 'server/tests/'

sys.argv.insert(1, '--with-spec')
sys.argv.insert(1, '--spec-color')
sys.argv.insert(1, '--nocapture')
sys.argv.insert(1, '--nologcapture')

plugins = []
plugins.append(spec.Spec())
nose.main(addplugins=plugins)
