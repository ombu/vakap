#! /usr/bin/env python
import json
from fabric.api import * 
from pprint import pprint

env.key_filename = ['/Users/axolx/.ssh/axolx-base']

def main():
    sites = parse_sites('sites.json')
    for site in sites:
        print '+ Processing site %s' % site["name"]
        for component in site["components"]:
            c = Component.factory(component)
            c.run()

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

    def run(self):
        print "  Running %s on %s" % (type(self).__name__, self.hostString)
        self._run()

class TgzComponent(Component):
    def __init__(self, componentRawData):
        super(type(self), self).__init__(componentRawData)
        self.command = "tar czf foo.tgz bar" 

    def _run(self):
        with settings(host_string=self.hostString):
            getRef(self.sitePath)

class MysqlComponent(Component):
    def __init__(self, componentRawData):
        super(type(self), self).__init__(componentRawData)
        self.command = "mysqldump bar" 

    def _run(self):
        with settings(host_string=self.hostString):
            showDb(self.dbName)

@task
def getRef(path):
    with cd(path): 
        foo = run('readlink current')
        print foo


@task
def showDb(dbName):
    print('Implement me')
 
main()
