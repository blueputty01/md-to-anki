import os
import sys
import re

import markdown2
from urllib.parse import unquote

from rich.console import Console
from rich.progress import Progress

from utils import anki
from utils import markdownHelper
from utils import utils

from deckConsts import DECKS, OUTPUT_DIR, IGNORE_KEYWORDS


def parse_markdown(content, deck_name, tags, media_root):
    def create_card(t, e, base_tags, heading_tags):
        def process(raw_string):
            raw_string = raw_string.strip()

            s = markdown2.markdown(
                raw_string,
                extras={
                    "breaks": {"on_newline": True, "on_backslash": True},
                    # Allows a code block to not have to be indented by fencing it with '```' on a line before and after
                    # Based on http://github.github.com/github-flavored-markdown/ with support for syntax highlighting.
                    "fenced-code-blocks": None,
                    # tables: Tables using the same format as GFM and PHP-Markdown Extra.
                    "tables": None,
                    # cuddled-lists: Allow lists to be cuddled to the preceding paragraph.
                    "cuddled-lists": None,
                    # code-friendly: The code-friendly extra disables the use of leading, trailing and
                    # --most importantly-- intra-word emphasis (<em>) and strong (<strong>)
                    # using single or double underscores, respectively.
                    "code-friendly": None,
                    # footnotes: support footnotes as in use on daringfireball.net and implemented in other
                    # Markdown processors (tho not in Markdown.pl v1.0.1).
                    "footnotes": None,
                    # smarty-pants: Fancy quote, em-dash and ellipsis handling similar to
                    # http://daringfireball.net/projects/smartypants/. See old issue 42 for discussion.
                    "smarty-pants": None,
                    # target-blank-links: Add target="_blank" to all <a> tags with an href.
                    # This causes the link to be opened in a new tab upon a click.
                    "target-blank-links": None,
                }
            )
            s = s.replace("<p>", "").replace("</p>", "")

            # process latex. must happen after markdown conversion as markdown2 consumes backslash
            # multi-line
            ml_latex = re.findall(r"\$\$(.*?)\$\$", raw_string)
            for latex in ml_latex:
                new_latex = latex.replace("}}", "} }")
                raw_string = raw_string.replace(f"$${latex}$$", f"\\[{new_latex}\\]")

            # single line
            sl_latex = re.findall(r"\$(.*?)\$", raw_string)
            for latex in sl_latex:
                new_latex = latex.replace("}}", "} }")
                raw_string = raw_string.replace(f"${latex}$", f"\\({new_latex}\\)")

            # process images
            images = re.findall(r'<img src="(.*?)"', s)

            for image in images:
                image_path = os.path.join(
                    media_root, unquote(image).replace("/", os.sep)
                )
                _, ext = os.path.splitext(image_path)

                image_id = utils.hash_file(image_path)
                filename = f"{image_id}{ext}"

                anki.send_media({"filename": filename, "path": image_path})

                s = s.replace(image, filename)

            return s.strip("\n")

        t = process(t)
        e = process(e)

        # process clozes
        cloze_id = 1
        bold_matches = re.findall(r"<strong>(.*?)</strong>", t)
        for bold_text in bold_matches:
            cloze_text = bold_text
            if not re.match(r"^\d+::.*", bold_text):
                cloze_text = f"{cloze_id}::{bold_text}"
                cloze_id += 1
            cloze_text = f"{{{{c{cloze_text}}}}}"

            t = t.replace(f"<strong>{bold_text}</strong>", cloze_text)

        if len(heading_tags) > 0:
            heading_tag = "::".join(heading_tags)
            new_tags = [f'{tag}::{heading_tag}' for tag in base_tags]
        else:
            new_tags = base_tags

        return {
            "deckName": deck_name,
            "modelName": "cloze",
            "fields": {"Text": t, "Extra": e},
            "tags": new_tags,
            "options": {
                "allowDuplicate": False,
                "duplicateScope": deck_name,
                "duplicateScopeOptions": {
                    "deckName": deck_name,
                    "checkChildren": False,
                    "checkAllModels": False,
                },
            },
        }

    content = content.split("\n")

    text = ""
    extra = ""

    all_cards = []

    tag_hierarchy = []

    # is building multi line extra
    is_building_ml_extra = False

    is_building_code = False

    append = False
    for line in iter(content):
        # only strip on right to prevent stripping of indent/extra indicator
        line = line.rstrip()

        if line.lstrip() == "+":
            text += "\n"
            text += "\n"
            continue

        if line.startswith("#"):
            heading_indicator, heading = line.split(" ", 1)
            tag = utils.string_to_tag(heading)
            h_level = heading_indicator.count("#")
            if len(tag_hierarchy) < h_level - 1:
                raise ValueError("Invalid heading level")
            while len(tag_hierarchy) > h_level - 1:
                tag_hierarchy.pop()
            tag_hierarchy.append(tag)
            continue

        if line.startswith("```"):
            if is_building_ml_extra:
                extra += line
                extra += "\n"
            else:
                text += line
                text += "\n"
            is_building_code = not is_building_code
            continue

        if is_building_code:
            if is_building_ml_extra:
                extra += line
                extra += "\n"
            else:
                text += line
                text += "\n"
            continue

        if line == "---":
            if is_building_ml_extra:
                all_cards.append(create_card(text, extra, tags, tag_hierarchy))
                text = ""
                extra = ""
                append = False

            is_building_ml_extra = not is_building_ml_extra
            if is_building_ml_extra:
                append = False
            continue

        if line == "":
            if not is_building_ml_extra:
                append = True
            continue

        if append:
            if text != "":
                all_cards.append(create_card(text, extra, tags, tag_hierarchy))
                append = False
            text = ""
            extra = ""

        if is_building_ml_extra or line.startswith("\t") or line.startswith(" "):
            append = False
            extra += line.lstrip()
            extra += "\n"
        else:
            append = False
            text += line
            text += "\n"

    if text != "":
        all_cards.append(create_card(text, extra, tags, tag_hierarchy))

    return all_cards


def process_file(root, deck_name, deck_directory, file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

        # isolate yaml stuff
        content = markdownHelper.remove_yaml(content)

        if content.rstrip("\n ").endswith("***"):
            return []

        if "***" in content:
            imported_parts = content.split("***")
            content = imported_parts[-1]

        tag = "#"
        tag += "::#".join(deck_name.replace(" ", "").split("::"))

        last_path = file_path.replace(deck_directory, "").replace(".md", "")

        tag += "::"
        tag += utils.string_to_tag(last_path)

        return parse_markdown(content, deck_name, [tag], root)


def main():
    console = Console()

    # status = console.status("Initializing")
    with Progress(console=console, transient=True) as progress:
        # with Live(Group( progress, status)):
        task = None

        # iterate over the specified deck names and directories
        for deck_path, deck_directory in DECKS.items():
            if task is not None:
                progress.remove_task(task)

            console.print(f" --- [blue]{deck_path}[/blue] --- ")

            for root, _, files in os.walk(deck_directory):
                task = progress.add_task(f"[green][bold]{deck_path}", total=len(files))

                # Process each note file in the current deck directory
                for file in files:
                    if root.split(os.sep)[-1].startswith(IGNORE_KEYWORDS):
                        print(f"Skipping {file}")
                        continue
                    # status.update(f"{file} -- Parsing")

                    # Process only Markdown files and ignore files starting with '_'
                    if file.startswith("_") or not file.endswith(".md"):
                        progress.advance(task)
                        continue

                    file_path = os.path.join(root, file)
                    try:
                        # status.update(f"{file} -- Processing file contents")
                        all_cards = process_file(
                            root, deck_path, deck_directory, file_path
                        )

                        if len(all_cards) == 0:
                            progress.advance(task)
                            continue

                        # import cards using AnkiConnect api
                        # status.update(f"{file} -- Sending")
                        console.print(f"[bold]{file}[/bold]")
                        rejected = anki.send_notes(console, all_cards)

                        # status.update(f"{file} -- Sent!")
                    except anki.AnkiError as e:
                        # progress.console.print_exception()
                        for i, item in enumerate(all_cards):
                            progress.console.print(f"{item["fields"]["Text"]}\n\t{item["fields"]["Extra"]}", style='bold red' if e.result is None or e.result[i] is None else 'bold green')
                            progress.console.print("\n----------\n\n")
                        progress.console.print(e.result)
                        progress.console.print(e.e)

                        sys.exit(1)

                    if rejected:
                        base_file_name = "anki-import-error"
                        file_extension = ".txt"
                        counter = 1

                        while os.path.exists(
                                os.path.join(
                                    OUTPUT_DIR,
                                    f"{base_file_name}_{counter}{file_extension}",
                                )
                        ):
                            counter += 1

                        file_name = f"{base_file_name}_{counter}{file_extension}"

                        with open(
                                os.path.join(OUTPUT_DIR, file_name), "w", encoding="utf-8"
                        ) as error_file:
                            error_file.write("\n".join(rejected))

                        print(f"Output written to {file_name}")
                        progress.advance(task)
                        continue

                    with open(file_path, "a+", encoding="utf-8") as f:
                        f.write("\n***\n")

                    progress.advance(task)


if __name__ == "__main__":
    main()
    