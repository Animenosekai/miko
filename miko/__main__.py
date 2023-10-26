"""The CLI implementation for `miko`"""
import argparse
import json
import pathlib

import miko
from miko import static

NO_ACTION = """\
usage: miko [-h] [--version] {info,clean} ...
miko: error: the following arguments are required: action"""


def main(args: argparse.Namespace):
    """
    Core flow for the CLI

    Parameters
    ----------
    args: argparse.Namespace
        The CLI arguments
    """
    if not args.action:
        return print(NO_ACTION)

    if pathlib.Path(args.input).is_file():
        source_code = pathlib.Path(args.input).read_text()
    else:
        source_code = str(args.input)

    if args.action == "info":
        if args.raw:
            info_results = miko.Documentation(source_code,
                                              flag_prefix=args.flag_prefix,
                                              noself=args.noself).exported
        else:
            info_results = static.info(source_code,
                                       indent=args.indent,
                                       noself=args.noself,
                                       flag_prefix=args.flag_prefix,
                                       safe_annotations=args.safe_annotations)

        if args.minify:
            stringified = json.dumps(
                info_results,
                ensure_ascii=False,
                separators=(",", ":")
            )
        else:
            stringified = json.dumps(
                info_results,
                indent=args.indent,
                ensure_ascii=False
            )

        if args.output and pathlib.Path(args.output).is_file():
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(stringified)
        else:
            print(stringified)

        return info_results

    if args.raw:
        clean_results = miko.Documentation(source_code,
                                           flag_prefix=args.flag_prefix,
                                           noself=args.noself).dumps(indent=args.indent)
    else:
        clean_results = static.clean(source_code,
                                     indent=args.indent,
                                     noself=args.noself,
                                     flag_prefix=args.flag_prefix,
                                     safe_annotations=args.safe_annotations)

    if args.output and pathlib.Path(args.output).is_file():
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(clean_results)
    else:
        print(clean_results)

    return clean_results


def entry():
    """Main entrypoint for the CLI"""
    parser = argparse.ArgumentParser(
        "miko", description="See how to use a Python object at a glance!")
    parser.add_argument('--version', '-v', action='version',
                        version=miko.__version__)

    subparser = parser.add_subparsers(help='Actions', dest="action")

    def prepare_parser(parser: argparse.ArgumentParser):
        parser.add_argument("--indent", "-i", action='store', type=int,
                            required=False, default=4, help='The indentation level for the result')
        parser.add_argument("--noself", action='store_true', required=False,
                            help='Ignoring the "self" parameter from signatures. (useful for class methods)')
        parser.add_argument("--flag-prefix", action='store', required=False,
                            default="!", help='The prefix for the docstring flags. (default: "!")')
        parser.add_argument("--safe-annotations", action='store_true', required=False,
                            help='If the annotations should be loaded safely')
        parser.add_argument("--output", "-o", action='store', type=str,
                            required=False, default=None, help='The file to output the result to. If not provided, `miko` will use STDOUT.')
        parser.add_argument("input", action='store', type=str, default=None,
                            help='The snippet of code or file to get the docstrings from.')
        parser.add_argument("--raw", action='store_true', required=False,
                            help='If the input should be treated as a docstring and not source code. (default: False)')

    parser_info = subparser.add_parser('info',
                                       help='Gathers information on the different elements in the input')
    parser_info.add_argument("--minify", action='store_true', required=False,
                             help='If the output should be minified. (default: False)')
    parser_clean = subparser.add_parser("clean",
                                        help="Cleans the given input")

    prepare_parser(parser_info)
    prepare_parser(parser_clean)

    args = parser.parse_args()

    main(args)


if __name__ == "__main__":
    entry()
