from dataclasses import dataclass
from typing import List
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate


@dataclass
class Sloka:
    lines: List[str]


def load_slokas(input_file: str) -> List[Sloka]:
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f.readlines()
                 if not line.startswith("#")]

        slokas: List[Sloka] = []
        current_lines: List[str] = []
        for idx, line in enumerate(lines):
            if len(line) > 0:
                current_lines.append(line)
            if len(line) == 0 or idx == len(lines) - 1:
                slokas.append(Sloka(lines=current_lines))
                current_lines = []
        return slokas


def convert_slokas(slokas: List[Sloka], scheme_map: SchemeMap, sanitize: bool = False):
    def sanitize_line(line: str) -> str:
        return line.replace("-", "").replace("·", " ") if sanitize else line

    sloka_lines = [
        [transliterate(sanitize_line(line), scheme_map=scheme_map)
            for line in sloka.lines]
        for sloka in slokas]

    for sloka in sloka_lines:
        if len(sloka) >= 4:
            sloka[-3] += " |"
            sloka[-1] += " ||"

    return [
        Sloka(lines=sloka)
        for sloka in sloka_lines
    ]


def write_tex(output_file: str, slokas: List[Sloka], latex_cmd: str, chapter: str = "",
              display_headers: bool = False, split_first_sloka: bool = False):
    def sloka_to_tex(sloka: Sloka, chapter: int, sloka_num: int, display_headers: bool) -> str:
        tex: List[str] = []
        for idx, line in enumerate(sloka.lines):
            sanitized = line.replace("~", "\\textasciitilde{}")

            line_opening = ""
            if display_headers and idx == 0:
                line_opening = f"\\textbf{{{chapter}.{sloka_num}}}"

            line_ending = ""
            if idx != len(sloka.lines) - 1:
                line_ending = " \\\\"

            tex.append(
                f"{line_opening} & \\{latex_cmd}{{{sanitized}}}{line_ending}")
        return "\n".join(tex)

    with open(output_file, "w") as f:
        for idx, sloka in enumerate(slokas):
            # Table header
            f.write("\\begin{table}[H]\n")
            f.write("\\begin{tabular}{cl}\n")
            # Table rows
            f.write(
                f"{sloka_to_tex(sloka, chapter, idx, display_headers=display_headers)}\n")
            # Table footer
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n\n")

            if split_first_sloka and idx == 0:
                f.write("\\newpage\n\n")


def convert_file(input_file: str, iast_file: str, telugu_file: str, devanagari_file: str,
                 chapter: str, display_headers: bool, split_first_sloka: bool = False):
    slokas = load_slokas(input_file)
    iast_slokas = convert_slokas(slokas, SchemeMap(
        SCHEMES[sanscript.ITRANS], SCHEMES[sanscript.IAST]), sanitize=False)
    telugu_slokas = convert_slokas(slokas, SchemeMap(
        SCHEMES[sanscript.ITRANS], SCHEMES[sanscript.TELUGU]), sanitize=True)
    devanagari_slokas = convert_slokas(slokas, SchemeMap(
        SCHEMES[sanscript.ITRANS], SCHEMES[sanscript.DEVANAGARI]), sanitize=True)

    write_tex(iast_file, iast_slokas, "romline", chapter,
              display_headers, split_first_sloka)
    write_tex(telugu_file, telugu_slokas, "natline", chapter,
              display_headers, split_first_sloka)
    write_tex(devanagari_file, devanagari_slokas, "natline", chapter,
              display_headers, split_first_sloka)
