from dataclasses import dataclass
import json
import sys
import time

import requests

from .timer import Timer


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
        """Run a speed test against the given URL."""
        url = self.url
        if range is not None:
            url += f"/range/0-{range}"
        url += "?" + self.options
        with Timer() as timer:
            response = requests.get(url)
        return self.Result(size=len(response.content), elapsed=timer.elapsed)

    def run_warm(self):
        """Run a speed test against the given URL, warming the cache first by
        requesting a small range of bytes before the full file."""
        self.run(range=0)
        self.run(range=2048)
        return self.run()


class SpeedTestGroup:
    BASE_URL = "https://api.fast.com/netflix/speedtest/v2"
    TOKEN = "YXNkZmFzZGxmbnNkYWZoYXNkZmhrYWxm"

    def __init__(self, servers, iterations, trim):
        self.tests = []
        self.results = []
        self.last = None
        self.history = {}
        self.servers = servers
        self.options = {
            "https": True,
            "urlCount": self.servers,
            "token": self.TOKEN,
        }
        self.iterations = iterations
        self.current_iteration = 0
        self.trim = trim

    def refresh(self):
        response = requests.get(self.BASE_URL, params=self.options)
        data = response.json()
        self.tests = [SpeedTest(x["url"]) for x in data.get("targets", [])]

    def loop(self, verbose, timeout):
        start = time.time()
        for i in range(self.iterations):
            self.current_iteration = i
            self.refresh()
            for test in self.tests:
                url = test.url
                history_count = self.history.get(url, 0)
                self.history[url] = history_count + 1
                self.last = test.run_warm()
                self.results.append(self.last)
                self.results.sort()
                if verbose:
                    print(self)
                    print("-" * 28)
                elapsed = time.time() - start
                if elapsed > timeout:
                    if verbose:
                        print(
                            f"Timeout of {timeout} seconds reached, stopping"
                            " early"
                        )
                    return

    def run(self, verbose, json_output, timeout):
        self.loop(verbose, timeout)
        if json_output:
            json.dump(
                {
                    "count": len(self.results),
                    "unique_servers": len(self.history.keys()),
                    "median": self.median.speed,
                    "mean": self.mean,
                    "mean_trimmed": self.mean_trimmed,
                    "max": self.max.speed,
                    "last": self.last and self.last.speed,
                },
                sys.stdout,
                indent=2,
            )
            print(file=sys.stdout)
        else:
            print("Max speed:", self.max)
            print("Mean speed:", self.mean_trimmed)

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
        trim = int(len(self.results) * (self.trim / 100))
        trimmed = self.results[trim:-trim]
        if not trimmed:
            return self.mean
        return self.get_mean([x.speed for x in trimmed])

    @property
    def planned_count(self):
        return self.iterations * self.servers

    def __str__(self):
        if not self.results:
            return "No results yet"

        return (
            f"Count: {len(self.results)}/{self.planned_count}\n"
            f"Loop: {self.current_iteration + 1}/{self.iterations}\n"
            f"Unique servers: {len(self.history.keys())}\n"
            f"Median: {self.median}"
            f"\nMean: {self.mean}"
            f"\nMean (trimmed): {self.mean_trimmed}"
            f"\nMax: {self.max}"
            f"\nLast: {self.last}"
        )
