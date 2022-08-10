import argparse
import inspect
import json
import pathlib
import sys

import miko

NO_ACTION = """\
usage: miko [-h] [--version] {info,clean} ...
miko: error: the following arguments are required: action"""


class MikoSignature:
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
        self.return_annotation = self.return_annotation if self.return_annotation else inspect._empty

        annotations_results = [""]

        OPENED_BRACKET = 0

        for c in annotations:
            if c == "," and OPENED_BRACKET <= 0:
                annotations_results.append("")
                continue
            elif c == "[":
                OPENED_BRACKET += 1
            elif c == "]":
                OPENED_BRACKET -= 1

            annotations_results[-1] += c

        # print("annotations", annotations)
        # print("annotations_results", annotations_results)

        results = [self.Parameter(v) for v in annotations_results if v]  # problem if using type annotation with commas like Union[hello, world]
        self.parameters = {v.name: v for v in results}

    def as_dict(self, camelCase: bool = False):
        return {
            "line": self.line,
            "parameters": {v: k.as_dict(camelCase) for v, k in self.parameters.items()},
            "returnAnnotation" if camelCase else "return_annotation": self.return_annotation if self.return_annotation is not inspect._empty else None
        }


class FileReadingElement:
    def __init__(self, start_line: int = None, end_line: int = None, indent: int = 0, docstring: str = "", signature: MikoSignature = None, had_docstring: bool = False, quotation: str = '"""', noself: bool = False) -> None:
        self.start_line = start_line
        self.end_line = end_line
        self.indent = indent
        self.docstring = docstring
        self.signature = signature
        self.had_docstring = had_docstring
        self.quotation = str(quotation)
        self.noself = noself

    @property
    def docs(self) -> miko.Docs:
        return miko.Docs(self.docstring, self.signature, noself=self.noself)

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


def read_file(text: str, noself: bool = False):
    results = []

    IN_DOCSTRING = False
    LAST_ELEMENT = FileReadingElement(noself=noself)
    for index, line in enumerate(text.splitlines(), start=1):
        current_indent = len(line) - len(line.lstrip())
        docstring_line = line.removeprefix(" " * LAST_ELEMENT.indent)
        line = line.strip()

        if LAST_ELEMENT.signature is not None and index - LAST_ELEMENT.signature.line > 1 and not IN_DOCSTRING:
            # print("LINE:", line, "HAS_SIGNATURE_AND_PASSED", index - LAST_ELEMENT.signature.line)
            results.append(LAST_ELEMENT)
            LAST_ELEMENT = FileReadingElement(noself=noself)

        if line.startswith("def ") and not IN_DOCSTRING:
            # print("LINE:", line, "STARTSWITH_DEF")
            LAST_ELEMENT.signature = MikoSignature(line, index)
            LAST_ELEMENT.start_line = index
            LAST_ELEMENT.indent = current_indent + 4
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
                LAST_ELEMENT = FileReadingElement(noself=noself)
                IN_DOCSTRING = False
            elif not IN_DOCSTRING:
                # print("LINE:", line, "NOT_IN_DOCSTRING")
                if not LAST_ELEMENT.signature:
                    LAST_ELEMENT.start_line = index
                LAST_ELEMENT.indent = current_indent
                LAST_ELEMENT.had_docstring = True
                LAST_ELEMENT.quotation = '"""' if line.startswith('"""') else "'''"
                IN_DOCSTRING = True
                LAST_ELEMENT.docstring += line.removeprefix(LAST_ELEMENT.quotation) + "\n"
        elif IN_DOCSTRING:
            # print("LINE:", line, "IN_DOCSTRING")
            LAST_ELEMENT.docstring += docstring_line + "\n"

    if not LAST_ELEMENT.had_docstring and LAST_ELEMENT.signature is not None:
        # print("LINE:", "HAD_DOCSTRING_AND_SIGNATURE")
        results.append(LAST_ELEMENT)

    return results


def main():
    parser = argparse.ArgumentParser("miko", description="See how to use a Python object at a glance!")
    parser.add_argument('--version', '-v', action='version', version=miko.__version__)

    subparser = parser.add_subparsers(help='Actions', dest="action")

    parser_info = subparser.add_parser('info', help='Retrieve info on the given docstring')
    parser_info.add_argument('--text', '-t', action='store', type=str, required=False, help='The docstring to get the information from')
    parser_info.add_argument("--file", "-f", action='store', type=str, required=False, help='The file to get the docstrings from.')
    parser_info.add_argument("--indent", "-i", action='store', type=int, required=False, default=4, help='The indentation for the JSON result.')
    parser_info.add_argument("--noself", action='store_true', required=False, default=False,
                             help='Ignoring the "self" parameter from signatures. (useful for class methods)')

    parser_clean = subparser.add_parser("clean", help="Clean the docstring")
    parser_clean.add_argument('--text', '-t', action='store', type=str, required=False, help='The docstring to clean')
    parser_clean.add_argument("--file", "-f", action='store', type=str, required=False, help='The file to get the docstrings from.')
    parser_clean.add_argument("--output", "-o", action='store', type=str, required=False,
                              default=None, help='The file to output the cleaned result to.')

    parser_clean.add_argument("--indent", "-i", action='store', type=int, required=False, default=4, help='The indentation to clean the docs.')
    parser_clean.add_argument("--noself", action='store_true', required=False, default=False,
                              help='Ignoring the "self" parameter from signatures. (useful for class methods)')

    args = parser.parse_args()

    if not args.action:
        print(NO_ACTION)
        sys.exit(1)

    if args.text:
        if args.action == "clean":
            result = miko.Docs(args.text, noself=args.noself).dumps(indent=args.indent)
            if parser_clean.output:
                with open(parser_clean.output, "w") as f:
                    f.write(result)
                return
            return print(result)
        return print(json.dumps(miko.Docs(args.text, noself=args.noself).as_dict(True), indent=args.indent, ensure_ascii=False))

    file = pathlib.Path(args.file)
    if not file.is_file():
        raise ValueError("The given file '{path}' does not seem to be a file".format(path=file))

    with open(file) as f:
        text = f.read()
    # text = file.read_text()

    results = read_file(text, noself=args.noself)
    if args.action == "clean":
        returning = []
        INDEXES = {}
        for element in results:
            # element: FileReadingElement
            # if element.signature:
            INDEXES[element.start_line] = element
            if element.end_line:
                for l in range(element.start_line + 1, element.end_line + 1):
                    INDEXES[l] = False
        # {
        #     "line<int>": FileReadingElement,
        #     "line+1<int>": False,
        #     "line+2<int>": False,

        #     "line<int>": FileReadingElement,
        #     "line+1<int>": False,
        # }
        for index, line in enumerate(text.splitlines(), start=1):
            current = INDEXES.get(index, None)

            if current is False:
                # print("🈲 LINE", str(index).zfill(3), ":", '\033[91m', line, '\033[0m')
                continue
            # print("✅ LINE", str(index).zfill(3), ":", '\033[92m', line, '\033[0m')

            if current is None or current.signature:
                returning.append(line)

            if current is None:
                continue

            # current: FileReadingElement

            returning.append("{i}{q}".format(i=" " * current.indent, q=current.quotation))
            for l in current.docs.dumps(indent=args.indent).splitlines():
                returning.append("{i}{l}".format(i=" " * current.indent, l=l))
            returning.append("{i}{q}".format(i=" " * current.indent, q=current.quotation))
        output = "\n".join(returning)
        if args.output:
            with open(args.output, "w") as f:
                f.write(output)
            return
        return print(output)
    print(json.dumps([r.as_dict(True) for r in results], indent=args.indent, ensure_ascii=False))


if __name__ == "__main__":
    main()
