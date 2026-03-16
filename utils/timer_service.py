"""
计时服务：在主进程中用 Kivy Clock 驱动计时，到达提醒间隔时触发回调
"""
from kivy.clock import Clock


class TimerService:
    def __init__(self, on_trigger_callback):
        self._callback = on_trigger_callback
        self._elapsed_seconds = 0
        self._interval_seconds = 25 * 60
        self._running = False
        self._clock_event = None

    def start(self, interval_minutes=None):
        if interval_minutes is not None:
            self._interval_seconds = interval_minutes * 60
        self._elapsed_seconds = 0
        self._running = True
        if self._clock_event:
            self._clock_event.cancel()
        self._clock_event = Clock.schedule_interval(self._tick, 1)

    def stop(self):
        self._running = False
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None

    def reset(self):
        """休息结束后重置计时器"""
        self._elapsed_seconds = 0

    def set_interval(self, minutes: int):
        self._interval_seconds = minutes * 60

    @property
    def elapsed_minutes(self) -> int:
        return self._elapsed_seconds // 60

    @property
    def remaining_seconds(self) -> int:
        return max(0, self._interval_seconds - self._elapsed_seconds)

    def _tick(self, dt):
        if not self._running:
            return
        self._elapsed_seconds += 1
        if self._elapsed_seconds >= self._interval_seconds:
            self._running = False
            self._callback(self.elapsed_minutes)
