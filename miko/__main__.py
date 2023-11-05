"""The CLI implementation for `miko`"""
import argparse
import json
import pathlib

import miko
from miko import static, markdown

NO_ACTION = """\
usage: miko [-h] [--version] {info,clean,docs,overview} ...
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

    if args.action == "docs":
        if not args.entry:
            entry_file = pathlib.Path() / "__init__.py"
        else:
            entry_file = pathlib.Path(args.entry)

        if not entry_file.is_file():
            raise FileNotFoundError(f"The file '{args.entry}' does not exist")

        if args.output:
            output_dir = pathlib.Path(args.output)
        else:
            output_dir = pathlib.Path("./docs")

        if not output_dir.is_dir():
            output_dir.mkdir(parents=True)

        ignored = []
        for group in args.ignore:
            for path in group:
                ignored.append(pathlib.Path(path))

        def ignore_file(file: pathlib.Path):
            return file in ignored

        if args.include_private:
            def ignore_element(element: static.Element):
                return False
        else:
            def ignore_element(element: static.Element):
                return element.is_private

        return markdown.make.make_docs(args.entry, output_dir=output_dir, file_filter=ignore_file,
                                       element_filter=ignore_element, safe=args.safe)

    if args.action == "overview":
        if not args.module:
            module = pathlib.Path() / "__init__.py"
        else:
            module = pathlib.Path(args.module)

        if not module.is_file():
            raise FileNotFoundError(f"The file '{args.module}' does not exist")

        if args.output:
            output_file = pathlib.Path(args.output)
        else:
            # this is a placeholder and won't actually be used
            output_file = pathlib.Path("./miko_temp_overview.md")

        if args.include_private:
            def ignore_element(element: static.Element):
                return False
        else:
            def ignore_element(element: static.Element):
                return element.is_private

        rendered = markdown.make.make_module_docs(args.module, output_file=output_file,
                                                  element_filter=ignore_element,
                                                  safe=args.safe)
        if not args.output:
            return print(rendered)
        output_file.write_text(rendered)
        return

    try:
        if pathlib.Path(args.input).is_file():
            source_code = pathlib.Path(args.input).read_text()
        else:
            raise ValueError("Internal Error: The given input is not a file path")
    except Exception:
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
                                       safe=args.safe)

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
                                     safe=args.safe)

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
        parser.add_argument("--safe", action='store_true', required=False,
                            help='If the annotations and exceptions should be loaded safely (without loading the modules) (default: False)')
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

    def prepare_docs_parser(parser: argparse.ArgumentParser):
        parser.add_argument("--include-private", action="store_true", default=False,
                            help="If the private objects should be included in the documentation")
        parser.add_argument("--safe", action='store_true', required=False,
                            help='If the annotations and exceptions should be loaded safely (without loading the modules) (default: False)')

    parser_docs = subparser.add_parser("docs",
                                       help="Generate the documentation for the files loaded by the entry file")
    parser_docs.add_argument("entry", action='store', type=str,
                             help='The entry file to document. An entry file could be for example the __init__.py of a library.')
    parser_docs.add_argument("--output", "-o", action='store', type=str,
                             required=False, default=None, help='The directory to output the result to. If not provided, `miko` will use "./docs"')
    parser_docs.add_argument("--ignore", action="store", nargs="*", type=str, default=[],
                             help="The files to ignore when generating the documentation")

    prepare_docs_parser(parser_docs)

    parser_overview = subparser.add_parser("overview",
                                           help="Provides documentation for the given module")
    parser_overview.add_argument("module", action='store', type=str,
                                 help='The module to provide documentation for')
    parser_overview.add_argument("--output", "-o", action='store', type=str,
                             required=False, default=None, help='The file to output the result to. If not provided, `miko` will use STDOUT')
    prepare_docs_parser(parser_overview)

    args = parser.parse_args()

    main(args)


if __name__ == "__main__":
    entry()
