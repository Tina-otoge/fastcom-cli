from dataclasses import dataclass
import json
import time

import requests

BASE_URL = "https://api.fast.com/netflix/speedtest/v2"
OPTIONS = {
    "https": True,
    "urlCount": 5,
    "token": "YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm",
}


class Timer:
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


def humanify_size(size: str | int) -> str:
    if isinstance(size, str):
        size = int(size)
    return f"{size / 1024 / 1024:.2f} MiB"


class SpeedTest:
    @dataclass
    class Result:
        size: int
        elapsed: float

        @classmethod
        def str(cls, speed):
            return f"{speed * 8 / 1024 / 1024:.2f} Mbps"

        @property
        def speed(self) -> float:
            return self.size / self.elapsed

        def __str__(self):
            return self.str(self.speed)

        def __lt__(self, other):
            return self.speed < other.speed

    def __init__(self, url: str):
        self.url, self.options = url.split("?")

    def run(self, range=None):
        url = self.url
        if range is not None:
            url += f"/range/0-{range}"
        url += "?" + self.options
        with Timer() as timer:
            response = requests.get(url)
        return self.Result(size=len(response.content), elapsed=timer.elapsed)

    def run_warm(self):
        self.run(range=0)
        self.run(range=2048)
        return self.run()


class SpeedTestGroup:
    # def __init__(self, urls: list[str]):
    #     self.tests = [SpeedTest(url) for url in urls]
    #     self.results = []

    def __init__(self):
        self.tests = []
        self.results = []
        self.last = None
        self.history = {}

    def refresh(self):
        response = requests.get(BASE_URL, params=OPTIONS)
        data = response.json()
        self.tests = [SpeedTest(x["url"]) for x in data.get("targets", [])]

    def run(self, iterations=10):
        for _ in range(iterations):
            self.refresh()
            for test in self.tests:
                url = test.url
                history_count = self.history.get(url, 0)
                self.history[url] = history_count + 1
                self.last = test.run_warm()
                self.results.append(self.last)
                self.results.sort()
                print(self)
                print("-" * 80)

    @property
    def speeds(self):
        return [x.speed for x in self.results]

    @property
    def median(self):
        return self.results[len(self.results) // 2]

    @property
    def max(self):
        return self.results[-1]

    @property
    def mean(self):
        return self.get_mean(self.speeds)

    def get_mean(self, results):
        speed = sum(results) / len(results)
        return SpeedTest.Result.str(speed)

    @property
    def mean_trimmed(self):
        trim = len(self.results) // 10
        trimmed = self.results[trim:-trim]
        if not trimmed:
            return self.mean
        return self.get_mean([x.speed for x in trimmed])

    def __str__(self):
        if not self.results:
            return "No results yet"

        return (
            f"Count: {len(self.results)}\n"
            f"Unique servs: {len(self.history.keys())}\n"
            f"Median: {self.median}"
            f"\nMean: {self.mean}"
            f"\nMean (trimmed): {self.mean_trimmed}"
            f"\nMax: {self.max}"
            f"\nLast: {self.last}"
        )


group = SpeedTestGroup()
group.run()
# print(json.dumps(data, indent=2))
