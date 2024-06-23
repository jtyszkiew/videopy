class Time:
    def __init__(self, start, duration):
        self.start = float(start)
        self.duration = float(duration)

    def get_end(self):
        return self.start + self.duration

    def __str__(self):
        return f"VideoYmlTime(start={self.start}, duration={self.duration})"
