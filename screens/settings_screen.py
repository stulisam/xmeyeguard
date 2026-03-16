"""
家长设置界面
需 PIN 码验证后才可进入，支持遥控器 DPAD 导航
"""
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.app import App
from kivy.utils import get_color_from_hex


INTERVAL_OPTIONS = [15, 20, 25, 30, 45, 60]
REST_OPTIONS = [1, 2, 3, 5, 10]


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._focus_index = 0
        self._focusable = []
        self._build_ui()

    def _build_ui(self):
        root = FloatLayout()
        with root.canvas.before:
            Color(*get_color_from_hex('#0A1929'))
            self._bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._update_bg, size=self._update_bg)

        main = BoxLayout(
            orientation='vertical',
            spacing=28,
            size_hint=(0.7, 0.90),
            pos_hint={'center_x': 0.5, 'center_y': 0.52}
        )

        main.add_widget(Label(
            text='家长设置',
            font_size='52sp',
            bold=True,
            color=get_color_from_hex('#FFD700'),
            size_hint=(1, 0.12),
        ))

        # ── 提醒间隔 ──────────────────────────────────
        main.add_widget(Label(
            text='提醒间隔（分钟）',
            font_size='34sp',
            color=get_color_from_hex('#B2DFDB'),
            halign='left',
            size_hint=(1, 0.07),
        ))
        interval_row = BoxLayout(orientation='horizontal', spacing=14, size_hint=(1, 0.11))
        self._interval_btns = []
        for v in INTERVAL_OPTIONS:
            btn = Button(
                text=str(v),
                font_size='32sp',
                background_normal='',
                background_color=get_color_from_hex('#1E3A5F'),
                color=get_color_from_hex('#FFFFFF'),
            )
            btn.bind(on_release=lambda inst, val=v: self._set_interval(val))
            self._interval_btns.append(btn)
            interval_row.add_widget(btn)
        main.add_widget(interval_row)

        # ── 休息时长 ──────────────────────────────────
        main.add_widget(Label(
            text='休息时长（分钟）',
            font_size='34sp',
            color=get_color_from_hex('#B2DFDB'),
            halign='left',
            size_hint=(1, 0.07),
        ))
        rest_row = BoxLayout(orientation='horizontal', spacing=14, size_hint=(1, 0.11))
        self._rest_btns = []
        for v in REST_OPTIONS:
            btn = Button(
                text=str(v),
                font_size='32sp',
                background_normal='',
                background_color=get_color_from_hex('#1E3A5F'),
                color=get_color_from_hex('#FFFFFF'),
            )
            btn.bind(on_release=lambda inst, val=v: self._set_rest(val))
            self._rest_btns.append(btn)
            rest_row.add_widget(btn)
        main.add_widget(rest_row)

        # ── 语音开关 ──────────────────────────────────
        self.voice_btn = Button(
            text='语音提醒：开启',
            font_size='34sp',
            background_normal='',
            background_color=get_color_from_hex('#2E7D32'),
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(0.5, 0.11),
        )
        self.voice_btn.bind(on_release=self._toggle_voice)
        main.add_widget(self.voice_btn)

        # ── 修改密码 ──────────────────────────────────
        btn_change_pin = Button(
            text='修改家长密码',
            font_size='34sp',
            background_normal='',
            background_color=get_color_from_hex('#4A148C'),
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(0.5, 0.11),
        )
        btn_change_pin.bind(on_release=self._change_pin)
        main.add_widget(btn_change_pin)

        # ── 返回 ──────────────────────────────────────
        btn_back = Button(
            text='返回',
            font_size='34sp',
            background_normal='',
            background_color=get_color_from_hex('#37474F'),
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(0.3, 0.11),
        )
        btn_back.bind(on_release=lambda x: setattr(App.get_running_app().sm, 'current', 'home'))
        main.add_widget(btn_back)

        root.add_widget(main)
        self.add_widget(root)

        # 可聚焦控件列表（按上下顺序）
        self._focusable = (
            self._interval_btns +
            self._rest_btns +
            [self.voice_btn, btn_change_pin, btn_back]
        )

    def _update_bg(self, instance, value):
        self._bg.pos = instance.pos
        self._bg.size = instance.size

    def on_enter(self):
        app = App.get_running_app()
        cfg = app.config_mgr
        self._highlight_interval(cfg.reminder_interval)
        self._highlight_rest(cfg.rest_duration)
        self._update_voice_btn(cfg.voice_enabled)
        self._set_focus(0)

    def _highlight_interval(self, value):
        for btn in self._interval_btns:
            if int(btn.text) == value:
                btn.background_color = get_color_from_hex('#1565C0')
                btn.bold = True
            else:
                btn.background_color = get_color_from_hex('#1E3A5F')

    def _highlight_rest(self, value):
        for btn in self._rest_btns:
            if int(btn.text) == value:
                btn.background_color = get_color_from_hex('#1565C0')
            else:
                btn.background_color = get_color_from_hex('#1E3A5F')

    def _update_voice_btn(self, enabled):
        if enabled:
            self.voice_btn.text = '语音提醒：开启'
            self.voice_btn.background_color = get_color_from_hex('#2E7D32')
        else:
            self.voice_btn.text = '语音提醒：关闭'
            self.voice_btn.background_color = get_color_from_hex('#B71C1C')

    def _set_interval(self, value):
        app = App.get_running_app()
        app.config_mgr.reminder_interval = value
        app.timer_service.set_interval(value)
        self._highlight_interval(value)

    def _set_rest(self, value):
        App.get_running_app().config_mgr.rest_duration = value
        self._highlight_rest(value)

    def _toggle_voice(self, instance):
        app = App.get_running_app()
        new_val = not app.config_mgr.voice_enabled
        app.config_mgr.voice_enabled = new_val
        self._update_voice_btn(new_val)

    def _change_pin(self, instance):
        app = App.get_running_app()
        app.sm.get_screen('setup_pin').title_label.text = '请重新设置家长密码'
        app.sm.current = 'setup_pin'

    # ── 遥控器导航 ──────────────────────────────────────
    def _set_focus(self, index):
        for i, btn in enumerate(self._focusable):
            if i == index:
                btn.background_color = get_color_from_hex('#4A9FD4')
            # 不重置选中高亮的按钮颜色（interval/rest 已高亮）
        self._focus_index = index

    def on_keyboard(self, window, key, scancode, codepoint, modifier):
        n = len(self._focusable)
        if key == 273:   # UP
            self._set_focus((self._focus_index - 1) % n); return True
        elif key == 274: # DOWN
            self._set_focus((self._focus_index + 1) % n); return True
        elif key in (13, 32):
            self._focusable[self._focus_index].trigger_action(); return True
        elif key == 27:  # 返回键
            App.get_running_app().sm.current = 'home'; return True
        return False
