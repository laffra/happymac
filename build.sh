# cleanup
echo "###### clean up ###############"
echo "rm -rf build dist"
rm -rf build dist

# run py2app to package a MacOS .app file
echo
echo "###### run py2app ###############"
python setup.py py2app > /dev/null

# package up the .app into a MacOS .dmg distributable image
echo
echo "###### run create-dmg ###############"
cd dist
create-dmg happymac.app/
mv happymac\ 0.0.0.dmg happymac.dmg
cd ..

# run the result
echo
echo "###### done ###############"
echo "Distribution version is in: `pwd`/happymac.dmg"
echo "Running packaged happymac app now for testing: dist/happymac.app/Contents/MacOS/happymac"
dist/happymac.app/Contents/MacOS/happymac
