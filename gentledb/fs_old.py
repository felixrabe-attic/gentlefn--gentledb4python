#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011  Felix Rabe (www.felixrabe.net)
#
# GentleDB is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# GentleDB is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with GentleDB.  If not, see <http://www.gnu.org/licenses/>.

import os

from . import fs, interfaces


class GentleDB(fs.GentleDB):

    USER_HOME = os.path.expanduser("~")
    FS_DEFAULT_DIRECTORY = os.path.join(USER_HOME, ".gentle_tp_da92_default_datastore")
    FS_DEFAULT_ENVIRON_KEY = "GENTLE_TP_DA92_DIR"

    def __init__(self, directory=True, environ_key=True):
        # 'directory' is 'None' only if 'None' has been specified explicitly:
        if directory is None:  # bypass environment variables and just use default dir
            directory = self.FS_DEFAULT_DIRECTORY
        if directory is True:  # i.e. not specified, use environment variable if set
            directory = self.FS_DEFAULT_DIRECTORY
            # 'environ_key' is 'None' only if 'None' has been specified explicitly:
            if environ_key is not None:
                if environ_key is True:  # i.e. not specified
                    environ_key = self.FS_DEFAULT_ENVIRON_KEY
                directory = os.environ.get(environ_key, directory)
        super(GentleDB, self).__init__(directory)

    def _id_to_path(self, directory, id, create_dir=True):
        return os.path.join(directory, id)


class GentleDBFull(interfaces.GentleDBFull, GentleDB):
    pass
