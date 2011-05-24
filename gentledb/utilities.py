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

import os

def random(prefix=""):
    """
    Return a random-generated 256-bit number in hexadecimal representation.

    These numbers are suitable as pointer identifiers.

    A prefix may be specified, in which case the resulting number will start
    with the specified prefix.  This option should be used only rarely.  It is
    considered bad practice, as using prefixes goes against the even (random)
    distribution of GentleDB (content and pointer) identifiers.
    """
    validate_identifier(prefix, partial=True)
    n = os.urandom(256 / 8).encode("hex")
    return prefix + n[len(prefix):]

def create_file_with_mode(filename, mode):
    return os.fdopen(os.open(filename, os.O_CREAT | os.O_WRONLY, mode), "wb")

IDENTIFIER_LENGTH = 256 / 4
IDENTIFIER_DIGITS = "0123456789abcdef"

class GentleDBException(Exception):
    """
    Base class for all exceptions originating in Gentle.
    """

class InvalidIdentifierException(GentleDBException, LookupError):
    """
    Invalid Gentle identifier.
    """
    def __init__(self, bad_identifier):
        super(InvalidIdentifierException, self).__init__("Bad identifier: %r" %
                                                         bad_identifier)

def is_identifier_valid(identifier, partial=False):
    if not isinstance(identifier, basestring): return False
    if not (len(identifier) <= IDENTIFIER_LENGTH and
            all(c in IDENTIFIER_DIGITS for c in identifier)):
        return False
    if partial or len(identifier) == IDENTIFIER_LENGTH: return True
    return False

def validate_identifier(identifier, partial=False):
    if not is_identifier_valid(identifier, partial):
        raise InvalidIdentifierException(identifier)
