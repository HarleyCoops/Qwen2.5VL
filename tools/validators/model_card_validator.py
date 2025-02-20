"""
Model Card Validator

This script provides utilities for validating model cards against a defined template structure.
It ensures all required sections are present and properly formatted.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class ModelCardValidator:
    """Validates model cards against the template structure."""

    REQUIRED_SECTIONS = [
        "Model Details",
        "Model Architecture",
        "Intended Use",
        "Factors",
        "Metrics",
        "Training Data",
        "Ethical Considerations",
        "Caveats and Recommendations"
    ]

    REQUIRED_METRICS = [
        "Visual Grounding",
        "Video Understanding",
        "Agent Capabilities"
    ]

    def __init__(self, model_card_path: str):
        """Initialize with path to model card markdown file."""
        self.model_card_path = Path(model_card_path)
        self.content = self._read_model_card()
        self.sections = self._parse_sections()

    def _read_model_card(self) -> str:
        """Read the model card content."""
        try:
            with open(self.model_card_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Model card not found at {self.model_card_path}")

    def _parse_sections(self) -> Dict[str, str]:
        """Parse the model card into sections."""
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

    def validate_required_sections(self) -> Tuple[bool, List[str]]:
        """Check if all required sections are present."""
        missing_sections = [
            section for section in self.REQUIRED_SECTIONS
            if section not in self.sections
        ]
        return len(missing_sections) == 0, missing_sections

    def validate_metrics_section(self) -> Tuple[bool, List[str]]:
        """Validate the metrics section."""
        if 'Metrics' not in self.sections:
            return False, ["Metrics section missing"]

        metrics_content = self.sections['Metrics']
        missing_metrics = [
            metric for metric in self.REQUIRED_METRICS
            if metric not in metrics_content
        ]
        return len(missing_metrics) == 0, missing_metrics

    def validate_model_details(self) -> Tuple[bool, List[str]]:
        """Validate the model details section."""
        required_details = [
            "Model Name",
            "Version",
            "Type",
            "Organization",
            "License"
        ]
        
        if 'Model Details' not in self.sections:
            return False, ["Model Details section missing"]

        details_content = self.sections['Model Details']
        missing_details = [
            detail for detail in required_details
            if f"**{detail}**" not in details_content
        ]
        return len(missing_details) == 0, missing_details

    def validate_placeholders(self) -> Tuple[bool, List[str]]:
        """Check for remaining placeholder values."""
        placeholder_pattern = r'\[([^\]]+)\]'
        placeholders = re.findall(placeholder_pattern, self.content)
        return len(placeholders) == 0, placeholders

    def validate_all(self) -> Dict[str, Tuple[bool, List[str]]]:
        """Run all validations."""
        return {
            "required_sections": self.validate_required_sections(),
            "metrics": self.validate_metrics_section(),
            "model_details": self.validate_model_details(),
            "placeholders": self.validate_placeholders()
        }

def validate_model_card(model_card_path: str) -> Dict[str, Tuple[bool, List[str]]]:
    """
    Validate a model card file.
    
    Args:
        model_card_path: Path to the model card markdown file
        
    Returns:
        Dictionary containing validation results
    """
    validator = ModelCardValidator(model_card_path)
    return validator.validate_all()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python model_card_validator.py <path_to_model_card>")
        sys.exit(1)
        
    model_card_path = sys.argv[1]
    results = validate_model_card(model_card_path)
    
    # Print validation results
    print("\nModel Card Validation Results:")
    print("==============================")
    
    for check, (passed, details) in results.items():
        status = "✓" if passed else "✗"
        print(f"\n{check.replace('_', ' ').title()}: {status}")
        if not passed:
            print("Issues found:")
            for detail in details:
                print(f"  - {detail}")
