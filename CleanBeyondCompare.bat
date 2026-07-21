@echo off
chcp 936 >nul
title 清理Beyond Compare缓存

echo 正在清理 Beyond Compare 4 缓存文件...

:: 检查文件夹是否存在
if exist "C:\Users\Lenovo\AppData\Roaming\Scooter Software\Beyond Compare 4" (
    echo 找到目标文件夹，开始清理...
    
    :: 删除文件夹下所有文件和子文件夹
    del /f /s /q "C:\Users\Lenovo\AppData\Roaming\Scooter Software\Beyond Compare 4\*.*" 2>nul
    for /d %%i in ("C:\Users\Lenovo\AppData\Roaming\Scooter Software\Beyond Compare 4\*") do rd /s /q "%%i" 2>nul
    
    echo 清理完成！
) else (
    echo 错误：找不到目标文件夹
    echo 请确认路径是否正确
)

echo.
echo 即将退出...
timeout /t 2 >nul
exit