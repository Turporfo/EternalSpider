Set WshShell = WScript.CreateObject("WScript.Shell")

strCurFolder = createobject("Scripting.FileSystemObject").GetFolder(".").Path '当前路径
strDesktop = WshShell.SpecialFolders("Desktop")

set oShellLink = WshShell.CreateShortcut(strDesktop & "\EternalSpider.lnk")
oShellLink.TargetPath = strCurFolder & "\EternalSpider.vbs"  '可执行文件路径
oShellLink.Arguments = "" 
oShellLink.WindowStyle = 7 '参数1默认窗口激活，参数3最大化激活，参数7最小化
oShellLink.Hotkey = "Ctrl+Shift+e"  '快捷键
oShellLink.IconLocation = strCurFolder &"\spider\favicon\favicon.ico"  
oShellLink.Description = "EternalSpider by turporfo"  
oShellLink.WorkingDirectory = strCurFolder  '起始位置
oShellLink.Save  '创建保存快捷方式