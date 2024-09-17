from typing import Optional
from urllib.parse import unquote

import bs4
import re
from pathlib import Path
import markdown
from markdown.extensions import codehilite, fenced_code

from md_mathjax import Md4MathjaxExtension
from utils import utils

REM_CONVERSION = 16


def remove_yaml(content):
    if content.startswith("---"):
        part = content[2:]
        last_index = part.index("---")
        return part[last_index + 3 :]
    return content


def remove_paragraph_tags(soup: bs4.BeautifulSoup) -> None:
    for tag in soup.find_all("p"):
        tag.unwrap()


def process_images(
    soup: bs4.BeautifulSoup, media_root: Path
) -> list[dict[str, object]]:
    images = soup.find_all("img")
    media_to_post = []
    for img in images:
        src = img["src"]
        alt = img["alt"]

        image_path: Path = media_root / Path(unquote(src))
        image_id = utils.hash_file(image_path)
        filename = f"{image_id}{image_path.suffix}"
        media_to_post.append({"filename": filename, "path": str(image_path)})

        alt_size = re.match(r"^\|(\d+)", alt)
        if alt_size:
            img["width"] = str(int(alt_size.group(1)) / REM_CONVERSION) + "rem"
            img["height"] = "auto"

        img["src"] = filename
        img["alt"] = ""
    return media_to_post


def md_to_html(raw_string: str) -> str:
    raw_string = raw_string.strip()

    s = markdown.markdown(
        raw_string,
        extensions=[
            codehilite.CodeHiliteExtension(),
            fenced_code.FencedCodeExtension(),
            Md4MathjaxExtension(),
            "nl2br",
        ],
    )

    return s.replace("\n", "")


def process_field(
    raw_string: str, root: Path
) -> tuple[bs4.BeautifulSoup, list[dict[str, object]]]:
    s = md_to_html(raw_string)

    soup = bs4.BeautifulSoup(s, "html.parser")
    remove_paragraph_tags(soup)
    media_to_post = process_images(soup, root)

    return soup, media_to_post


class Card:
    text: str
    extra: str
    tags: Optional[list[str]]
    images: Optional[list[dict[str, object]]]

    def __init__(
        self,
        text: str,
        extra: str,
        tags: Optional[list[str]] = None,
        images: Optional[list[dict[str, object]]] = None,
    ):
        self.text = text
        self.extra = extra
        self.tags = tags
        self.images = images


def process_fields(
    t: str, e: str, root: Path
) -> tuple[str, str, list[dict[str, object]]]:
    text_field, t_img = process_field(t, root)
    extra_field, e_img = process_field(e, root)

    images = t_img + e_img

    text_string = str(text_field)

    bold_tags = ("<strong>", "</strong>")

    # replace remaining ** with <strong> and </strong>
    asterisk_matches = re.findall(r"\*\*(.*?)\*\*", text_string)
    for asterisk_text in asterisk_matches:
        text_string = text_string.replace(
            f"**{asterisk_text}**", f"{bold_tags[0]}{asterisk_text}{bold_tags[1]}"
        )

    # process clozes
    cloze_id = 1
    bold_matches = re.findall(rf"{bold_tags[0]}(.*?){bold_tags[1]}", text_string)
    for bold_text in bold_matches:
        cloze_text = bold_text
        if not re.match(r"^\d+::.*", bold_text):
            cloze_text = f"{cloze_id}::{bold_text}"
            cloze_id += 1
        cloze_text = f"{{{{c{cloze_text}}}}}"

        text_string = text_string.replace(
            f"{bold_tags[0]}{bold_text}{bold_tags[1]}", cloze_text
        )

    return text_string, str(extra_field), images


def parse_markdown(raw: str, root: Path) -> list[Card]:
    content = raw.split("\n")

    text = ""
    extra = ""

    extracted_fields = []

    tag_hierarchy: list[str] = []

    is_building_multiline_extra = False
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
            if is_building_multiline_extra:
                extra += line
                extra += "\n"
            else:
                text += line
                text += "\n"
            is_building_code = not is_building_code
            continue

        if is_building_code:
            if is_building_multiline_extra:
                extra += line
                extra += "\n"
            else:
                text += line
                text += "\n"
            continue

        if line == "---":
            if is_building_multiline_extra:
                extracted_fields.append((text, extra, tag_hierarchy))
                text = ""
                extra = ""
                append = False

            is_building_multiline_extra = not is_building_multiline_extra
            if is_building_multiline_extra:
                append = False
            continue

        if line == "":
            if not is_building_multiline_extra:
                append = True
            continue

        if append:
            if text != "":
                extracted_fields.append((text, extra, tag_hierarchy))
                append = False
            text = ""
            extra = ""

        if is_building_multiline_extra or line.startswith("\t") or line.startswith(" "):
            append = False
            extra += line.lstrip()
            extra += "\n"
        else:
            append = False
            text += line
            text += "\n"

    if text != "":
        extracted_fields.append((text, extra, tag_hierarchy))

    all_cards: list[Card] = []
    for text, extra, tag_hierarchy in extracted_fields:
        text, extra, images = process_fields(text, extra, root)
        all_cards.append(Card(text, extra, tag_hierarchy, images))

    return all_cards
