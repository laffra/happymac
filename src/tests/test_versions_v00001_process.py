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
from psutil import AccessDenied
from psutil import Popen
import psutil._common
from psutil._common import addr
import re
from re import Scanner
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


class ProcessTest(unittest.TestCase):

    @patch.object(Popen, 'pid')
    @patch.object(Popen, 'wrapper')
    @patch.object(Popen, '__hash__')
    @patch.object(Popen, '__eq__')
    def test_child_processes(self, mock___eq__, mock___hash__, mock_wrapper, mock_pid):
        mock___eq__.return_value = True
        mock___hash__.return_value = 3750713895001177006
        mock_wrapper.return_value = [psutil.Process(pid=33514, name='Python', started='15:52:08')]
        mock_pid.return_value = 508
        self.assertEqual(
            versions.v00001.process.child_processes(includeSelf=False,pid=30420),
            []
        )


    def test_clear_process_cache(self):
        self.assertEqual(
            versions.v00001.process.clear_process_cache(),
            None
        )


    @patch.object(log, 'log')
    def test_cpu(self, mock_log):
        mock_log.return_value = None
        self.assertEqual(
            versions.v00001.process.cpu(pid=197),
            0.0
        )


    def test_create_process(self):
        self.assertIsInstance(
            versions.v00001.process.create_process(pid=403),
            psutil.Process
        )


    @patch.object(App, 'clicked')
    @patch.object(App, '__init__')
    @patch.object(App, 'run')
    @patch.object(ObjCLazyModule, '__getattr__')
    @patch.object(App, 'text')
    @patch.object(objc._convenience, 'add_convenience_methods')
    def test_execute_as_root(self, mock_add_convenience_methods, mock_text, mock___getattr__, mock_run, mock___init__, mock_clicked):
        mock_add_convenience_methods.return_value = None
        mock_text.return_value = u'igov&1nm'
        mock___getattr__.return_value = NSWorkspace()
        mock_run.return_value = Response()
        mock___init__.return_value = None
        mock_clicked.return_value = 1
        self.assertEqual(
            versions.v00001.process.execute_as_root(command='kill -CONT 25779',description='resume process 25779 (CrashPlanService)'),
            True
        )


    def test_execute_shell_command(self):
        self.assertEqual(
            versions.v00001.process.execute_shell_command(command='kill -STOP 396',operation='suspend',pid=396),
            True
        )


    @patch.object(Popen, '__hash__')
    def test_family(self, mock___hash__):
        mock___hash__.return_value = 3750713895001177006
        self.assertEqual(
            versions.v00001.process.family(pid=395L),
            [psutil.Process(pid=32838, name='vsls-agent', started='15:44:35'), psutil.Process(pid=33509, name='Python', started='15:52:08'), psutil.Process(pid=33514, name='Python', started='15:52:08'), psutil.Process(pid=32263, name='bash', started='15:44:26'), psutil.Process(pid=32301, name='Code Helper', started='15:44:26'), psutil.Process(pid=467, name='Code Helper', started='2018-11-20 00:02:35'), psutil.Process(pid=32584, name='Code Helper', started='15:44:30'), psutil.Process(pid=32262, name='Code Helper', started='15:44:26'), psutil.Process(pid=1, name='launchd', started='2018-11-20 00:01:42'), psutil.Process(pid=436, name='Code Helper', started='2018-11-20 00:02:27'), psutil.Process(pid=395L, name='Electron', started='2018-11-20 00:02:24'), psutil.Process(pid=32261, name='Code Helper', started='15:44:24'), psutil.Process(pid=44191, name='Python', started='15:59:46')]
        )


    @patch.object(psutil, 'cpu_percent')
    def test_get_cpu_percent(self, mock_cpu_percent):
        mock_cpu_percent.return_value = 31.4
        self.assertEqual(
            versions.v00001.process.get_cpu_percent(),
            31.4
        )


    @patch.object(Popen, 'name')
    def test_get_name(self, mock_name):
        mock_name.return_value = 'iTunesHelper'
        self.assertEqual(
            versions.v00001.process.get_name(pid=337),
            'trustd'
        )


    @patch.object(Popen, '__init__')
    def test_get_process(self, mock___init__):
        mock___init__.return_value = None
        self.assertIsInstance(
            versions.v00001.process.get_process(pid=581),
            psutil.Process
        )


    @patch.object(addr, 'wrapper')
    def test_get_total_time(self, mock_wrapper):
        mock_wrapper.return_value = pcputimes()
        self.assertEqual(
            versions.v00001.process.get_total_time(pid=112),
            None
        )


    def test_is_system_process(self):
        self.assertEqual(
            versions.v00001.process.is_system_process(pid=572),
            False
        )


    @patch.object(Popen, 'cmdline')
    @patch.object(re, 'sub')
    def test_location(self, mock_sub, mock_cmdline):
        mock_sub.return_value = '/usr/libexec/xartstorageremoted'
        mock_cmdline.return_value = ['/Applications/Google Chrome.app/Contents/Versions/70.0.3538.102/Google Chrome Helper.app/Contents/MacOS/Google Chrome Helper', '--type=renderer', '--field-trial-handle=1014873197873945333,4216514382308589012,131072', '--service-pipe-token=6365535800482859512', '--lang=en-GB', '--extension-process', '--enable-offline-auto-reload', '--enable-offline-auto-reload-visible-only', '--num-raster-threads=2', '--enable-zero-copy', '--enable-gpu-memory-buffer-compositor-resources', '--enable-main-frame-before-activation', '--service-request-channel-token=6365535800482859512', '--renderer-client-id=8', '--no-v8-untrusted-code-mitigations', '--seatbelt-client=276']
        self.assertEqual(
            versions.v00001.process.location(pid=1479),
            'com.docker.osxfs'
        )


    @patch.object(addr, 'wrapper')
    def test_parent_pid(self, mock_wrapper):
        mock_wrapper.return_value = pcputimes()
        self.assertEqual(
            versions.v00001.process.parent_pid(pid=1),
            0
        )


    @patch.object(Popen, 'pid')
    @patch.object(Popen, '__hash__')
    def test_parents(self, mock___hash__, mock_pid):
        mock___hash__.return_value = 3750713895001177006
        mock_pid.return_value = 508
        self.assertEqual(
            versions.v00001.process.parents(includeSelf=True,pid=395L),
            [psutil.Process(pid=1, name='launchd', started='2018-11-20 00:01:42'), psutil.Process(pid=395L, name='Electron', started='2018-11-20 00:02:24')]
        )


    def test_resume_pid(self):
        self.assertEqual(
            versions.v00001.process.resume_pid(pid=25801),
            True
        )


    def test_set_allow_root(self):
        self.assertEqual(
            versions.v00001.process.set_allow_root(allow_root=True),
            None
        )


    def test_suspend_pid(self):
        self.assertEqual(
            versions.v00001.process.suspend_pid(pid=64674),
            True
        )


    @patch.object(App, 'alert')
    def test_terminate_pid(self, mock_alert):
        mock_alert.return_value = 1
        self.assertEqual(
            versions.v00001.process.terminate_pid(pid=64674),
            True
        )


    @patch.object(psutil, 'pids')
    def test_top(self, mock_pids):
        mock_pids.return_value = [44192, 44191, 44148, 35300, 35299, 33514, 33509, 33482, 33481, 32888, 32862, 32858, 32838, 32584, 32301, 32263, 32262, 32261, 32194, 31766, 31694, 31481, 30445, 30420, 29038, 29035, 29030, 29027, 27001, 26917, 26820, 25824, 25801, 25779, 22968, 22967, 44134, 5298, 8105, 7499, 13250, 3582, 14756, 88448, 86853, 86646, 57949, 80704, 80373, 77797, 98000, 97999, 97998, 97413, 64230, 40062, 38310, 66584, 64678, 64677, 64674, 15794, 6656, 98448, 64724, 11790, 68073, 699, 34942, 95521, 65607, 7005, 6997, 6996, 17991, 13470, 79714, 78533, 78515, 76230, 75782, 75775, 40800, 36160, 33373, 81677, 17265, 17202, 72990, 71797, 66105, 66099, 65530, 65390, 64931, 64930, 64929, 64927, 61982, 60891, 58202, 47988, 47987, 47985, 46725, 46724, 46190, 46156, 44008, 2474, 96208, 57070, 46979, 83674, 55689, 52949, 52273, 52270, 52192, 41106, 41105, 41104, 38896, 36134, 36133, 34475, 34474, 34316, 34223, 34202, 34043, 33925, 33923, 19519, 10238, 7286, 6219, 6218, 6217, 5696, 5584, 5182, 5179, 4143, 3408, 2539, 1489, 1481, 1480, 1479, 1478, 1477, 789, 748, 747, 743, 739, 738, 643, 622, 621, 619, 618, 615, 613, 612, 611, 610, 609, 606, 594, 593, 587, 584, 582, 581, 580, 579, 572, 570, 569, 567, 566, 562, 558, 545, 531, 530, 529, 527, 521, 519, 517, 511, 508, 507, 505, 504, 503, 502, 500, 499, 498, 496, 495, 494, 492, 490, 488, 486, 484, 479, 478, 476, 472, 467, 466, 465, 461, 460, 459, 458, 454, 451, 447, 444, 443, 437, 436, 434, 433, 432, 431, 429, 428, 427, 426, 423, 422, 421, 420, 419, 418, 417, 416, 415, 414, 413, 412, 411, 410, 409, 406, 405, 404, 403, 402, 401, 399, 397, 396, 395, 394, 393, 392, 390, 389, 388, 386, 385, 384, 381, 379, 378, 377, 376, 374, 371, 370, 369, 368, 366, 365, 361, 359, 358, 357, 356, 355, 353, 352, 351, 350, 349, 348, 347, 346, 345, 343, 342, 341, 340, 339, 338, 337, 336, 334, 333, 332, 330, 329, 328, 319, 318, 317, 312, 311, 305, 300, 299, 293, 289, 287, 286, 283, 282, 279, 278, 277, 270, 269, 268, 265, 264, 257, 254, 250, 249, 243, 241, 239, 238, 237, 236, 235, 234, 232, 229, 228, 225, 219, 214, 204, 199, 198, 197, 196, 195, 194, 189, 188, 187, 186, 185, 184, 181, 168, 166, 164, 161, 159, 154, 151, 150, 148, 147, 144, 137, 135, 129, 128, 126, 123, 122, 121, 120, 119, 118, 116, 115, 113, 112, 111, 110, 105, 104, 103, 101, 99, 98, 96, 95, 94, 93, 92, 91, 90, 87, 86, 85, 83, 78, 77, 76, 69, 68, 64, 63, 61, 59, 58, 57, 54, 52, 51, 50, 46, 45, 1, 0]
        self.assertEqual(
            versions.v00001.process.top(count=5,exclude=[psutil.Process(pid=32263, name='bash', started='15:44:26'), psutil.Process(pid=1, name='launchd', started='2018-11-20 00:01:42'), psutil.Process(pid=32261, name='Code Helper', started='15:44:24'), psutil.Process(pid=395, name='Electron', started='2018-11-20 00:02:24'), psutil.Process(pid=44191L, name='Python', started='15:59:46')]),
            [psutil.Process(pid=611, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=168, name='WindowServer', started='2018-11-20 00:01:51'), psutil.Process(pid=374, name='Google Chrome', started='2018-11-20 00:02:22'), psutil.Process(pid=1489, name='com.docker.hyperkit', started='2018-11-20 00:03:14'), psutil.Process(pid=235, name='mds_stores', started='2018-11-20 00:01:53')]
        )


if __name__ == "__main__":
    unittest.main()
