#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Airspy Spectrum Analyzer
# Author: Sahil Mahajan
# Description: Takes data from the Airspy device, performs an FFT, and records the result to a file called "audio.dat"
# Generated: Wed Sep 16 15:40:56 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.fft import logpwrfft
from gnuradio.filter import firdes
from optparse import OptionParser
import osmosdr
import sahil
import sys
import time

from distutils.version import StrictVersion
class airspy_spectrum_analyzer(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Airspy Spectrum Analyzer")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Airspy Spectrum Analyzer")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "airspy_spectrum_analyzer")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10000000.0
        self.fft_size = fft_size = 1024
        self.pi = pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679
        self.frame_rate = frame_rate = samp_rate/fft_size
        self.center_freq = center_freq = 91900000

        ##################################################
        # Blocks
        ##################################################
        self.sahil_save_N_to_h5_0 = sahil.save_N_to_h5("sahilisanidiot.h5", 1000, vec_len = fft_size)
        self.sahil_average_0 = sahil.average(.1, fft_size)
        self.sahil_addheaders_0 = sahil.addheaders(samp_rate, center_freq - samp_rate, samp_rate, vec_len = fft_size)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.osmosdr_source_0.set_time_source("gpsdo", 0)
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_freq, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(1, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(True, 0)
        self.osmosdr_source_0.set_gain(10, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
          
        self.logpwrfft_x_0 = logpwrfft.logpwrfft_c(
        	sample_rate=samp_rate,
        	fft_size=fft_size,
        	ref_scale=2,
        	frame_rate=frame_rate,
        	avg_alpha=.1,
        	average=True,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.logpwrfft_x_0, 0), (self.sahil_addheaders_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.logpwrfft_x_0, 0))    
        self.connect((self.sahil_addheaders_0, 0), (self.sahil_average_0, 0))    
        self.connect((self.sahil_average_0, 0), (self.sahil_save_N_to_h5_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "airspy_spectrum_analyzer")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_frame_rate(self.samp_rate/self.fft_size)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.logpwrfft_x_0.set_sample_rate(self.samp_rate)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self.set_frame_rate(self.samp_rate/self.fft_size)

    def get_pi(self):
        return self.pi

    def set_pi(self, pi):
        self.pi = pi

    def get_frame_rate(self):
        return self.frame_rate

    def set_frame_rate(self, frame_rate):
        self.frame_rate = frame_rate

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.osmosdr_source_0.set_center_freq(self.center_freq, 0)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = airspy_spectrum_analyzer()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
