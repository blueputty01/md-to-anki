import hashlib
import os
from pathlib import Path

# read in 64kb chunks
BUFF_SIZE = 65536


def hash_file(path: str | Path) -> str:
    sha1 = hashlib.sha1()
    with open(path, "rb") as f:
        while True:
            data = f.read(BUFF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


def string_to_tag(s: str) -> str:
    # remove leading/trailing slashes
    tag_path = s.strip(os.sep)
    # replace slashes with double colons
    tag_path = tag_path.replace(os.sep, "::")
    # remove spaces
    tag_path = tag_path.replace(" ", "")
    # replace dashes with sub tag
    return tag_path.replace("-", "::")
