"""Provide modules for working with ICJIA's web-published datasets.

This package provides modules to update and generate datasets to be published
on ICJIA website with a user-friedly command-line interface. The package
consists of the following six modules:

``database.py``: Offers functions for interacting with the SQL database. 
``inputtools.py``: Offers functions for handling user input.
``outputtools.py``: Offers functions for generating outputs.
``population.py``: Offers functions for automating the processs of
    updating the ``Population`` table in the database.
``simplecount.py``: Offers functions for automating the process of
    updating the ``SimpleCount`` table in the database.
``ui.py``: Offers functions for user interface.

"""
from . import database
from . import inputtools
from . import outputtools
from . import population
from . import simplecount
from . import ui