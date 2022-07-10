import argparse
import inspect
import json
import pathlib
import sys
import typing

import zero

NO_ACTION = """\
usage: zero [-h] [--version] {info,clean} ...
zero: error: the following arguments are required: action"""


class ZeroSignature:
    class Parameter:
        def __init__(self, annotation: str) -> None:
            annotation = str(annotation).strip()
            if "=" in annotation:
                annotation, _, self.default = annotation.partition("=")
                self.default = self.default.strip()
            else:
                self.default = inspect._empty

            if ":" in annotation:
                annotation, _, self.annotation = annotation.partition(":")
                self.annotation = self.annotation.strip()
            else:
                self.annotation = inspect._empty

            self.name = annotation.strip().replace(" ", "")

        def as_dict(self, camelCase: bool = False):
            return {
                "name": self.name,
                "annotation": self.annotation if self.annotation is not inspect._empty else None,
                "default": self.default if self.default is not inspect._empty else None
            }

    def __init__(self, definition: str, line: int) -> None:
        self.line = int(line)

        definition = str(definition).strip()
        _, _, definition = definition.partition("(")
        annotations, _, definition = definition.partition(")")

        _, _, definition = definition.rpartition("->")
        definition = definition.strip(":")
        self.return_annotation = str(definition).strip()
        self.return_annotation if self.return_annotation else inspect._empty

        results = [self.Parameter(v) for v in annotations.split(",")]  # problem if using type annotation with commas like Union[hello, world]
        self.parameters = {v.name: v for v in results}

    def as_dict(self, camelCase: bool = False):
        return {
            "line": self.line,
            "parameters": {v: k.as_dict(camelCase) for v, k in self.parameters.items()},
            "returnAnnotation" if camelCase else "return_annotation": self.return_annotation if self.return_annotation is not inspect._empty else None
        }


class FileReadingElement:
    def __init__(self, start_line: int = None, end_line: int = None, indent: int = None, docstring: str = "", signature: ZeroSignature = None, had_docstring: bool = False, quotation: str = '"""') -> None:
        self.start_line = start_line
        self.end_line = end_line
        self.indent = indent
        self.docstring = docstring
        self.signature = signature
        self.had_docstring = had_docstring
        self.quotation = str(quotation)

    @property
    def docs(self) -> zero.Docs:
        return zero.Docs(self.docstring, self.signature)

    def as_dict(self, camelCase: bool = False):
        return {
            "startLine" if camelCase else "start_line": self.start_line,
            "endLine" if camelCase else "end_line": self.end_line,
            "indent": self.indent,
            "docs": self.docs.as_dict(camelCase),
            "signature": self.signature.as_dict(camelCase) if self.signature else None,
            "hadDocstring" if camelCase else "had_docstring": self.had_docstring,
            "quotation": self.quotation
        }


def read_file(filepath: typing.Union[str, pathlib.Path]):
    file = pathlib.Path(filepath)
    if not file.is_file():
        raise ValueError("The given file '{path}' does not seem to be a file".format(path=filepath))

    results = []

    IN_DOCSTRING = False
    LAST_ELEMENT = FileReadingElement()
    for index, line in enumerate(file.read_text().splitlines(), start=1):
        current_indent = len(line) - len(line.lstrip())
        line = line.strip()

        if LAST_ELEMENT.signature is not None and index - LAST_ELEMENT.signature.line > 1 and not IN_DOCSTRING:
            # print("LINE:", line, "HAS_SIGNATURE_AND_PASSED", index - LAST_ELEMENT.signature.line)
            results.append(LAST_ELEMENT)
            LAST_ELEMENT = FileReadingElement()

        if line.startswith("def ") and not IN_DOCSTRING:
            # print("LINE:", line, "STARTSWITH_DEF")
            LAST_ELEMENT.signature = ZeroSignature(line, index)
        elif (line.startswith('"""') or line.startswith("'''")):
            if line.startswith('"""'):
                if '"""' in line.removeprefix('"""'):  # if inline
                    continue
            else:
                if "'''" in line.removeprefix("'''"):  # if inline
                    continue
            if IN_DOCSTRING and line.startswith(LAST_ELEMENT.quotation):
                # print("LINE:", line, "IN_DOCSTRING_STARTSWITH_QUOTATION:", LAST_ELEMENT.quotation)
                LAST_ELEMENT.end_line = index
                results.append(LAST_ELEMENT)
                LAST_ELEMENT = FileReadingElement()
                IN_DOCSTRING = False
            elif not IN_DOCSTRING:
                # print("LINE:", line, "NOT_IN_DOCSTRING")
                LAST_ELEMENT.start_line = index
                LAST_ELEMENT.indent = current_indent
                LAST_ELEMENT.had_docstring = True
                LAST_ELEMENT.quotation = '"""' if line.startswith('"""') else "'''"
                IN_DOCSTRING = True
        elif IN_DOCSTRING:
            # print("LINE:", line, "IN_DOCSTRING")
            LAST_ELEMENT.docstring += line + "\n"

    if not LAST_ELEMENT.had_docstring and LAST_ELEMENT.signature is not None:
        # print("LINE:", "HAD_DOCSTRING_AND_SIGNATURE")
        results.append(LAST_ELEMENT)

    return results


def main():
    parser = argparse.ArgumentParser("zero", description="See how to use a Python object at a glance!")
    parser.add_argument('--version', '-v', action='version', version=zero.__version__)

    subparser = parser.add_subparsers(help='Actions', dest="action")

    parser_info = subparser.add_parser('info', help='Retrieve info on the given docstring')
    parser_info.add_argument('--text', '-t', action='store', type=str, required=False, help='The docstring to get the information from')
    parser_info.add_argument("--file", "-f", action='store', type=str, required=False, help='The file to get the docstrings from.')
    parser_info.add_argument("--indent", "-i", action='store', type=int, required=False, default=4, help='The indentation for the JSON result.')

    parser_clean = subparser.add_parser("clean", help="Clean the docstring")
    parser_clean.add_argument('--text', '-t', action='store', type=str, required=False, help='The docstring to clean')
    parser_clean.add_argument("--file", "-f", action='store', type=str, required=False, help='The file to get the docstrings from.')
    parser_clean.add_argument("--indent", "-i", action='store', type=int, required=False, default=4, help='The indentation to clean the docs.')

    args = parser.parse_args()

    if not args.action:
        print(NO_ACTION)
        sys.exit(1)

    if args.text:
        if args.action == "clean":
            return print(zero.Docs(args.text).dumps(indent=args.indent))
        return print(json.dumps(zero.Docs(args.text).as_dict(True), indent=args.indent, ensure_ascii=False))

    results = read_file(args.file)
    if args.action == "clean":
        return
    print(json.dumps([r.as_dict(True) for r in results], indent=args.indent, ensure_ascii=False))


if __name__ == "__main__":
    main()
