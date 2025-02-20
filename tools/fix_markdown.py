"""
Markdown Formatter

This script fixes common markdown formatting issues:
- Adds blank lines around headings
- Adds blank lines around lists
- Adds blank lines around code blocks

With added error handling and logging to prevent issues during automation.
"""

import os
import re
import sys
import logging
from typing import List, Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('markdown_formatting.log')
    ]
)

def is_file_locked(file_path: str) -> bool:
    """Check if a file is locked/being used by another process."""
    try:
        with open(file_path, 'r+'):
            return False
    except IOError:
        return True

def fix_markdown_file(file_path: str) -> Optional[bool]:
    """
    Fix markdown formatting in a single file.
    Returns True if changes were made, False if no changes needed, None if error occurred.
    """
    if is_file_locked(file_path):
        logging.warning(f"File {file_path} is locked. Skipping.")
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        # Store original content for comparison
        modified_content = original_content

        # Add blank lines around headings
        modified_content = re.sub(r'([^\n])\n(#{1,6} )', r'\1\n\n\2', modified_content)
        modified_content = re.sub(r'(#{1,6} .*?)\n([^\n])', r'\1\n\n\2', modified_content)

        # Add blank lines around lists
        modified_content = re.sub(r'([^\n])\n(- |\d+\. )', r'\1\n\n\2', modified_content)
        modified_content = re.sub(r'(- |\d+\. .*?)\n([^\n-])', r'\1\n\n\2', modified_content)

        # Add blank lines around code blocks
        modified_content = re.sub(r'([^\n])\n```', r'\1\n\n```', modified_content)
        modified_content = re.sub(r'```\n([^\n])', r'```\n\n\1', modified_content)

        # Remove multiple blank lines
        modified_content = re.sub(r'\n{3,}', r'\n\n', modified_content)

        # Only write if content changed
        if modified_content != original_content:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                logging.info(f"Updated formatting in {file_path}")
                return True
            except Exception as e:
                logging.error(f"Failed to write to {file_path}: {str(e)}")
                return None
        else:
            logging.info(f"No formatting changes needed in {file_path}")
            return False

    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")
        return None

def process_directory(directory: str) -> tuple[int, int, int]:
    """
    Process all markdown files in a directory.
    Returns tuple of (files_changed, files_unchanged, files_errored)
    """
    changed, unchanged, errors = 0, 0, 0
    
    try:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    result = fix_markdown_file(file_path)
                    
                    if result is True:
                        changed += 1
                    elif result is False:
                        unchanged += 1
                    else:  # None indicates error
                        errors += 1
                        
    except Exception as e:
        logging.error(f"Error walking directory {directory}: {str(e)}")
        
    return changed, unchanged, errors

def main(directories: List[str]) -> int:
    """
    Main function to process markdown files.
    Returns exit code (0 for success, 1 for errors).
    """
    total_changed = total_unchanged = total_errors = 0
    
    for directory in directories:
        if not os.path.exists(directory):
            logging.warning(f"Directory {directory} does not exist. Skipping.")
            continue
            
        logging.info(f"Processing directory: {directory}")
        changed, unchanged, errors = process_directory(directory)
        
        total_changed += changed
        total_unchanged += unchanged
        total_errors += errors
    
    logging.info(f"""
    Processing complete:
    - Files changed: {total_changed}
    - Files unchanged: {total_unchanged}
    - Files with errors: {total_errors}
    """)
    
    return 1 if total_errors > 0 else 0

if __name__ == "__main__":
    directories = [
        "academic",
        "implementation",
        "model",
        "docs",
        "."  # Root directory for README.md and PROGRESS.md
    ]
    
    sys.exit(main(directories))
