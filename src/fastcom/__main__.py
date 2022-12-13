from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from .test import SpeedTestGroup


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
        "-t",
        "--trim",
        type=int,
        default=10,
        help=(
            "Controls the percentage of results to trim from the top and bottom"
            ' of the results for the "Mean (trimmed)" value'
        ),
    )
    args = parser.parse_args()

    if args.json:
        args.quiet = True

    group = SpeedTestGroup(
        servers=args.servers, iterations=args.iterations, trim=args.trim
    )
    group.run(verbose=not args.quiet, json_output=args.json)


if __name__ == "__main__":
    main()