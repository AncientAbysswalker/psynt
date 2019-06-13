# -*- coding: utf-8 -*-
"""This module defines panes - master panels that act as direct children of the progenitor frame"""

import os
import wx
import itertools

import cst_panel
import cst_widget
import gbl_colors
import config
from cst_frame import app_root


def list_max_index(ls, n):
    """Takes a list of numbers and returns the n max indices from max to min. Ties are returned as tuples at index"""
    ls_return = []

    reverse_ordered_list = list(reversed(sorted(set(ls))))

    try:
        for k in range(n):
            ls_return.append([i for i, j in enumerate(ls) if j == reverse_ordered_list[k]])
    except IndexError:
        pass

    return ls_return


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

        # Load cover image
        image = wx.Image(os.path.join(app_root, 'img', 'cover.jpg'))
        (w1, h1) = image.GetSize()
        (w2, h2) = wx.GetDisplaySize()

        # Resize accordingly
        if w1 / h1 < w2 / h2:
            image_bitmap = wx.StaticBitmap(self, bitmap=wx.Bitmap(image.Rescale(w2, h1 * w2 / w1)))
        else:
            image_bitmap = wx.StaticBitmap(self, bitmap=wx.Bitmap(image.Rescale(w1 * h2 / h1, h2)))

        # Bind keypresses to an event that governs their behaviour
        self.Bind(wx.EVT_CHAR_HOOK, self.event_keypress)

        # Main Sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(image_bitmap, proportion=1, flag=wx.ALL | wx.EXPAND)

        self.SetSizer(self.sizer)

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
                return

    def event_change_pane(self, event):
        """Toggle frame's sizer to correspond to the quiz pane"""

        # Only proceed if this pane is active
        if self.IsShown():
            self.Hide()
            self.parent.pane_instruct.Show()
            self.parent.pane_instruct.SetFocus()
            self.parent.SetSizer(self.parent.sizer_instruct)
            self.parent.Layout()


class PaneInstruct(wx.Panel):
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

        # Draw Style
        font = self.GetFont()
        font.SetPointSize(15)
        self.SetFont(font)
        self.SetBackgroundColour(gbl_colors.background)

        # Bind keypresses to continue to the next page
        self.Bind(wx.EVT_CHAR_HOOK, self.event_keypress)

        # Instructions
        instruct_header = wx.StaticText(self, size=(-1, -1), label="Instructions:")
        instruct = wx.TextCtrl(self, -1, config.instructions +
                               "\r\n\r\n You can navigate this quiz either by clicking your answers "
                               "manually. If you would prefer to answer using the keyboard, press TAB to "
                               "enter keyboard mode. The controls are as follows:\r\n > Keys 1-4 answer "
                               "questions and move on to the next question\r\n > TAB moves to the next "
                               "question\r\n > SHIFT-TAB moves back a question\r\n > ENTER submits your"
                               "answer for the current batch of questions",
                               size=(-1, 35),
                               style=wx.TE_MULTILINE |
                                     wx.TE_WORDWRAP |
                                     wx.TE_NO_VSCROLL |
                                     wx.TE_READONLY |
                                     wx.BORDER_NONE)
        instruct.SetBackgroundColour(gbl_colors.background)

        # Start button with bind
        button_start = wx.Button(self, label='Start')
        button_start.Bind(wx.EVT_BUTTON, self.event_change_pane)

        # Main Sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(instruct_header)
        self.sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), flag=wx.EXPAND)
        self.sizer.Add(instruct, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.sizer.Add(button_start, flag=wx.CENTER)
        self.SetSizer(self.sizer)

        self.Layout()

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

    def event_change_pane(self, event):
        """Toggle frame's sizer to correspond to the quiz pane"""

        # Only proceed if this pane is active
        if self.IsShown():
            self.Hide()
            self.parent.pane_quiz.Show()
            self.parent.pane_quiz.SetFocus()
            self.parent.SetSizer(self.parent.sizer_quiz)
            self.parent.Layout()


class PaneTest(wx.Panel):
    """Master pane that handles the quiz portion of the application

            Args:
                parent (ptr): Reference to the wx.object this panel belongs to

            Attributes:
                parent (ptr): Reference to the wx.object this panel belongs to
                quantity (int): Integer count of the number of questions to populate - based on your screen size
                radio_boxes (list: ptr->wx.widget): List of pointers to all radio box widgets generated
                current_questions (list: list): List of all questions to be shown in current set of questions
                selected_question (int): Current selected question for tab-through handling. -1 indicates no selection
    """

    def __init__(self, parent, *args, **kwargs):
        """Constructor"""
        wx.Panel.__init__(self, parent, *args, **kwargs)

        # Attributes
        self.parent = parent
        self.quantity = wx.GetDisplaySize()[1] // (15 + 2 * (15 + 7)) - 2  # Take height (px) and divide by entry size
        self.radio_boxes = []
        self.current_questions = []
        self.selected_question = -1

        # Draw Style
        font = self.GetFont()
        font.SetPointSize(15)
        self.SetFont(font)
        self.SetBackgroundColour(gbl_colors.background)

        # Bordered sizer with text surrounding all quiz questions
        temp = wx.StaticBox(self, label=config.staticbox_label)
        self.sizer_bordered = wx.StaticBoxSizer(temp, orient=wx.VERTICAL)

        # Load in radio buttons and place a reference in a list
        for i in range(self.quantity):
            rbox = cst_widget.QuizRadioBox(self, config.rbox_labels, gbl_colors.background)
            self.radio_boxes.append(rbox)
            self.sizer_bordered.Add(rbox, flag=wx.CENTER | wx.EXPAND)

        # Load questions and push them to the radio buttons
        self.pop_questions()
        self.push_questions()

        # Add a 'Next' button with click binding
        button_next = wx.Button(self, label='Next')
        button_next.Bind(wx.EVT_BUTTON, self.event_next_question_set)

        # Bind keypresses to an event that governs their behaviour
        self.Bind(wx.EVT_CHAR_HOOK, self.event_keypress)

        # Main Sizer
        self.sizer_main = wx.BoxSizer(wx.VERTICAL)
        self.sizer_main.Add(self.sizer_bordered, border=13, flag=wx.ALL | wx.EXPAND)
        self.sizer_main.Add(button_next, flag=wx.CENTER)

        self.SetSizer(self.sizer_main)

    def pop_questions(self):
        """Pop some questions to be ready for display. If there are too few, pop the rest of the questions"""
        self.current_questions = []
        if self.quantity < len(self.parent.questions):
            for i in range(self.quantity):
                self.current_questions.append(self.parent.questions.pop(0))
        else:
            self.current_questions = self.parent.questions
            self.parent.questions = []

    def push_questions(self):
        """Push question parameters into radio buttons, hiding any that remain unfilled at the end"""
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

            self.Layout()

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

            # If there are more questions, pop/push a set and reset the radio buttons to no selection
            if len(self.parent.questions) > 0:
                self.select_first()
                self.pop_questions()
                self.push_questions()

                # Reset radio buttons
                for rbox in self.radio_boxes:
                    rbox.SetSelection(0)

            # Otherwise, toggle frame's sizer to correspond to the summary pane and carry out ranking
            else:
                self.Hide()
                self.parent.pane_summary.Show()
                self.parent.SetSizer(self.parent.sizer_summary)
                self.parent.pane_summary.SetFocus()
                self.parent.Layout()

                # Determine the proper ranking (indices) of scores and determine your results from the key
                self.parent.ranking = list_max_index(self.parent.scoring, 4)

                print(self.parent.ranking)
                self.determine_results()

                # Update the summary pane, freezing and thawing to prevent graphical artifacts on population
                self.parent.Freeze()
                self.parent.pane_summary.panel_scroll.refresh()
                self.parent.Thaw()

    def select_next(self):
        """Select next radio button"""
        if self.selected_question == -1:
            self.selected_question = 0
            self.radio_boxes[0].SelectedQuestion(True)
            self.Layout()
        elif self.selected_question < len(self.current_questions) - 1:#len(self.radio_boxes) - 1:
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
            self.radio_boxes[self.selected_question].SelectedQuestion(False)
            self.selected_question = 0
            self.radio_boxes[0].SelectedQuestion(True)
            self.Layout()

    def determine_results(self):
        """Populate the results based on ranking"""

        print(self.parent.scoring)

        combined_ranks = []

        for ranks in self.parent.ranking[:3]:
            combined_ranks.extend(ranks)

        comb = list(itertools.permutations(combined_ranks, 3))
        for key in comb:
            mask = oct(key[2] + key[1] * 8 + key[0] * 8 ** 2)
            self.add_result(mask, "|".join([config.initials[i] for i in key]))

    def add_result(self, mask, rank):
        try:
            self.parent.results.extend([i + [rank] for i in self.parent.convert_key[int(mask, 8)]])
        except KeyError:
            pass


class PaneSummary(wx.Panel):
    """Master pane that handles the quiz portion of the application

                Args:
                    parent (ptr): Reference to the wx.object this panel belongs to

                Attributes:
                    parent (ptr): Reference to the wx.object this panel belongs to
                    quantity (int): Integer count of the number of questions to populate - based on your screen size
                    radio_boxes (list: ptr->wx.widget): List of pointers to all radio box widgets generated
                    current_questions (list: list): List of all questions to be shown in current set of questions
                    selected_question (int): Current selected question for tab-through handling. -1 indicates no selection
    """

    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent

        # Draw Style
        font = self.GetFont()
        font.SetPointSize(15)
        self.SetFont(font)
        self.SetBackgroundColour(gbl_colors.background)

        # Bind keypresses to an event that governs their behaviour
        self.Bind(wx.EVT_CHAR_HOOK, self.event_keypress)

        self.listofscores = []

        title_text = wx.StaticText(self, size=(-1, -1), label=config.summary_text)
        self.panel_scroll = cst_panel.ScrolledResultsPanel(self)
        #for index, score in enumerate(parent.scoring):
        #    self.listofscores.append(wx.StaticText(self, size=(-1, -1), label="0"))

        # Sizer Layout
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(title_text, flag=wx.ALL | wx.EXPAND)
        self.sizer.Add(wx.StaticLine(self, style=wx.LI_HORIZONTAL), flag=wx.EXPAND)
        self.sizer.Add(self.panel_scroll, proportion=1, flag=wx.ALL | wx.EXPAND)
        #for pleq in self.listofscores:
        #    self.sizer.Add(pleq, proportion=1, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()

    def event_keypress(self, event):
        """Reads keypresses and deals with their events"""

        # Only proceed if this pane is active
        if self.IsShown():
            # Handles the use of ESC to close application
            if event.GetKeyCode() == wx.WXK_ESCAPE:
                self.parent.Close()
