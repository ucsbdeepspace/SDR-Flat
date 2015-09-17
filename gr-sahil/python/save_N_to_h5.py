#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 <Sahil Mahajan>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 



import numpy
import h5py
from gnuradio import gr


class save_N_to_h5(gr.sync_block):
    """
saves N items to h5 file
    """
    def __init__(self, filename, num_items, vec_len):
        self.num_items = num_items
        self.vec_len = vec_len + 4
        self.filename = filename
        self.count = 0
	self.fileno = 0
	self.length = len(str(self.filename))
        gr.sync_block.__init__(self,
            name="save_N_to_h5",
            in_sig=[(numpy.float32,self.vec_len)],
            out_sig=None)
	self._h5 = h5py.File(name = (str(self.filename)[0:(self.length-3)] + '_%d' % self.fileno + str(self.filename)[(self.length-3):self.length]), mode = 'w')
        self.dset = self._h5.create_dataset('Spectral_Data', (self.count,self.vec_len), dtype = numpy.float64, maxshape=(None,self.vec_len))

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in0 = numpy.asarray(in0)
        in0 = numpy.float64(in0)
        self.count = self.count + 1
	self.dset.resize((self.count,self.vec_len))
	self.dset[(self.count-1)] = in0
	if self.num_items == self.count:
		self.count = 0
		self.fileno = self.fileno + 1
		self._h5.close()
		self._h5 = h5py.File(name = (str(self.filename)[0:(self.length-3)] + '_%d' % self.fileno + str(self.filename)[(self.length-3):self.length]), mode = 'w')
		self.dset = self._h5.create_dataset('Spectral_Data', (self.count,self.vec_len), dtype = numpy.float64, maxshape=(None,self.vec_len))

        return len(input_items[0])

    def set_h5(self, filename):
        self._h5.set_h5(filename)
