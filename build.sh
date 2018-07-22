python scripts/bot_assetLister.py app/assets/assets_list app/
python build.py
rm -rf build
rm dist/w9xpopen.exe
mkdir dist/assets
cp app/assets/* dist/assets/
mv dist/main.exe dist/BOT.exe
