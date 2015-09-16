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
from gnuradio import gr

class addheaders(gr.sync_block):
    """
   Add timestamps, starting frequency, bandwidth, and number of bins
    """
    def __init__(self, samp_rate, starting_freq, bandwidth, vec_len):
	self.samp_rate = samp_rate
	self.vec_len = vec_len
	self.starting_freq = starting_freq
	self.bandwidth = bandwidth
	self.count = 0
        gr.sync_block.__init__(self,
            name="addheaders",
            in_sig=[(numpy.float32,self.vec_len)],
            out_sig=[(numpy.float32,self.vec_len+4)])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
	dim = in0.shape[0]
	timestamp = numpy.zeros((dim,1))
	headers = numpy.zeros((dim,3))
	for i in range(dim):
		timestamp[i] = self.vec_len*self.count/self.samp_rate
		self.count = self.count + 1
	for i in range(dim):
		headers[i][0] = self.starting_freq
		headers[i][1] = self.bandwidth
		headers[i][2] = self.vec_len
	in0 = numpy.hstack((timestamp, headers, in0))
        out[:] = in0
        return len(output_items[0])

