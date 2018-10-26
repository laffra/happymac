# cleanup
rm -rf build dist

# run py2app to package a MacOS .app file
python setup.py py2app

# package up the .app into a MacOS .dmg distributable image
cd dist
create-dmg happymac.app/
mv happymac\ 0.0.0.dmg happymac.dmg

# run the result
echo "Distribution version is in: dist/happymac.dmg"
happymac.app/Contents/MacOS/happymac
