#
# TODO: Fix tests, needs work on Auger's automatic test generator
#
from collections import defaultdict
import datetime
import error
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
import sys
import unittest
import utils
import versions.v00001.process
import versions.v00001.suspender
from versions.v00001.suspender import defaultdict
import versions.v00001.utils
from versions.v00001.utils import OnMainThread


class LicenseTest(unittest.TestCase):
    @patch.object(preferences, 'get')
    def test_get_license(self, mock_get):
        mock_get.return_value = None
        self.assertEqual(
            license.get_license(),
            u'0e69a4f4-ae73-47f8-8d87-7205b4b96e15'
        )


if __name__ == "__main__":
    unittest.main()
