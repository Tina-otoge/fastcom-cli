from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import importlib.metadata

from .test import SpeedTestGroup

__pkg__ = "fastcom-cli"
__version__ = importlib.metadata.version(__pkg__)


def main():
    parser = ArgumentParser(
        description="A CLI tool to test your Internet speed using Fast.com.",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppresses progress output"
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=10,
        help="Controls the number of loops",
    )
    parser.add_argument(
        "-s",
        "--servers",
        type=int,
        default=5,
        help="Controls the number of servers to test against during each loop",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Outputs a JSON formatted summary (implies --quiet)",
    )
    parser.add_argument(
        "-r",
        "--trim",
        type=int,
        default=10,
        help=(
            "Controls the percentage of results to trim from the top and bottom"
            ' of the results for the "Mean (trimmed)" value'
        ),
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=60,
        help="Controls the number of seconds to wait before stopping all tests",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{__pkg__} {__version__}",
    )
    args = parser.parse_args()

    if args.json:
        args.quiet = True

    group = SpeedTestGroup(
        servers=args.servers, iterations=args.iterations, trim=args.trim
    )
    group.run(
        verbose=not args.quiet, json_output=args.json, timeout=args.timeout
    )


if __name__ == "__main__":
    main()
