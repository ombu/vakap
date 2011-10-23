vakap
=====

I build vakap to me manage the sites hosted by OMBU on Amazon AWS. It is meant
to help manage sites, not servers. Initially it was going to be exclusively a
backup script, but I quickly realized it could easily provide other
functionality necessary to manage sites. My goal is to make it useful to one
purpose rather than be a general purpose tool.

## What it does

- Allows to run a command on a list of sites (e.g. back them up)
- Backs up to Amazon S3
- Encrypts content with `gnupg` before sending it to S3

## Commands
### Implemented
- backup

### Planned
- rotate backups (e.g. delete older files from S3)
- list sites
- perform an http request on sites
- Get revision deployed for a site and deployment metadata 

## Components

### General
All commands require the following arguments:

- _host\_string_: The fabric host string where the database lives

### MysqlComponent
Backup a MySQL database. Arguments:

- _db\_name_: The database name
- _db\_user_: The database user name. This user must have sufficient privilege in
  the host to run `mysqldump` on this database without requiring a password

### TgzComponent
Tar & gzip a directory (follow symlinks). Arguments:

- _db\_name_: The database name

## Dependencies
- Client: `python` and [Fabric](http://docs.fabfile.org)
- Hosts: `s3cmd`, `gnupg` with a [trusted public
  key](http://www.gnupg.org/gph/en/manual.html#AEN346) for encryption

## Setup
- Provide a hosts file (vakap will look for hosts.json). Hosts file should look
  like:

        [
          {
            "name": "vv-stage",
            "components" : [
              {
                "type": "MysqlComponent",
                "host_string": "ombu@d2:34165",
                "db_name": "veritableveg",
                "db_user": "backup"
              },
              {
                "type": "TgzComponent",
                "host_string": "ombu@d2:34165",
                "site_path": "/mnt/main/qa/qa3"
              }
            ]
          }
        ]

- All hosts must have [s3cmd](http://s3tools.org/s3cmd) installed and
  configured.
- Provide an Amazon S3 bucket that the host's s3cmd can write to.

## License

Copyright (c) 2011 OMBU martin@ombuweb.com, except where otherwise
noted.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

The Software shall be used for Good, not Evil.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
