import pytest
from pathlib import Path
import json

test_case_directory = Path('fixtures')
test_case_paths = [x for x in test_case_directory.iterdir() if x.is_dir()]
test_case_names = [path.name for path in test_case_paths]


@pytest.fixture(params=test_case_paths, ids=test_case_names)
def test_data(request: pytest.FixtureRequest):
    test_case_directory = request.param
    given_contents = (test_case_directory / 'input.md').read_text()
    expected_contents = (test_case_directory / 'expected.json').read_text()
    return given_contents, json.loads(expected_contents)