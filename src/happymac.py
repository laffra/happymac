#pylint: disable=E0401

import error
import sys
import version_manager

try:
    version_manager.main()
except:
    error.error("Could not launch HappyMac")
    sys.exit(1)
