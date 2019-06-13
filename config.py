# -*- coding: utf-8 -*-
"""This module loads common parameters from the config.yaml for reference"""

import os
import yaml

from cst_frame import app_root, is_demo

# Defining & Initializing config variables
staticbox_label = None
rbox_labels = None
summary_col_1 = None
summary_col_2 = None
summary_col_3 = None
summary_col_4 = None
link_1 = None
link_2 = None
link_3 = None
link_4 = None
link_vis_1 = None
link_vis_2 = None
link_vis_3 = None
link_vis_4 = None
link_var_1 = None
link_var_2 = None
link_var_3 = None
link_var_4 = None
summary_text = None
initials = None
instructions = None


def load_config():
    """Load the parameters"""
    if is_demo:
        _file = 'config_demo.yaml'
    else:
        _file = 'config_production.yaml'

    with open(os.path.join(app_root, _file), 'r') as stream:
        _temp = yaml.safe_load(stream)

        # Load in variables that match those defined above and are not modules or the like
        for k in globals():
            if k[:2] != "__" and k not in ['yaml', 'os', 'app_root', 'is_demo', 'load_config']:
                globals()[k] = _temp[k]
