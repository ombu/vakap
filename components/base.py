from fabric.api import hide, run

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
        return eval(component["type"])(site_name, component)

""" Base Utilities """

def s3_upload(src, dst):
    """ Upload a path to S3 """
    print "  - Uploading to S3: %s" % dst
    with hide('running', 'stdout'):
        try:
            run("s3cmd --acl-public --human-readable-sizes put %s %s" % (src, dst))
        finally:
            run('rm %s' % src)