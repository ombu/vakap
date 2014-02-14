from datetime import datetime
import json
from fabric.decorators import task, settings
from fabric.api import run
from .base import BaseComponent


class Component(BaseComponent):
    """ Sync a path to S3 with [aws-cli](https://github.com/aws/aws-cli) """

    def __init__(self, site_name, raw_data):
        super(Component, self).__init__(site_name, raw_data)
        try:
            self.region = raw_data['region']
            self.volume_id = raw_data['volume_id']
        except KeyError:
            print "- Error. The component %s requires `region` and " \
                  "`volume_id` parameters. Skipping." % __name__

    def backup(self):
        snapshot_name = '%s-%s' % (
            self.site_name,
            datetime.now().strftime('%Y.%m.%d')
        )
        with settings(host_string=self.host_string):
            ebs_snapshot(self.region, self.volume_id, snapshot_name)


@task
def ebs_snapshot(region, volume_id, snapshot_name):
    print "  - Making an EBS snapshot of %s" % volume_id
    result = run('aws --region=%s ec2 create-snapshot --volume-id %s '
                 '--description "Created by vakap"' % (region, volume_id))
    result = json.loads(result)
    run('aws --region=%s ec2 create-tags --resources %s --tags Key=Name,'
        'Value=%s' % (region, result['SnapshotId'], snapshot_name))
