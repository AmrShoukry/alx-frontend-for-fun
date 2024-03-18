#!/usr/bin/python3
""" Markdown to HTML """

import sys
import os
import re

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
    ordered_list_mode = 0
    unordered_list_mode = 0
    p_mode = 0
    patterns = {
        r"\*\*(.*?)\*\*": 'b',
        r"__(.*?)__": 'em'
    }
    elements = {
      '#': 'h1',
      '##': 'h2',
      '###': 'h3',
      '####': 'h4',
      '#####': 'h5',
      '######': 'h6',
      '-': 'li',
      '*': 'li'
    }

    with open(read_file, 'r') as file:
        for line in file:
            line_trimmed = line.strip()
            if not line_trimmed:
                p_mode = 0
                queue.append(stack.pop())
            if line_trimmed:
                tokens = line_trimmed.split(' ')
                length = len(tokens)

                for index, token in enumerate(tokens):
                    if token in elements:
                        p_mode = 0
                        if token != '-':
                            unordered_list_mode = 0
                        if token == '-' and unordered_list_mode == 0:
                            queue.append('<ul>')
                            stack.append('</ul>')
                            unordered_list_mode = 1
                        if token != '*':
                            ordered_list_mode = 0
                        if token == '*' and ordered_list_mode == 0:
                            queue.append('<ol>')
                            stack.append('</ol>')
                            ordered_list_mode = 1
                        queue.append(f"<{elements[token]}>")
                        stack.append(f"</{elements[token]}>")
                    else:
                        if index == 0:
                            if p_mode == 0:
                                queue.append('<p>')
                                stack.append('</p>')
                                p_mode = 1
                            else:
                                queue.append('<br />')

                        matched = 0
                        print(token)
                        for pattern, tag in patterns.items():
                            match = re.search(pattern, token)
                            if (match):
                                print(token)
                                match_start = match.start()
                                match_end = match.end()
                                matched_text = match.group(1)
                                queue.append(token[:match_start])
                                queue.append(f"<{tag}>")
                                queue.append(matched_text)
                                queue.append(f"</{tag}>")
                                queue.append(token[match_end:])
                                matched = 1

                        if matched == 0:
                            if index == length - 1:
                                queue.append(f"{token}")
                            else:
                                queue.append(f"{token} ")
                while stack:
                    current = stack[-1]
                    if (unordered_list_mode == 1 and current == '</ul>')\
                      or (ordered_list_mode == 1 and current == '</ol>')\
                          or (p_mode == 1 and current == '</p>'):
                        break
                    queue.append(stack.pop())
                lines += "".join(queue)
                queue = []
    while stack:
        lines += stack.pop()
    while queue:
        lines += queue.pop(0)

    lines = lines.strip()

    with open(write_file, 'w') as file:
        file.writelines(lines)
