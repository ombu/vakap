from fabric.decorators import task
from fabric.api import settings, cd, run, env
from fabric.contrib.files import exists as file_exists
from base import Component, s3_upload, s3_file_exists, s3_latest_file_in_bucket


class TgzComponent(Component):
    def __init__(self, site_name, raw_data):
        super(TgzComponent, self).__init__(site_name, raw_data)

    def backup(self):
        with settings(host_string=self.host_string):
            try:
                backup_files(self.site_name, self.site_path, self.tmpdir)
            except AttributeError:
                backup_files(self.site_name, self.site_path)

    def status(self):
        date = s3_latest_file_in_bucket(env.s3_bucket, self.site_name)
        print("%s last backed up: %s" % (self.__class__.__name__, date))


@task
def backup_files(site_name, path, tmpdir='/tmp'):
    from time import gmtime, strftime
    with cd(path):
        date = strftime("%Y.%m.%d", gmtime())
        gpg_file = 'files-%s.tgz.gpg' % date
        local_file = "%s/vakap-%s" % (tmpdir, gpg_file)
        s3_dest = "s3://%s/%s/%s" % (env.s3_bucket, site_name, gpg_file)
        if s3_file_exists(s3_dest):
            print "  - File exists: %s. Skipping" % s3_dest
            return
        else:
            print "  - Taring and gziping directory: %s => %s" % (path, tmpdir)
            if file_exists('current'):
                run("tar czh current | gpg --encrypt --recipient %s > %s" %
                    (env.gpg_key, local_file))
            else:
                run("tar czh . | gpg --encrypt --recipient %s > %s" %
                    (env.gpg_key, local_file))
            s3_upload(local_file, s3_dest)