"""
主界面 - 儿童视角
显示已用时长、距下次休息倒计时、设置入口
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.utils import get_color_from_hex


class HomeScreen(Screen):
    FOCUS_BUTTONS = ['btn_settings']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._focus_index = 0
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()

        # 背景渐变色块
        with root.canvas.before:
            Color(*get_color_from_hex('#1a2a3a'))
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        # 中央内容区
        content = BoxLayout(
            orientation='vertical',
            spacing=40,
            size_hint=(0.7, 0.75),
            pos_hint={'center_x': 0.5, 'center_y': 0.52}
        )

        # 标题
        title_label = Label(
            text='护眼小卫士',
            font_size='64sp',
            bold=True,
            color=get_color_from_hex('#FFD700'),
            size_hint=(1, 0.2),
        )

        # 已用时长卡片
        self.elapsed_label = Label(
            text='你已经看了 0 分钟',
            font_size='48sp',
            color=get_color_from_hex('#E0F7FA'),
            size_hint=(1, 0.25),
        )

        # 距下次休息卡片
        self.remaining_label = Label(
            text='距离休息还有 25 分钟',
            font_size='42sp',
            color=get_color_from_hex('#B2EBF2'),
            size_hint=(1, 0.25),
        )

        # 设置按钮
        self.btn_settings = Button(
            text='家长设置  ⚙',
            font_size='36sp',
            size_hint=(0.45, 0.18),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=get_color_from_hex('#2C5F8A'),
            color=get_color_from_hex('#FFFFFF'),
        )
        self.btn_settings.bind(on_release=lambda x: App.get_running_app().go_to_settings())

        content.add_widget(title_label)
        content.add_widget(self.elapsed_label)
        content.add_widget(self.remaining_label)
        content.add_widget(self.btn_settings)

        root.add_widget(content)
        self.add_widget(root)

        # 每秒刷新显示
        Clock.schedule_interval(self._refresh, 1)
        self._set_focus(0)

    def _update_bg(self, instance, value):
        self._bg.pos = instance.pos
        self._bg.size = instance.size

    def _refresh(self, dt):
        app = App.get_running_app()
        ts = app.timer_service
        elapsed = ts.elapsed_minutes
        remaining_sec = ts.remaining_seconds
        remaining_min = remaining_sec // 60
        remaining_s = remaining_sec % 60

        self.elapsed_label.text = f'你已经看了 {elapsed} 分钟'
        self.remaining_label.text = f'距离休息还有 {remaining_min:02d}:{remaining_s:02d}'

    def on_enter(self):
        """进入主界面时确保计时器在运行"""
        app = App.get_running_app()
        ts = app.timer_service
        if not ts._running:
            interval = app.config_mgr.reminder_interval
            ts.start(interval)
        self._set_focus(0)

    # ── 遥控器焦点导航 ──────────────────────────────────
    def _set_focus(self, index):
        self._focus_index = index
        btns = [self.btn_settings]
        for i, btn in enumerate(btns):
            if i == index:
                btn.background_color = get_color_from_hex('#4A9FD4')
            else:
                btn.background_color = get_color_from_hex('#2C5F8A')

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        # DPAD_CENTER / ENTER = 13, DPAD_UP = 273, DPAD_DOWN = 274
        if key in (13, 32):   # 确认键
            btns = [self.btn_settings]
            btns[self._focus_index].trigger_action()
            return True
        return False
