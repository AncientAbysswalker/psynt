# -*- coding: utf-8 -*-
"""This module defines custom panels - any panels that are defined as a separate class for ease or proper function"""

import wx
import wx.lib.scrolledpanel as scrolled
from wx.adv import HyperlinkCtrl as hyperlink

class ScrolledResultsPanel(scrolled.ScrolledPanel):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, parent):
        """Constructor"""
        super().__init__(parent, style=wx.BORDER_SIMPLE)

        self.parent = parent
        self.interspace = 5

        sizer_cols = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_affinity = wx.BoxSizer(wx.VERTICAL)
        self.sizer_code_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_code_2 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_title_1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer_title_2 = wx.BoxSizer(wx.VERTICAL)

        self.sizer_affinity.Add(wx.StaticText(self, size=(-1, -1), label="Affinity"), flag=wx.ALL | wx.EXPAND)
        self.sizer_code_1.Add(wx.StaticText(self, size=(-1, -1), label=self.parent.parent.code_1), flag=wx.ALL | wx.EXPAND)
        self.sizer_code_2.Add(wx.StaticText(self, size=(-1, -1), label=self.parent.parent.code_2), flag=wx.ALL | wx.EXPAND)
        self.sizer_title_1.Add(wx.StaticText(self, size=(-1, -1), label=self.parent.parent.title_1), flag=wx.ALL | wx.EXPAND)
        self.sizer_title_2.Add(wx.StaticText(self, size=(-1, -1), label=self.parent.parent.title_2), flag=wx.ALL | wx.EXPAND)
        self.sizer_affinity.AddSpacer(self.interspace)
        self.sizer_code_1.AddSpacer(self.interspace)
        self.sizer_title_1.AddSpacer(self.interspace)
        self.sizer_code_2.AddSpacer(self.interspace)
        self.sizer_title_2.AddSpacer(self.interspace)

        sizer_cols.Add(self.sizer_affinity, flag=wx.ALL | wx.EXPAND)
        sizer_cols.AddSpacer(15)
        sizer_cols.Add(self.sizer_code_1, flag=wx.ALL | wx.EXPAND)
        sizer_cols.AddSpacer(15)
        sizer_cols.Add(self.sizer_code_2, flag=wx.ALL | wx.EXPAND)
        sizer_cols.AddSpacer(15)
        sizer_cols.Add(self.sizer_title_1, flag=wx.ALL | wx.EXPAND)
        sizer_cols.AddSpacer(15)
        sizer_cols.Add(self.sizer_title_2, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(sizer_cols)

        # Setup the scrolling style and function, wanting only vertical scroll to be available
        # self.SetAutoLayout(1)
        self.SetupScrolling()
        self.ShowScrollbars(wx.SHOW_SB_NEVER, wx.SHOW_SB_ALWAYS)
        self.SetWindowStyle(wx.VSCROLL)

        self.Layout()

    def refresh(self):
        code_1_link = "http://noc.esdc.gc.ca/English/noc/Profile.aspx?val=4&val1={}&ver=16"
        code_2_link = "https://www.onetcodeconnector.org/ccreport/{}"

        print(self.parent.parent.results)
        for result in self.parent.parent.results:
            #self.sizer_code_1.Add(wx.StaticText(self, label=result[0])) # proportion=1, border=15, flag=wx.ALL | wx.EXPAND)
            #http://noc.esdc.gc.ca/English/noc/Profile.aspx?val=4&val1=5112&ver=16

            print(result)
            self.sizer_affinity.Add(wx.StaticText(self, label=result[4]))
            self.sizer_affinity.AddSpacer(self.interspace-1)
            self.sizer_code_1.Add(hyperlink(self,
                                            label=result[0],
                                            url=code_1_link.format(result[0])))
            self.sizer_code_1.AddSpacer(self.interspace)
            self.sizer_title_1.Add(hyperlink(self,
                                            label=result[1],
                                            url=code_1_link.format(result[0])))
            self.sizer_title_1.AddSpacer(self.interspace)
            self.sizer_code_2.Add(hyperlink(self,
                                            label=result[2],
                                            url=code_2_link.format(result[2])))
            self.sizer_code_2.AddSpacer(self.interspace)
            self.sizer_title_2.Add(hyperlink(self,
                                            label=result[3],
                                            url=code_2_link.format(result[2])))
            self.sizer_title_2.AddSpacer(self.interspace)

            self.Layout()
            self.parent.Layout()