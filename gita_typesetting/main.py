from gita_typesetting.transliterator import convert_file
from os.path import dirname, join
from pathlib import Path


def get_root_directory():
    file_dir = dirname(__file__)
    return Path(file_dir).parent


def write_latex(
    section_name: str,
    chapter: str,
    display_headers: bool,
    split_first_sloka: bool = False,
):
    root_directory = get_root_directory()
    source_directory = join(root_directory, "resources")
    output_directory = join(root_directory, "latex", "sections")

    input_file = join(source_directory, f"{section_name}.toml")
    iast_file = join(output_directory, "iast", f"{section_name}.tex")
    telugu_file = join(output_directory, "telugu", f"{section_name}.tex")
    devanagari_file = join(output_directory, "devanagari", f"{section_name}.tex")

    print(f"Generating .tex files for {input_file}")
    convert_file(
        input_file,
        iast_file,
        telugu_file,
        devanagari_file,
        chapter,
        display_headers,
        split_first_sloka,
    )


def main():
    write_latex("opening-slokas", "0", False)
    write_latex("closing-slokas", "0", False)
    write_latex("chapter-1", "1", True)
    write_latex("chapter-2", "2", True)
    write_latex("chapter-3", "3", True)
    write_latex("chapter-4", "4", True)
    write_latex("chapter-5", "5", True)
    write_latex("chapter-6", "6", True)
    write_latex("chapter-7", "7", True)
    write_latex("chapter-8", "8", True)
    write_latex("chapter-9", "9", True)
    write_latex("chapter-10", "10", True)
    write_latex("chapter-11", "11", True)
    write_latex("chapter-12", "12", True)
    write_latex("chapter-13", "13", True)
    write_latex("chapter-14", "14", True)
    write_latex("chapter-15", "15", True)
    write_latex("chapter-16", "16", True)
    write_latex("chapter-17", "17", True)
    write_latex("chapter-18", "18", True)


if __name__ == "__main__":
    main()
