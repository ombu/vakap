from fabric.decorators import task
from fabric.api import settings, cd, hide, run, env

from base import Component, s3_upload, s3_file_exists, s3_list

class TgzComponent(Component):
    def __init__(self, site_name, raw_data):
        super(type(self), self).__init__(site_name, raw_data)

    def backup(self):
        with settings(host_string=self.host_string):
            backup_files(self.site_name, self.site_path)

    def check(self):
        s3_path = "s3://%s/%s/" % (env.s3_bucket, self.site_name)
        with settings(host_string=self.host_string):
            print run(s3_list(s3_path))

@task
def backup_files(site_name, path):
    from time import gmtime, strftime
    with cd(path):
        date = strftime("%Y.%m.%d", gmtime())
        gpg_file = 'files-%s.tgz.gpg' % date
        local_file = "%s/vakap-%s" % ('/tmp', gpg_file)
        s3_dest = "s3://%s/%s/%s" % (env.s3_bucket, site_name, gpg_file)
        if s3_file_exists(s3_dest):
            print "  - File exists: %s. Skipping" % s3_dest
            return
        else:
            print "  - Taring and gziping directory: %s" % path
            with hide('running', 'stdout'):
                run("tar czh current | gpg --encrypt --recipient %s > %s" %
                    (env.gpg_key, local_file))
            s3_upload(local_file, s3_dest)
