from time import gmtime, strftime
from fabric.api import task, settings, run, env
from base import BaseComponent, s3_upload, s3_file_exists, \
    s3_latest_file_in_bucket


class Component(BaseComponent):
    def __init__(self, site_name, raw_data):
        super(Component, self).__init__(site_name, raw_data)
        try:
            self.db_name = raw_data['db_name']
            self.db_user = raw_data['db_user']
        except KeyError:
            print "- Error. The component %s requires `db_name` and " \
                  "`db_user` parameters. Skipping." % __name__

    def backup(self):
        with settings(host_string=self.host_string):
            backup_mysql(self.site_name, self.db_name, self.db_user)

    def status(self):
        date = s3_latest_file_in_bucket(env.s3_bucket, self.site_name)
        print("%s last backed up: %s" % (self.__class__.__name__, date))


@task
def backup_mysql(site_name, db_name, db_user):
    date = strftime("%Y.%m.%d", gmtime())
    gpg_file = 'sql-%s.sql.gz.gpg' % date
    local_file = "%s/vakap-%s" % ('/tmp', gpg_file)
    s3_path = "s3://%s/%s/%s" % (env.s3_bucket, site_name, gpg_file)
    if s3_file_exists(s3_path):
        print "  - File exists: %s. Skipping." % s3_path
        return
    else:
        print "  - Dumping and encrypting database: %s" % db_name
        run("""mysqldump -u {db_user} --add-drop-table {db_name} \
            | gzip | gpg --encrypt --recipient {key} > {local_file}"""
            .format(db_user=db_user, db_name=db_name, key=env.gpg_key,
                    local_file=local_file))
        s3_upload(local_file, s3_path)
