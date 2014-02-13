from fabric.decorators import task
from fabric.api import settings, cd, run, env
from fabric.contrib.files import exists as file_exists
from base import BaseComponent, s3_upload, s3_file_exists, \
    s3_latest_file_in_bucket


class Component(BaseComponent):

    def __init__(self, site_name, raw_data):
        super(Component, self).__init__(site_name, raw_data)
        try:
            self.site_path = raw_data['site_path']
        except KeyError:
            print "- Error. The component %s requires `site_path` parameter." \
                  " Skipping." % __name__
        # Optional parameters
        self.temp_dir = getattr(raw_data, 'temp_dir', '/tmp')

    def backup(self):
        with settings(host_string=self.host_string):
            try:
                backup_files(self.site_name, self.site_path, self.temp_dir)
            except AttributeError:
                backup_files(self.site_name, self.site_path)

    def status(self):
        date = s3_latest_file_in_bucket(env.s3_bucket, self.site_name)
        print("%s last backed up: %s" % (self.__class__.__name__, date))


@task
def backup_files(site_name, path, temp_dir):
    from time import gmtime, strftime
    with cd(path):
        date = strftime("%Y.%m.%d", gmtime())
        gpg_file = 'files-%s.tgz.gpg' % date
        local_file = "%s/vakap-%s" % (temp_dir, gpg_file)
        s3_path = "s3://%s/%s/%s" % (env.s3_bucket, site_name, gpg_file)
        if s3_file_exists(s3_path):
            print "  - File exists: %s. Skipping" % s3_path
            return
        else:
            print "  - Taring and gziping directory: %s => %s" % \
                  (path, temp_dir)
            if file_exists('current'):
                run("tar czh current | gpg --encrypt --recipient %s > %s" %
                    (env.gpg_key, local_file))
            else:
                run("tar czh . | gpg --encrypt --recipient %s > %s" %
                    (env.gpg_key, local_file))
            s3_upload(local_file, s3_path)