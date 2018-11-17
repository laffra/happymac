import glob
import inspect
import re
import os
from versions import v00001

names = [ "main", "install", "process", "suspender", "utils" ]
contents = ""
short_names = {}

SHORTEN_NAME = False
LOCAL_TEST = False

if LOCAL_TEST:
    SEPARATOR = "\n"
    DEST_DIR = "src"
else:
    SEPARATOR = "@@@"
    DEST_DIR = "/tmp"

def shorten(name):
    if not SHORTEN_NAME:
        return name
    if name in short_names:
        return short_names[name]
    short_names[name] = "h%d" % len(short_names)
    return short_names[name]

for name in names:
    contents += "#" * 30 + "# %s\n\n" % name
    source = open("src/versions/v00001/%s.py" % name).read()
    mod = getattr(v00001, name)
    for key in reversed(sorted(dir(mod))):
        item = getattr(mod, key)
        if SHORTEN_NAME and key.upper() == key:
            source = source.replace(key, "%s" % shorten(key))
        if name != "main":
            if inspect.isfunction(item):
                func_name = item.__name__
                if func_name[0] == "_":
                    continue
                source = source.replace("%s(" % func_name, "%s_%s(" % (shorten(name), shorten(func_name)))
                source = source.replace("map(%s," % func_name, "map(%s_%s," % (shorten(name), shorten(func_name)))
                source = source.replace(" = %s" % func_name, " = %s_%s" % (shorten(name), shorten(func_name)))
    contents += source + "\n"

for name in names:
    if name == "main":
        continue
    contents = contents.replace("import %s\n" % name, "")
    mod = getattr(v00001, name)
    for key in dir(mod):
        item = getattr(mod, key)
        if inspect.isfunction(item):
            func_name = item.__name__
            if func_name[0] == "_":
                continue
            contents = contents.replace("def %s(" % func_name, "def %s_%s(" % (shorten(name), shorten(func_name)))
            contents = contents.replace("%s.%s(" % (name, func_name), "%s_%s(" % (shorten(name), shorten(func_name)))
        if name == "utils" and inspect.isclass(item):
            class_name = item.__name__
            if class_name == "Timer":
                contents = contents.replace("class %s(" % class_name, "class %s_%s(" % (shorten(name), shorten(class_name)))
                contents = contents.replace("%s.%s(" % (name, class_name), "%s_%s(" % (shorten(name), shorten(class_name)))
                contents = contents.replace("super(%s," % class_name, "super(%s_%s," % (shorten(name), shorten(class_name)))

with open("%s/last.py" % DEST_DIR, "w") as fout:
    if SEPARATOR != "\n":
        contents = contents.replace("\n", SEPARATOR)
    fout.write(contents)
    fout.write("""if __name__ == "__main__":%s    run()%s""" % (SEPARATOR, SEPARATOR))

os.system(r"/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code %s/last.py" % DEST_DIR)
