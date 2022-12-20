# Fast.com CLI

*Unofficial CLI tool to run Internet speed measurement tests using Fast.com's
service.*

## Installation
```bash
pip install --user fastcom-cli
```

### Usage

```
fastcom [-h] [-q] [-i ITERATIONS] [-s SERVERS] [-j] [-r TRIM] [-t TIMEOUT] [-v]

A CLI tool to test your Internet speed using Fast.com.

options:
  -h, --help            show this help message and exit
  -q, --quiet           Suppresses progress output (default: False)
  -i ITERATIONS, --iterations ITERATIONS
                        Controls the number of loops (default: 10)
  -s SERVERS, --servers SERVERS
                        Controls the number of servers to test against during
                        each loop (default: 5)
  -j, --json            Outputs a JSON formatted summary (implies --quiet)
                        (default: False)
  -r TRIM, --trim TRIM  Controls the percentage of results to trim from the top
                        and bottom of the results for the "Mean (trimmed)" value
                        (default: 10)
  -t TIMEOUT, --timeout TIMEOUT
                        Controls the number of seconds to wait before stopping
                        all tests (default: 60)
  -v, --version         show program's version number and exit
```

Simply run `fastcom` for the default usage.

```
$ fastcom

Count: 1/50
Loop: 1/10
Unique servers: 1
Median: 796.40 Mbps
Mean: 796.40 Mbps
Mean (trimmed): 796.40 Mbps
Max: 796.40 Mbps
Last: 796.40 Mbps
----------------------------
...
Max speed: 822.98 Mbps
Mean speed: 574.89 Mbps
```

```
$ fastcom --json

{
  "count": 50,
  "unique_servers": 39,
  "median": 72451737.42476499,
  "mean": "559.08 Mbps",
  "mean_trimmed": "567.41 Mbps",
  "max": 107790185.14579706,
  "last": 36975053.209750414
}
```
