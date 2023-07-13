import toml
from pathlib import Path
from os.path import dirname, join


def get_root_directory():
    file_dir = dirname(__file__)
    return Path(file_dir).parent


def process_file(input_file, output_file):
    root_directory = get_root_directory()
    input_file_path = join(root_directory, "resources", input_file)
    output_file_path = join(root_directory, "resources", output_file)

    with open(input_file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if not line.startswith("#")]

    slokas = []
    current_lines: List[str] = []
    for idx, line in enumerate(lines):
        if len(line) > 0:
            current_lines.append(line)
        if len(line) == 0 or idx == len(lines) - 1:
            slokas.append({"lines": current_lines})
            current_lines = []

    with open(output_file_path, "w") as f:
        for sloka in slokas:
            f.write("[[sloka]]\n")
            sloka_lines = "\n".join(sloka["lines"])
            f.write(f'lines = """\n{sloka_lines}"""\n\n')


def main():
    process_file(f"opening-slokas.txt", f"opening-slokas.toml")
    process_file(f"closing-slokas.txt", f"closing-slokas.toml")
    for i in range(18, 19):
        process_file(f"chapter-{i}.txt", f"chapter-{i}.toml")


if __name__ == "__main__":
    main()
