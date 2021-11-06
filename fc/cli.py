import argparse

from .parser import Parser
from .pdf.outputter import OutputterPDF


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a flipbook from a .flip file.")

    parser.add_argument('input', metavar='in.flip',
                        help='.flip recipe for flipbook')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-o', '--output', help='the file into which to write the generated flipbook')

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    parser = Parser()
    with open(args.input, "r") as f:
        program = parser.parse(f)

    outputter = OutputterPDF("A4", landscape=True)
    outputter.output(args.output, program)
    return 0
