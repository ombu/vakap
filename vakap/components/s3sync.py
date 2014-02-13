from fabric.decorators import task
from fabric.api import settings, run
from base import BaseComponent


class Component(BaseComponent):
    """ Sync a path to S3 with [aws-cli](https://github.com/aws/aws-cli) """

    def __init__(self, site_name, raw_data):
        super(Component, self).__init__(site_name, raw_data)
        try:
            self.site_path = raw_data['db_name']
        except KeyError:
            print "- Error. The component %s requires `site_path` parameter." \
                  " Skipping." % __name__

    def backup(self):
        with settings(host_string=self.host_string):
            backup_files(self.site_name, self.site_path)


@task
def backup_files(site_name, path, bucket='s3://files.ombuweb.com',
                 region='us-west-2'):
    print "  - Running s3sync on directory: %s" % path
    run('aws --region=%s s3 sync %s %s/%s' %
        (region, path, bucket, site_name))
