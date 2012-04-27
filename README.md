vakap
=====

I built *vakap* to help manage the sites hosted by OMBU. It's meant for managing
sites, not servers. The original scope was to handle backups, but it's
structured to allow any operation on a site, such as a log rotation.

**Warning:** This is a work in progress, subject to major refactoring. Use at your own
risk. If you find it useful, I'd love to hear about it, and get feedback.


## What it does

- Allows to run a command on a list of sites (e.g. back them up).
- Stores backups in Amazon S3.
- Encrypts files client-side with `gnupg` before sending to S3.

## Commands

### Implemented

- `list`: List managed sites.
- `backup`: Backup sites.
- `status`: When appropriate, reports date of componenet execution. For example,
  the last backup date.

### Planned

- Rotate backups (e.g. delete older files from S3).
- Run maintenance scripts on sites.
- Report site metadata, such as currenly deployed VCS revision.

## Components

### General
All commands require the following arguments:

- `host_string`: The fabric host string where the database lives.

### MysqlComponent
Backup a MySQL database. Arguments:

- `db_name`: The database name.
- `db_user`: The database user name. This user must have sufficient privilege in
  the host to run `mysqldump` on this database without requiring a password.

### PostgresComponent
Same functionality as MysqlComponent for PostgreSQL databases.

### TgzComponent
Tar & gzip a directory (follow symlinks). Arguments:

- `db_name`: The database name

### DuplicityComponent
Same functionality as MysqlComponent for PostgreSQL databases.

## Dependencies
- Client: Python and [Fabric](http://docs.fabfile.org)
- Hosts: `s3cmd`, `gnupg` with a [trusted public
  key](http://www.gnupg.org/gph/en/manual.html#AEN346) for encryption

## Setup
- Provide a settings file (vakap will look for settings.json). See
  `settings.sample.json` for an exmaple .
- Site hosts must have [s3cmd](http://s3tools.org/s3cmd) installed and
  configured.
- Site hosts must have the gpg public key in their keyring

## License

Copyright (c) 2012, OMBU Inc. http://ombuweb.com
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

- Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

- Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

- Neither the name of OMBU INC. nor the names of its contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL OMBU INC. BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

