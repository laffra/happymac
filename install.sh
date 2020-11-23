
sudo easy_install --upgrade pip

# Project dependencies:
PIP=pip


echo "### Install Python dependencies"
sudo $PIP install pycairo
sudo $PIP install pyobjc-core
sudo $PIP install pyobjc-framework-Quartz
sudo $PIP install AppKit
sudo $PIP install py2app
sudo $PIP install rumps
sudo $PIP install psutil
sudo $PIP install requests
sudo $PIP install chardet
sudo $PIP install pyinstaller==3.4

echo "### SETUP Dependencies"
brew install pkg-config libffi
export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.2.1/lib/pkgconfig/:$PKG_CONFIG_PATH
brew install gobject-introspection
brew install cairo


brew install gdbm

./install-quartz.sh

rm -rf .eggs
