from md_to_anki import main
from pathlib import Path
import json

def test_basic_parsing(test_data):
    given, expected = test_data
    assert main.parse_markdown(given, "temp", "#delete", "root") == expected

def test_full_note_parsing():
    test_case_directory = Path('fixtures/full')
    given_contents = (test_case_directory / 'input.md').read_text()
    res = main.parse_markdown(given_contents, "temp", "#delete", test_case_directory)
    expected = json.loads(expected_contents)