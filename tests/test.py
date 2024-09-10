if __name__ == "__main__":
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from main import parse_markdown
    else:
        from ..main import parse_markdown

    with open("test.md", "r", encoding="utf-8") as f:
        content = f.read()
        test = parse_markdown(content, "temp", "#delete", "root")
        print(test[0]['fields']['Text'])
