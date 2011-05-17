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

from . import interfaces, utilities


class GentleDBEasy(interfaces.GentleDBFull):
    """
    Wrapper for GentleDBFull tailored to interactive use.

    This allows the user to specify partial identifiers wherever this makes
    sense.
    """

    def __init__(self, db):
        super(GentleDBEasy, self).__init__()
        self.db = db

    def _find_single_id(self, partial_id, find):
        if len(partial_id) == 64:
            return partial_id
        else:
            found_ids = find(partial_id)
        if len(found_ids) != 1:
            raise utilities.GentleDBException(
                "Number of identifiers starting with %r is != 1" % partial_id)
        return found_ids[0]

    def _find_single_content_id(self, partial_content_id):
        return self._find_single_id(partial_content_id, self.db.findc)

    def _find_single_pointer_id(self, partial_pointer_id):
        return self._find_single_id(partial_pointer_id, self.db.findp)

    def __add__(self, content):
        return self.db + content

    def __sub__(self, partial_content_id):
        content_id = self._find_single_content_id(partial_content_id)
        return self.db - content_id

    def __invert__(self):
        return ~self.db

    def __setitem__(self, partial_pointer_id, partial_content_id):
        pointer_id = self._find_single_pointer_id(partial_pointer_id)
        content_id = self._find_single_content_id(partial_content_id)
        self.db[pointer_id] = content_id

    def __getitem__(self, partial_pointer_id):
        pointer_id = self._find_single_pointer_id(partial_pointer_id)
        return self.db[pointer_id]

    def __call__(self, *args):
        if len(args) == 0:
            return self.db()
        else:
            content_id = self._find_single_content_id(args[0])
            return self.db(content_id)

    def findc(self, partial_content_id=""):
        return self.db.findc(partial_content_id)

    def findp(self, partial_pointer_id=""):
        return self.db.findp(partial_pointer_id)

    def __getattr__(self, name):
        return getattr(self.db, name)
