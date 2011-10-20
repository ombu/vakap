#! /usr/bin/env python
import sys
from optparse import OptionParser
import json
from fabric.api import * 
from pprint import pprint

env.key_filename = ['/Users/axolx/.ssh/axolx-base']
env.s3bucket = 'backup.ombuweb.com'
env.gpg_key = 'A01D2B0D'

def main():
    usage = "usage: %prog command"
    desc = "Run a command on a set of hosts"
    parser = OptionParser(description=desc, usage=usage)
    parser.add_option("-f", "--file", dest="filename",
                      help="Hosts manifest JSON file")
    
    (options, args) = parser.parse_args()
    
    if len(args) == 0:
        sys.exit("No command supplied")
        
    sites = parse_sites(options.filename if options.filename else 'hosts.json')
    for site in sites:
        print '+ Processing site %s' % site["name"]
        env.site = site["name"]
        for component in site["components"]:
            c = Component.factory(component)
            for command in args:
                getattr(c, command)()

def parse_sites(jsonFile):
    try:
        f = open(jsonFile)
        return json.load(f)
    finally: 
        f.close()

class Component(object):
    @staticmethod
    def factory(component):
        return eval(component["type"])(component)

    def __init__(self, rawData):
        self.rawData = rawData
        self.__dict__.update(rawData)

class TgzComponent(Component):
    def __init__(self, componentRawData):
        super(type(self), self).__init__(componentRawData)

    def backup(self):
        with settings(host_string=self.hostString):
            backup_files(self.sitePath)


class MysqlComponent(Component):
    def __init__(self, componentRawData):
        super(type(self), self).__init__(componentRawData)

    def backup(self):
        with settings(host_string=self.hostString):
            backup_db(self.dbName)
@task
def get_ref(path):
    with cd(path): 
        foo = run('readlink current')
        print foo

@task
def backup_files(path):
    from time import gmtime, strftime
    with cd(path):
        date= strftime("%Y.%m.%d", gmtime())
        gpg = 'files-%s.tgz.gpg' % date
        with settings(warn_only=True):
            run('rm /tmp/vakap-*')
        run("""tar czh current | gpg --encrypt --recipient {key} > {tmp}/vakap-{gpg}"""
                .format( tmp='/tmp', gpg=gpg, key=env.gpg_key))
        run("""s3cmd --acl-public --human-readable-sizes put  \
                {tmp}/vakap-{gpg} s3://{bucket}/{site}/{gpg}"""
                .format(tmp='/tmp',gpg=gpg,bucket=env.s3bucket,site=env.site))
        with settings(warn_only=True):
            run('rm /tmp/vakap-*')
@task
def backup_db(dbname):
    run('which mysql')
 
main()
