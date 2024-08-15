#!/bin/sh
echo -e "\033[0;34mPreparing build folder\033[0m"
if [ -d build_pyxapp ]; then rm -r build_pyxapp; fi
mkdir -p build_pyxapp/levels
cd build_pyxapp
cp ../levels.py .
cp ../rock.py .
cp ../player.py .
cp ../ticoban.py .
cp ../levels/oficial.txt levels/
cp ../assets.pyxres .
cp ../assets.pyxpal .
echo -e "\033[0;34mPackaging the game\033[0m"
pyxel package . ticoban.py
mv build_pyxapp.pyxapp ../ticoban-pyxel.pyxapp

echo -e "\033[0;34mMaking the executable\033[0m"
pyxel app2exe ticoban-pyxel.pyxapp
cd ..
# rm -r build_pyxapp
echo -e "\033[0;34mMaking the executable\033[0m"
pyxel app2exe ticoban-pyxel.pyxapp

if [[ $# -eq 1 && $1 = '--appimage' ]]; then
	echo -e "\033[0;34mPreparing AppImage\033[0m"
	mkdir -p AppDir/usr/bin
	cp ticoban-pyxel AppDir/usr/bin/ticoban
fi
echo -e "\033[0;32mFinished\033[0m"