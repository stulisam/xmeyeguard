[app]
title = 护眼小卫士
package.name = eyeguard
package.domain = com.eyeguard

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ogg,mp3,wav,json
source.include_patterns = assets/*,data/*

version = 1.0.0

requirements = python3,kivy==2.3.0,pyjnius

# 方向：横屏（电视）
orientation = landscape

# Android 配置
android.minapi = 21
android.api = 33
android.ndk = 25b
android.sdk = 33

android.arch = arm64-v8a

# 权限
android.permissions = \
    SYSTEM_ALERT_WINDOW,\
    RECEIVE_BOOT_COMPLETED,\
    FOREGROUND_SERVICE,\
    WAKE_LOCK,\
    FOREGROUND_SERVICE_MEDIA_PLAYBACK

# 触摸屏非必须（电视无触摸屏）
android.uses_features = android.hardware.touchscreen;required=false

# 全屏
fullscreen = 1

# 允许备份
android.allow_backup = True

# Android TV：Leanback Launcher intent filter
# 让 APK 出现在电视主屏幕应用列表中
android.manifest.intent_filters = \
    <intent-filter>\
        <action android:name="android.intent.action.MAIN" />\
        <category android:name="android.intent.category.LEANBACK_LAUNCHER" />\
    </intent-filter>

# 不需要 Google Play 服务
android.add_compile_options = "sourceCompatibility = JavaVersion.VERSION_1_8"

# 服务配置
services = EyeGuardService:service/main.py:foreground

[buildozer]
log_level = 2
warn_on_root = 0

# CI 环境优化
android.accept_sdk_license = True
android.skip_update = False
