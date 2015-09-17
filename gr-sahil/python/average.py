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

class average(gr.sync_block):
    """
    Calculate average for each segment of time
    """
    def __init__(self, time, vec_len):
	self.time = time
	self.vec_len = vec_len
	self.count = 1
        gr.sync_block.__init__(self,
            name="average",
            in_sig=[(numpy.float32,self.vec_len+4)],
            out_sig=[(numpy.float32,self.vec_len+4)])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
	avg = []
	while in0[0][0] <= self.count*self.time:
		avg.append(in0[1::])
	self.count = self.count + 1
	avg = numpy.asarray(avg)
	in0 = avg.mean(axis=0)
	in0 = numpy.hstack(((self.count-1)*self.time,in0))
        out[:] = in0
        return len(output_items[0])

