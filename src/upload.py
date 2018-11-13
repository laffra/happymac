import glob
import inspect
import re
import os
from versions import v00001

names = [ "main", "activity", "install", "process", "server", "suspender", "utils" ]
contents = ""
short_names = {}

def shorten(name):
    return name
    if name in short_names:
        return short_names[name]
    short_names[name] = "_%d_" % len(short_names)
    return short_names[name]

for name in names:
    contents += "#" * 30 + "# %s\n\n" % name
    source = open("src/versions/v00001/%s.py" % name).read()
    mod = getattr(v00001, name)
    if name != "main":
        for key in dir(mod):
            item = getattr(mod, key)
            if inspect.isfunction(item):
                func_name = item.__name__
                source = source.replace("%s(" % func_name, "_%s__%s(" % (shorten(name), shorten(func_name)))
                source = source.replace("map(%s," % func_name, "map(_%s__%s," % (shorten(name), shorten(func_name)))
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
            contents = contents.replace("def %s(" % func_name, "def _%s__%s(" % (shorten(name), shorten(func_name)))
            contents = contents.replace("%s.%s(" % (name, func_name), "_%s__%s(" % (shorten(name), shorten(func_name)))
        if name == "utils" and inspect.isclass(item):
            class_name = item.__name__
            if class_name == "Timer":
                contents = contents.replace("class %s(" % class_name, "class _%s__%s(" % (shorten(name), shorten(class_name)))
                contents = contents.replace("%s.%s(" % (name, class_name), "_%s__%s(" % (shorten(name), shorten(class_name)))
                contents = contents.replace("super(%s," % class_name, "super(_%s__%s," % (shorten(name), shorten(class_name)))

with open("/tmp/last.py", "w") as fout:
    contents = contents.replace("\n", "@@@")
    fout.write(contents)
    fout.write("""if __name__ == "__main__":@@@    run()@@@""")

os.system(r"/Applications/Visual\ Studio\ Code.app/Contents/Resources/app/bin/code /tmp/last.py")
