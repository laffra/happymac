# Project dependencies:

brew install pkg-config libffi
export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.2.1/lib/pkgconfig/:$PKG_CONFIG_PATH
brew install gobject-introspection
brew install cairo
pip install pycairo
pip install pyobjc-core
pip install pyobjc-framework-Quartz
pip install AppKit
pip install py2app
pip install rumps
pip install psutil
brew install gdbm

# Quartz is harder
pip download quartz
gunzip quartz-0.0.1.dev0.tar.gz
tar xvf quartz-0.0.1.dev0.tar
sed "s/requirements.txt/quartz.egg-info\/requires.txt/" < quartz-0.0.1.dev0/setup.py > quartz-0.0.1.dev0/setup2.py
mv quartz-0.0.1.dev0/setup2.py quartz-0.0.1.dev0/setup.py
pip install -e quartz-0.0.1.dev0
rm -rf quartz-0.0.1.dev0*

rm -rf .eggs