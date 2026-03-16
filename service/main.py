"""
后台前台服务 - 独立进程
保持计时，避免被系统回收
通过 OSC 与主进程通信
"""
import time
import os

# python-for-android 服务环境
try:
    from jnius import autoclass
    from android import mActivity
    Context = autoclass('android.content.Context')
    SERVICE_CLASS = autoclass('org.kivy.android.PythonService')
    _on_android = True
except Exception:
    _on_android = False


def create_foreground_notification():
    """创建前台服务通知，防止系统杀死"""
    if not _on_android:
        return
    try:
        NotificationBuilder = autoclass('android.app.Notification$Builder')
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        Build = autoclass('android.os.Build')

        service = SERVICE_CLASS.mService
        context = service

        channel_id = 'eyeguard_bg'
        if Build.VERSION.SDK_INT >= 26:
            channel = NotificationChannel(
                channel_id,
                '护眼小卫士后台',
                NotificationManager.IMPORTANCE_LOW
            )
            nm = context.getSystemService(Context.NOTIFICATION_SERVICE)
            nm.createNotificationChannel(channel)

        builder = NotificationBuilder(context, channel_id)
        builder.setSmallIcon(context.getApplicationInfo().icon)
        builder.setContentTitle('护眼小卫士')
        builder.setContentText('正在守护孩子的眼睛...')
        builder.setOngoing(True)
        notification = builder.build()
        service.startForeground(42, notification)
        print('[service] 前台服务已启动')
    except Exception as e:
        print(f'[service] 创建通知失败: {e}')


if __name__ == '__main__':
    print('[service] 后台服务启动')
    create_foreground_notification()
    # 保持服务存活（主进程通过 kivy Clock 负责计时，此服务仅用于保活）
    while True:
        time.sleep(30)
