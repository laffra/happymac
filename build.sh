
# cleanup
echo "###### clean up ###############"
echo "rm -rf build dist"
rm -rf build dist

# run py2app to package a MacOS .app file
echo
echo "###### run py2app ###############"
python3 setup.py py2app

# package up the .app into a MacOS .dmg distributable image
echo
echo "###### run create-dmg ###############"
cd dist

echo "###### codesign subcomponents ###############"
# https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/Procedures/Procedures.html
# https://forum.xojo.com/49408-10-14-hardened-runtime-and-app-notarization/0
# https://stackoverflow.com/questions/52905940/how-to-codesign-and-enable-the-hardened-runtime-for-a-3rd-party-cli-on-xcode

# codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libgdbm.6.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libcrypto.1.0.0.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/libssl.1.0.0.dylib
codesign --force --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/Frameworks/Python.framework/Versions/2.7/Python
codesign --force --entitlements ../app.entitlements --options runtime --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/MacOS/python
codesign --force --entitlements ../app.entitlements --options runtime --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" -f happymac.app/Contents/MacOS/happymac

echo "###### create dmg ###############"
create-dmg happymac.app/
mv happymac\ 0.0.0.dmg happymac.dmg

echo "###### codesign dmg ###############"
codesign --force --options runtime --deep --sign "Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)" happymac.dmg

codesign -v happymac.dmg


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
echo "Running packaged happymac app now for testing: dist/happymac.app/Contents/MacOS/happymac"
dist/happymac.app/Contents/MacOS/happymac
