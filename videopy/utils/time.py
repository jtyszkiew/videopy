class Time:
    def __init__(self, start, duration):
        self.start = start
        self.duration = duration

    def get_end(self):
        return self.start + self.duration

    def __str__(self):
        return f"VideoYmlTime(start={self.start}, duration={self.duration})"
