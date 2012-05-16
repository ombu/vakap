from fabric.api import hide, run, env

class Component(object):
    """ Component Parent Class """
    def __init__(self, site_name, raw_data):
        self.site_name = site_name
        self.raw_data = raw_data
        self.__dict__.update(raw_data)

    @staticmethod
    def factory(site_name, component):
        from mysql import MysqlComponent
        from tgz import TgzComponent
        from postgres import PostgresComponent
        from duplicity import DuplicityComponent
        return eval(component["type"])(site_name, component)

""" Base Utilities """

def s3_upload(src, dst):
    """ Upload a path to S3 """
    print "  - Uploading: %s" % dst
    try:
        run("s3cmd --acl-public --human-readable-sizes put %s %s" % (src, dst))
    finally:
        run('rm %s' % src)

def s3_file_exists(s3_path):
    """ Whether a file exists on S3 """
    return bool(s3_path in run("s3cmd ls %s" % s3_path))

def s3_list(s3_path):
    return run("s3cmd ls %s" % s3_path)

def s3_latest_file_in_bucket(bucket, prefix):
    from boto.s3.connection import S3Connection
    from datetime import datetime
    import re
    conn = S3Connection(env.s3_access_key, env.s3_secret)
    keys = []
    l = conn.get_bucket(bucket).list(prefix)
    for i in l:
        m = re.search(r"\d{4}\.\d{2}\.\d{2}", i.key)
        if(m):
            keys.append({
                'date':  datetime.strptime(m.group(0), "%Y.%m.%d"),
                'key':  i.key,
            })
    keys = sorted(keys, key=lambda k: k['date'])
    if(len(keys)):
        return keys.pop()['date']
    else:
        return "Never?"
