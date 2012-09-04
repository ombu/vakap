vakap
=====

*vakap* is a site manager, originally intended to automate backups of sites
hosted by OMBU.  However, it's architecture allows any operation on sites, such
as executing maintenance scripts, rotating logs etc.

This is currently a work in progress so if you use it, do so at your own risk.
If you find it useful, I'd love to hear your feedback.

What it does
------------

- Allows running a command on a list of sites, such as backing them up.
- Stores backups in Amazon S3.
- Encrypts files client-side with `gnupg` before sending to S3.

Commands
--------

### Implemented

- `list`: Lists managed sites
- `backup`: Backs-up sites
- `status`: Report on a site, such as when it was last backed-up

### Planned

There's a milestone in the bugtracker for [Planned & Proposed
Components](https://github.com/ombu/vakap/issues?milestone=3)

Components
----------

### General
All commands require the following arguments:

- `host_string`: The fabric host string where the database lives.

### MysqlComponent
Backup a MySQL database. Arguments:

- `db_name`: The database name.
- `db_user`: The database user name. This user must have sufficient privilege in
  the host to run `mysqldump` on this database without requiring a password.

### PostgresComponent
Same options as MysqlComponent.

### TgzComponent
Tar & gzip a directory (follows symlinks). Arguments:

- `db_name`: The database name

### DuplicityComponent
Same options as TgzComponent.

Dependencies
------------

- Client: Python and [Fabric](http://docs.fabfile.org)
- Hosts: `s3cmd`, `gnupg` with a [trusted public
  key](http://www.gnupg.org/gph/en/manual.html#AEN346) for encryption

Setup
-----

- Provide a settings file (vakap will look for settings.json). See
  `settings.sample.json` for an exmaple .
- Site hosts must have [s3cmd](http://s3tools.org/s3cmd) installed and
  configured.
- Site hosts must have the gpg public key in their keyring

Build
-----

To build the egg:

    python setup.py sdist

More info at: <http://docs.python.org/distutils>

License
-------

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

