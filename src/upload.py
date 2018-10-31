import glob
import os

SEPARATOR = "#@#@#@#@#"

last_version = glob.glob("src/versions/v[0-9]*")[-1]
output_path = os.path.join("/tmp/", last_version.split(os.path.sep)[-1]) + ".py"

print "Saving latest version in %s" % output_path

with open(output_path, "w") as fout:
    for file in glob.glob(os.path.join(last_version, "*.py")):
        print "add file %s" % file
        fout.write("@@@%s %s@@@" % (SEPARATOR, file[len("src/versions/v00000/"):]))
        fout.write(open(file).read().replace("\n", "@@@"))
        fout.write("@@@")

os.system("open %s" % output_path)
