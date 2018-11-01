import os
import platform
import rumps
import traceback

home_dir = os.path.join(os.path.expanduser("~"), "HappyMacApp")

def get_system_info():
    return """
System Details:

    Version:  %s
    Compiler: %s
    Build:    %s
    Platform: %s
    System:   %s
    Node:     %s
    Release:  %s
    Version:  %s

""" % (
        platform.python_version(),
        platform.python_compiler(),
        platform.python_build(),
        platform.platform(),
        platform.system(),
        platform.node(),
        platform.release(),
        platform.version(),
    )

def get_home_dir_info():
    return "\nHome Folder:\n%s\n\n" % "\n".join([
        "    %s" % os.path.join(root, filename)
        for root, _, filenames in os.walk(home_dir)
        for filename in filenames
    ])

def get_preferences():
    try:
        import preferences
        import json
        if preferences.preferences:
            return "Preferences:\n%s\n\n" % json.dumps(preferences.preferences, indent=4)
    except:
        return ""

def get_versions():
    try:
        import version_manager
        return "Versions:\n%s\n\n" % version_manager.get_versions()
    except:
        return ""


def error(message):
    stack = "Stack:\n%s\n\n" % "".join(traceback.format_stack()[:-1])
    exception = "Exception:\n%s\n\n" % traceback.format_exc()
    error = "%s\n%s%s%s%s%s%s%s\n" % (message, get_system_info(), get_home_dir_info(), exception, get_preferences(), get_versions(), stack, message)
    path = os.path.join(os.path.expanduser("~"), "happymac.error")
    with open(path, "w") as out:
        out.write(error)
    print error
    rumps.notification("HappyMac", "%s. For details see:" % message, path)