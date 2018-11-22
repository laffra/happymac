#
# TODO: Fix tests, needs work on Auger's automatic test generator
#
import AppKit
import Foundation
import Quartz
from Quartz import CG
from Quartz import CoreGraphics
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
import objc
import objc._convenience
import objc._convenience_mapping
from objc._convenience_mapping import selector
import objc._lazyimport
from objc._lazyimport import ObjCLazyModule
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
import struct
import suspender
import sys
import tempfile
import threading
import time
import traceback
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
from versions.v00001.utils import Timer
import webbrowser
from webbrowser import BackgroundBrowser


class UtilsTest(unittest.TestCase):
    @patch.object(App, '_nsimage_from_file')
    def test__nsimage_from_file(self, mock__nsimage_from_file):
        mock__nsimage_from_file.return_value = <NSImage 0x7fd611093700 Size={20, 20} Reps=(
    "NSBitmapImageRep 0x7fd60ec407a0 Size={32, 32} ColorSpace=sRGB IEC61966-2.1 colorspace BPS=8 BPP=32 Pixels=32x32 Alpha=YES Planar=NO Format=2 CurrentBacking=<CGImageRef: 0x7fd611745690> CGImageSource=0x7fd61170f2c0"
)>
        self.assertEqual(
            versions.v00001.utils._nsimage_from_file(path='/Users/chris/dev/happymac/icons/happy-transparent.png',dimensions=None,template=None),
            <NSImage 0x7fd60ec48f30 Size={20, 20} Reps=(
    "NSBitmapImageRep 0x7fd60efa3ca0 Size={32, 32} ColorSpace=sRGB IEC61966-2.1 colorspace BPS=8 BPP=32 Pixels=32x32 Alpha=YES Planar=NO Format=2 CurrentBacking=<CGImageRef: 0x7fd60efa95b0> CGImageSource=0x7fd60ef8cb70"
)>
        )


    def test_clear_windows_cache(self):
        self.assertEqual(
            versions.v00001.utils.clear_windows_cache(),
            None
        )


    @patch.object(ObjCLazyModule, '__getattr__')
    @patch.object(objc._convenience, 'add_convenience_methods')
    def test_get_current_app(self, mock_add_convenience_methods, mock___getattr__):
        mock_add_convenience_methods.return_value = None
        mock___getattr__.return_value = NSWorkspace()
        self.assertEqual(
            versions.v00001.utils.get_current_app(),
            {
    NSApplicationBundleIdentifier = "org.python.python";
    NSApplicationName = Python;
    NSApplicationPath = "/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app";
    NSApplicationProcessIdentifier = 44191;
    NSApplicationProcessSerialNumberHigh = 0;
    NSApplicationProcessSerialNumberLow = 1466726;
    NSWorkspaceApplicationKey = "<NSRunningApplication: 0x7fd611644610 (org.python.python - 44191)>";
}
        )


    @patch.object(objc._convenience_mapping, '__getitem__objectForKey_')
    def test_get_current_app_pid(self, mock___getitem__objectForKey_):
        mock___getitem__objectForKey_.return_value = __NSCFNumber()
        self.assertIsInstance(
            versions.v00001.utils.get_current_app_pid(),
            objc.__NSCFNumber
        )


    def test_initWithCallback_(self):
        onmainthread_instance = OnMainThread()
        self.assertIsInstance(
            onmainthread_instance.initWithCallback_,
            versions.v00001.utils.OnMainThread
        )


    @patch.object(HappyMacStatusBarApp, 'update')
    def test_run_(self, mock_update):
        mock_update.return_value = None
        onmainthread_instance = OnMainThread()
        self.assertEqual(
            onmainthread_instance.run_,
            None
        )


if __name__ == "__main__":
    unittest.main()
