def remove_yaml(content):
    if content.startswith("---"):
        part = content[2:]
        last_index = part.index("---")
        return part[last_index + 3 :]
    return content