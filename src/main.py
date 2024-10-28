import os
import re
from typing import Collection
from pathlib import Path

from rich.console import Console
from rich.progress import Progress

import argparse
import parser
from utils import anki
from utils import utils

from deckConsts import DECKS, IGNORE_KEYWORDS  # type: ignore


def process_file(
    root: Path, deck_name: str, deck_directory: str, file_path: str, force: bool
) -> tuple[list[dict[str, Collection[str]]], list[dict[str, str]]]:
    """Returns tuple representing payload for cards and images to be imported to Anki"""

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = parser.remove_yaml(content)

    if not force:
        if content.rstrip("\n ").endswith("***"):
            return [], []

        if "***" in content:
            imported_parts = content.split("***")
            content = imported_parts[-1]
    else:
        content = content.replace("***", "")

    tag = "#"
    tag += "::#".join(deck_name.replace(" ", "").split("::"))

    last_path = file_path.replace(deck_directory, "").replace(".md", "")

    tag += "::"
    tag += utils.string_to_tag(last_path)

    parsed_cards = parser.parse_markdown(content, root)

    # future integration path for multiple tag syntax
    base_tags = [tag]

    cards_payload = []
    images_payload = []

    unclozed_cards = []
    for card in parsed_cards:
        text = card.text

        if not re.search(r"\{\{c\d+::", text):
            unclozed_cards.append((text, card.extra))
            continue

        if card.tags and len(card.tags) > 0:
            heading_tag = "::".join(card.tags)
            new_tags = [f"{tag}::{heading_tag}" for tag in base_tags]
        else:
            new_tags = base_tags

        if card.images:
            images_payload.extend(card.images)

        single_card_payload = {
            "deckName": deck_name,
            "modelName": "cloze",
            "fields": {"Text": card.text, "Extra": card.extra},
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
        cards_payload.append(single_card_payload)

    if unclozed_cards:
        raise ValueError("Some cards are not clozed: " + str(unclozed_cards))

    return cards_payload, images_payload


def parse_args():
    parser = argparse.ArgumentParser(prog="md-to-anki")
    parser.add_argument("-f", "--force", action="store_true")
    return parser.parse_args()


def main():
    console = Console()
    args = parse_args()

    with Progress(console=console, transient=True) as progress:
        task = None

        for deck_path, deck_directory in DECKS.items():
            # 'task' is a whole progress bar -- remove old ones and only show the current one while processing
            if task is not None:
                progress.remove_task(task)

            console.print(f" --- [blue]{deck_path}[/blue] --- ")

            for root, _, files in os.walk(deck_directory):
                task = progress.add_task(
                    f"[green][bold]{deck_path}", total=len(files) - 1
                )

                for file in files:
                    if root.split(os.sep)[-1] in IGNORE_KEYWORDS:
                        print(f"Skipping {file}")
                        continue

                    if file.startswith("_") or not file.endswith(".md"):
                        progress.advance(task)
                        continue

                    file_path = os.path.join(root, file)

                    try:
                        all_cards, all_images = process_file(
                            root, deck_path, deck_directory, str(file_path), args.force
                        )
                    except ValueError as e:
                        console.print(f"Error processing {file}: {e}")
                        progress.advance(task)
                        continue

                    if len(all_cards) == 0:
                        progress.advance(task)
                        continue

                    if all_images:
                        for image in all_images:
                            console.print(f"Uploading {image['filename']} to Anki")
                            anki.send_media(image)

                    console.print(f"[bold]Processing {file}[/bold]")

                    try:
                        anki.send_notes(all_cards)
                    except anki.AnkiError as e:
                        for i, item in enumerate(all_cards):
                            style = (
                                "bold red"
                                if e.result is None or e.result[i] is None
                                else "bold green"
                            )
                            progress.console.print(
                                "Text: " + item["fields"]["Text"], style=style
                            )
                            progress.console.print(
                                "Extra: " + item["fields"]["Extra"], style=style
                            )
                            progress.console.print("\n----------\n\n")
                        progress.console.print(e.result)
                        progress.console.print(e.e)

                        continue

                    # TODO: fix multi-write of end delimiter on force
                    with open(file_path, "a+", encoding="utf-8") as f:
                        f.write("\n***\n")

                    progress.advance(task)


if __name__ == "__main__":
    main()
