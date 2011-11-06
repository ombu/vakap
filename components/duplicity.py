from fabric.decorators import task
from fabric.api import settings, cd, hide, run, env

from base import Component

class DuplicityComponent(Component):
    """ Backup a path with [Duplicity](http://duplicity.nongnu.org/) """
    def __init__(self, site_name, raw_data):
        super(type(self), self).__init__(site_name, raw_data)

    def backup(self):
        with settings(host_string=self.host_string):
            backup_files(self.site_name, self.site_path)

@task
def backup_files(site_name, path):
    from time import gmtime, strftime
    s3_dest = "s3+http://%s/%s/%s" % (env.s3_bucket, site_name, 'duplicity')
    print "  - Running Duplicity on directory: %s" % path
    with hide('running', 'stdout'):
        run("AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s duplicity \
                --encrypt-key %s --full-if-older-than 30D %s %s" %
            (env.s3_access_key, env.s3_secret, env.gpg_key, path, s3_dest))
