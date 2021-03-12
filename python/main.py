from transliterator import convert_file
from os.path import dirname, join
from pathlib import Path


def get_root_directory():
    file_dir = dirname(__file__)
    return Path(file_dir).parent


def write_latex(section_name: str, chapter: str, display_headers: bool, split_first_sloka: bool = False):
    root_directory = get_root_directory()
    source_directory = join(root_directory, "resources")
    output_directory = join(root_directory, "latex", "sections")

    input_file = join(source_directory, f"{section_name}.txt")
    iast_file = join(output_directory, "iast", f"{section_name}.tex")
    telugu_file = join(output_directory, "telugu", f"{section_name}.tex")

    print(f"Generating .tex files for {input_file}")
    convert_file(input_file, iast_file, telugu_file,
                 chapter, display_headers, split_first_sloka)


def main():
    write_latex("opening-slokas", "0", False)
    write_latex("opening-slokas", "0", False)
    write_latex("chapter-2", "2", True)
    write_latex("chapter-12", "12", True)


if __name__ == "__main__":
    main()