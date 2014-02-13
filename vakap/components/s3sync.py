from fabric.decorators import task
from fabric.api import settings, run
from base import Component


class S3SyncComponent(Component):
    """ Sync a path to S3 with [aws-cli](https://github.com/aws/aws-cli) """

    def backup(self):
        with settings(host_string=self.host_string):
            backup_files(self.site_name, self.site_path)


@task
def backup_files(site_name, path, bucket='s3://files.ombuweb.com',
                 region='us-west-2'):
    print "  - Running s3sync on directory: %s" % path
    run('aws --region=%s s3 sync %s %s/%s' %
        (region, path, bucket, site_name))
