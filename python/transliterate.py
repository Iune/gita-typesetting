from dataclasses import dataclass
from itertools import groupby
from typing import List
from indic_transliteration import sanscript
import argparse


@dataclass
class Sloka:
    lines: List[str]


def load_slokas(file_path: str) -> List[Sloka]:
    def load_lines():
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines() if not line.startswith('#')]

    lines = load_lines()
    # Group lines for each sloka, which are separated by blank lines
    # Here, key=bool returns false for blank lines
    slokas = [list(group)
              for key, group in groupby(lines, key=bool) if key]
    return [Sloka(lines=sloka_lines) for sloka_lines in slokas]


def convert_slokas(slokas: List[Sloka], scheme_map=sanscript.SchemeMap, remove_dashes: bool = True) -> List[Sloka]:
    if remove_dashes:
        return [Sloka(lines=[sanscript.transliterate(line.replace('-', '').replace('·', ' '), scheme_map=scheme_map)
                             for line in sloka.lines]) for sloka in slokas]
    else:
        return [Sloka(lines=[sanscript.transliterate(line, scheme_map=scheme_map)
                             for line in sloka.lines]) for sloka in slokas]


def write_to_txt(path: str, iast_slokas: List[Sloka], output_slokas: List[Sloka], headers: bool = False, chapter: str = None):
    def lines_to_text(sloka) -> str:
        return "\n".join(sloka.lines)

    with open(path, 'w') as f:
        for index, (iast, output) in enumerate(zip(iast_slokas, output_slokas)):
            if headers and chapter:
                f.write(f"({chapter}.{index})\n")
            f.write(f"{lines_to_text(output)}\n\n")
            f.write(f"{lines_to_text(iast)}\n\n\n")


def write_to_tex(path: str, iast_slokas: List[Sloka], output_slokas: List[Sloka], headers: bool = False, chapter: str = None, split_first_sloka: bool = False):
    def lines_to_tex(iast: Sloka, output: Sloka) -> str:
        lines = []
        for index, (iast_line, output_line) in enumerate(zip(iast.lines, output.lines)):
            # Normalize ~ to handle LaTeX issues
            iast_line = iast_line.replace('~', "\\textasciitilde{}")
            output_line = output_line.replace('~', "\\textasciitilde{}")

            line_ending = " \\\\" if index != len(iast.lines) - 1 else ""
            line = f"\\natline{{{output_line}}} & \\romline{{{iast_line}}}{line_ending}"
            lines.append(line)
        return '\n'.join(lines)

    with open(path, 'w') as f:
        for index, (iast, output) in enumerate(zip(iast_slokas, output_slokas)):
            if headers and chapter:
                f.write(f"\\subsection*{{{chapter}.{index}}}\n")

            # Table header
            f.write("\\begin{table}[H]\n")
            f.write("\\centering\n")
            f.write("\\begin{tabular}{ll}\n")
            # Table rows
            f.write(f"{lines_to_tex(iast, output)}\n")
            # Table footer
            f.write("\end{tabular}\n")
            f.write("\end{table}\n\n")

            if split_first_sloka and index == 0:
                f.write("\\newpage\n")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("slokas", help="Text file containing slokas")
    parser.add_argument(
        "--chapter", help="Bhagavad Gita chapter", required=True)
    parser.add_argument(
        "--input-scheme", help="Input transliteration scheme", required=True)
    parser.add_argument(
        "--output-scheme", help="Output transliteration scheme", required=True)
    parser.add_argument(
        "--file", help="Output .tex file to save transliterations (default: output.tex)", default="output.tex")
    parser.add_argument(
        "--no-headers", help="Whether to add sloka numbering (default: true)", default=True, action='store_false')
    parser.add_argument(
        "--split-first-sloka", help="Whether to add \\newline after first sloka (default: false)", default=False, action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()

    input_scheme = sanscript.SCHEMES[args.input_scheme.lower()]
    iast_scheme = sanscript.SCHEMES["iast"]
    output_scheme = sanscript.SCHEMES[args.output_scheme.lower()]

    input_slokas = load_slokas(args.slokas)
    iast_slokas = convert_slokas(
        slokas=input_slokas,
        scheme_map=sanscript.SchemeMap(input_scheme, iast_scheme),
        remove_dashes=False
    )
    output_slokas = convert_slokas(
        input_slokas,
        scheme_map=sanscript.SchemeMap(input_scheme, output_scheme),
        remove_dashes=True
    )

    write_to_tex(args.file, iast_slokas, output_slokas,
                 chapter=args.chapter, headers=args.no_headers, split_first_sloka=args.split_first_sloka)


if __name__ == "__main__":
    main()
