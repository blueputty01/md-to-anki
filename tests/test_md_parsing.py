from md_to_anki import main

def test_my_function(test_data):
    given, expected = test_data
    assert main.parse_markdown(given, "temp", "#delete", "root") == expected


# todo add image alt to size fixture; can just remove for now