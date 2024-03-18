#!/usr/bin/python3
""" Markdown to HTML """

if __name__ == "__main__":
    import sys
    import os

    length = len(sys.argv)

    if (length < 3):
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Missing {file_path}")
        exit(1)
