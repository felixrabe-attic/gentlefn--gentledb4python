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

from __future__ import absolute_import, print_function

import glob
from hashlib import sha256
import os
import tempfile

from . import interfaces, utilities


class GentleDB(interfaces.GentleDB):

    def __init__(self, directory=None):
        super(GentleDB, self).__init__()
        self.directory = directory or os.path.expanduser("~/.gentledb")
        self.directory = os.path.abspath(self.directory)
        self.content_dir = os.path.join(self.directory, "content_db")
        self.pointer_dir = os.path.join(self.directory, "pointer_db")
        self.tmp_dir = os.path.join(self.directory, "tmp")
        for directory in (self.directory, self.content_dir, self.pointer_dir,
                          self.tmp_dir):
            if not os.path.exists(directory):
                try:
                    os.mkdir(directory, 0700)
                except:
                    raise utilities.GentleDBException(
                        "Could not create directory %r" % directory)

    def _id_to_path(self, directory, id, create_dir=True):
        idpath = filter(bool, (id[:2], id[2:4], id[4:7], id[7:]))
        directory = os.path.join(directory, *idpath[:-1])
        if create_dir:
            if not os.path.exists(directory):
                os.makedirs(directory)
        return os.path.join(directory, idpath[-1])

    def _get_content_filename(self, *a, **k):
        return self._id_to_path(self.content_dir, *a, **k)

    def _get_pointer_filename(self, *a, **k):
        return self._id_to_path(self.pointer_dir, *a, **k)

    def _find_partial_id(self, directory, partial_id):
        id = partial_id + (64 - len(partial_id)) * "?"
        path_to_glob = self._id_to_path(directory, id, create_dir=False)
        found = glob.glob(path_to_glob)
        found = [f[len(directory):].replace(os.sep, "") for f in found]
        return found

    def __add__(self, content):
        content_id = sha256(content).hexdigest()
        filename = self._get_content_filename(content_id, create_dir=True)
        if not os.path.exists(filename):
            with utilities.create_file_with_mode(filename, 0400) as f:
                f.write(content)
        return content_id

    def __sub__(self, content_id):
        utilities.validate_identifier(content_id)
        filename = self._get_content_filename(content_id, create_dir=False)
        content = open(filename, "rb").read()
        return content

    def __invert__(self):
        return utilities.random()

    def __setitem__(self, pointer_id, content_id):
        utilities.validate_identifier(pointer_id)
        if content_id:
            utilities.validate_identifier(content_id)
            filename = self._get_pointer_filename(pointer_id, create_dir=True)
            with utilities.create_file_with_mode(filename, 0600) as f:
                f.write(content_id)
        else:  # remove pointer
            filename = self._get_pointer_filename(pointer_id, create_dir=False)
            if os.path.exists(filename):
                os.remove(filename)
        return pointer_id

    def __getitem__(self, pointer_id):
        utilities.validate_identifier(pointer_id)
        filename = self._get_pointer_filename(pointer_id, create_dir=False)
        content_id = open(filename, "rb").read()
        return content_id

    def __call__(self, *args):
        if len(args) == 0:      # ex.: f=db() ; f.write(content) ; content_id=f()
            return _OutFile(self)
        else:                   # ex.: f=db(content_id) ; content=f.read()
            return _InFile(self, args[0])


class GentleDBFull(interfaces.GentleDBFull, GentleDB):

    def findc(self, partial_content_id=""):
        utilities.validate_identifier(partial_content_id, partial=True)
        content_ids = self._find_partial_id(self.content_dir, partial_content_id)
        return content_ids

    def findp(self, partial_pointer_id=""):
        utilities.validate_identifier(partial_pointer_id, partial=True)
        pointer_ids = self._find_partial_id(self.pointer_dir, partial_pointer_id)
        return pointer_ids


class _OutFile(object):

    def __init__(self, db):
        super(_OutFile, self).__init__()
        self.db = db
        self.hash_obj = sha256()
        directory = os.path.join(self.db.directory, "tmp")
        self.tmpfile_f, self.tmpfile_path = tempfile.mkstemp(dir=directory)
        self.tmpfile = os.fdopen(self.tmpfile_f, "wb")
        self.is_open = True

    def write(self, data):
        self.hash_obj.update(data)
        self.tmpfile.write(data)

    def close(self):
        if not self.is_open:
            raise utilities.GentleDBException("File already closed")
        self.tmpfile.close()
        self.is_open = False
        content_id = self()
        filename = self.db._get_content_filename(content_id, create_dir=True)
        if not os.path.exists(filename):
            os.chmod(self.tmpfile_path, 0400)
            os.rename(self.tmpfile_path, filename)
        else:  # we do not overwrite existing content
            os.remove(self.tmpfile_path)

    def __call__(self):
        if self.is_open:
            self.close()
        content_id = self.hash_obj.hexdigest()
        return content_id

    def __del__(self):
        if self.is_open:
            self.close()


class _InFile(object):

    def __init__(self, db, content_id):
        super(_InFile, self).__init__()
        filename = db._get_content_filename(content_id, create_dir=False)
        self.content_file = open(filename, "rb")

    def read(self, size=-1):
        return self.content_file.read(size)
