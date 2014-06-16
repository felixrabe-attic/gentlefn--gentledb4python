GentleDB - The Simplest Database in the World (Python implementation)
=====================================================================

A database that even a non-scientist can understand.


Database operations
-------------------

* It can store and retrieve content:
    content_id      = db + <some content>
    <some content>  = db - content_id

* It can store and retrieve a pointer ID to a content ID:
    pointer_id      = ~db
    db[pointer_id]  = content_id
    content_id      = db[pointer_id]

Both IDs are lower-case hexadecimal string represenations of 256-bit values.
Content IDs are the SHA-256 sum of the respective content.  Pointer IDs are the
same format, but random-generated.  Pointer IDs are equivalent to file names.


Requirements
------------

* Python 2.6
* http://pypi.python.org/pypi/setuptools
  Probably already installed - try: python -c 'import setuptools'


Installation instructions
-------------------------

    python setup.py install


Tutorial
--------

    >>> from gentledb import Memory
    >>> db = Memory()
    >>> content_id = db + "Some content"            # store content
    >>> content_id                                  # SHA-256 of "Some content"
    '9c6609fc5111405ea3f5bb3d1f6b5a5efd19a0cec53d85893fd96d265439cd5b'
    >>> db - content_id                             # retrieve content
    'Some content'
    >>> pointer_id = ~db                            # random value to keep
    >>> db[pointer_id] = content_id                 # store pointer to content
    >>> db[pointer_id]                              # retrieve content from pointer
    '9c6609fc5111405ea3f5bb3d1f6b5a5efd19a0cec53d85893fd96d265439cd5b'


GentleDB for Python also supports
---------------------------------

* File-like objects instead of strings to store and retrieve content:
    f = db()
    f.write(content)
    content_id = f()

    f = db(content_id)
    content = f.read()

* Filesystem store:
    from gentledb import FS
    system_db = FS("/var/lib/gentledb")
    home_db = FS()  # path defaults to "$HOME/.gentledb"

* Network-transparent storage using ZeroMQ: (not yet included)
    from gentledb import Memory, ZeroMQ
    db = Memory()
    ZeroMQ(db, "tcp://127.0.0.1:9876").run()    # server

    from gentledb import ZeroMQ
    db = ZeroMQ("tcp://127.0.0.1:9876")         # client


Copyright statement
-------------------

Copyright (C) 2012  Felix Rabe (www.felixrabe.net)

GentleDB is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

GentleDB is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with GentleDB.  If not, see <http://www.gnu.org/licenses/>.


The file lgpl-2.1.txt, included in the library's distribution, contains the
license text.
