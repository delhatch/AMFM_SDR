#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: AMFM_nosel_v1
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
import math
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import sdrplay3
from xmlrpc.server import SimpleXMLRPCServer
import threading



from gnuradio import qtgui

class AMFM_nosel_v1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AMFM_nosel_v1", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AMFM_nosel_v1")
        qtgui.util.check_set_qss()
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

        self.settings = Qt.QSettings("GNU Radio", "AMFM_nosel_v1")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.disp_freq = disp_freq = 98.1e6
        self.SDR_rate = SDR_rate = 2.304e6
        self.FM1 = FM1 = 1
        self.AM1 = AM1 = 0
        self.volume = volume = 0.0
        self.scroll_speed = scroll_speed = 0.5
        self.qtgui_msgdigitalnumbercontrol_0_0_0 = qtgui_msgdigitalnumbercontrol_0_0_0 = disp_freq
        self.qtgui_msgdigitalnumbercontrol_0 = qtgui_msgdigitalnumbercontrol_0 = disp_freq
        self.pilot_carrier_filter_coeffs = pilot_carrier_filter_coeffs = firdes.complex_band_pass(1.0, SDR_rate/6, 17000, 21000, 2000, window.WIN_HAMMING, 6.76)
        self.freq_speed = freq_speed = 0.1
        self.freq_correct = freq_correct = 0
        self.fm_xition_width = fm_xition_width = 15000
        self.fm_ifbw = fm_ifbw = 200e3
        self.deviation_hz = deviation_hz = 100000
        self.decim = decim = 6
        self.cf_offset = cf_offset = 30e3
        self.cent_freq = cent_freq = 98.1e6
        self.blend_width = blend_width = 200
        self.blend_freq = blend_freq = 300
        self.audio_filter_coeffs = audio_filter_coeffs = firdes.low_pass(1, SDR_rate/6, 15000,1500, window.WIN_HAMMING, 6.76)
        self.am_xition_width = am_xition_width = 500
        self.am_ifbw = am_ifbw = 5000
        self.FM6AM48 = FM6AM48 = 6+(AM1*42)
        self.FM4AM1 = FM4AM1 = 1+(FM1*3)
        self.FM1AM8 = FM1AM8 = 1+(AM1*7)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_tab_widget_0 = Qt.QTabWidget()
        self.qtgui_tab_widget_0_widget_0 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_0)
        self.qtgui_tab_widget_0_grid_layout_0 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_0.addLayout(self.qtgui_tab_widget_0_grid_layout_0)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_0, 'FM')
        self.qtgui_tab_widget_0_widget_1 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_1)
        self.qtgui_tab_widget_0_grid_layout_1 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_1.addLayout(self.qtgui_tab_widget_0_grid_layout_1)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_1, 'FM details')
        self.qtgui_tab_widget_0_widget_2 = Qt.QWidget()
        self.qtgui_tab_widget_0_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.qtgui_tab_widget_0_widget_2)
        self.qtgui_tab_widget_0_grid_layout_2 = Qt.QGridLayout()
        self.qtgui_tab_widget_0_layout_2.addLayout(self.qtgui_tab_widget_0_grid_layout_2)
        self.qtgui_tab_widget_0.addTab(self.qtgui_tab_widget_0_widget_2, 'AM')
        self.top_layout.addWidget(self.qtgui_tab_widget_0)
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8080), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.sdrplay3_rsp1a_1 = sdrplay3.rsp1a(
            '',
            stream_args=sdrplay3.stream_args(
                output_type='fc32',
                channels_size=1
            ),
        )
        self.sdrplay3_rsp1a_1.set_sample_rate(SDR_rate)
        self.sdrplay3_rsp1a_1.set_center_freq((cent_freq-cf_offset))
        self.sdrplay3_rsp1a_1.set_bandwidth(5000e3)
        self.sdrplay3_rsp1a_1.set_gain_mode(True)
        self.sdrplay3_rsp1a_1.set_gain(-40, 'IF')
        self.sdrplay3_rsp1a_1.set_gain(-float('9'), 'RF')
        self.sdrplay3_rsp1a_1.set_freq_corr(freq_correct)
        self.sdrplay3_rsp1a_1.set_dc_offset_mode(False)
        self.sdrplay3_rsp1a_1.set_iq_balance_mode(False)
        self.sdrplay3_rsp1a_1.set_agc_setpoint((-30))
        self.sdrplay3_rsp1a_1.set_rf_notch_filter(False)
        self.sdrplay3_rsp1a_1.set_dab_notch_filter(False)
        self.sdrplay3_rsp1a_1.set_biasT(False)
        self.sdrplay3_rsp1a_1.set_debug_mode(False)
        self.sdrplay3_rsp1a_1.set_sample_sequence_gaps_check(False)
        self.sdrplay3_rsp1a_1.set_show_gain_changes(False)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=3,
                decimation=FM4AM1,
                taps=[],
                fractional_bw=0)
        self.qtgui_waterfall_sink_x_0_0_0_0_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (SDR_rate/6), #bw
            "IF", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_update_time(scroll_speed)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0_0_0.qwidget(), Qt.QWidget)

        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_0_win, 2, 0, 3, 1)
        for r in range(2, 5):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_waterfall_sink_x_0_0_0_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            (SDR_rate/(6*8)), #bw
            "IF", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0_0_0_0.set_update_time(scroll_speed)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0_0_0_0.enable_axis_labels(True)

        self.qtgui_waterfall_sink_x_0_0_0_0.disable_legend()


        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [6, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0_0_0_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0_0_0_0.qwidget(), Qt.QWidget)

        self.qtgui_tab_widget_0_grid_layout_2.addWidget(self._qtgui_waterfall_sink_x_0_0_0_0_win, 2, 0, 3, 1)
        for r in range(2, 5):
            self.qtgui_tab_widget_0_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_2.setColumnStretch(c, 1)
        self._qtgui_msgdigitalnumbercontrol_0_0_0_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl='Frequency = ', min_freq_hz=0.0, max_freq_hz=1700e6, parent=self, thousands_separator=",", background_color="white", fontColor="black", var_callback=self.set_qtgui_msgdigitalnumbercontrol_0_0_0, outputmsgname='cent_freq')
        self._qtgui_msgdigitalnumbercontrol_0_0_0_msgdigctl_win.setValue(disp_freq )
        self._qtgui_msgdigitalnumbercontrol_0_0_0_msgdigctl_win.setReadOnly(True)
        self.qtgui_msgdigitalnumbercontrol_0_0_0 = self._qtgui_msgdigitalnumbercontrol_0_0_0_msgdigctl_win

        self.qtgui_tab_widget_0_grid_layout_2.addWidget(self._qtgui_msgdigitalnumbercontrol_0_0_0_msgdigctl_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_2.setColumnStretch(c, 1)
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl='Frequency = ', min_freq_hz=0.0, max_freq_hz=1700e6, parent=self, thousands_separator=",", background_color="white", fontColor="black", var_callback=self.set_qtgui_msgdigitalnumbercontrol_0, outputmsgname='cent_freq')
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win.setValue(disp_freq )
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win.setReadOnly(True)
        self.qtgui_msgdigitalnumbercontrol_0 = self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win

        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_1_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_HAMMING, #wintype
            0, #fc
            (SDR_rate/6), #bw
            "Tuner", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1_0.set_update_time(freq_speed)
        self.qtgui_freq_sink_x_0_1_0.set_y_axis((-110), (-30))
        self.qtgui_freq_sink_x_0_1_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_1_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0_1_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1_0.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_0_1_0.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1_0.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_grid_layout_2.addWidget(self._qtgui_freq_sink_x_0_1_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.qtgui_tab_widget_0_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_HAMMING, #wintype
            0, #fc
            SDR_rate, #bw
            "Tuner", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1.set_update_time(freq_speed)
        self.qtgui_freq_sink_x_0_1.set_y_axis((-120), (-30))
        self.qtgui_freq_sink_x_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_0_1.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.qtgui_tab_widget_0_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_f(
            4096, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            ((SDR_rate*3)/(6*4*2)), #bw
            "FM Baseband", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(freq_speed)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-100), (-20))
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(True)

        self.qtgui_freq_sink_x_0_0.disable_legend()

        self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_win, 0, 0, 1, 3)
        for r in range(0, 1):
            self.qtgui_tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 3):
            self.qtgui_tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            512, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(freq_speed)
        self.qtgui_const_sink_x_0.set_y_axis((-1.0), 1.0)
        self.qtgui_const_sink_x_0.set_x_axis((-1.0), 1.0)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(False)

        self.qtgui_const_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [3, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["dark red", "green", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [2, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.qtgui_tab_widget_0_grid_layout_1.addWidget(self._qtgui_const_sink_x_0_win, 1, 0, 1, 3)
        for r in range(1, 2):
            self.qtgui_tab_widget_0_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 3):
            self.qtgui_tab_widget_0_grid_layout_1.setColumnStretch(c, 1)
        self.low_pass_filter_1_1 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                48e3,
                blend_freq,
                blend_width,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_1_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                48e3,
                blend_freq,
                blend_width,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_1 = filter.fir_filter_fff(
            2,
            firdes.low_pass(
                1,
                ((SDR_rate*9)/(6*12)),
                100000,
                2000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            8,
            firdes.low_pass(
                1,
                (SDR_rate/(6)),
                am_ifbw,
                am_xition_width,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            FM1AM8,
            firdes.low_pass(
                1,
                (SDR_rate/decim),
                (fm_ifbw/(2)),
                fm_xition_width,
                window.WIN_BLACKMAN,
                6.76))
        self.high_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.high_pass(
                1,
                48000,
                blend_freq,
                blend_width,
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decim, firdes.complex_band_pass(1,SDR_rate,-192e3,192e3,35000), cf_offset, SDR_rate)
        self.fft_filter_xxx_3_0 = filter.fft_filter_fff(8, audio_filter_coeffs, 1)
        self.fft_filter_xxx_3_0.declare_sample_delay(0)
        self.fft_filter_xxx_3 = filter.fft_filter_fff(8, audio_filter_coeffs, 1)
        self.fft_filter_xxx_3.declare_sample_delay(0)
        self.fft_filter_xxx_1 = filter.fft_filter_ccc(1, pilot_carrier_filter_coeffs, 1)
        self.fft_filter_xxx_1.declare_sample_delay(0)
        self.fft_filter_xxx_0 = filter.fft_filter_fff(8, audio_filter_coeffs, 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.dc_blocker_xx_1 = filter.dc_blocker_ff(512, True)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(512, True)
        self.blocks_var_to_msg_0_1 = blocks.var_to_msg_pair('send_AM1')
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_float*1,AM1,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,AM1,0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(2)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(volume)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume)
        self.blocks_float_to_complex_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_delay_2 = blocks.delay(gr.sizeof_gr_complex*1, 35000)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_add_xx_0_1 = blocks.add_vff(1)
        self.blocks_add_xx_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_2 = audio.sink(48000, '', True)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(((SDR_rate/6)/(2*math.pi*deviation_hz)))
        self.analog_pll_refout_cc_0 = analog.pll_refout_cc(0.001, (2*3.13159*18800/(SDR_rate/6)), (2*3.13159*19200/(SDR_rate/6)))
        self.analog_pll_carriertracking_cc_0_0 = analog.pll_carriertracking_cc(.05, (-0.0654), 0.0654)
        self.analog_fm_deemph_0_0 = analog.fm_deemph(fs=48000, tau=(75e-6))
        self.analog_fm_deemph_0 = analog.fm_deemph(fs=48000, tau=(75e-6))
        self.analog_agc_xx_0 = analog.agc_cc(0.07, 0.5, 0.5)
        self.analog_agc_xx_0.set_max_gain(4096)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_var_to_msg_0_1, 'msgout'), (self.blocks_selector_0, 'iindex'))
        self.msg_connect((self.blocks_var_to_msg_0_1, 'msgout'), (self.blocks_selector_0_0, 'iindex'))
        self.connect((self.analog_agc_xx_0, 0), (self.analog_pll_carriertracking_cc_0_0, 0))
        self.connect((self.analog_fm_deemph_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.analog_fm_deemph_0_0, 0), (self.blocks_selector_0_0, 0))
        self.connect((self.analog_pll_carriertracking_cc_0_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_pll_refout_cc_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_float_to_complex_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.dc_blocker_xx_1, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.fft_filter_xxx_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.fft_filter_xxx_3_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.low_pass_filter_1_0, 0))
        self.connect((self.blocks_add_xx_0_0, 0), (self.analog_fm_deemph_0_0, 0))
        self.connect((self.blocks_add_xx_0_1, 0), (self.analog_fm_deemph_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_delay_2, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_delay_2, 0))
        self.connect((self.blocks_float_to_complex_1, 0), (self.fft_filter_xxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.audio_sink_2, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.fft_filter_xxx_3, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.low_pass_filter_1_1, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_selector_0, 1))
        self.connect((self.dc_blocker_xx_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.dc_blocker_xx_1, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.fft_filter_xxx_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.fft_filter_xxx_1, 0), (self.analog_pll_refout_cc_0, 0))
        self.connect((self.fft_filter_xxx_3, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.fft_filter_xxx_3, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.fft_filter_xxx_3_0, 0), (self.high_pass_filter_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0_1_0, 0))
        self.connect((self.high_pass_filter_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.high_pass_filter_0, 0), (self.blocks_add_xx_0_1, 1))
        self.connect((self.low_pass_filter_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_waterfall_sink_x_0_0_0_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.low_pass_filter_1_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.low_pass_filter_1_1, 0), (self.blocks_add_xx_0_1, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.low_pass_filter_1, 0))
        self.connect((self.sdrplay3_rsp1a_1, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.sdrplay3_rsp1a_1, 0), (self.qtgui_freq_sink_x_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "AMFM_nosel_v1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_disp_freq(self):
        return self.disp_freq

    def set_disp_freq(self, disp_freq):
        self.disp_freq = disp_freq
        self._qtgui_msgdigitalnumbercontrol_0_msgdigctl_win.setValue(self.disp_freq )
        self._qtgui_msgdigitalnumbercontrol_0_0_0_msgdigctl_win.setValue(self.disp_freq )

    def get_SDR_rate(self):
        return self.SDR_rate

    def set_SDR_rate(self, SDR_rate):
        self.SDR_rate = SDR_rate
        self.set_audio_filter_coeffs(firdes.low_pass(1, self.SDR_rate/6, 15000, 1500, window.WIN_HAMMING, 6.76))
        self.set_pilot_carrier_filter_coeffs(firdes.complex_band_pass(1.0, self.SDR_rate/6, 17000, 21000, 2000, window.WIN_HAMMING, 6.76))
        self.analog_pll_refout_cc_0.set_max_freq((2*3.13159*18800/(self.SDR_rate/6)))
        self.analog_pll_refout_cc_0.set_min_freq((2*3.13159*19200/(self.SDR_rate/6)))
        self.analog_quadrature_demod_cf_0.set_gain(((self.SDR_rate/6)/(2*math.pi*self.deviation_hz)))
        self.freq_xlating_fir_filter_xxx_0.set_taps(firdes.complex_band_pass(1,self.SDR_rate,-192e3,192e3,35000))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, (self.SDR_rate/self.decim), (self.fm_ifbw/(2)), self.fm_xition_width, window.WIN_BLACKMAN, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, (self.SDR_rate/(6)), self.am_ifbw, self.am_xition_width, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, ((self.SDR_rate*9)/(6*12)), 100000, 2000, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, ((self.SDR_rate*3)/(6*4*2)))
        self.qtgui_freq_sink_x_0_1.set_frequency_range(0, self.SDR_rate)
        self.qtgui_freq_sink_x_0_1_0.set_frequency_range(0, (self.SDR_rate/6))
        self.qtgui_waterfall_sink_x_0_0_0_0.set_frequency_range(0, (self.SDR_rate/(6*8)))
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_frequency_range(0, (self.SDR_rate/6))
        self.sdrplay3_rsp1a_1.set_sample_rate(self.SDR_rate)

    def get_FM1(self):
        return self.FM1

    def set_FM1(self, FM1):
        self.FM1 = FM1
        self.set_FM4AM1(1+(self.FM1*3))

    def get_AM1(self):
        return self.AM1

    def set_AM1(self, AM1):
        self.AM1 = AM1
        self.set_FM1AM8(1+(self.AM1*7))
        self.set_FM6AM48(6+(self.AM1*42))
        self.blocks_selector_0.set_input_index(self.AM1)
        self.blocks_selector_0_0.set_input_index(self.AM1)
        self.blocks_var_to_msg_0_1.variable_changed(self.AM1)

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume)
        self.blocks_multiply_const_vxx_0_0.set_k(self.volume)

    def get_scroll_speed(self):
        return self.scroll_speed

    def set_scroll_speed(self, scroll_speed):
        self.scroll_speed = scroll_speed
        self.qtgui_waterfall_sink_x_0_0_0_0.set_update_time(self.scroll_speed)
        self.qtgui_waterfall_sink_x_0_0_0_0_0.set_update_time(self.scroll_speed)

    def get_qtgui_msgdigitalnumbercontrol_0_0_0(self):
        return self.qtgui_msgdigitalnumbercontrol_0_0_0

    def set_qtgui_msgdigitalnumbercontrol_0_0_0(self, qtgui_msgdigitalnumbercontrol_0_0_0):
        self.qtgui_msgdigitalnumbercontrol_0_0_0 = qtgui_msgdigitalnumbercontrol_0_0_0

    def get_qtgui_msgdigitalnumbercontrol_0(self):
        return self.qtgui_msgdigitalnumbercontrol_0

    def set_qtgui_msgdigitalnumbercontrol_0(self, qtgui_msgdigitalnumbercontrol_0):
        self.qtgui_msgdigitalnumbercontrol_0 = qtgui_msgdigitalnumbercontrol_0

    def get_pilot_carrier_filter_coeffs(self):
        return self.pilot_carrier_filter_coeffs

    def set_pilot_carrier_filter_coeffs(self, pilot_carrier_filter_coeffs):
        self.pilot_carrier_filter_coeffs = pilot_carrier_filter_coeffs
        self.fft_filter_xxx_1.set_taps(self.pilot_carrier_filter_coeffs)

    def get_freq_speed(self):
        return self.freq_speed

    def set_freq_speed(self, freq_speed):
        self.freq_speed = freq_speed
        self.qtgui_const_sink_x_0.set_update_time(self.freq_speed)
        self.qtgui_freq_sink_x_0_0.set_update_time(self.freq_speed)
        self.qtgui_freq_sink_x_0_1.set_update_time(self.freq_speed)
        self.qtgui_freq_sink_x_0_1_0.set_update_time(self.freq_speed)

    def get_freq_correct(self):
        return self.freq_correct

    def set_freq_correct(self, freq_correct):
        self.freq_correct = freq_correct
        self.sdrplay3_rsp1a_1.set_freq_corr(self.freq_correct)

    def get_fm_xition_width(self):
        return self.fm_xition_width

    def set_fm_xition_width(self, fm_xition_width):
        self.fm_xition_width = fm_xition_width
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, (self.SDR_rate/self.decim), (self.fm_ifbw/(2)), self.fm_xition_width, window.WIN_BLACKMAN, 6.76))

    def get_fm_ifbw(self):
        return self.fm_ifbw

    def set_fm_ifbw(self, fm_ifbw):
        self.fm_ifbw = fm_ifbw
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, (self.SDR_rate/self.decim), (self.fm_ifbw/(2)), self.fm_xition_width, window.WIN_BLACKMAN, 6.76))

    def get_deviation_hz(self):
        return self.deviation_hz

    def set_deviation_hz(self, deviation_hz):
        self.deviation_hz = deviation_hz
        self.analog_quadrature_demod_cf_0.set_gain(((self.SDR_rate/6)/(2*math.pi*self.deviation_hz)))

    def get_decim(self):
        return self.decim

    def set_decim(self, decim):
        self.decim = decim
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, (self.SDR_rate/self.decim), (self.fm_ifbw/(2)), self.fm_xition_width, window.WIN_BLACKMAN, 6.76))

    def get_cf_offset(self):
        return self.cf_offset

    def set_cf_offset(self, cf_offset):
        self.cf_offset = cf_offset
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.cf_offset)
        self.sdrplay3_rsp1a_1.set_center_freq((self.cent_freq-self.cf_offset))

    def get_cent_freq(self):
        return self.cent_freq

    def set_cent_freq(self, cent_freq):
        self.cent_freq = cent_freq
        self.sdrplay3_rsp1a_1.set_center_freq((self.cent_freq-self.cf_offset))

    def get_blend_width(self):
        return self.blend_width

    def set_blend_width(self, blend_width):
        self.blend_width = blend_width
        self.high_pass_filter_0.set_taps(firdes.high_pass(1, 48000, self.blend_freq, self.blend_width, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, 48e3, self.blend_freq, self.blend_width, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_1.set_taps(firdes.low_pass(1, 48e3, self.blend_freq, self.blend_width, window.WIN_HAMMING, 6.76))

    def get_blend_freq(self):
        return self.blend_freq

    def set_blend_freq(self, blend_freq):
        self.blend_freq = blend_freq
        self.high_pass_filter_0.set_taps(firdes.high_pass(1, 48000, self.blend_freq, self.blend_width, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, 48e3, self.blend_freq, self.blend_width, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_1.set_taps(firdes.low_pass(1, 48e3, self.blend_freq, self.blend_width, window.WIN_HAMMING, 6.76))

    def get_audio_filter_coeffs(self):
        return self.audio_filter_coeffs

    def set_audio_filter_coeffs(self, audio_filter_coeffs):
        self.audio_filter_coeffs = audio_filter_coeffs
        self.fft_filter_xxx_0.set_taps(self.audio_filter_coeffs)
        self.fft_filter_xxx_3.set_taps(self.audio_filter_coeffs)
        self.fft_filter_xxx_3_0.set_taps(self.audio_filter_coeffs)

    def get_am_xition_width(self):
        return self.am_xition_width

    def set_am_xition_width(self, am_xition_width):
        self.am_xition_width = am_xition_width
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, (self.SDR_rate/(6)), self.am_ifbw, self.am_xition_width, window.WIN_HAMMING, 6.76))

    def get_am_ifbw(self):
        return self.am_ifbw

    def set_am_ifbw(self, am_ifbw):
        self.am_ifbw = am_ifbw
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, (self.SDR_rate/(6)), self.am_ifbw, self.am_xition_width, window.WIN_HAMMING, 6.76))

    def get_FM6AM48(self):
        return self.FM6AM48

    def set_FM6AM48(self, FM6AM48):
        self.FM6AM48 = FM6AM48

    def get_FM4AM1(self):
        return self.FM4AM1

    def set_FM4AM1(self, FM4AM1):
        self.FM4AM1 = FM4AM1

    def get_FM1AM8(self):
        return self.FM1AM8

    def set_FM1AM8(self, FM1AM8):
        self.FM1AM8 = FM1AM8




def main(top_block_cls=AMFM_nosel_v1, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
