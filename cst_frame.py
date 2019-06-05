# -*- coding: utf-8 -*-
"""This is the frame module, defines the frame the application resides in"""


import wx
import random
import sys
import os

import cst_pane
import yaml


# Handle whether we are frozen
if getattr(sys, 'frozen', False):
    app_root = sys._MEIPASS
else:
    app_root = os.path.dirname(os.path.abspath(__file__))


class MainApp(wx.Frame):
    """Quiz application frame.

            Attributes:
                questions (list: [str, int]): A list of questions, each a 2-entry list of question and skill type
                qkey (list: str): A list of skill types, index: value is a key-value pair
                scoring (list: int): Cumulative score throughout the test
                ranking (list: list): List of rankings - TODO EXPLAIN
                 (list: TODO): Original text to display when editing
                esp_crosswalk (dict): Dictionary translating 3-digit keys to applicable results
        """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        # Load questions
        self.questions = []
        self.load_questions()

        self.scoring = [0] * 7
        self.ranking = []
        self.results = []
        self.convert_key = {}
        self.load_convert_key()

        # Sizers for individual panes
        self.sizer_cover = wx.BoxSizer(wx.VERTICAL)
        self.sizer_quiz = wx.BoxSizer(wx.VERTICAL)
        self.sizer_summary = wx.BoxSizer(wx.VERTICAL)

        # Shuffle questions
        random.shuffle(self.questions)

        # Load all panels; only show cover initially
        self.panel_cover = cst_pane.PaneCover(self)
        self.panel_quiz = cst_pane.PaneTest(self)
        self.panel_summary = cst_pane.PaneSummary(self)
        self.panel_quiz.Hide()
        self.panel_summary.Hide()
        self.sizer_cover.Add(self.panel_cover, proportion=1, flag=wx.EXPAND)
        self.sizer_quiz.Add(self.panel_quiz, proportion=1, flag=wx.EXPAND)
        self.sizer_summary.Add(self.panel_summary, proportion=1, flag=wx.EXPAND)

        # Set initial sizer and show self
        self.SetSizer(self.sizer_cover)
        self.Show()

    def load_questions(self):
        """Load the questions file and populate self.questions"""
        with open(os.path.join(app_root, 'questions.txt'), 'r') as file:
            for line in file:
                _type, _question = line.strip().split(" :: ")
                self.questions.append([_question, int(_type)])

    def load_convert_key(self):
        """Load the parameters key"""
        with open(os.path.join(app_root, 'convert_key.yaml'), 'r') as stream:
            self.convert_key = yaml.safe_load(stream)


def main():
    """Run application as full-screen window"""
    app = wx.App()
    window = MainApp(None, size=(700, 500), style=wx.NO_BORDER)
    window.Maximize(True)
    window.Show(True)

    app.MainLoop()


if __name__ == '__main__':
    main()
