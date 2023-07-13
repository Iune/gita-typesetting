from copy import deepcopy
import toml
from dataclasses import dataclass
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate


@dataclass
class Sloka:
    lines: list[str]
    should_number: bool = True
    add_punctuation: bool = True
    number: int | None = None


def load_slokas(input_file: str) -> list[Sloka]:
    with open(input_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if not line.startswith("#")]

        slokas: list[Sloka] = []
        current_lines: list[str] = []
        for idx, line in enumerate(lines):
            if len(line) > 0:
                current_lines.append(line)
            if len(line) == 0 or idx == len(lines) - 1:
                slokas.append(Sloka(lines=current_lines))
                current_lines = []
        return slokas


def load_slokas_toml(input_file: str) -> list[str]:
    with open(input_file, "r") as f:
        data = toml.load(f)

    slokas: list[Sloka] = []
    sloka_count = 0
    for sloka in data["sloka"]:
        should_number = sloka["should_number"] if "should_number" in sloka else True
        add_punctuation = (
            sloka["add_punctuation"] if "add_punctuation" in sloka else True
        )
        lines = sloka["lines"].split("\n")

        sloka_num = None
        if should_number:
            sloka_count += 1
            sloka_num = sloka_count
        slokas.append(
            Sloka(
                lines=lines,
                should_number=should_number,
                number=sloka_num,
                add_punctuation=add_punctuation,
            )
        )
    return slokas


def convert_slokas(slokas: list[Sloka], scheme_map: SchemeMap, sanitize: bool = False):
    def sanitize_line(line: str) -> str:
        return line.replace("-", "").replace("·", " ") if sanitize else line

    to_return = []
    for sloka in slokas:
        sloka = deepcopy(sloka)
        sloka.lines = [
            transliterate(sanitize_line(line), scheme_map=scheme_map)
            for line in sloka.lines
        ]

        if sloka.add_punctuation:
            if len(sloka.lines) >= 4:
                sloka.lines[-3] += " |"
                sloka.lines[-1] += " ||"

        to_return.append(sloka)
    return to_return


def write_tex(
    output_file: str,
    slokas: list[Sloka],
    latex_cmd: str,
    chapter: str = "",
    display_headers: bool = False,
    split_first_sloka: bool = False,
):
    def sloka_to_tex(sloka: Sloka, chapter: str, display_headers: bool) -> str:
        tex: list[str] = []
        for idx, line in enumerate(sloka.lines):
            sanitized = line.replace("~", "\\textasciitilde{}")

            line_opening = ""
            if sloka.should_number and idx == 0:
                line_opening = f"\\textbf{{{chapter}.{sloka.number}}}"

            line_ending = ""
            if idx != len(sloka.lines) - 1:
                line_ending = " \\\\"

            tex.append(f"{line_opening} & \\{latex_cmd}{{{sanitized}}}{line_ending}")
        return "\n".join(tex)

    with open(output_file, "w") as f:
        for sloka in slokas:
            # Table header
            f.write("\\begin{table}[H]\n")
            # f.write("\\centering\n")
            f.write("\\begin{tabular}{cl}\n")
            # Table rows
            f.write(
                f"{sloka_to_tex(sloka, chapter, display_headers=display_headers)}\n"
            )
            # Table footer
            f.write("\\end{tabular}\n")
            f.write("\\end{table}\n\n")

            # if split_first_sloka and idx == 0:
            #     f.write("\\newpage\n\n")


def convert_file(
    input_file: str,
    iast_file: str,
    telugu_file: str,
    devanagari_file: str,
    chapter: str,
    display_headers: bool,
    split_first_sloka: bool = False,
):
    slokas = load_slokas_toml(input_file)
    iast_slokas = convert_slokas(
        slokas,
        SchemeMap(SCHEMES[sanscript.ITRANS], SCHEMES[sanscript.IAST]),
        sanitize=False,
    )
    telugu_slokas = convert_slokas(
        slokas,
        SchemeMap(SCHEMES[sanscript.ITRANS], SCHEMES[sanscript.TELUGU]),
        sanitize=True,
    )
    devanagari_slokas = convert_slokas(
        slokas,
        SchemeMap(SCHEMES[sanscript.ITRANS], SCHEMES[sanscript.DEVANAGARI]),
        sanitize=True,
    )

    write_tex(
        iast_file, iast_slokas, "romline", chapter, display_headers, split_first_sloka
    )
    write_tex(
        telugu_file,
        telugu_slokas,
        "natline",
        chapter,
        display_headers,
        split_first_sloka,
    )
    write_tex(
        devanagari_file,
        devanagari_slokas,
        "natline",
        chapter,
        display_headers,
        split_first_sloka,
    )
