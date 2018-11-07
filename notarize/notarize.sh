echo -n "############### Enter Apple Password: "
read -s password
echo

echo "Uploading to the app store for notarization now..."
xcrun altool --notarize-app -f ../dist/happymac.dmg --primary-bundle-id app.happymac -u laffra@gmail.com -p $password &> request.uuid
# should respond with something like:
# RequestUUID = 28fad4c5-68b3-4dbf-a0d4-fbde8e6a078f

echo "Upload result:"
cat request.uuid

echo "Next, wait and run ./check.sh until success is reported"

