"""
全屏提醒覆盖层界面
到达提醒时间后强制显示，拦截所有按键，倒计时结束自动恢复
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
from kivy.utils import get_color_from_hex
import os


TIPS = [
    '站起来活动活动身体吧！',
    '望向窗外的远处，让眼睛放松！',
    '做几次深呼吸，喝点水吧！',
    '眨眨眼睛，活动一下脖子！',
    '去看看窗外的花花草草吧！',
]


class ReminderScreen(Screen):
    REMINDER_TEXT = '小眼睛，亮晶晶，小朋友，你已经看了{minutes}分钟啦，\n让眼睛休息一下，去看看花花草草吧！'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._rest_seconds = 0
        self._rest_total = 3 * 60
        self._countdown_event = None
        self._tip_index = 0
        self._sound = None
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()

        # 深色半透明全屏背景
        with root.canvas.before:
            Color(*get_color_from_hex('#0D1B2A'))
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        content = BoxLayout(
            orientation='vertical',
            spacing=50,
            size_hint=(0.85, 0.85),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # 大号眼睛图标文字
        eye_label = Label(
            text='👀',
            font_size='120sp',
            size_hint=(1, 0.2),
        )

        # 提醒主文字
        self.reminder_label = Label(
            text=self.REMINDER_TEXT.format(minutes=25),
            font_size='46sp',
            color=get_color_from_hex('#FFFDE7'),
            halign='center',
            valign='middle',
            size_hint=(1, 0.3),
        )
        self.reminder_label.bind(size=lambda inst, val: setattr(inst, 'text_size', val))

        # 倒计时
        self.countdown_label = Label(
            text='还需休息 03:00',
            font_size='72sp',
            bold=True,
            color=get_color_from_hex('#FF8A65'),
            size_hint=(1, 0.2),
        )

        # 小贴士
        self.tip_label = Label(
            text=f'💡 {TIPS[0]}',
            font_size='36sp',
            color=get_color_from_hex('#B2DFDB'),
            size_hint=(1, 0.15),
        )

        # 家长解锁按钮（不显眼，需要遥控器导航到此）
        self.btn_unlock = Button(
            text='家长解锁',
            font_size='28sp',
            size_hint=(0.25, 0.1),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=get_color_from_hex('#37474F'),
            color=get_color_from_hex('#90A4AE'),
            opacity=0.6,
        )
        self.btn_unlock.bind(on_release=self._on_unlock)

        content.add_widget(eye_label)
        content.add_widget(self.reminder_label)
        content.add_widget(self.countdown_label)
        content.add_widget(self.tip_label)
        content.add_widget(self.btn_unlock)

        root.add_widget(content)
        self.add_widget(root)

    def _update_bg(self, instance, value):
        self._bg.pos = instance.pos
        self._bg.size = instance.size

    def start_reminder(self, elapsed_minutes: int):
        """由 App 在触发提醒时调用"""
        app = App.get_running_app()
        self._rest_total = app.config_mgr.rest_duration * 60
        self._rest_seconds = self._rest_total

        # 更新提醒文字中的分钟数
        self.reminder_label.text = self.REMINDER_TEXT.format(minutes=elapsed_minutes)

        # 循环贴士
        self._tip_index = (self._tip_index + 1) % len(TIPS)
        self.tip_label.text = f'💡 {TIPS[self._tip_index]}'

        self._update_countdown_label()

        # 启动倒计时
        if self._countdown_event:
            self._countdown_event.cancel()
        self._countdown_event = Clock.schedule_interval(self._tick, 1)

        # 播放语音
        if app.config_mgr.voice_enabled:
            self._play_voice()

    def _tick(self, dt):
        self._rest_seconds -= 1
        self._update_countdown_label()
        if self._rest_seconds <= 0:
            self._countdown_event.cancel()
            self._countdown_event = None
            self._end_reminder()

    def _update_countdown_label(self):
        m = self._rest_seconds // 60
        s = self._rest_seconds % 60
        self.countdown_label.text = f'还需休息 {m:02d}:{s:02d}'

    def _end_reminder(self):
        """休息结束，恢复计时并返回主界面"""
        app = App.get_running_app()
        app.timer_service.reset()
        app.timer_service.start(app.config_mgr.reminder_interval)
        app.sm.current = 'home'

    def _play_voice(self):
        # 尝试多种音频格式
        base_dir = os.path.dirname(os.path.dirname(__file__))
        audio_files = [
            os.path.join(base_dir, 'assets', 'audio', 'reminder.ogg'),
            os.path.join(base_dir, 'assets', 'audio', 'reminder.mp3'),
            os.path.join(base_dir, 'assets', 'audio', 'reminder.wav'),
        ]
        
        audio_path = None
        for f in audio_files:
            if os.path.exists(f):
                audio_path = f
                break
        
        if audio_path:
            if self._sound:
                self._sound.stop()
            self._sound = SoundLoader.load(audio_path)
            if self._sound:
                self._sound.play()
                print(f'[Voice] Playing: {os.path.basename(audio_path)}')
        else:
            print('[Voice] No audio file found')

    def _on_unlock(self, instance):
        """家长解锁按钮：跳转 PIN 验证，验证通过后停止休息计时"""
        app = App.get_running_app()
        pin_screen = app.sm.get_screen('pin')
        pin_screen.set_next_screen('home')
        pin_screen.set_on_verified(self._force_end_reminder)
        app.sm.current = 'pin'

    def _force_end_reminder(self):
        """家长输入正确密码后提前结束休息"""
        if self._countdown_event:
            self._countdown_event.cancel()
            self._countdown_event = None
        self._end_reminder()

    def on_leave(self):
        # 离开界面时停止语音
        if self._sound:
            self._sound.stop()
