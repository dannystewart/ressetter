taskkill /IM "4K120.exe" /F
poetry run pyinstaller --noconfirm --clean --distpath=dist --workpath=build --upx-dir=. 4k120.spec
