from time import gmtime, strftime
from fabric.api import task, settings, cd, hide, run, env

from base import Component, s3_upload, s3_file_exists, s3_latest_file_in_bucket

class MysqlComponent(Component):
    def __init__(self, site_name, raw_data):
        super(type(self), self).__init__(site_name, raw_data)

    def backup(self):
        with settings(host_string=self.host_string):
            backup_mysql(self.site_name, self.db_name, self.db_user)

    def status(self):
        date = s3_latest_file_in_bucket(env.s3_bucket, self.site_name)
        print("%s last backed up: %s" % (self.__class__.__name__, date))

@task
def backup_mysql(site_name, dbname, dbuser):
    date = strftime("%Y.%m.%d", gmtime())
    gpg_file = 'sql-%s.sql.gz.gpg' % date
    local_file = "%s/vakap-%s" % ('/tmp', gpg_file)
    s3_dest = "s3://%s/%s/%s" % (env.s3_bucket, site_name, gpg_file)
    if s3_file_exists(s3_dest):
        print "  - File exists: %s. Skipping." % s3_dest
        return
    else:
        print "  - Dumping and encrypting database: %s" % dbname
        run("""mysqldump -u {dbuser} --add-drop-table {dbname} \
            | gzip | gpg --encrypt --recipient {key} > {local_file}"""
            .format(dbuser=dbuser, dbname=dbname, key=env.gpg_key,
                local_file=local_file))
        s3_upload(local_file, s3_dest)
