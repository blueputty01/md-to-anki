# Markdown to Anki 📄

Imports Markdown files into Anki (spaced repetition software) to keep memory of notes fresh.

# How to use 🤔

1. Setup Anki and install the [AnkiConnect](https://ankiweb.net/shared/info/2055492159) plugin.
2. Create a deckConsts.py file in the same directory as main.py with the content:

```python
# Path to the root directory of your markdown notes
ROOT = ""

# Mapping of deck names to markdown directories
DECKS = {
    # deck name : markdown directory path
    "math::math241": "@2.1/math241"  # deck name is math::math241, markdown directory path is @2.1/math241
}

# automatically builds full key/value path mapping
DECKS = {k: ROOT + v for k, v in DECKS.items()}
# if the title of the markdown file contains any of these keywords, it will be ignored
IGNORE_KEYWORDS = "discussion"
# output directory for any errors
OUTPUT_DIR = ""
```

3. Suggested: set up virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Suggested: set up runners for the `main.py` file. See examples/runners for examples for most operating systems. These
   are useful when for me to run md-to-anki from macOS Spotlight and the equivalent on Windows/Linux

## Features ⚒️

* LaTeX support via MathJax
* Cloze deletion
* Syntax highlighting (must set up [pygments.css](https://github.com/richleland/pygments-css) in Anki card styles)
* Images
* Uses [anki-connect](https://github.com/FooSoft/anki-connect#media-actions) to automatically add parsed data to Anki

## Cloze deletion syntax

All notes are imported to the cloze type. Any bold text, notated by markdown `**bold text**` is converted to cloze
fields.

By default, cloze fields will be numbered in the order they appear in the note. To manually number cloze fields, use
`{{c#::text}}`. The automatic counting does not increment in this case.

## New card syntax

Double line breaks delineate new cards.

## Tag syntax

The title of the markdown file is used as the tag for the imported notes. `-` in the title denotes a subtag (replaced
with ::).

Alternatively, use headings in the markdown file to denote tags. The first heading will be the main tag, and the second
heading will be the subtag, etc.

### Example:

Folder set up in `deckConsts.py` is `"math::math240": "blueputty01/math240/"`. A markdown file is processed at
`"blueputty01/math240/6 Orthogonality and Least Squares/2 Orthogonal Sets.md"`.
The tag for the imported notes will be `#math::#math240::6OrthogonalityandLeastSquares::2OrthogonalSets`.

## Extra field

Indented text refer to text in the extra field for the card directly above.

Alternatively, an extra field may be surrounded by `---`.

```markdown

The **Articles of Confederation** defined the government that ran the American Revolution.

---

This text is in the extra field

* Land Ordinance Act of 1785
    * allowed federal government to sell western lands
        * pay off national debt
        * organize new lands into townships and public schools
* Northwest Ordinance of 1787
    * provided that when new territory reached population of 60K → could apply for statehood with no slavery allowed

---

This is another card; **this text will be marked for cloze**.
This line is in the extra field.

```

### Parsed result of note 1:

Text:
> The {{c1::Articles of Confederation}} defined the government that ran the American Revolution.

Extra:

> * Land Ordinance Act of 1785
    >

* allowed federal government to sell western lands

> * pay off national debt
>   * organize new lands into townships and public schools
> * Northwest Ordinance of 1787
> * provided that when new territory reached population of 60K → could apply for statehood with no slavery allowed

# How it works 🛠️

Once a file is successfully parsed, the script will add `***` to the end of the file name to indicate that it has been
processed. If the file has already been processed, it will be skipped.

# Contributing 🤝

Feel free to contribute to this project by opening an issue or creating a pull request!

If adding a package, please run `python3 -m  pipreqs.pipreqs . --force` to update the requirements.txt file.

Please ensure that code is typed properly with `mypy md_to_anki/main.py`

