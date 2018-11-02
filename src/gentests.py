#pylint: disable=E0401
#pylint: disable=E1121

import auger
import traceback

tester = None

def start():
    print "######## Auger testing start"

    import error
    import log
    import preferences
    import version_manager

    test_subjects = [
        error,
        log,
        preferences,
        version_manager,
    ]
    global tester
    tester = auger.magic(test_subjects)
    tester.__enter__()

    version_manager.main(done)

def done():
    print "######## Auger testing done"
    try:
        tester.__exit__(None, None, None)
    except:
        traceback.print_exc()

start()