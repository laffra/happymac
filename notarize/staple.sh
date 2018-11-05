echo "staple the notarization to the app"
xcrun stapler staple happymac.dmg

echo "verify with spctl"
spctl -a -v happymac.dmg