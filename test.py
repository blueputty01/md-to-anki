from pathlib import Path

from main import parse_markdown

with open("test.md", "r", encoding="utf-8") as f:
    content = f.read()
    test = parse_markdown(content, "temp", "#delete", "root")
    print(test)

def test_markdown():
    assert func(3) == 5



