class PomodoroTimer:
    def __init__(self):
        self.work_duration = 25 * 60  # 25 minutes in seconds
        self.break_duration = 5 * 60  # 5 minutes in seconds
        self.long_break_duration = 15 * 60  # 15 minutes in seconds
        self.current_time = 0
        self.is_running = False
        self.sessions_completed = 0

    def start(self):
        self.is_running = True

    def pause(self):
        self.is_running = False

    def reset(self):
        self.current_time = 0
        self.is_running = False
        if self.current_time >= self.work_duration:
            self.sessions_completed += 1 