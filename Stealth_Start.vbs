Set WshShell = CreateObject("WScript.Shell")
' Arkada siyah CMD ekrani cikmadan tamamen gizli baslatir.
WshShell.Run "cmd /c cd /d """ & CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & """ && ""C:\Users\eidan\AppData\Local\Programs\Python\Python310\python.exe"" main.py", 0, False
