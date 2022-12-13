import time


class Timer:
    """Context manager for timing code blocks"""
    def __init__(self):
        self.start = None
        self.end = None

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()

    @property
    def elapsed(self):
        if not self.end or not self.start:
            raise ValueError("Timer not started or ended")
        return self.end - self.start