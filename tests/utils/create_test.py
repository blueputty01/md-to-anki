from md_to_anki import main
import json
from pathlib import Path


if __name__ == '__main__':
    folder = Path("../fixtures/image")

    if not folder.exists():
        folder.mkdir()
        with open(folder / "input.md", "w", encoding="utf-8") as f:
            f.write("[]")
        input("Add input.md file to folder and press enter")



    with open(folder / "input.md", "r", encoding="utf-8") as f:
        content = f.read()
    test = main.parse_markdown(content, "temp", "#delete", "root")
    with open(folder / "expected.json", "w", encoding="utf-8") as f:
        json.dump(test, f, indent=4)
        print(test)
