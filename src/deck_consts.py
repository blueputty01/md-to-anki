import os

ROOT = "/Users/alexyang/Nextcloud/class_notes/"

decks = dict()

FOLDERS = {
    "cs": "cs",
    "math": "math",
}

prefix_rules = {
    "cmsc": FOLDERS["cs"],
    "amsc": FOLDERS["math"],
    "math": FOLDERS["math"],
}

exact_rules = {
    "leetcode": FOLDERS["cs"],
    "web": FOLDERS["cs"],
}

for course in os.scandir(ROOT):
    if course.is_dir():
        n = course.name
        if n.startswith("."):
            continue
        if n in exact_rules:
            decks[f"{exact_rules[n]}::{n}"] = course.path
        else:
            for prefix, folder in prefix_rules.items():
                if n.startswith(prefix):
                    decks[f"{folder}::{n}"] = course.path
                    break

print("Detected the following decks:")
for k, v in decks.items():
    print(f"- {k}: {v}")

IGNORE_KEYWORDS = []

DECKS = decks

OUTPUT_DIR = "/Users/alexyang/Desktop"
