# -*- coding: utf-8 -*-
"""This is the frame module, defines the frame the application resides in"""

import os
import sys
import wx
import random
import yaml

import cst_pane
import config

is_demo = True

# Handle whether we are frozen
if getattr(sys, 'frozen', False):
    app_root = sys._MEIPASS
else:
    app_root = os.path.dirname(os.path.abspath(__file__))


class MainApp(wx.Frame):
    """Quiz application frame.

            Attributes:
                questions (list: [str, int]): A list of questions, each a 2-entry list of question and type
                scoring (list: int): Cumulative score throughout the test
                ranking (list): List of score indices, ranked high to low
                results (list: list): List of returned texts based on 3-digit octal key
                convert_key (dict) Dictionary translating 3-digit octal keys to applicable results
    """

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        # Load questions and shuffle
        self.questions = []
        self.load_questions()
        random.shuffle(self.questions)

        # Initialize variables
        self.scoring = [0] * 7
        self.ranking = []
        self.results = []
        self.convert_key = {}
        self.load_convert_key()

        config.load_config()

        # Pane sizers
        self.sizer_cover = wx.BoxSizer(wx.VERTICAL)
        self.sizer_instruct = wx.BoxSizer(wx.VERTICAL)
        self.sizer_quiz = wx.BoxSizer(wx.VERTICAL)
        self.sizer_summary = wx.BoxSizer(wx.VERTICAL)

        # Load all panels and place in their sizers
        self.pane_cover = cst_pane.PaneCover(self)
        self.pane_instruct = cst_pane.PaneInstruct(self)
        self.pane_quiz = cst_pane.PaneTest(self)
        self.pane_summary = cst_pane.PaneSummary(self)
        self.sizer_cover.Add(self.pane_cover, proportion=1, flag=wx.EXPAND)
        self.sizer_instruct.Add(self.pane_instruct, proportion=1, flag=wx.EXPAND)
        self.sizer_quiz.Add(self.pane_quiz, proportion=1, flag=wx.EXPAND)
        self.sizer_summary.Add(self.pane_summary, proportion=1, flag=wx.EXPAND)

        # Only show the cover initially
        self.pane_instruct.Hide()
        self.pane_quiz.Hide()
        self.pane_summary.Hide()

        # Set initial sizer and show self
        self.SetSizer(self.sizer_cover)
        self.Show()

    def load_questions(self):
        """Load the questions file and populate self.questions"""
        if is_demo:
            _file = 'questions_demo.txt'
        else:
            _file = 'questions_production.txt'

        with open(os.path.join(app_root, _file), 'r') as file:
            for line in file:
                _type, _question = line.strip().split(" :: ")
                self.questions.append([_question, int(_type)])

    def load_convert_key(self):
        """Load the parameters key"""
        if is_demo:
            _file = 'convert_key_demo.yaml'
        else:
            _file = 'convert_key_production.yaml'

        with open(os.path.join(app_root, _file), 'r') as stream:
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
