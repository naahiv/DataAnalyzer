cp App.py App.pyw
git add . && git commit -m "readying for compilation" && git push origin master
rm -rf "dist\App"
pyinstaller --onedir "App.pyw"
