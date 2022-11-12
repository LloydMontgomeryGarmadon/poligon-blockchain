#!/bin/bash

set -o errexit -o nounset

# If the env variable NOTARIZE and the username and password variables are
# set, this will attempt to Notarize the signed DMG.

if [ ! "$FLOTEO_INSTALLER_VERSION" ]; then
	echo "WARNING: No environment variable FLOTEO_INSTALLER_VERSION set. Using 0.0.0."
	FLOTEO_INSTALLER_VERSION="0.0.0"
fi
echo "Floteo Installer Version is: $FLOTEO_INSTALLER_VERSION"

echo "Installing npm and electron packagers"
cd npm_macos || exit
npm ci
PATH=$(npm bin):$PATH
cd .. || exit

echo "Create dist/"
sudo rm -rf dist
mkdir dist

echo "Create executables with pyinstaller"
SPEC_FILE=$(python -c 'import chia; print(chia.PYINSTALLER_SPEC_PATH)')
pyinstaller --log-level=INFO "$SPEC_FILE"
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "pyinstaller failed!"
	exit $LAST_EXIT_CODE
fi
cp -r dist/daemon ../floteo-blockchain-gui/packages/gui
cd .. || exit
cd floteo-blockchain-gui || exit

echo "npm build"
lerna clean -y
npm ci
# Audit fix does not currently work with Lerna. See https://github.com/lerna/lerna/issues/1663
# npm audit fix
npm run build
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "npm run build failed!"
	exit $LAST_EXIT_CODE
fi

# Change to the gui package
cd packages/gui || exit

# sets the version for floteo-blockchain in package.json
brew install jq
cp package.json package.json.orig
jq --arg VER "$FLOTEO_INSTALLER_VERSION" '.version=$VER' package.json > temp.json && mv temp.json package.json

electron-packager . Floteo --asar.unpack="**/daemon/**" --platform=darwin \
--icon=src/assets/img/floteo.icns --overwrite --app-bundle-id=pl.floteoblockchain.blockchain \
--appVersion=$FLOTEO_INSTALLER_VERSION
LAST_EXIT_CODE=$?

# reset the package.json to the original
mv package.json.orig package.json

if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-packager failed!"
	exit $LAST_EXIT_CODE
fi

if [ "$NOTARIZE" == true ]; then
  electron-osx-sign Floteo-darwin-x64/Floteo.app --platform=darwin \
  --hardened-runtime=true --provisioning-profile=floteoblockchain.provisionprofile \
  --entitlements=entitlements.mac.plist --entitlements-inherit=entitlements.mac.plist \
  --no-gatekeeper-assess
fi
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-osx-sign failed!"
	exit $LAST_EXIT_CODE
fi

mv Floteo-darwin-x64 ../../../build_scripts/dist/
cd ../../../build_scripts || exit

DMG_NAME="Floteo-$FLOTEO_INSTALLER_VERSION.dmg"
echo "Create $DMG_NAME"
mkdir final_installer
NODE_PATH=./npm_macos/node_modules node build_dmg.js dist/Floteo-darwin-x64/Floteo.app $FLOTEO_INSTALLER_VERSION
LAST_EXIT_CODE=$?
if [ "$LAST_EXIT_CODE" -ne 0 ]; then
	echo >&2 "electron-installer-dmg failed!"
	exit $LAST_EXIT_CODE
fi

if [ "$NOTARIZE" == true ]; then
	echo "Notarize $DMG_NAME on ci"
	cd final_installer || exit
  notarize-cli --file=$DMG_NAME --bundle-id pl.floteoblockchain.blockchain \
	--username "$APPLE_NOTARIZE_USERNAME" --password "$APPLE_NOTARIZE_PASSWORD"
  echo "Notarization step complete"
else
	echo "Not on ci or no secrets so skipping Notarize"
fi

# Notes on how to manually notarize
#
# Ask for username and password. password should be an app specific password.
# Generate app specific password https://support.apple.com/en-us/HT204397
# xcrun altool --notarize-app -f Floteo-0.1.X.dmg --primary-bundle-id pl.floteoblockchain.blockchain -u username -p password
# xcrun altool --notarize-app; -should return REQUEST-ID, use it in next command
#
# Wait until following command return a success message".
# watch -n 20 'xcrun altool --notarization-info  {REQUEST-ID} -u username -p password'.
# It can take a while, run it every few minutes.
#
# Once that is successful, execute the following command":
# xcrun stapler staple Floteo-0.1.X.dmg
#
# Validate DMG:
# xcrun stapler validate Floteo-0.1.X.dmg
