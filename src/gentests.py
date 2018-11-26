from __future__ import print_function
#pylint: disable=E0401
#pylint: disable=E1121

import auger
import traceback

tester = None

def start():
    print("######## Auger testing start")

    import error
    import license
    import log
    import preferences
    import version_manager
    import versions

    test_subjects = [
        error,
        log,
        preferences,
        version_manager,
        license,
        versions.v00001.install,
        versions.v00001.main,
        versions.v00001.process,
        versions.v00001.suspender,
        versions.v00001.utils,
    ]

    mock_subsitutes = {
        "genericpath": "os.path",
        "posixpath": "os.path",
    }

    global tester
    tester = auger.magic(test_subjects, mock_substitutes=mock_subsitutes)
    tester.__enter__()

    version_manager.main(done)

def done():
    print("######## Auger testing done")
    try:
        tester.__exit__(None, None, None)
    except:
        traceback.print_exc()

start()