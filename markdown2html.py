#!/usr/bin/python3
""" Markdown to HTML """

import sys
import os

def check_incoming_data():
    """ Check incoming data """
    length = len(sys.argv)

    if (length < 3):
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Missing {file_path}")
        exit(1)
    return file_path

if __name__ == "__main__":
    read_file = check_incoming_data()
    write_file = sys.argv[2]
    queue = []
    stack = []
    lines = ""
    list_mode = 0
    elements = {
      '#': 'h1',
      '##': 'h2',
      '###': 'h3',
      '####': 'h4',
      '#####': 'h5',
      '######': 'h6',
      '-': 'li'
    }

    with open(read_file, 'r') as file:
        for line in file:
            line_trimmed = line.strip()
            if line_trimmed:
                tokens = line_trimmed.split(' ')
                length = len(tokens)
                for index, token in enumerate(tokens):
                    if token in elements:
                        if token != '-':
                            list_mode = 0
                        if token == '-' and list_mode == 0:
                            queue.append('<ul>')
                            stack.append('</ul>')
                            list_mode = 1
                        queue.append(f"<{elements[token]}>")
                        stack.append(f"</{elements[token]}>")
                    else:
                        if index == length - 1:
                            queue.append(f"{token}")
                        else:
                            queue.append(f"{token} ")
                while stack:
                    current = stack[-1]
                    if list_mode == 1 and current == '</ul>':
                        break
                    queue.append(stack.pop())
                queue.append("\n")
                lines += "".join(queue)
                queue = []
    while stack:
        lines += stack.pop()

    lines = lines.strip()

    with open(write_file, 'w') as file:
        file.writelines(lines)
