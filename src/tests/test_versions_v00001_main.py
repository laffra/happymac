#
# TODO: Fix tests, needs work on Auger's automatic test generator
#
import abc
from abc import ABCMeta
import collections
from collections import OrderedDict
from collections import defaultdict
import datetime
import error
import functools
import gc
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
import time
import unittest
import utils
import version_manager
import versions.v00001.main
from versions.v00001.main import HappyMacStatusBarApp
import versions.v00001.process
import versions.v00001.suspender
from versions.v00001.suspender import defaultdict
import versions.v00001.utils
from versions.v00001.utils import OnMainThread
import webbrowser
from webbrowser import BackgroundBrowser


class MainTest(unittest.TestCase):
    @patch.object(App, '__new__')
    @patch.object(App, 'icon')
    @patch.object(App, 'menu')
    @patch.object(ABCMeta, '__instancecheck__')
    @patch.object(App, 'menu')
    @patch.object(App, '__init__')
    def test_create_menu(self, mock___init__, mock_menu, mock___instancecheck__, mock_menu, mock_icon, mock___new__):
        mock___init__.return_value = None
        mock_menu.return_value = Menu()
        mock___instancecheck__.return_value = False
        mock_menu.return_value = None
        mock_icon.return_value = None
        mock___new__.return_value = MenuItem()
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.create_menu(),
            None
        )


    def test_get_icon(self):
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.get_icon(percent=31.4),
            '/Users/chris/dev/happymac/icons/unhappy-transparent.png'
        )


    @patch.object(versions.v00001.process, 'get_name')
    @patch.object(log, 'log')
    @patch.object(webbrowser, 'open')
    def test_google(self, mock_open, mock_log, mock_get_name):
        mock_open.return_value = True
        mock_log.return_value = None
        mock_get_name.return_value = 'Python'
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.google(menuItem=<MenuItem: [u'Google this...' -> []; callback: <functools.partial object at 0x114d3f4c8>]>,pid=44784),
            None
        )


    def test_handle_action(self):
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.handle_action(menuItem=None),
            None
        )


    @patch.object(versions.v00001.process, 'set_allow_root')
    def test_menuDidClose_(self, mock_set_allow_root):
        mock_set_allow_root.return_value = None
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.menuDidClose_(menu=<NSMenu: 0x7fd6111823d0>
	Title:
	Open bounds: [t=1418, l=2067, b=1099, r=2341]
	Supermenu: 0x0 (None), autoenable: YES
	Items:     (
        "<NSMenuItem: 0x7fd60ee6a530 About HappyMac - v00001>",
        "<NSMenuItem: 0x7fd6111665e0 >",
        "<NSMenuItem: 0x7fd61107bd80 Current App Tasks>",
        "<NSMenuItem: 0x7fd6128274e0 Python - 32%, submenu: 0x7fd612e8f940 ()>",
        "<NSMenuItem: 0x7fd6124f7d00 Electron - 5%, submenu: 0x7fd612cbdaf0 ()>",
        "<NSMenuItem: 0x7fd61282f980 Code Helper - 4%, submenu: 0x7fd61170bc70 ()>",
        "<NSMenuItem: 0x7fd611163fe0 >",
        "<NSMenuItem: 0x7fd6110940e0 Background Tasks:>",
        "<NSMenuItem: 0x7fd60ed202d0 >",
        "<NSMenuItem: 0x7fd60ee69f70 Suspended Background Tasks:>",
        "<NSMenuItem: 0x7fd612916590 CbOsxSensorService - 0%, submenu: 0x7fd612bba2d0 ()>",
        "<NSMenuItem: 0x7fd6124abcc0 idea - 0%, submenu: 0x7fd612bcc970 ()>",
        "<NSMenuItem: 0x7fd61281d400 CrashPlanService - 0%, submenu: 0x7fd612acc4b0 ()>",
        "<NSMenuItem: 0x7fd61226e130 CrashPlanWeb - 0%, submenu: 0x7fd612e9f0e0 ()>",
        "<NSMenuItem: 0x7fd611166ed0 >",
        "<NSMenuItem: 0x7fd60ee6c1f0 Quit HappyMac>"
    )),
            None
        )


    @patch.object(versions.v00001.process, 'set_allow_root')
    def test_menuWillOpen_(self, mock_set_allow_root):
        mock_set_allow_root.return_value = None
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.menuWillOpen_(menu=<NSMenu: 0x7fd6111823d0>
	Title:
	Open bounds: [t=1418, l=2067, b=1099, r=2341]
	Supermenu: 0x0 (None), autoenable: YES
	Items:     (
        "<NSMenuItem: 0x7fd60ee6a530 About HappyMac - v00001>",
        "<NSMenuItem: 0x7fd6111665e0 >",
        "<NSMenuItem: 0x7fd61107bd80 Current App Tasks>",
        "<NSMenuItem: 0x7fd6128274e0 Python - 32%, submenu: 0x7fd612e8f940 ()>",
        "<NSMenuItem: 0x7fd6124f7d00 Electron - 5%, submenu: 0x7fd612cbdaf0 ()>",
        "<NSMenuItem: 0x7fd61282f980 Code Helper - 4%, submenu: 0x7fd61170bc70 ()>",
        "<NSMenuItem: 0x7fd611163fe0 >",
        "<NSMenuItem: 0x7fd6110940e0 Background Tasks:>",
        "<NSMenuItem: 0x7fd60ed202d0 >",
        "<NSMenuItem: 0x7fd60ee69f70 Suspended Background Tasks:>",
        "<NSMenuItem: 0x7fd612916590 CbOsxSensorService - 0%, submenu: 0x7fd612bba2d0 ()>",
        "<NSMenuItem: 0x7fd6124abcc0 idea - 0%, submenu: 0x7fd612bcc970 ()>",
        "<NSMenuItem: 0x7fd61281d400 CrashPlanService - 0%, submenu: 0x7fd612acc4b0 ()>",
        "<NSMenuItem: 0x7fd61226e130 CrashPlanWeb - 0%, submenu: 0x7fd612e9f0e0 ()>",
        "<NSMenuItem: 0x7fd611166ed0 >",
        "<NSMenuItem: 0x7fd60ee6c1f0 Quit HappyMac>"
    )),
            None
        )


    @patch.object(App, 'menu')
    def test_menu_is_highlighted(self, mock_menu):
        mock_menu.return_value = Menu()
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.menu_is_highlighted(),
            None
        )


    @patch.object(App, '__new__')
    @patch.object(Popen, 'pid')
    @patch.object(versions.v00001.utils, 'get_current_app_pid')
    @patch.object(versions.v00001.process, 'cpu')
    @patch.object(versions.v00001.process, 'get_name')
    @patch.object(App, 'icon')
    @patch.object(App, '__init__')
    @patch.object(App, 'add')
    def test_menu_item_for_process(self, mock_add, mock___init__, mock_icon, mock_get_name, mock_cpu, mock_get_current_app_pid, mock_pid, mock___new__):
        mock_add.return_value = None
        mock___init__.return_value = None
        mock_icon.return_value = None
        mock_get_name.return_value = 'Python'
        mock_cpu.return_value = 0.43375777413908767
        mock_get_current_app_pid.return_value = __NSCFNumber()
        mock_pid.return_value = 508
        mock___new__.return_value = MenuItem()
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.menu_item_for_process(p=psutil.Process(pid=610, name='Google Chrome Helper', started='2018-11-20 00:02:51'),resumable=False,suspendable=False),
            None
        )


    @patch.object(versions.v00001.suspender, 'resume_process')
    def test_resume(self, mock_resume_process):
        mock_resume_process.return_value = None
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.resume(menuItem=<MenuItem: [u'Resume' -> []; callback: <functools.partial object at 0x116d0de68>]>,pid=64674),
            None
        )


    @patch.object(versions.v00001.suspender, 'suspend_process')
    def test_suspend(self, mock_suspend_process):
        mock_suspend_process.return_value = None
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.suspend(menuItem=<MenuItem: [u'Suspend' -> []; callback: <functools.partial object at 0x11734bcb0>]>,pid=64674),
            None
        )


    @patch.object(versions.v00001.process, 'terminate_pid')
    def test_terminate(self, mock_terminate_pid):
        mock_terminate_pid.return_value = True
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.terminate(menuItem=<MenuItem: [u'Terminate' -> []; callback: <functools.partial object at 0x118b52ba8>]>,pid=64674),
            None
        )


    @patch.object(versions.v00001.process, 'clear_process_cache')
    @patch.object(versions.v00001.suspender, 'activate_current_app')
    @patch.object(versions.v00001.utils, 'get_current_app_pid')
    @patch.object(versions.v00001.process, 'top')
    @patch.object(versions.v00001.utils, 'clear_windows_cache')
    @patch.object(versions.v00001.process, 'get_cpu_percent')
    @patch.object(versions.v00001.process, 'family')
    @patch.object(versions.v00001.suspender, 'get_suspended_tasks')
    @patch.object(versions.v00001.suspender, 'manage')
    def test_update(self, mock_manage, mock_get_suspended_tasks, mock_family, mock_get_cpu_percent, mock_clear_windows_cache, mock_top, mock_get_current_app_pid, mock_activate_current_app, mock_clear_process_cache):
        mock_manage.return_value = None
        mock_get_suspended_tasks.return_value = [psutil.Process(pid=87, name='CbOsxSensorServi', started='2018-11-20 00:01:50'), psutil.Process(pid=25779, name='CrashPlanService', started='14:08:58')]
        mock_family.return_value = [psutil.Process(pid=1, name='launchd', started='2018-11-20 00:01:42'), psutil.Process(pid=44148, status='terminated'), psutil.Process(pid=30445, name='Google Chrome Helper', started='15:26:37'), psutil.Process(pid=32194, name='Google Chrome Helper', started='15:42:39'), psutil.Process(pid=27001, name='Google Chrome Helper', started='14:41:21'), psutil.Process(pid=33481, name='Google Chrome Helper', started='15:51:15'), psutil.Process(pid=80373, name='Google Chrome Helper', started='21:11:46'), psutil.Process(pid=98000, name='Google Chrome Helper', started='20:58:54'), psutil.Process(pid=97413, name='Google Chrome Helper', started='20:58:52'), psutil.Process(pid=615, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=572, name='Google Chrome Helper', started='2018-11-20 00:02:46'), psutil.Process(pid=738, name='Google Chrome Helper', started='2018-11-20 00:02:58'), psutil.Process(pid=4143, name='Google Chrome Helper', started='2018-11-20 00:03:40'), psutil.Process(pid=40800, name='Google Chrome Helper', started='2018-11-20 11:30:16'), psutil.Process(pid=32888, name='Google Chrome Helper', started='15:46:00'), psutil.Process(pid=582, name='Google Chrome Helper', started='2018-11-20 00:02:47'), psutil.Process(pid=618, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=6656, name='Google Chrome Helper', started='18:20:40'), psutil.Process(pid=97998, name='Google Chrome Helper', started='20:58:54'), psutil.Process(pid=64230, name='Google Chrome Helper', started='20:52:05'), psutil.Process(pid=40062, name='Google Chrome Helper', started='19:53:25'), psutil.Process(pid=97999, name='Google Chrome Helper', started='20:58:54'), psutil.Process(pid=567, name='Google Chrome Helper', started='2018-11-20 00:02:46'), psutil.Process(pid=98448, name='Google Chrome Helper', started='18:19:14'), psutil.Process(pid=521, name='Google Chrome Helper', started='2018-11-20 00:02:41'), psutil.Process(pid=562, name='Google Chrome Helper', started='2018-11-20 00:02:46'), psutil.Process(pid=622, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=612, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=570, name='Google Chrome Helper', started='2018-11-20 00:02:46'), psutil.Process(pid=566, name='Google Chrome Helper', started='2018-11-20 00:02:46'), psutil.Process(pid=619, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=613, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=569, name='Google Chrome Helper', started='2018-11-20 00:02:46'), psutil.Process(pid=38310, name='Google Chrome Helper', started='19:52:51'), psutil.Process(pid=80704, name='Google Chrome Helper', started='21:11:49'), psutil.Process(pid=30420, name='Google Chrome Helper', started='15:24:52'), psutil.Process(pid=610, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=584, name='Google Chrome Helper', started='2018-11-20 00:02:47'), psutil.Process(pid=29027, name='Google Chrome Helper', started='14:58:59'), psutil.Process(pid=580, name='Google Chrome Helper', started='2018-11-20 00:02:46'), psutil.Process(pid=68073, name='Google Chrome Helper', started='2018-11-21 13:48:34'), psutil.Process(pid=33482, name='Google Chrome Helper', started='15:51:17'), psutil.Process(pid=579, name='Google Chrome Helper', started='2018-11-20 00:02:46'), psutil.Process(pid=77797, name='Google Chrome Helper', started='21:11:29'), psutil.Process(pid=472, name='Google Chrome Helper', started='2018-11-20 00:02:35'), psutil.Process(pid=699, name='Google Chrome Helper', started='2018-11-21 13:35:41'), psutil.Process(pid=621, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=587, name='Google Chrome Helper', started='2018-11-20 00:02:47'), psutil.Process(pid=609, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=611, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=64724, name='Google Chrome Helper', started='18:12:13'), psutil.Process(pid=581, name='Google Chrome Helper', started='2018-11-20 00:02:47'), psutil.Process(pid=458, name='Google Chrome Helper', started='2018-11-20 00:02:33'), psutil.Process(pid=374L, name='Google Chrome', started='2018-11-20 00:02:22')]
        mock_get_cpu_percent.return_value = 31.4
        mock_clear_windows_cache.return_value = None
        mock_top.return_value = [psutil.Process(pid=64724, name='Google Chrome Helper', started='18:12:13'), psutil.Process(pid=374, name='Google Chrome', started='2018-11-20 00:02:22'), psutil.Process(pid=611, name='Google Chrome Helper', started='2018-11-20 00:02:51'), psutil.Process(pid=1489, name='com.docker.hyperkit', started='2018-11-20 00:03:14'), psutil.Process(pid=610, name='Google Chrome Helper', started='2018-11-20 00:02:51')]
        mock_get_current_app_pid.return_value = __NSCFNumber()
        mock_activate_current_app.return_value = None
        mock_clear_process_cache.return_value = None
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.update(force_update=False),
            None
        )


    @patch.object(App, 'menu')
    @patch.object(App, '__delitem__')
    @patch.object(OrderedDict, 'items')
    @patch.object(App, 'insert_after')
    def test_update_menu(self, mock_insert_after, mock_items, mock___delitem__, mock_menu):
        mock_insert_after.return_value = None
        mock_items.return_value = [(u'About HappyMac - v00001', <MenuItem: [u'About HappyMac - v00001' -> []; callback: <bound method HappyMacStatusBarApp.about of <versions.v00001.main.HappyMacStatusBarApp object at 0x10fbee610>>]>), ('separator_1', <rumps.rumps.SeparatorMenuItem object at 0x10e530210>), (u'Current App Tasks', <MenuItem: [u'Current App Tasks' -> []; callback: None]>), (u'Google Chrome - 22%', <MenuItem: [u'Google Chrome - 22%' -> ['Google this...', 'Terminate']; callback: None]>), (u'Google Chrome Helper - 14%', <MenuItem: [u'Google Chrome Helper - 14%' -> ['Google this...', 'Terminate']; callback: None]>), ('separator_2', <rumps.rumps.SeparatorMenuItem object at 0x10e02f3d0>), (u'Background Tasks:', <MenuItem: [u'Background Tasks:' -> []; callback: None]>), (u'WindowServer - 5%', <MenuItem: [u'WindowServer - 5%' -> ['Google this...', 'Suspend', 'Terminate']; callback: None]>), (u'Code Helper - 7%', <MenuItem: [u'Code Helper - 7%' -> ['Google this...', 'Suspend', 'Terminate']; callback: None]>), (u'Code Helper - 6%', <MenuItem: [u'Code Helper - 6%' -> ['Google this...', 'Suspend', 'Terminate']; callback: None]>), (u'Electron - 4%', <MenuItem: [u'Electron - 4%' -> ['Google this...', 'Suspend', 'Terminate']; callback: None]>), ('separator_3', <rumps.rumps.SeparatorMenuItem object at 0x10fbeee50>), (u'Suspended Background Tasks:', <MenuItem: [u'Suspended Background Tasks:' -> []; callback: None]>), (u'com.docker.hyperkit - 0%', <MenuItem: [u'com.docker.hyperkit - 0%' -> ['Google this...', 'Resume', 'Terminate']; callback: None]>), (u'qemu-system-i386 - 0%', <MenuItem: [u'qemu-system-i386 - 0%' -> ['Google this...', 'Resume', 'Terminate']; callback: None]>), (u'CbOsxSensorService - 0%', <MenuItem: [u'CbOsxSensorService - 0%' -> ['Google this...', 'Resume', 'Terminate']; callback: None]>), (u'idea - 0%', <MenuItem: [u'idea - 0%' -> ['Google this...', 'Resume', 'Terminate']; callback: None]>), (u'CrashPlanService - 0%', <MenuItem: [u'CrashPlanService - 0%' -> ['Google this...', 'Resume', 'Terminate']; callback: None]>), (u'CrashPlanWeb - 0%', <MenuItem: [u'CrashPlanWeb - 0%' -> ['Google this...', 'Resume', 'Terminate']; callback: None]>), ('separator_4', <rumps.rumps.SeparatorMenuItem object at 0x10fbeeed0>), (u'Quit HappyMac', <MenuItem: [u'Quit HappyMac' -> []; callback: <bound method HappyMacStatusBarApp.quit of <versions.v00001.main.HappyMacStatusBarApp object at 0x10fbee610>>]>)]
        mock___delitem__.return_value = None
        mock_menu.return_value = Menu()
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.update_menu(background_tasks=[psutil.Process(pid=159, name='coreaudiod', started='2018-11-20 00:01:50'), psutil.Process(pid=168, name='WindowServer', started='2018-11-20 00:01:51'), psutil.Process(pid=1489, name='com.docker.hyperkit', started='2018-11-20 00:03:14'), psutil.Process(pid=64674, status='terminated'), psutil.Process(pid=610, name='Google Chrome Helper', started='2018-11-20 00:02:51')],foreground_tasks=[psutil.Process(pid=32838, name='vsls-agent', started='15:44:35'), psutil.Process(pid=33509, name='Python', started='15:52:08'), psutil.Process(pid=33514, name='Python', started='15:52:08'), psutil.Process(pid=32263, name='bash', started='15:44:26'), psutil.Process(pid=32584, name='Code Helper', started='15:44:30'), psutil.Process(pid=32301, name='Code Helper', started='15:44:26'), psutil.Process(pid=467, name='Code Helper', started='2018-11-20 00:02:35'), psutil.Process(pid=32262, name='Code Helper', started='15:44:26'), psutil.Process(pid=1, name='launchd', started='2018-11-20 00:01:42'), psutil.Process(pid=436, name='Code Helper', started='2018-11-20 00:02:27'), psutil.Process(pid=395L, name='Electron', started='2018-11-20 00:02:24'), psutil.Process(pid=32261, name='Code Helper', started='15:44:24'), psutil.Process(pid=44191, name='Python', started='15:59:46')],force_update=True,suspended_tasks=[psutil.Process(pid=25801, name='CrashPlanWeb', started='14:09:04'), psutil.Process(pid=25779, name='CrashPlanService', started='14:08:58'), psutil.Process(pid=396, name='idea', started='2018-11-20 00:02:24'), psutil.Process(pid=87, name='CbOsxSensorServi', started='2018-11-20 00:01:50')]),
            None
        )


    @patch.object(versions.v00001.process, 'get_cpu_percent')
    @patch.object(App, 'icon')
    def test_update_statusbar(self, mock_icon, mock_get_cpu_percent):
        mock_icon.return_value = None
        mock_get_cpu_percent.return_value = 31.4
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.update_statusbar(),
            None
        )


    @patch.object(version_manager, 'last_version')
    def test_version(self, mock_last_version):
        mock_last_version.return_value = 'v00001'
        happymacstatusbarapp_instance = HappyMacStatusBarApp(<function done at 0x10e13fa28>)
        self.assertEqual(
            happymacstatusbarapp_instance.version(),
            'v00001'
        )


if __name__ == "__main__":
    unittest.main()
