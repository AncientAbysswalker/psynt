# -*- coding: utf-8 -*-
"""This module contains custom dialog boxes to work with the main code base.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * NONE ATM

"""

import wx
import os

from cst_frame import app_root


class QuizRadioBox(wx.Control):
    def __init__(self, parent, choices=[], background_c=None):
        wx.Control.__init__(self, parent, style=wx.BORDER_NONE)

        self.SetBackgroundColour(background_c)

        self.q_type = None

        self.sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_padding = wx.BoxSizer(wx.VERTICAL)
        self.sizer_rbox = wx.BoxSizer(wx.HORIZONTAL)

        self.question_text = wx.StaticText(self, size=(-1, -1), label="NULL")
        self.sizer_main.Add(self.question_text, border=15, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.select_arrow = wx.StaticBitmap(self, bitmap=wx.Bitmap(wx.Image(os.path.join(app_root, 'larr.png'))))

        self.sizer_rbox.Add(self.select_arrow, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.select_arrow.Hide()

        self._items = []
        self._selection = None
        self.Append("")
        for i in choices:
            self.Append(i)

        self.sizer_padding.Add(self.sizer_rbox, flag=wx.ALL | wx.ALIGN_RIGHT)
        self.sizer_main.Add(self.sizer_padding, proportion=1, flag=wx.ALL | wx.ALIGN_RIGHT | wx.EXPAND)
        self.SetSizer(self.sizer_main)

    def Append(self, item):
        if len(self._items) == 0:
            rb = wx.RadioButton(self, -1, item, style=wx.RB_GROUP)
            self._selection = 0
            rb.Hide()
        else:
            rb = wx.RadioButton(self, -1, item)
            self.sizer_rbox.Add(rb, border=15, flag=wx.ALL)

        self.Bind(wx.EVT_RADIOBUTTON, self.OnSelect, rb)

        self._items.append(rb)

    # selection
    def GetSelection(self):
        return self._selection

    def SetSelection(self, s):
        self._items[s].SetValue(True)
        self._selection = s

    Selection = property(GetSelection, SetSelection)

    def OnSelect(self, evt):
        ctrl = evt.GetEventObject()
        for i, (rb, cd) in enumerate(self._items):
            if rb.GetLabel() == ctrl.GetLabel():
                self._selection = i
                break
        # prepare an event to send to the parent control, so it can be catched outside
        # as an event of the class, not it's inner controls
        event = wx.CommandEvent(wx.EVT_RADIOBUTTON.evtType[0], self.Id)
        event.SetEventObject(self)
        event.SetInt(self._selection)
        self.Command(event)

    def SelectedQuestion(self, query):
        if query:
            self.select_arrow.Show()
        else:
            self.select_arrow.Hide()
