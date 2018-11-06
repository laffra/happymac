
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

echo "###### codesign subcomponents ###############"
# https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/Procedures/Procedures.html
# https://forum.xojo.com/49408-10-14-hardened-runtime-and-app-notarization/0
# https://stackoverflow.com/questions/52905940/how-to-codesign-and-enable-the-hardened-runtime-for-a-3rd-party-cli-on-xcode

rm -rf happymac.app/Contents/Frameworks/libgio-2.0.0.dylib
rm -rf happymac.app/Contents/Resources/lib/tcl8.6
rm -rf happymac.app/Contents/Resources/lib/tk8.6
rm -rf happymac.app/Contents/Resources/lib/tk8

codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libffi.6.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libgio-2.0.0.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libgirepository-1.0.1.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libglib-2.0.0.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libgmodule-2.0.0.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libgobject-2.0.0.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libintl.8.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libpcre.1.dylib
codesign --force --entitlements ../app.entitlements --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/Python.framework/Versions/2.7/Python
codesign --force --entitlements ../app.entitlements --options runtime --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/MacOS/python
codesign --force --entitlements ../app.entitlements --options runtime --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/MacOS/happymac
# codesign --force --entitlements ../app.entitlements --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libffi.6.dylib

echo "###### create dmg ###############"
create-dmg happymac.app/
mv happymac\ 0.0.0.dmg happymac.dmg

echo "###### codesign dmg ###############"
codesign --force --options runtime --deep --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" happymac.dmg

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
