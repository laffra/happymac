
echo "Check for status"
echo -n "############### Enter Apple Password: "
read -s password
echo

UUID=`cat request.uuid | grep UUID | sed "s/.* //"`
echo "The last request:"
echo $UUID
ls -l request.uuid

xcrun altool --notarization-history -u laffra@gmail.com -p $password

xcrun altool --notarization-info $UUID -u laffra@gmail.com -p $password
