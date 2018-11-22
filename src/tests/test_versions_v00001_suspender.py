#
# TODO: Fix tests, needs work on Auger's automatic test generator
#
from collections import defaultdict
import log
from mock import patch
import os
import preferences
import process
import psutil
from psutil import Popen
import unittest
import utils
import versions.v00001.process
import versions.v00001.suspender
from versions.v00001.suspender import defaultdict
import versions.v00001.utils
from versions.v00001.utils import OnMainThread


class SuspenderTest(unittest.TestCase):
    @patch.object(Popen, 'pid')
    def test_<lambda>(self, mock_pid):
        mock_pid.return_value = 508
        self.assertEqual(
            versions.v00001.suspender.<lambda>(task=psutil.Process(pid=25779, name='CrashPlanService', started='14:08:58')),
            True
        )


    @patch.object(versions.v00001.utils, 'get_current_app_pid')
    def test_activate_current_app(self, mock_get_current_app_pid):
        mock_get_current_app_pid.return_value = __NSCFNumber()
        self.assertEqual(
            versions.v00001.suspender.activate_current_app(),
            None
        )


    @patch.object(versions.v00001.process, 'resume_pid')
    def test_exit(self, mock_resume_pid):
        mock_resume_pid.return_value = True
        self.assertEqual(
            versions.v00001.suspender.exit(),
            None
        )


    @patch.object(versions.v00001.process, 'get_name')
    @patch.object(preferences, 'get')
    def test_get_suspend_preference(self, mock_get, mock_get_name):
        mock_get.return_value = None
        mock_get_name.return_value = 'Python'
        self.assertEqual(
            versions.v00001.suspender.get_suspend_preference(pid=611),
            None
        )


    @patch.object(versions.v00001.process, 'get_process')
    def test_get_suspended_tasks(self, mock_get_process):
        mock_get_process.return_value = Process()
        self.assertEqual(
            versions.v00001.suspender.get_suspended_tasks(),
            [psutil.Process(pid=87, name='CbOsxSensorServi', started='2018-11-20 00:01:50'), psutil.Process(pid=25779, name='CrashPlanService', started='14:08:58')]
        )


    @patch.object(Popen, 'pid')
    @patch.object(versions.v00001.process, 'is_system_process')
    def test_manage(self, mock_is_system_process, mock_pid):
        mock_is_system_process.return_value = False
        mock_pid.return_value = 508
        self.assertEqual(
            versions.v00001.suspender.manage(foregroundTasks=[psutil.Process(pid=32838, name='vsls-agent', started='15:44:35'), psutil.Process(pid=1, name='launchd', started='2018-11-20 00:01:42'), psutil.Process(pid=33509, name='Python', started='15:52:08'), psutil.Process(pid=33514, name='Python', started='15:52:08'), psutil.Process(pid=32263, name='bash', started='15:44:26'), psutil.Process(pid=32584, name='Code Helper', started='15:44:30'), psutil.Process(pid=32301, name='Code Helper', started='15:44:26'), psutil.Process(pid=467, name='Code Helper', started='2018-11-20 00:02:35'), psutil.Process(pid=32262, name='Code Helper', started='15:44:26'), psutil.Process(pid=436, name='Code Helper', started='2018-11-20 00:02:27'), psutil.Process(pid=395L, name='Electron', started='2018-11-20 00:02:24'), psutil.Process(pid=32261, name='Code Helper', started='15:44:24'), psutil.Process(pid=44191, name='Python', started='15:59:46')],backgroundTasks=[psutil.Process(pid=374, name='Google Chrome', started='2018-11-20 00:02:22'), psutil.Process(pid=159, name='coreaudiod', started='2018-11-20 00:01:50'), psutil.Process(pid=168, name='WindowServer', started='2018-11-20 00:01:51'), psutil.Process(pid=1489, name='com.docker.hyperkit', started='2018-11-20 00:03:14'), psutil.Process(pid=64674, status='terminated')]),
            None
        )


    @patch.object(versions.v00001.process, 'get_name')
    @patch.object(versions.v00001.process, 'resume_pid')
    def test_resume_process(self, mock_resume_pid, mock_get_name):
        mock_resume_pid.return_value = True
        mock_get_name.return_value = 'Python'
        self.assertEqual(
            versions.v00001.suspender.resume_process(manual=False,pid=38310),
            None
        )


    @patch.object(preferences, 'set')
    def test_set_suspend_preference(self, mock_set):
        mock_set.return_value = None
        self.assertEqual(
            versions.v00001.suspender.set_suspend_preference(name='com.docker.hyperkit',value=False),
            None
        )


    @patch.object(versions.v00001.process, 'get_name')
    @patch.object(versions.v00001.process, 'suspend_pid')
    def test_suspend_process(self, mock_suspend_pid, mock_get_name):
        mock_suspend_pid.return_value = True
        mock_get_name.return_value = 'Python'
        self.assertEqual(
            versions.v00001.suspender.suspend_process(manual=False,pid=64674),
            None
        )


if __name__ == "__main__":
    unittest.main()
