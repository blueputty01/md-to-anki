from main import parse_markdown

if __name__ == "__main__":
    with open("test.md", "r", encoding="utf-8") as f:
        content = f.read()
        test = parse_markdown(content, "temp", "#delete", "root")
        print(test)
