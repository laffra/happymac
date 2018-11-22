from collections import defaultdict
import datetime
import log
from mock import patch
import os
import os.path
import preferences
import process
import psutil
#
# TODO: Fix tests, needs work on Auger's automatic test generator
#
from psutil import Popen
import sys
import unittest
import utils
import versions.v00001.process
import versions.v00001.suspender
from versions.v00001.suspender import defaultdict
import versions.v00001.utils
from versions.v00001.utils import OnMainThread


class LogTest(unittest.TestCase):
    @patch.object(os.path, 'join')
    @patch.object(os.path, 'exists')
    def test_get_log_path(self, mock_exists, mock_join):
        mock_exists.return_value = True
        mock_join.return_value = '/Users/chris/HappyMacApp/downloads/v00001'
        self.assertEqual(
            log.get_log_path(),
            '/Users/chris/HappyMacApp/happymac_log.txt'
        )


    def test_log(self):
        self.assertEqual(
            log.log(message='Google process 44784 ()',error=None),
            None
        )


if __name__ == "__main__":
    unittest.main()
