
echo "###### codesign ###############"
# http://www.manpagez.com/man/1/codesign/
# https://developer.apple.com/library/archive/technotes/tn2206/_index.html
# https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/Procedures/Procedures.html
# https://forum.xojo.com/49408-10-14-hardened-runtime-and-app-notarization/0
# https://stackoverflow.com/questions/52905940/how-to-codesign-and-enable-the-hardened-runtime-for-a-3rd-party-cli-on-xcode


ID="Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)"

for filename in $(find dist/happymac.app/ -name "*.dylib"); do
    codesign -v -f -s "$ID" $filename
done
for filename in $(find dist/happymac.app/ -name "*.so"); do
    codesign -v -f -s "$ID" $filename
done
codesign -v -f -s "$ID" dist/happymac.app/Contents/Frameworks/Python.framework/Versions/2.7/Python
codesign -v -f --entitlements app.entitlements -o runtime -s "$ID" dist/happymac.app/Contents/MacOS/python
codesign -v -f --entitlements app.entitlements -o runtime -s "$ID" dist/happymac.app/Contents/MacOS/happymac

spctl --assess --type execute dist/happymac.app