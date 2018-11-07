# cleanup
echo "###### clean up ###############"
echo "rm -rf build dist"
rm -rf build dist

# run py2app to package a MacOS .app file
echo
echo "###### run py2app ###############"
export PKG_CONFIG_PATH=/usr/local/Cellar/libffi/3.2.1/lib/pkgconfig/:$PKG_CONFIG_PATH
python setup.py py2app > /dev/null
rm -rf .eggs

# package up the .app into a MacOS .dmg distributable image
echo
echo "###### run create-dmg ###############"
cd dist

echo "###### fix python to Nov1 version #############"
hdiutil attach ../happymac-nov-1.dmg
rm -rf HappyMac.app/Contents/Frameworks/Python.framework
rm -rf HappyMac.app/Contents/MacOS/python
cp -r /Volumes/happymac/happymac.app/Contents/Frameworks/Python.framework HappyMac.app/Contents/Frameworks/
cp -r /Volumes/happymac/happymac.app/Contents/MacOS/python HappyMac.app/Contents/MacOS
hdiutil detach /Volumes/happymac

echo "###### codesign subcomponents ###############"
# https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/Procedures/Procedures.html
# https://forum.xojo.com/49408-10-14-hardened-runtime-and-app-notarization/0
# https://stackoverflow.com/questions/52905940/how-to-codesign-and-enable-the-hardened-runtime-for-a-3rd-party-cli-on-xcode

for filename in $(find HappyMac.app/ -name "*.dylib"); do
    echo "Codesign $filename"
    codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f $filename
done
for filename in $(find HappyMac.app/ -name "*.so"); do
    echo "Codesign $filename"
    codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f $filename
done
codesign --force --entitlements ../app.entitlements --options runtime --deep --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f HappyMac.app/Contents/Frameworks/Python.framework/Versions/2.7/Python
codesign --force --entitlements ../app.entitlements --options runtime --deep --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f HappyMac.app/Contents/MacOS/python
codesign --force --entitlements ../app.entitlements --options runtime --deep --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f HappyMac.app/Contents/MacOS/happymac

echo "###### create dmg ###############"
create-dmg happymac.app/
mv happymac\ 0.1.0.dmg happymac.dmg

echo "###### codesign dmg ###############"
codesign --force --entitlements ../app.entitlements --options runtime --deep --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" happymac.dmg

# create pkg
hdiutil attach happymac.dmg
pkgbuild --root /Volumes/happymac --version 1.0 --identifier app.happymac --install-location / happymac.pkg
hdiutil detach /Volumes/happymac
ls -l
cd ..

# run the result
echo
echo "###### done ###############"
echo "Distribution version is in: `pwd`/dist/happymac.dmg"
dist/happymac.app/Contents/MacOS/happymac
# open dist/happymac.dmg
