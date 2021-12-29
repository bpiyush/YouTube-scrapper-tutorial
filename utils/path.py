"""
Utilities for path processing/parsing etc.
"""
from os.path import dirname, realpath

repo_path = dirname(dirname(dirname(realpath(__file__))))
