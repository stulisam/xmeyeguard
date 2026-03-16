#!/bin/bash
# 护眼小卫士 - macOS/Linux 一键安装脚本

read -p "请输入小米电视4的IP地址: " TV_IP
APK_FILE="eyeguard-1.0.0.apk"
PACKAGE="com.eyeguard.eyeguard"

echo ""
echo "[1/4] 连接电视..."
adb connect "$TV_IP":5555 || { echo "连接失败"; exit 1; }

echo ""
echo "[2/4] 安装 APK..."
adb -s "$TV_IP":5555 install -r "$APK_FILE" || { echo "安装失败"; exit 1; }

echo ""
echo "[3/4] 授予悬浮窗权限..."
adb -s "$TV_IP":5555 shell pm grant "$PACKAGE" android.permission.SYSTEM_ALERT_WINDOW \
    && echo "悬浮窗权限已授予" \
    || echo "权限授予失败，请手动执行：adb shell pm grant $PACKAGE android.permission.SYSTEM_ALERT_WINDOW"

echo ""
echo "[4/4] 启动应用..."
adb -s "$TV_IP":5555 shell monkey -p "$PACKAGE" -c android.intent.category.LAUNCHER 1

echo ""
echo "========================================"
echo " 安装完成！首次启动需要设置家长密码"
echo "========================================"
