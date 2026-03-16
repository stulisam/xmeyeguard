"""
Android 平台工具：前台服务启动、悬浮窗权限请求
仅在 Android 平台下导入此模块
"""
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast
    from android import mActivity

    Context = autoclass('android.content.Context')
    Intent = autoclass('android.content.Intent')
    PendingIntent = autoclass('android.app.PendingIntent')
    NotificationBuilder = autoclass('android.app.Notification$Builder')
    NotificationManager = autoclass('android.app.NotificationManager')
    NotificationChannel = autoclass('android.app.NotificationChannel')
    Settings = autoclass('android.provider.Settings')
    Uri = autoclass('android.net.Uri')
    Build = autoclass('android.os.Build')


def start_foreground_service():
    """启动前台服务以保持后台计时不被系统杀死"""
    if platform != 'android':
        return
    try:
        context = mActivity
        channel_id = 'eyeguard_channel'

        # Android 8.0+ 需要创建 NotificationChannel
        if Build.VERSION.SDK_INT >= 26:
            channel = NotificationChannel(
                channel_id,
                '护眼小卫士',
                NotificationManager.IMPORTANCE_LOW
            )
            nm = cast(
                NotificationManager,
                context.getSystemService(Context.NOTIFICATION_SERVICE)
            )
            nm.createNotificationChannel(channel)

        # 构建持久通知
        builder = NotificationBuilder(context, channel_id)
        builder.setSmallIcon(context.getApplicationInfo().icon)
        builder.setContentTitle('护眼小卫士')
        builder.setContentText('正在守护孩子的眼睛健康...')
        builder.setOngoing(True)
        notification = builder.build()

        # 将 Activity 提升为前台服务（通过 startForeground）
        # Kivy Activity 本身以前台模式运行
        service = autoclass('org.kivy.android.PythonActivity').mService
        if service:
            service.startForeground(1, notification)
    except Exception as e:
        print(f'[android_utils] start_foreground_service error: {e}')


def request_overlay_permission():
    """检查并请求 SYSTEM_ALERT_WINDOW 悬浮窗权限"""
    if platform != 'android':
        return True
    try:
        context = mActivity
        if Build.VERSION.SDK_INT >= 23:
            if not Settings.canDrawOverlays(context):
                intent = Intent(
                    Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse(f'package:{context.getPackageName()}')
                )
                context.startActivity(intent)
                return False
        return True
    except Exception as e:
        print(f'[android_utils] request_overlay_permission error: {e}')
        return False


def has_overlay_permission() -> bool:
    """检查是否已有悬浮窗权限"""
    if platform != 'android':
        return True
    try:
        context = mActivity
        if Build.VERSION.SDK_INT >= 23:
            return Settings.canDrawOverlays(context)
        return True
    except Exception:
        return False
