# -*- coding: utf-8 -*-
"""This module contains a custom widget that is essentially the default radio buttons, but with needed functionality."""

import wx
import os

from cst_frame import app_root


class QuizRadioBox(wx.Control):
    """Custom widget, similar to a standard radio button, but allows no selection as well

                Args:
                    parent (ptr): Reference to the wx.object this panel belongs to
                    choices (list: str): List of choices, and thus indirectly the number of buttons
                    q_type (int): Dirty bootstrap so that I can determine the type of question answered

                Attributes:
                    parent (ptr): Reference to the wx.object this panel belongs to

        """

    def __init__(self, parent, choices=[], background_c=None):
        """Constructor"""
        wx.Control.__init__(self, parent, style=wx.BORDER_NONE)

        self.SetBackgroundColour(background_c)

        self.q_type = None

        # Create sizers
        self.sizer_main = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_padding = wx.BoxSizer(wx.VERTICAL)
        self.sizer_rbox = wx.BoxSizer(wx.HORIZONTAL)

        # Question text and selection arrow objects
        self.question_text = wx.StaticText(self, size=(-1, -1), label="NULL")
        self.select_arrow = wx.StaticBitmap(self, bitmap=wx.Bitmap(wx.Image(os.path.join(app_root,
                                                                                         'img',
                                                                                         'r_arr.png'))))

        # Add question and arrow to sizers, hide arrow
        self.sizer_main.Add(self.question_text, border=15, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.sizer_rbox.Add(self.select_arrow, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.select_arrow.Hide()

        # Add radio buttons
        self._items = []
        self._selection = None
        self.append_radio_button("")
        for i in choices:
            self.append_radio_button(i)

        # Finish setting up sizers
        self.sizer_padding.Add(self.sizer_rbox, flag=wx.ALL | wx.ALIGN_RIGHT)
        self.sizer_main.Add(self.sizer_padding, proportion=1, flag=wx.ALL | wx.ALIGN_RIGHT | wx.EXPAND)
        self.SetSizer(self.sizer_main)

    def append_radio_button(self, item):
        """Add a radio button"""
        if len(self._items) == 0:
            rb = wx.RadioButton(self, -1, item, style=wx.RB_GROUP)
            self._selection = 0
            rb.Hide()
        else:
            rb = wx.RadioButton(self, -1, item)
            self.sizer_rbox.Add(rb, border=15, flag=wx.ALL)

        self.Bind(wx.EVT_RADIOBUTTON, self.on_select, rb)

        self._items.append(rb)

    def on_select(self, evt):
        """Upon clicking, set value and send event"""
        ctrl = evt.GetEventObject()
        for i, rb in enumerate(self._items):
            if rb.GetLabel() == ctrl.GetLabel():
                self.set_selection(i)
                break
        # prepare an event to send to the parent control, so it can be catched outside
        # as an event of the class, not it's inner controls
        event = wx.CommandEvent(wx.EVT_RADIOBUTTON.evtType[0], self.Id)
        event.SetEventObject(self)
        event.SetInt(self._selection)

        self.Command(event)

    def get_selection(self):
        """Return the index of the selected radio button"""
        return self._selection

    def set_selection(self, s):
        """Set the index of the selected radio button"""
        self._items[s].SetValue(True)
        self._selection = s

    def selected_question(self, query):
        if query:
            self.select_arrow.Show()
        else:
            self.select_arrow.Hide()
