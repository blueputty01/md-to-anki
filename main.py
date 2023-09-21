import hashlib
import os
import re
import markdown2
import yaml
import anki
from urllib.parse import unquote

DECKS = {
    "math::math240 linear algebra": r"D:\Documents\Obsidian\default\$vault\school\year 1\math240",
    "socy::socy100": r"D:\Documents\Obsidian\default\$vault\school\year 1\socy100",
    "socy::socy230": r"D:\Documents\Obsidian\default\$vault\school\year 1\socy230",
}

# iterate through all markdown files in directory, ignoring files that begin with _.
# then, read yaml frontmatter and ignore files that have "imported" set to true.
# finally, parse the markdown into anki cards and import them using the AnkiConnect api


def parse_markdown(content, deck_name, tag, media_root):
    def create_card(t, e):
        t = t.strip()
        e = e.strip()

        cloze_id = 1
        bold_matches = re.findall(r'\*\*(.*?)\*\*', t)
        for bold_text in bold_matches:
            cloze_text = bold_text
            if not re.match(r'^\d+::.*', bold_text):
                cloze_text = f"{cloze_id}::{bold_text}"
                cloze_id += 1
            cloze_text = f"{{{{c{cloze_text}}}}}"

            t = t.replace(f"**{bold_text}**", cloze_text)

        def general_conversion(s):
            s = markdown2.markdown(s, extras=["fenced-code-blocks", "tables", "cuddled-lists", "code-friendly",
                                              "footnotes", "header-ids", "smarty-pants", "target-blank-links"])

            s = s.replace("<p>", "").replace("</p>", "")

            # process latex
            ml_latex = re.findall(r'\$\$(.*?)\$\$', s)
            for latex in ml_latex:
                s = s.replace(f"$${latex}$$", f"\\({latex}\\)")

            latex = re.findall(r'\$(.*?)\$', s)
            for l in latex:
                s = s.replace(f"${l}$", f"\\({l}\\)")

            # process images
            images = re.findall(r'<img src="(.*?)"', s)

            def hash_file(path):
                BUFF_SIZE = 65536  # read in 64kb chunks

                sha1 = hashlib.sha1()

                with open(path, 'rb') as f:
                    while True:
                        data = f.read(BUFF_SIZE)
                        if not data:
                            break
                        sha1.update(data)

                return sha1.hexdigest()

            for image in images:
                image_path = os.path.join(media_root, unquote(image).replace("/", os.sep))
                _, ext = os.path.splitext(image_path)

                image_id = hash_file(image_path)
                filename = f"{image_id}{ext}"

                anki.send_media({"filename": filename, 'path': image_path})

                s = s.replace(image, filename)

            return s.strip("\n")

        t = general_conversion(t)
        e = general_conversion(e)

        new_line = "<br />"
        t = t.replace("\n", new_line).replace(f">{new_line}<", "> <")
        e = e.replace("\n", new_line)

        # print(f"Creating card with text: {t}")
        # print(f"Creating card with extra: {e}")

        return {'deckName': deck_name,
                'modelName': "cloze",
                'fields': {'Text': t, 'Extra': e},
                'tags': [tag],
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": deck_name,
                    "duplicateScopeOptions": {
                        "deckName": deck_name,
                        "checkChildren": False,
                        "checkAllModels": False
                    }
                }}

    content = content.split('\n')

    text = ''
    extra = ''

    all = []

    is_building_ml_extra = False

    append = False
    for line in iter(content):
        # only strip on right to prevent stripping of indent/extra indicator
        line = line.rstrip()

        if line == "+":
            text += "\n"
            continue

        if line == "---":
            if is_building_ml_extra:
                all.append(create_card(text, extra))
                text = ''
                extra = ''
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
            if text != '':
                all.append(create_card(text, extra))
                append = False
            text = ''
            extra = ''

        if is_building_ml_extra or line.startswith("\t") or line.startswith(" "):
            append = False
            extra += line.lstrip()
            extra += "\n"
        else:
            append = False
            text += line
            text += "\n"

    if text != '':
        all.append(create_card(text, extra))

    return all


def main():
    # Iterate over the specified deck names and directories
    for deck_name, deck_directory in DECKS.items():
        # Process each note file in the current deck directory
        for root, dirs, files in os.walk(deck_directory):
            for file in files:

                all_cards = []
                # Process only Markdown files and ignore files starting with '_'
                if not file.startswith("_") and file.endswith(".md"):

                    file_path = os.path.join(root, file)

                    # read yaml frontmatter and ignore files that have "imported" set to true
                    front_matter = {}

                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                        if content.startswith("---"):
                            part = content[3:]
                            last_index = part.index("---")
                            yaml_parts = part[0:last_index]
                            content = part[last_index + 4:]
                            front_matter = yaml.safe_load(yaml_parts)
                            if front_matter.get("imported"):
                                continue

                        print(f"Processing {file}")
                        tag = "#"
                        tag += "::#".join(deck_name.replace(" ", "").split("::"))

                        last_path = file_path.replace(deck_directory, "").replace(".md", "")

                        tag += "::"
                        tag += last_path.strip("\\").replace("\\", "::").replace(" ", "")

                        cards = parse_markdown(content, deck_name, tag, root)

                        all_cards.extend(cards)

                    with open(file_path, "w", encoding="utf-8") as f:
                        # import cards using AnkiConnect api
                        rejected = anki.send_notes(all_cards)

                        if rejected:
                            base_file_name = "output"
                            file_extension = ".txt"
                            counter = 1

                            while os.path.exists(f"{base_file_name}_{counter}{file_extension}"):
                                counter += 1

                            file_name = f"{base_file_name}_{counter}{file_extension}"

                            with open(file_name, "w") as error_file:
                                error_file.write("\n".join(rejected))

                            print(f"Output written to {file_name}")

                        # set "imported" to true in yaml frontmatter
                        front_matter["imported"] = True
                        f.seek(0)
                        f.write("---\n")
                        f.write(yaml.dump(front_matter))
                        f.write("---\n")
                        f.write(content)


if __name__ == "__main__":
    main()

    # with open("test.md", "r", encoding="utf-8") as f:
    #     content = f.read()
    #     test = parse_markdown(content, "temp", "#delete", "root")
    # print(test)
