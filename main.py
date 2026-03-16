"""
护眼小卫士 - 主入口
小米电视4 儿童用眼提醒应用
"""
import os
import json
import hashlib
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform

from screens.home_screen import HomeScreen
from screens.reminder_screen import ReminderScreen
from screens.pin_screen import PinScreen
from screens.settings_screen import SettingsScreen
from screens.setup_pin_screen import SetupPinScreen
from utils.config import Config
from utils.timer_service import TimerService

# Android 平台特殊处理
if platform == 'android':
    from android.permissions import request_permissions, Permission  # noqa
    from utils.android_utils import start_foreground_service, request_overlay_permission


class EyeGuardApp(App):
    def build(self):
        self.title = '护眼小卫士'
        self.config_mgr = Config()
        self.timer_service = TimerService(self.on_reminder_trigger)

        # 遥控器返回键拦截
        Window.bind(on_keyboard=self.on_keyboard)

        # 构建界面管理器
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(ReminderScreen(name='reminder'))
        self.sm.add_widget(PinScreen(name='pin'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(SetupPinScreen(name='setup_pin'))

        return self.sm

    def on_start(self):
        # Android 平台启动前台服务
        if platform == 'android':
            start_foreground_service()

        # 首次使用：未设置 PIN 码则跳转到设置 PIN 页面
        if not self.config_mgr.has_pin():
            self.sm.current = 'setup_pin'
        else:
            self.sm.current = 'home'
            self.timer_service.start()

    def on_reminder_trigger(self, elapsed_minutes):
        """计时到达提醒时间的回调"""
        reminder = self.sm.get_screen('reminder')
        reminder.start_reminder(elapsed_minutes)
        self.sm.current = 'reminder'

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        """拦截遥控器返回键（key=27）和菜单键"""
        current = self.sm.current
        # 提醒覆盖层期间完全拦截返回键
        if current == 'reminder':
            return True
        # 设置页面按返回键回到主界面
        if current in ('settings', 'pin') and key == 27:
            self.sm.current = 'home'
            return True
        return False

    def go_to_settings(self):
        """从主界面点击设置：先验证 PIN"""
        pin_screen = self.sm.get_screen('pin')
        pin_screen.set_next_screen('settings')
        self.sm.current = 'pin'

    def on_pin_verified(self):
        """PIN 验证通过后的跳转由 PinScreen 负责"""
        pass


if __name__ == '__main__':
    EyeGuardApp().run()
