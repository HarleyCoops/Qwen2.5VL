"""
Markdown Formatter

This script fixes common markdown formatting issues:
- Adds blank lines around headings
- Adds blank lines around lists
- Adds blank lines around code blocks
"""

import os
import re

def fix_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add blank lines around headings
    content = re.sub(r'([^\n])\n(#{1,6} )', r'\1\n\n\2', content)
    content = re.sub(r'(#{1,6} .*?)\n([^\n])', r'\1\n\n\2', content)

    # Add blank lines around lists
    content = re.sub(r'([^\n])\n(- |\d+\. )', r'\1\n\n\2', content)
    content = re.sub(r'(- |\d+\. .*?)\n([^\n-])', r'\1\n\n\2', content)

    # Add blank lines around code blocks
    content = re.sub(r'([^\n])\n```', r'\1\n\n```', content)
    content = re.sub(r'```\n([^\n])', r'```\n\n\1', content)

    # Remove multiple blank lines
    content = re.sub(r'\n{3,}', r'\n\n', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                fix_markdown_file(file_path)

if __name__ == "__main__":
    # Process all markdown files in these directories
    directories = [
        "academic",
        "implementation",
        "model",
        "docs",
        "."  # Root directory for README.md and PROGRESS.md
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            process_directory(directory)
            print(f"Processed markdown files in {directory}")
