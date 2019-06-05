# -*- coding: utf-8 -*-
"""This module defines panes - master panels that act as direct children of the progenitor frame"""


import wx
import cst_widget
import cst_panel
import itertools
import os

import global_colors

from cst_frame import app_root

class PaneCover(wx.Panel):
    """Master pane that acts as the landing page of the application

            Args:
                parent (ptr): Reference to the wx.object this panel belongs to

            Attributes:
                parent (ptr): Reference to the wx.object this panel belongs to
    """

    def __init__(self, parent, *args, **kwargs):
        """Constructor"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # Cover image
        image = wx.Image(os.path.join(app_root, 'cover.jpg'), wx.BITMAP_TYPE_ANY)
        (w1, h1) = image.GetSize()
        (w2, h2) = wx.GetDisplaySize()

        # Resize accordingly
        if w1 / h1 < w2 / h2:
            image_bitmap = wx.StaticBitmap(self, bitmap=wx.Bitmap(image.Rescale(w2, h1 * w2 / w1)))
        else:
            image_bitmap = wx.StaticBitmap(self, bitmap=wx.Bitmap(image.Rescale(w1 * h2 / h1, h2)))

        # Bind ENTER presses to continue to the next page
        self.Bind(wx.EVT_CHAR_HOOK, self.event_keypress)

        # Next button with bind - Deprecated
        #button_start = wx.Button(self, label='Start')
        #button_start.Bind(wx.EVT_BUTTON, self.event_change_pane)

        # Main Sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(image_bitmap, proportion=1, flag=wx.ALL | wx.EXPAND)
        #self.sizer.Add(button_start, flag=wx.CENTER)
        self.SetSizer(self.sizer)

        self.Layout()

    def event_change_pane(self, event):
        """Toggle frame's sizer to correspond to the quiz pane"""
        if self.IsShown():
            self.parent.SetTitle("Question 1")
            self.Hide()
            self.parent.panel_quiz.Show()
            self.parent.panel_quiz.SetFocus()
            self.parent.SetSizer(self.parent.sizer_quiz)
            self.parent.Layout()

    def event_keypress(self, event):
        """Reads keypresses and deals with their events"""

        # Only proceed if this pane is active
        if self.IsShown():
            # Handles the use of ENTER to move on to the quiz itself
            if event.GetKeyCode() == wx.WXK_RETURN:
                self.event_change_pane(event)
                return

            # Handles the use of ESC to close application
            if event.GetKeyCode() == wx.WXK_ESCAPE:
                self.parent.Close()


class PaneTest(wx.Panel):
    """Master pane that handles the quiz portion of the application

            Args:
                parent (ptr): Reference to the wx.object this panel belongs to

            Attributes:
                parent (ptr): Reference to the wx.object this panel belongs to
    """

    def __init__(self, parent, *args, **kwargs):
        """Constructor"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        # Attributes
        self.parent = parent
        self.quantity = wx.GetDisplaySize()[1] // (15 + 2 * (15 + 7)) - 2
        self.radio_boxes = []
        self.current_questions = []
        self.selected_question = -1

        # Draw Style
        font = self.GetFont()
        font.SetPointSize(15)
        self.SetFont(font)
        self.SetBackgroundColour(global_colors.background)

        # Bordered Sizer
        temp = wx.StaticBox(self, label="Please select your preference level for each of the following actions")
        self.sizer_bordered = wx.StaticBoxSizer(temp, orient=wx.VERTICAL)

        # Define radio buttons
        lbl_list = ["No Preference", "Mild Preference", "Moderate Preference", "Strong Preference"]
        for i in range(self.quantity):
            rbox = cst_widget.QuizRadioBox(self, lbl_list, global_colors.background)
            self.radio_boxes.append(rbox)
            self.sizer_bordered.Add(rbox, flag=wx.CENTER | wx.EXPAND)

        # Load questions into the radio buttons
        self.pop_questions()
        self.push_questions()

        # Next button with bind
        button_next = wx.Button(self, label='Next')
        button_next.Bind(wx.EVT_BUTTON, self.event_next_question_set)

        # Bind ENTER presses to continue to the next page
        self.Bind(wx.EVT_CHAR_HOOK, self.event_keypress)

        # Main Sizer
        self.sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.sizer_main.Add(self.sizer_bordered, border=13, flag=wx.ALL | wx.EXPAND)
        self.sizer_main.Add(button_next, flag=wx.CENTER)

        self.SetSizer(self.sizer_main)

    def pop_questions(self):
        """Pop some questions to be ready for display"""
        self.current_questions = []
        if self.quantity < len(self.parent.questions):
            for i in range(self.quantity):
                self.current_questions.append(self.parent.questions.pop(0))
        else:
            self.current_questions = self.parent.questions
            self.parent.questions = []

    def push_questions(self):
        """Push question parameters into radio buttons"""
        if 0 < len(self.parent.questions):
            for i in range(self.quantity):
                self.radio_boxes[i].question_text.SetLabel(self.current_questions[i][0])
                self.radio_boxes[i].q_type = self.current_questions[i][1]
        else:
            for i in range(len(self.current_questions)):
                self.radio_boxes[i].question_text.SetLabel(self.current_questions[i][0])
                self.radio_boxes[i].q_type = self.current_questions[i][1]
            for i in range(self.quantity - len(self.current_questions)):
                self.radio_boxes[i + len(self.current_questions)].Hide()

    def event_keypress(self, event):
        """Reads keypresses and deals with their events"""

        # Only proceed if this pane is active
        if self.IsShown():
            # Handles the use of TAB and SHIFT-TAB to move through questions
            if event.GetKeyCode() == wx.WXK_TAB:
                if wx.GetKeyState(wx.WXK_SHIFT):
                    self.select_prev()
                    return
                else:
                    self.select_next()
                    return

            # Handles the use of ESC to close application
            if event.GetKeyCode() == wx.WXK_ESCAPE:
                self.parent.Close()

            # Handles the use of ENTER to move to the next set of questions
            if event.GetKeyCode() == wx.WXK_RETURN:
                self.event_next_question_set(event)
                return

            # Handles the use of number keys (1-4) to set question answer
            if event.GetKeyCode() in range(49, 53) and self.selected_question >= 0:
                self.radio_boxes[self.selected_question].SetSelection(event.GetKeyCode() - 48)
                self.select_next()
                return

    def event_next_question_set(self, event):
        """Load next set of questions or toggle frame's sizer to correspond to the summary pane"""

        # Only proceed if all radio buttons have been filled and this pane is active
        if self.IsShown():
            for rbox in self.radio_boxes:
                if rbox.GetSelection() == 0 and rbox.IsShown():
                    return

            # Commit scoring results
            for rbox in self.radio_boxes:
                self.parent.scoring[rbox.q_type] += rbox.GetSelection()

            if len(self.parent.questions) > 0:
                self.select_first()
                self.pop_questions()
                self.push_questions()

                # Reset radio buttons
                for rbox in self.radio_boxes:
                    rbox.SetSelection(0)
            else:
                self.Hide()
                self.parent.panel_summary.Show()
                self.parent.SetSizer(self.parent.sizer_summary)
                self.parent.Layout()

                self.parent.ranking = list_max_index(self.parent.scoring, 4)

                self.rank_results()

                print(self.parent.panel_summary.listofscores)
                self.parent.Freeze()
                self.parent.panel_summary.summary_panel.refresh()
                self.parent.Thaw()

    def select_next(self):
        """Select next radio button"""
        if self.selected_question == -1:
            self.selected_question = 0
            self.radio_boxes[0].SelectedQuestion(True)
            self.Layout()
        elif self.selected_question < len(self.radio_boxes) - 1:
            self.radio_boxes[self.selected_question].SelectedQuestion(False)
            self.selected_question += 1
            self.radio_boxes[self.selected_question].SelectedQuestion(True)
            self.Layout()

    def select_prev(self):
        """Select previous radio button"""
        if self.selected_question == 0:
            self.radio_boxes[0].SelectedQuestion(False)
            self.selected_question = -1
            self.Layout()
        elif self.selected_question > 0:
            self.radio_boxes[self.selected_question].SelectedQuestion(False)
            self.selected_question -= 1
            self.radio_boxes[self.selected_question].SelectedQuestion(True)
            self.Layout()

    def select_first(self):
        """Select first radio button"""
        if self.selected_question >= 0:
            self.selected_question = 0
            self.radio_boxes[0].SelectedQuestion(True)
            for rbox in self.radio_boxes[1:]:
                rbox.SelectedQuestion(False)
                self.Layout()

    def rank_results(self):
        """Rank results and populate the list"""

        print(self.parent.ranking)
        print(self.parent.scoring)

        # In the case where you have a 3-way tie for first
        if len(self.parent.ranking[0]) >= 3:
            comb = list(itertools.permutations(self.parent.ranking[0], 3))
            for key in comb:
                mask = oct(key[2] + key[1] * 8 + key[0] * 8 ** 2)
                self.add_result(mask)
            if self.parent.results:
                print("exit 3")
                return
        print("faile 3")

        # In the case where you have a 2-way tie for first
        if len(self.parent.ranking[0]) == 2:
            comb = list(itertools.permutations(self.parent.ranking[0], 2))
            for first2dig in comb:
                for lastdig in self.parent.ranking[1]:
                    mask = oct(lastdig + first2dig[1] * 8 + first2dig[0] * 8 ** 2)
                    self.add_result(mask)
            if self.parent.results:
                print("exit 2")
                return
        print("faile 2")

        # In the normal case where you have a single first pick
        if len(self.parent.ranking[0]) == 1:
            if len(self.parent.ranking[1]) >= 2:
                comb = list(itertools.permutations(self.parent.ranking[1], 2))
                for last2dig in comb:
                    mask = oct(last2dig[1] + last2dig[0] * 8 + self.parent.ranking[0][0] * 8 ** 2)
                    self.add_result(mask)
                if self.parent.results:
                    print("exit 3-2")
                    return
            print("faile 1-2")

            for lastdig in self.parent.ranking[2]:
                mask = oct(lastdig + self.parent.ranking[1][0] * 8 + self.parent.ranking[0][0] * 8 ** 2)
                self.add_result(mask)
            if self.parent.results:
                print("exit 3-1-1")
                return
            print("scree")

            for lastdig in self.parent.ranking[3]:
                mask = oct(lastdig + self.parent.ranking[1][0] * 8 + self.parent.ranking[0][0] * 8 ** 2)
                self.add_result(mask)
            if self.parent.results:
                print("exit 3-1-1-err")
                return

    def add_result(self, mask):
        try:
            self.parent.results.extend(self.parent.convert_key[int(mask, 8)])
        except KeyError:
            pass


class PaneSummary(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        self.listofscores = []

        title_text = wx.StaticText(self, size=(-1, -1), label="I AM LES TEXTQUES")
        self.summary_panel = cst_panel.ScrolledResultsPanel(self)
        #for index, score in enumerate(parent.scoring):
        #    self.listofscores.append(wx.StaticText(self, size=(-1, -1), label="0"))

        # Sizer Layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(title_text, flag=wx.ALL | wx.EXPAND)
        self.sizer.Add(self.summary_panel, proportion=1, flag=wx.ALL | wx.EXPAND)
        #for pleq in self.listofscores:
        #    self.sizer.Add(pleq, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()

    def changeIntroPanel( self, event ):
        if self.IsShown():
            self.parent.SetTitle("Question 1")
            self.Hide()
            self.parent.panelTwo.Show()

def list_max_index(ls, n):
    ls_return = []
    ord_set = list(reversed(sorted(set(ls))))

    try:
        for k in range(n):
            ls_return.append([i for i, j in enumerate(ls) if j == ord_set[k]])
    except IndexError:
        pass
    return ls_return