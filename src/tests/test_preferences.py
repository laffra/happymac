import genericpath
from genericpath import unicode
import log
from mock import patch
import os
import os.path
from os.path import unicode
import preferences
import sys
import unittest


class PreferencesTest(unittest.TestCase):
    def test_get(self):
        self.assertEqual(
            preferences.get(default='v00006',key='version'),
            'v00001'
        )


    @patch.object(posixpath, 'join')
    @patch.object(posixpath, 'expanduser')
    @patch.object(genericpath, 'exists')
    def test_get_preferences_path(self, mock_exists, mock_expanduser, mock_join):
        mock_exists.return_value = True
        mock_expanduser.return_value = '/Users/chris'
        mock_join.return_value = u'/Users/chris/HappyMacApp/downloads/v00006'
        self.assertEqual(
            preferences.get_preferences_path(),
            '/Users/chris/HappyMacApp/happymac.prefs'
        )


    @patch.object(log, 'log')
    def test_set(self, mock_log):
        mock_log.return_value = None
        self.assertEqual(
            preferences.set(value='v00001',key='version'),
            None
        )


if __name__ == "__main__":
    unittest.main()
