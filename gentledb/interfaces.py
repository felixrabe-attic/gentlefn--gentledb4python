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

class GentleDB(object):
    """
    A GentleDB instance.
    """

    def __add__(self, content):
        """
        Enter content into the database and return its content identifier.

        The content identifier is a hash value of the content.  The current
        implementation uses the SHA-256 value of the content as the content
        identifier.

        This method gives priority to pre-existing content.  This means that
        content will not be saved if its hash value already exists as a key in
        the database.

        Example:
        >>> content_id = db + "some content"
        """

    def __sub__(self, content_id):
        """
        Get content from the database.
        """

    def __invert__(self):
        """
        Return a random-generated 256-bit number in hexadecimal representation.

        These numbers are suitable as identifiers in a pointer database.

        Example:
        >>> new_identifier = ~db
        """

    def __setitem__(self, pointer_id, content_id):
        """
        Create, change, or remove a pointer in the pointer database.

        A pointer can be removed by providing None or the empty string "" as the
        content_id.
        """

    def __delitem__(self, pointer_id):
        "Same as: self[pointer_id] = None"
        return self.__setitem__(pointer_id, None)

    def __getitem__(self, pointer_id):
        """
        Retrieve the content_id the given pointer_id points to.
        """

    def __call__(self, content_id=None):
        """
        Get or store content by providing a file-like interface.

        Return a file-like object.

        Examples:
        >>> file_to_write = db()
        >>> file_to_write.write(content)
        >>> content_id = file_to_write()  # __call__() also calls close()
        >>> file_to_read = db(content_id)
        >>> content = file_to_read.read()
        """

class GentleDBFull(GentleDB):
    """
    A GentleDB that provides more methods which depend on direct access to the
    underlying data store.
    """

    def findc(self, partial_content_id=""):
        """
        Find all content identifiers registered in this database that start with
        partial_content_id.  Return an unsorted list.  The list may be empty.

        If partial_content_id is not specified (default is ""), return the full
        list of all content identifiers in the database.
        """

    def findp(self, partial_pointer_id=""):
        """
        Find all pointer identifiers registered in this database that start with
        partial_pointer_id.  Return an unsorted list.  The list may be empty.

        If partial_pointer_id is not specified (default is ""), return the full
        list of all pointer identifiers in the database.
        """
