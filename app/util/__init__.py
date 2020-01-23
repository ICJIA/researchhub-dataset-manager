"""
A custom library for maintaining datasets on the ICJIA Data Portal 
==================================================================

This package provides utility functionalities to update and generate datasets
to be published on the ICJIA Data Portal through a user-friedly command-line
interface.

Main features
-------------
    * Automating the dataset maintanance process.
    * Generating a dataset in a JSON format contining metatdata and
      the actual data.
    * Interacting with a sqlite database file storing raw data.
    * Interacting with the Data Portal backend server.
    * Providing a user interface for manually processing datasets.
"""

from util.data.api import *
from util.database.api import *
from util.dataset.api import *
from util.fs.api import *
from util.ui.api import *