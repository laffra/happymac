#
# TODO: Fix tests, needs work on Auger's automatic test generator
#
import StringIO
import abc
from abc import ABCMeta
import collections
from collections import OrderedDict
from collections import defaultdict
import datetime
import error
import functools
import gc
import glob
import imp
import inspect
import install
import json
import license
import log
from mock import patch
import os
import os.path
import preferences
import process
import psutil
from psutil import Popen
import requests
import rumps
import rumps.rumps
from rumps.rumps import App
import suspender
import sys
import tempfile
import time
import unittest
import utils
import version_manager
import versions
import versions.v00001.main
from versions.v00001.main import HappyMacStatusBarApp
import versions.v00001.process
import versions.v00001.suspender
from versions.v00001.suspender import defaultdict
import versions.v00001.utils
from versions.v00001.utils import OnMainThread
import webbrowser
from webbrowser import BackgroundBrowser


class Version_managerTest(unittest.TestCase):
    @patch.object(os.path, 'join')
    @patch.object(os.path, 'exists')
    @patch.object(log, 'log')
    def test_find_downloaded_version(self, mock_log, mock_exists, mock_join):
        mock_log.return_value = None
        mock_exists.return_value = True
        mock_join.return_value = '/Users/chris/HappyMacApp/downloads/v00001'
        self.assertEqual(
            version_manager.find_downloaded_version(version='v00001'),
            None
        )


    @patch.object(log, 'log')
    def test_find_version(self, mock_log):
        mock_log.return_value = None
        self.assertIsInstance(
            version_manager.find_version(version='v00001'),
            __builtin__.module
        )


    def test_last_version(self):
        self.assertEqual(
            version_manager.last_version(),
            'v00001'
        )


if __name__ == "__main__":
    unittest.main()
