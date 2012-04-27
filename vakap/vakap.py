import os
import sys
import json
from optparse import OptionParser
from fabric.api import env
from components.base import Component
import pprint
import ssh


# https://github.com/fabric/fabric/issues/312
ssh.io_sleep = 0.1

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
            default="./settings.json")
    parser.add_option("-i", "--include", dest="include",
            help="Comma-separated list of sites to process [default: all sites]")
    parser.add_option("-x", "--exclude", dest="exclude",
            help="Comma-separated list of sites to exclude")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
            default=False, help="Verbose output")

    (options, args) = parser.parse_args()
    if len(args) == 0:
        print "No command supplied"
        print "Available commands: list, status, backup"
        sys.exit(0)

    import fabric.state

    fabric.state.output['status'] = False
    fabric.state.output['aborts'] = True
    fabric.state.output['warnings'] = True
    fabric.state.output['running'] = False
    fabric.state.output['stdout'] = False
    fabric.state.output['stderr'] = True
    fabric.state.output['user'] = True

    if options.verbose:
        fabric.state.output['status'] = True
        fabric.state.output['running'] = True
        fabric.state.output['stdout'] = True

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
    f = open('./' + options.settings)
    try:
        config = json.load(f)
        env.key_filename = config['settings']['default_ssh_key']
        env.gpg_key = config['settings']['gpg_key']
        env.s3_bucket = config['settings']['s3_bucket']
        env.s3_access_key = config['settings']['s3_access_key']
        env.s3_secret = config['settings']['s3_secret']

        # include and exclude options
        if options.include:
            include_sites = [x.strip() for x in options.include.split(',')]
            hosts = filter(lambda x: x['name'] in include_sites, config['hosts'])
        elif options.exclude:
            exclude_sites = [x.strip() for x in options.exclude.split(',')]
            hosts = filter(lambda x: x['name'] not in exclude_sites, config['hosts'])
        else:
            hosts = config['hosts']
        return hosts
    finally:
        f.close()
