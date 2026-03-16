@echo off
REM 护眼小卫士 - Windows 一键安装脚本
REM 使用前请确保：
REM 1. 安装了 ADB（Android Platform Tools）
REM 2. 小米电视4 开启了 ADB 调试（设置 -> 账号与安全 -> ADB调试）
REM 3. 电视和电脑在同一局域网

set /p TV_IP="请输入小米电视4的IP地址（可在 设置->网络->当前网络 中查看）: "
set APK_FILE=eyeguard-1.0.0.apk
set PACKAGE=com.eyeguard.eyeguard

echo.
echo [1/4] 连接电视...
adb connect %TV_IP%:5555
if %errorlevel% neq 0 (
    echo 连接失败，请检查 IP 地址和 ADB 调试是否已开启
    pause
    exit /b 1
)

echo.
echo [2/4] 安装 APK...
adb -s %TV_IP%:5555 install -r %APK_FILE%
if %errorlevel% neq 0 (
    echo 安装失败，请检查 APK 文件是否存在
    pause
    exit /b 1
)

echo.
echo [3/4] 授予悬浮窗权限（SYSTEM_ALERT_WINDOW）...
adb -s %TV_IP%:5555 shell pm grant %PACKAGE% android.permission.SYSTEM_ALERT_WINDOW
if %errorlevel% neq 0 (
    echo 权限授予失败，可稍后手动执行：
    echo adb shell pm grant %PACKAGE% android.permission.SYSTEM_ALERT_WINDOW
) else (
    echo 悬浮窗权限已授予
)

echo.
echo [4/4] 启动应用...
adb -s %TV_IP%:5555 shell monkey -p %PACKAGE% -c android.intent.category.LAUNCHER 1

echo.
echo ========================================
echo  安装完成！
echo  请在电视上按 HOME 键返回主屏幕
echo  在应用列表中找到「护眼小卫士」并打开
echo  首次启动需要设置家长密码
echo ========================================
pause
