#! /usr/bin/env python
import sys
from optparse import OptionParser
import json
from fabric.api import * 
from pprint import pprint

env.key_filename = ['/Users/axolx/.ssh/axolx-base']
env.s3_bucket = 'backup.ombuweb.com'
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
        for component in site["components"]:
            c = Component.factory(site["name"], component)
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
    def factory(site_name, component):
        return eval(component["type"])(site_name, component)

    def __init__(self, site_name, raw_data):
        self.site_name = site_name 
        self.raw_data = raw_data
        self.__dict__.update(raw_data)

class TgzComponent(Component):
    def __init__(self, site_name, raw_data):
        super(type(self), self).__init__(site_name, raw_data)

    def backup(self):
        with settings(host_string=self.host_string):
            backup_files(self.site_name, self.site_path)


class MysqlComponent(Component):
    def __init__(self, site_name, raw_data):
        super(type(self), self).__init__(site_name, raw_data)

    def backup(self):
        with settings(host_string=self.host_string):
            backup_mysql(self.site_name, self.db_name, self.db_user)
# @task
# def get_ref(path):
#     with cd(path): 
#         foo = run('readlink current')
#         print foo

@task
def backup_files(site_name, path):
    from time import gmtime, strftime
    with cd(path):
        date = strftime("%Y.%m.%d", gmtime())
        gpg_file = 'files-%s.tgz.gpg' % date
        local_file = "%s/vakap-%s" % ('/tmp', gpg_file)
        run("tar czh current | gpg --encrypt --recipient %s > %s" %
            (env.gpg_key, local_file))
        s3_dest = "s3://%s/%s/%s" % (env.s3_bucket, site_name, gpg_file)
        s3_upload(local_file, s3_dest)

@task
def backup_mysql(site_name, dbname, dbuser):
    from time import gmtime, strftime
    date = strftime("%Y.%m.%d", gmtime())
    gpg_file = 'sql-%s.gz.gpg' % date
    local_file = "%s/vakap-%s" % ('/tmp', gpg_file)
    run("""mysqldump -u {dbuser} --add-drop-table {dbname} \
            | gzip | gpg --encrypt --recipient {key} > {local_file}"""
            .format(dbuser=dbuser, dbname=dbname, key=env.gpg_key,
                local_file=local_file))
    s3_dest = "s3://%s/%s/%s" % (env.s3_bucket, site_name, gpg_file)
    s3_upload(local_file, s3_dest)

def s3_upload(src, dst):
    run("s3cmd --acl-public --human-readable-sizes put %s %s" % (src, dst))
    run('rm %s' % src)

main()
