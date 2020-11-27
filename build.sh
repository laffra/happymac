#!/bin/bash
set -e

rm -rf ~/HappyMacApp build dist

RED='\x1B[0;31m'
NC='\x1B[0m'

IDENTITY='Developer ID Application: LAFFRA JOHANNES (29P9D64BXJ)'

echo -e "${RED}-1. install dependencies"
python -m pip install -r requirements.txt

echo -e "${RED}0. Probably need a new version?${NC}"
python src/version.py

echo -e "${RED}1. run pyinstaller - this takes 15 seconds...${NC}"
cp app/pyinstaller.spec .
pyinstaller --onefile --windowed --osx-bundle-identifier com.chrislaffra.osx.happymac pyinstaller.spec
rm pyinstaller.spec

rm -rf build
echo -e "${RED}2. cp -R happymac.app dist${NC}"
cp -R app/happymac.app.template dist/happymac.app
echo -e "${RED}3. mv dist/happymac dist/happymac.app/Contents/MacOS${NC}"
mv dist/happymac dist/happymac.app/Contents/MacOS

echo -e "${RED}4. code sign package${NC}"
codesign -v -f --deep -i com.chrislaffra.osx.happymac -s "${IDENTITY}" dist/happymac.app/Contents/MacOs/happymac
codesign -v -f -i com.chrislaffra.osx.happymac -s "${IDENTITY}" dist/happymac.app

pushd dist
echo -e "${RED}5. create-dmg HappyMac.app${NC}"
src/vendor/create-dmg HappyMac.app
mv happymac\ 0.1.0.dmg happymac.dmg
popd

echo -e "${RED}6. code sign dmg${NC}"
ls -l dist
codesign -v -f -i com.chrislaffra.osx.happymac -s "${IDENTITY}" dist/happymac.dmg

echo -e "${RED}7. done building${NC}"
echo -e "${RED}8. Final step: open dist/happymac.dmg"
open dist/happymac.dmg
