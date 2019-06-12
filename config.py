# -*- coding: utf-8 -*-
"""This module loads common parameters from the config.yaml for reference"""

import os
import yaml

from cst_frame import app_root, is_demo


def load_config():
    """Load the parameters"""
    if is_demo:
        _file = 'config_demo.yaml'
    else:
        _file = 'config_production.yaml'

    with open(os.path.join(app_root, _file), 'r') as stream:
        _temp = yaml.safe_load(stream)
        globals()["staticbox_label"] = _temp["staticbox_label"]
        globals()["rbox_labels"] = _temp["rbox_labels"]
        globals()["summary_col_1"] = _temp["summary_col_1"]
        globals()["summary_col_2"] = _temp["summary_col_2"]
        globals()["summary_col_3"] = _temp["summary_col_3"]
        globals()["summary_col_4"] = _temp["summary_col_4"]
        globals()["link_1"] = _temp["link_1"]
        globals()["link_2"] = _temp["link_2"]
        globals()["link_3"] = _temp["link_1"]
        globals()["link_4"] = _temp["link_4"]
        globals()["link_vis_1"] = _temp["link_vis_1"]
        globals()["link_vis_2"] = _temp["link_vis_2"]
        globals()["link_vis_3"] = _temp["link_vis_3"]
        globals()["link_vis_4"] = _temp["link_vis_4"]
        globals()["link_var_1"] = _temp["link_var_1"]
        globals()["link_var_2"] = _temp["link_var_2"]
        globals()["link_var_3"] = _temp["link_var_3"]
        globals()["link_var_4"] = _temp["link_var_4"]
        globals()["summary_text"] = _temp["summary_text"]
        globals()["initials"] = _temp["initials"]