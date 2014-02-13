from fabric.decorators import task
from fabric.api import settings, run, env, local
from base import BaseComponent


class Component(BaseComponent):
    """ Backup a path with [Duplicity](http://duplicity.nongnu.org/) """

    def __init__(self, site_name, raw_data):
        super(Component, self).__init__(site_name, raw_data)
        try:
            self.site_path = raw_data['site_path']
        except KeyError:
            print "- Error. The component %s requires `site_path` parameter." \
                  " Skipping." % __name__

    def backup(self):
        with settings(host_string=self.host_string):
            backup_files(self.site_name, self.site_path)

    def status(self):
        with settings(host_string=self.host_string):
            s3_dest = _get_dest(self.site_name)
            run("AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s duplicity \
                    collection-status %s" % (env.s3_access_key, env.s3_secret,
                                             s3_dest))

    def clean(self):
        with settings(host_string=self.host_string):
            s3_dest = _get_dest(self.site_name)
            local("AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s duplicity "
                  "--force  remove-all-but-n-full 1 %s" % (
                  env.s3_access_key, env.s3_secret, s3_dest))
            local("AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s duplicity "
                  "cleanup --force %s" % (
                  env.s3_access_key, env.s3_secret, s3_dest))


@task
def backup_files(site_name, path):
    s3_dest = _get_dest(site_name)
    print "  - Running Duplicity on directory: %s" % path
    run("AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s duplicity \
            -v2 --volsize=256 --asynchronous-upload \
            --exclude %s/logs \
            --archive-dir /tmp/duplicity-cache \
            --encrypt-key %s --full-if-older-than 30D %s %s" %
        (env.s3_access_key, env.s3_secret, path, env.gpg_key, path, s3_dest))


def _get_dest(name):
    return "s3+http://%s/%s/%s" % (env.s3_bucket, name, 'duplicity')
