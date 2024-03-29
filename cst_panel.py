# -*- coding: utf-8 -*-
"""This module defines custom panels - any panels that are defined as a separate class for ease or proper function"""

import wx
import wx.lib.scrolledpanel as scrolled
from wx.adv import HyperlinkCtrl as hyperlink

import config


class ScrolledResultsPanel(scrolled.ScrolledPanel):
    """This scrolled panel contains the summary information populated from the quiz

            Class Variables:
                interspace (int): Vertical spacing between rows in results

            Args:
                parent (ptr): Reference to the wx.object this panel belongs to

            Attributes:
                parent (ptr): Reference to the wx.object this panel belongs to
    """

    interspace = 5

    def __init__(self, parent):
        """Constructor"""
        super().__init__(parent, style=wx.BORDER_SIMPLE)

        self.parent = parent

        # Create sizers
        sizer_cols = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_affinity = wx.BoxSizer(wx.VERTICAL)
        self.sizer_code_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_code_2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_title_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_title_2 = wx.BoxSizer(wx.VERTICAL)

        # Add headers to sizers
        self.sizer_affinity.Add(wx.StaticText(self, size=(-1, -1), label="Affinity"), flag=wx.ALL | wx.EXPAND)
        self.sizer_code_1.Add(wx.StaticText(self, size=(-1, -1), label=config.summary_col_1), flag=wx.ALL | wx.EXPAND)
        self.sizer_code_2.Add(wx.StaticText(self, size=(-1, -1), label=config.summary_col_2), flag=wx.ALL | wx.EXPAND)
        self.sizer_title_1.Add(wx.StaticText(self, size=(-1, -1), label=config.summary_col_3), flag=wx.ALL | wx.EXPAND)
        self.sizer_title_2.Add(wx.StaticText(self, size=(-1, -1), label=config.summary_col_4), flag=wx.ALL | wx.EXPAND)
        self.sizer_affinity.AddSpacer(ScrolledResultsPanel.interspace)
        self.sizer_code_1.AddSpacer(ScrolledResultsPanel.interspace)
        self.sizer_title_1.AddSpacer(ScrolledResultsPanel.interspace)
        self.sizer_code_2.AddSpacer(ScrolledResultsPanel.interspace)
        self.sizer_title_2.AddSpacer(ScrolledResultsPanel.interspace)

        # Nest sizers
        sizer_cols.Add(self.sizer_affinity, flag=wx.ALL | wx.EXPAND)
        sizer_cols.AddSpacer(15)
        sizer_cols.Add(self.sizer_code_1, flag=wx.ALL | wx.EXPAND)
        sizer_cols.AddSpacer(15)
        sizer_cols.Add(self.sizer_code_2, flag=wx.ALL | wx.EXPAND)
        sizer_cols.AddSpacer(15)
        sizer_cols.Add(self.sizer_title_1, flag=wx.ALL | wx.EXPAND)
        sizer_cols.AddSpacer(15)
        sizer_cols.Add(self.sizer_title_2, flag=wx.ALL | wx.EXPAND)

        # Set main sizer
        self.SetSizer(sizer_cols)

        # Setup the scrolling style and function, wanting only vertical scroll to be available
        self.SetupScrolling()
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)
        self.SetWindowStyle(wx.VSCROLL)

        self.Layout()

    def refresh(self):
        """Populate results into the panel and update the layout"""
        for result in self.parent.parent.results:
            self.sizer_affinity.Add(wx.StaticText(self, label=result[4]))
            self.sizer_affinity.AddSpacer(ScrolledResultsPanel.interspace-1)
            self.sizer_code_1.Add(self.text_or_hyper(result[0],
                                                     config.link_1.format(result[config.link_var_1]),
                                                     config.link_vis_1))
            self.sizer_code_1.AddSpacer(ScrolledResultsPanel.interspace)
            self.sizer_code_2.Add(self.text_or_hyper(result[2],
                                                     config.link_2.format(result[config.link_var_2]),
                                                     config.link_vis_2))
            self.sizer_code_2.AddSpacer(ScrolledResultsPanel.interspace)
            self.sizer_title_1.Add(self.text_or_hyper(result[1],
                                                      config.link_3.format(result[config.link_var_3]),
                                                      config.link_vis_3))
            self.sizer_title_1.AddSpacer(ScrolledResultsPanel.interspace)
            self.sizer_title_2.Add(self.text_or_hyper(result[3],
                                                      config.link_4.format(result[config.link_var_4]),
                                                      config.link_vis_4))
            self.sizer_title_2.AddSpacer(ScrolledResultsPanel.interspace)

            self.Layout()
            self.parent.Layout()

    def text_or_hyper(self, text, hyplin=None, toggle=True):
        """Returns a text or hyperlink object, dependent on optional provided hyperlink and toggle variables"""
        if hyplin and toggle:
            return hyperlink(self, label=text, url=hyplin)
        else:
            return wx.StaticText(self, label=text)
