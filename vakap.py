#! /usr/bin/env python
import sys
import json
from optparse import OptionParser
from fabric.api import env 

from components.base import Component

def main():
    usage = "usage: %prog command"
    desc = "Run a command on a set of hosts"
    parser = OptionParser(description=desc, usage=usage)
    parser.add_option("-s", "--settings", dest="settings",
                      help="Hosts manifest JSON file [default: %default]",
                      default="settings.json")

    (options, args) = parser.parse_args()
    if len(args) == 0:
        sys.exit("No command supplied")

    for site in parse_settings(options.settings):
        print '+ Processing site %s' % site["name"]
        for component in site["components"]:
            c = Component.factory(site["name"], component)
            for command in args:
                getattr(c, command)()

def parse_settings(jsonFile):
    try:
        f = open(jsonFile)
        config = json.load(f)
        env.key_filename = config['settings']['default_ssh_key']
        env.s3_bucket = config['settings']['backup_s3_bucket']
        env.gpg_key = config['settings']['gpg_key']
        return config['hosts']
    finally:
        f.close()

if __name__ == '__main__':
    sys.exit(main())
