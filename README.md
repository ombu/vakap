vakap
=====

**This is a work in progress, subject to major refactoring. Use at your own
risk. If you find it useful, I'd love to hear about it, and get feedback.**

I built *vakap* to help manage the sites hosted by OMBU. It's meant for managing
sites, not servers. The original scope was to handle backups, but it's
structured to allow any operation on a site, such as cron.

## What it does
- Allows to run a command on a list of sites (e.g. back them up)
- Stores backups in Amazon S3
- Encrypts files with `gnupg` before sending to S3

## Commands
### Implemented
- list: list managed sites
- backup: backup sites

### Planned
- rotate backups (e.g. delete older files from S3)
- run maintenance scripts on sites
- report site metadata, such as currenly deployed VCS revision 

## Components

### General
All commands require the following arguments:

- _host\_string_: The fabric host string where the database lives

### MysqlComponent
Backup a MySQL database. Arguments:

- _db\_name_: The database name
- _db\_user_: The database user name. This user must have sufficient privilege in
  the host to run `mysqldump` on this database without requiring a password

### PostgresComponent
Same functionality as MysqlComponent for PostgreSQL databases.

### TgzComponent
Tar & gzip a directory (follow symlinks). Arguments:

- _db\_name_: The database name

### DuplicityComponent
Same functionality as MysqlComponent for PostgreSQL databases.

## Dependencies
- Client: `python` and [Fabric](http://docs.fabfile.org)
- Hosts: `s3cmd`, `gnupg` with a [trusted public
  key](http://www.gnupg.org/gph/en/manual.html#AEN346) for encryption

## Setup
- Provide a settings file (vakap will look for settings.json). See
  `settings.sample.json` for an exmaple .
- Site hosts must have [s3cmd](http://s3tools.org/s3cmd) installed and
  configured.
- Site hosts must have the gpg public key in their keyring

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
