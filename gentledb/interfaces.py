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
    def __add__(self, content): pass
    def __sub__(self, content_id): pass
    def __invert__(self): pass
    def __setitem__(self, pointer_id, content_id): pass
    def __getitem__(self, pointer_id): pass
    def __call__(self, *args): pass

class GentleDBFull(GentleDB):
    def findc(self, content_id): pass
    def findp(self, pointer_id): pass
