import os
import sys
import yaml
from optparse import OptionParser
from fabric.api import env
from components.base import Component


class GlobalCommand(object):
    """ Global Commands """

    @staticmethod
    def list(sites):
        """ Outputs a list of sites and their components """
        for site in sites:
            print site["name"]
            for component in site["components"]:
                print " - %s" % component["type"]

    @staticmethod
    def hosts(sites):
        """ Outputs manifest grouping sites by host """
        raise NotImplementedError


def cli_args():
    usage = "usage: %prog command"
    desc = "Run a command on a set of hosts"
    parser = OptionParser(description=desc, usage=usage)
    parser.add_option(
        "-c", "--config", dest="config",
        help="Hosts manifest JSON file [default: %default]",
        default="./config.yaml")
    parser.add_option(
        "-i", "--include", dest="include",
        help="Comma-separated list of sites to process [default: all sites]")
    parser.add_option(
        "-x", "--exclude", dest="exclude",
        help="Comma-separated list of sites to exclude")
    parser.add_option(
        "-v", "--verbose", action="store_true", dest="verbose",
        default=False, help="Verbose output")

    # returns (options, args)
    return parser.parse_args()


def main():
    (options, args) = cli_args()
    run(options, args)


def run(options, args):

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

    if hasattr(options, 'verbose'):
        fabric.state.output['status'] = True
        fabric.state.output['running'] = True
        fabric.state.output['stdout'] = True

    sites = parse_config(options)

    # Try to run the command globablly
    for command in args:
        try:
            getattr(GlobalCommand, command)(sites)
        except AttributeError:
            pass

    # Try to run the command on site components
    for site in sites:
        print '+ Processing site %s' % site["name"]
        for component in site["components"]:
            c = Component.factory(site["name"], component)
            for command in args:
                try:
                    getattr(c, command)()
                except AttributeError:
                    pass


def parse_config(options):
    f = open(options.config, 'r')
    try:
        config = yaml.load(f)
        env.gpg_key = config['settings']['gpg_key']
        env.s3_bucket = config['settings']['s3_bucket']
        env.s3_access_key = os.environ['VAKAP_S3_ACCESS_KEY']
        env.s3_secret = os.environ['VAKAP_S3_SECRET']

        # include and exclude options
        if hasattr(options, 'include'):
            include_sites = [x.strip() for x in options.include.split(',')]
            return filter(
                lambda x: x['name'] in include_sites, config['sites'])
        elif hasattr(options, 'exclude'):
            exclude_sites = [x.strip() for x in options.exclude.split(',')]
            return filter(
                lambda x: x['name'] not in exclude_sites, config['sites'])
        else:
            return config['sites']
    finally:
        f.close()

if __name__ == '__main__':
   main()
