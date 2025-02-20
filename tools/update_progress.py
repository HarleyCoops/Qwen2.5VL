"""
Progress Tracking Updater

This script automatically updates the PROGRESS.md file based on:
1. Git commit history
2. Task completion status
3. Current development focus
"""

import re
from datetime import datetime
from pathlib import Path
import subprocess
from typing import List, Dict, Tuple

class ProgressUpdater:
    def __init__(self, progress_file: str = "PROGRESS.md"):
        self.progress_file = Path(progress_file)
        self.content = self._read_progress_file()
        self.sections = self._parse_sections()

    def _read_progress_file(self) -> str:
        """Read the current progress file content."""
        if not self.progress_file.exists():
            raise FileNotFoundError(f"Progress file not found: {self.progress_file}")
        return self.progress_file.read_text()

    def _parse_sections(self) -> Dict[str, str]:
        """Parse the progress file into sections."""
        sections = {}
        current_section = None
        current_content = []

        for line in self.content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line[3:].strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def get_git_history(self) -> List[str]:
        """Get recent git commit messages."""
        try:
            result = subprocess.run(
                ['git', 'log', '--pretty=format:%s', '-n', '10'],
                capture_output=True,
                text=True
            )
            return result.stdout.split('\n')
        except subprocess.CalledProcessError:
            return []

    def extract_tasks_from_commits(self, commits: List[str]) -> List[str]:
        """Extract tasks from commit messages."""
        tasks = []
        for commit in commits:
            # Look for task-like items in commit messages
            task_matches = re.findall(r'(?:Add|Update|Implement|Create|Fix)\s+([^:\.]+)', commit)
            tasks.extend(task_matches)
        return tasks

    def update_completed_tasks(self, new_tasks: List[str]):
        """Update the Completed Tasks section."""
        if 'Completed Tasks' not in self.sections:
            return

        completed_section = self.sections['Completed Tasks']
        existing_tasks = set(re.findall(r'- \[x\] (.+)', completed_section))
        
        for task in new_tasks:
            if task not in existing_tasks:
                completed_section += f"\n- [x] {task}"
        
        self.sections['Completed Tasks'] = completed_section

    def update_current_focus(self):
        """Update the Current Development Focus section based on recent activity."""
        recent_commits = self.get_git_history()
        current_focus = set()
        
        for commit in recent_commits[:5]:  # Look at 5 most recent commits
            # Extract main focus areas
            focus_matches = re.findall(r'(?:Add|Update|Implement|Create|Fix)\s+([^:\.]+)', commit)
            current_focus.update(focus_matches)

        if 'Current Development Focus' in self.sections:
            focus_section = "### Current Focus Areas\n"
            for focus in current_focus:
                focus_section += f"- {focus}\n"
            
            self.sections['Current Development Focus'] = focus_section

    def update_upcoming_tasks(self):
        """Update the Upcoming Tasks section based on TODOs in code."""
        try:
            result = subprocess.run(
                ['git', 'grep', '-l', 'TODO'],
                capture_output=True,
                text=True
            )
            todo_files = result.stdout.split('\n')
            
            if 'Upcoming Tasks' in self.sections:
                tasks_section = "### Identified Tasks\n"
                for file in todo_files:
                    if file:
                        tasks_section += f"- Review TODOs in {file}\n"
                
                self.sections['Upcoming Tasks'] = tasks_section
        except subprocess.CalledProcessError:
            pass

    def save_progress(self):
        """Save the updated progress file."""
        content = []
        content.append("# Project Progress and Roadmap\n")
        
        for section, text in self.sections.items():
            content.append(f"## {section}\n")
            content.append(text + "\n")

        self.progress_file.write_text('\n'.join(content))

def main():
    updater = ProgressUpdater()
    
    # Get recent activity
    commits = updater.get_git_history()
    new_tasks = updater.extract_tasks_from_commits(commits)
    
    # Update sections
    updater.update_completed_tasks(new_tasks)
    updater.update_current_focus()
    updater.update_upcoming_tasks()
    
    # Save updates
    updater.save_progress()

if __name__ == "__main__":
    main()
