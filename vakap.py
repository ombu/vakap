#! /usr/bin/env python
import sys
import json
from optparse import OptionParser
from fabric.api import env
from components.base import Component
import pprint

class GlobalCommand(object):
    """ Global Commands """

    @staticmethod
    def list(hosts):
        for site in hosts:
            print site["name"]
            for component in site["components"]:
                print " - %s" % component["type"]
        sys.exit(0)

def main():
    usage = "usage: %prog command"
    desc = "Run a command on a set of hosts"
    parser = OptionParser(description=desc, usage=usage)
    parser.add_option("-s", "--settings", dest="settings",
            help="Hosts manifest JSON file [default: %default]",
            default="settings.json")
    parser.add_option("-f", "--filter", dest="filter",
            help="Comma-separated list of sites to process [default: all sites]")
    parser.add_option("-x", "--exclude", dest="exclude",
            help="Comma-separated list of sites to exclude")

    (options, args) = parser.parse_args()
    if len(args) == 0:
        print "No command supplied"
        print "Available commands: list, backup"
        sys.exit(0)

    sites = parse_settings(options)

    # Try to run the command globablly
    for command in args:
        try: getattr(GlobalCommand, command)(sites)
        except AttributeError: pass

    # Try to run the command on site components
    for site in sites:
        print '+ Processing site %s' % site["name"]
        for component in site["components"]:
            c = Component.factory(site["name"], component)
            for command in args:
                try: getattr(c, command)()
                except AttributeError: pass

def parse_settings(options):
    f = open(options.settings)
    try:
        config = json.load(f)
        env.key_filename = config['settings']['default_ssh_key']
        env.gpg_key = config['settings']['gpg_key']
        env.s3_bucket = config['settings']['s3_bucket']
        env.s3_access_key = config['settings']['s3_access_key']
        env.s3_secret = config['settings']['s3_secret']

        # filter and exclude options
        if options.filter:
            filter_sites = [x.strip() for x in options.filter.split(',')]
            hosts = filter(lambda x: x['name'] in filter_sites, config['hosts'])
        if options.exclude:
            exclude_sites = [x.strip() for x in options.exclude.split(',')]
            hosts = filter(lambda x: x['name'] not in exclude_sites, config['hosts'])
        else:
            hosts = config['hosts']
        return hosts
    finally:
        f.close()

if __name__ == '__main__':
    sys.exit(main())
