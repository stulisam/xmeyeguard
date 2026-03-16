# 护眼小卫士

安装在小米电视4（Android TV）上的儿童用眼健康提醒应用。

## 项目结构

```
xiaomitv/
├── main.py                  # 应用入口
├── buildozer.spec           # Android 打包配置
├── install.bat              # Windows 一键安装脚本
├── install.sh               # macOS/Linux 安装脚本
├── screens/
│   ├── home_screen.py       # 主界面（儿童视角）
│   ├── reminder_screen.py   # 全屏提醒覆盖层
│   ├── pin_screen.py        # PIN 码验证界面
│   ├── setup_pin_screen.py  # 首次设置 PIN 界面
│   └── settings_screen.py  # 家长设置界面
├── utils/
│   ├── config.py            # 配置管理（JSON + PIN 哈希）
│   ├── timer_service.py     # 计时服务
│   └── android_utils.py    # Android 平台工具
├── service/
│   └── main.py             # 后台前台服务（保活）
├── assets/
│   └── audio/
│       └── reminder.ogg    # 语音提醒音频（需自行录制）
└── data/                   # 运行时生成，存放 config.json
```

## 开发环境要求

- Python 3.10+
- Kivy 2.3.0
- Buildozer（需要 Linux / WSL2）

## 本地调试（桌面）

```bash
pip install kivy
python main.py
```

## 打包 APK

在 Linux / WSL2 中执行：

```bash
pip install buildozer
buildozer android debug
```

APK 生成在 `bin/` 目录下。

## 安装到小米电视4

1. 开启电视 ADB 调试：设置 → 账号与安全 → ADB调试
2. 查看电视 IP：设置 → 网络 → 当前网络
3. 运行安装脚本：

**Windows：**
```
双击 install.bat，输入电视 IP
```

**macOS/Linux：**
```bash
chmod +x install.sh && ./install.sh
```

## 语音文件

需录制语音文件放置于 `assets/audio/reminder.ogg`：

> 小眼睛，亮晶晶，小朋友，你已经看了25分钟啦，让眼睛休息一下，去看看花花草草吧！

格式：OGG Vorbis，44100Hz，时长约 8-10 秒。

## 默认设置

| 项目 | 默认值 |
|------|--------|
| 提醒间隔 | 25 分钟 |
| 休息时长 | 3 分钟 |
| 语音提醒 | 开启 |
