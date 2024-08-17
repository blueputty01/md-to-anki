import hashlib
import os
import re
import markdown2
import anki
import logging
from urllib.parse import unquote
from rich import print
from rich.console import Console, Group
from rich.live import Live
from rich.logging import RichHandler
from rich.progress import Progress
from deckConsts import DECKS, OUTPUT_DIR, IGNORE_KEYWORDS


# from pygments import highlight
# from pygments.lexers import get_lexer_by_name
# from pygments.formatters import HtmlFormatter

# md_langname_to_pygments_lexer = {
#     "cs" : "csharp",
#     "java" : "java",
#     "js" : "javascript",
#     "py" : "python",
#     "python" : "python"
# }

# iterate through all markdown files in directory, ignoring files that begin with _.
# then, read yaml frontmatter and ignore files that have "imported" set to true.
# finally, parse the markdown into anki cards and import them using the AnkiConnect api


def parse_markdown(content, deck_name, tag, media_root):
    def create_card(t, e):
        def pre_process(input_string):
            input_string = input_string.strip()
            return input_string

        t = pre_process(t)
        e = pre_process(e)

        # process clozes
        cloze_id = 1
        bold_matches = re.findall(r"\*\*(.*?)\*\*", t)
        for bold_text in bold_matches:
            cloze_text = bold_text
            if not re.match(r"^\d+::.*", bold_text):
                cloze_text = f"{cloze_id}::{bold_text}"
                cloze_id += 1
            cloze_text = f"{{{{c{cloze_text}}}}}"

            t = t.replace(f"**{bold_text}**", cloze_text)

        def post_process(raw_string):
            s = markdown2.markdown(
                raw_string,
                extras=[
                    # Allows a code block to not have to be indented by fencing it with '```' on a line before and after
                    # Based on http://github.github.com/github-flavored-markdown/ with support for syntax highlighting.
                    #"fenced-code-blocks",
                    # tables: Tables using the same format as GFM and PHP-Markdown Extra.
                    "tables",
                    # cuddled-lists: Allow lists to be cuddled to the preceding paragraph.
                    "cuddled-lists",
                    # code-friendly: The code-friendly extra disables the use of leading, trailing and
                    # --most importantly-- intra-word emphasis (<em>) and strong (<strong>)
                    # using single or double underscores, respectively.
                    "code-friendly",
                    # footnotes: support footnotes as in use on daringfireball.net and implemented in other
                    # Markdown processors (tho not in Markdown.pl v1.0.1).
                    "footnotes",
                    # smarty-pants: Fancy quote, em-dash and ellipsis handling similar to
                    # http://daringfireball.net/projects/smartypants/. See old issue 42 for discussion.
                    "smarty-pants",
                    # target-blank-links: Add target="_blank" to all <a> tags with an href.
                    # This causes the link to be opened in a new tab upon a click.
                    "target-blank-links",
                ],
            )

            s = s.replace("<p>", "").replace("</p>", "")

            # # process code
            # ml_code = re.findall(r"\`\`\`(.*?)\`\`\`", s)
            # for code in ml_code:
            #     lang = ""
            #     if md_langname_to_pygments_lexer.contains_key(ml_code.split(' ')[0]):
            #         lang = md_langname_to_pygments_lexer[ml_code.split(' ')[0]]

            #     print("lang: " + lang);
            #     lexer = get_lexer_by_name(lang, stripall=True)
            #     formatter = HtmlFormatter(linenos=False, noclasses=True)
            #     print(highlight(code, lexer, formatter));

            
            # process latex
            # multi-line
            ml_latex = re.findall(r"\$\$(.*?)\$\$", s)
            for latex in ml_latex:
                latex = latex.replace("}}", "} }")
                s = s.replace(f"$${latex}$$", f"\\[{latex}\\]")

            # single line
            sl_latex = re.findall(r"\$(.*?)\$", s)
            for latex in sl_latex:
                latex = latex.replace("}}", "} }")
                s = s.replace(f"${latex}$", f"\\({latex}\\)")

            # process images
            images = re.findall(r'<img src="(.*?)"', s)

            def hash_file(path):
                BUFF_SIZE = 65536  # read in 64kb chunks

                sha1 = hashlib.sha1()

                with open(path, "rb") as f:
                    while True:
                        data = f.read(BUFF_SIZE)
                        if not data:
                            break
                        sha1.update(data)

                return sha1.hexdigest()

            for image in images:
                image_path = os.path.join(
                    media_root, unquote(image).replace("/", os.sep)
                )
                _, ext = os.path.splitext(image_path)

                image_id = hash_file(image_path)
                filename = f"{image_id}{ext}"

                anki.send_media({"filename": filename, "path": image_path})

                s = s.replace(image, filename)

            return s.strip("\n")

        t = post_process(t)
        e = post_process(e)

        new_line = "<br />"
        t = t.replace("\n", new_line).replace(f">{new_line}<", "> <")
        e = e.replace("\n", new_line)

        # print(f"Creating card with text: {t}")
        # print(f"Creating card with extra: {e}")

        return {
            "deckName": deck_name,
            "modelName": "cloze",
            "fields": {"Text": t, "Extra": e},
            "tags": [tag],
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

    all = []

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
                all.append(create_card(text, extra))
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
                all.append(create_card(text, extra))
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
        all.append(create_card(text, extra))

    return all

def get_content(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

        # isolate yaml stuff
        if content.startswith("---"):
            part = content[2:]
            last_index = part.index("---")
            content = part[last_index + 3:]

        if content.rstrip("\n ").endswith("***"):
            return ""

        if "***" in content:
            imported_parts = content.split("***")
            content = imported_parts[-2]
        
        return content

def process_file(root, deck_name, deck_directory, file_path):
    content = get_content(file_path)

    if content == "":
        return []

    tag = "#"
    tag += "::#".join(deck_name.replace(" ", "").split("::"))

    last_path = file_path.replace(deck_directory, "").replace(
        ".md", ""
    )

    # remove leading/trailing slashes
    tag_path = last_path.strip(os.sep)
    # replace slashes with double colons
    tag_path = tag_path.replace(os.sep, "::")
    # remove spaces
    tag_path = tag_path.replace(" ", "")
    # replace dashes with sub tag
    tag_path = tag_path.replace("-", "::")

    tag += "::"
    tag += tag_path

    return parse_markdown(content, deck_name, tag, root)

 
def main():
    console=Console()

    logging.basicConfig(level="NOTSET", handlers=[RichHandler(console=console, level="NOTSET")])
    logger = logging.getLogger('rich')

    # status = console.status("Initializing")
    with Progress(console=console, transient=True) as progress:
    # with Live(Group( progress, status)):
        task = None

        # iterate over the specified deck names and directories
        for deck_name, deck_directory in DECKS.items():
            if task is not None:
                progress.remove_task(task)

            # console.print(f" --- [blue]{deck_name}[/blue] --- ")

            root, _, files = next(os.walk(deck_directory))
            task = progress.add_task(f"[green][bold]{deck_name}", total=len(files))

            # Process each note file in the current deck directory
            for file in files:
                # status.update(f"{file} -- Parsing")

                all_cards = []
                rejected = []

                # Process only Markdown files and ignore files starting with '_'
                if root.split(os.sep)[-1].startswith(IGNORE_KEYWORDS) or file.startswith("_") or not file.endswith(".md"):
                    progress.advance(task)
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    # status.update(f"{file} -- Processing file contents")

                    # Process file md content 
                    all_cards = process_file(root, deck_name, deck_directory, file_path)

                    # No useful (unprocessed) md content
                    if len(all_cards) == 0:
                        progress.advance(task)
                        continue

                    # Import cards using AnkiConnect api
                    # status.update(f"{file} -- Sending")
                    console.print(f"[bold]{file}[/bold]")
                    rejected = anki.send_notes(console, all_cards)

                    # status.update(f"{file} -- Sent!")

                    # Write processed marker
                    with open(file_path, "a", encoding="utf-8") as f:
                        content = get_content(file_path)

                        # count number of new line characters at end of file
                        counter = 0
                        while content.endswith("\n"):
                            content = content[:-1]
                            counter += 1

                        if counter < 2:
                            f.write("\n\n")
                        f.write("***\n")
                except Exception:
                    progress.console.print_exception(show_locals=True)

                # status.stop()
                if rejected is None:
                    # anki connect is not running
                    return None

                if rejected:
                    base_file_name = "anki-import-error"
                    file_extension = ".txt"
                    counter = 1

                    while os.path.exists(
                            os.path.join(OUTPUT_DIR, f"{base_file_name}_{counter}{file_extension}")
                    ):
                        counter += 1

                    file_name = f"{base_file_name}_{counter}{file_extension}"

                    with open(
                            os.path.join(OUTPUT_DIR, file_name), "w"
                    ) as error_file:
                        error_file.write("\n".join(rejected))

                    print(f"Output written to {file_name}")
                    progress.advance(task)
                    continue

                
                progress.advance(task)


if __name__ == "__main__":
    main()
    print("Complete.")
