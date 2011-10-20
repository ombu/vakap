#! /usr/bin/env python
import sys
from optparse import OptionParser
import json
from fabric.api import * 
from pprint import pprint

env.key_filename = ['/Users/axolx/.ssh/axolx-base']

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
                # try: 
                getattr(c, command)()
                # Catching exceptions here was problematic because it was
                # catching excetions happing deeper in the stack.
                # what to do?
                # except AttributeError: 
                #     print("Command %s not found on %s" % (command, c))
                # except:
                #     print "Unexpected error:", sys.exc_info()[0]
                #     raise

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
    s3bucket = 'backup.ombuweb.com'
    with cd(path):
        print(path)
        date= strftime("%Y.%m.%d", gmtime())
        tgz = 'files-%s.tgz' % date
        run('tar czhf %s/%s files' % ('/tmp', tgz))
        run("""s3cmd --add-header=x-amz-server-side-encryption:AES256 \
                --human-readable-sizes put {tmp}/{tgz} s3://{bucket}/{site}/{tgz}"""
                .format(tmp='/tmp',tgz=tgz,bucket=s3bucket,site=env.site))
        run('rm %s', tgz)
@task
def backup_db(dbname):
    run('which mysql')
 
main()
