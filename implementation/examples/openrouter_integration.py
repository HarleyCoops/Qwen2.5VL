"""
OpenRouter Integration Example for Qwen2.5-VL

This script demonstrates how to interact with Qwen2.5-VL through the OpenRouter API.
It includes examples of different capabilities: image analysis, video understanding,
and document parsing.
"""

import os
import requests
from typing import Dict, Union, Optional
from pathlib import Path
import base64

class Qwen25VLClient:
    """Client for interacting with Qwen2.5-VL through OpenRouter."""
    
    def __init__(self, api_key: str):
        """
        Initialize the client.
        
        Args:
            api_key: OpenRouter API key
        """
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "qwen/qwen2.5-vl"
        
    def _encode_image(self, image_path: str) -> str:
        """
        Encode image to base64.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64 encoded image
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
            
    def _make_request(self, 
                     messages: list, 
                     temperature: float = 0.7) -> Dict:
        """
        Make API request to OpenRouter.
        
        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature
            
        Returns:
            API response
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        
        return response.json()

    def analyze_image(self, 
                     image_path: str, 
                     prompt: str) -> str:
        """
        Analyze an image using Qwen2.5-VL.
        
        Args:
            image_path: Path to image file
            prompt: Text prompt describing the analysis task
            
        Returns:
            Model's response
        """
        image_b64 = self._encode_image(image_path)
        
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image_b64
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
        
        response = self._make_request(messages)
        return response["choices"][0]["message"]["content"]

    def analyze_document(self, 
                        document_path: str, 
                        task: str) -> str:
        """
        Parse and analyze a document.
        
        Args:
            document_path: Path to document image
            task: Specific parsing task (e.g., "extract text", "analyze layout")
            
        Returns:
            Parsed content or analysis
        """
        return self.analyze_image(
            document_path,
            f"Please {task} from this document."
        )

    def process_video(self, 
                     video_frames: list, 
                     prompt: str) -> str:
        """
        Process video frames for analysis.
        
        Args:
            video_frames: List of paths to video frame images
            prompt: Analysis prompt
            
        Returns:
            Video analysis result
        """
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": self._encode_image(frame)
                    } for frame in video_frames
                ] + [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
        
        response = self._make_request(messages)
        return response["choices"][0]["message"]["content"]

def main():
    """Example usage of the Qwen2.5-VL client."""
    
    # Initialize client with API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("Please set OPENROUTER_API_KEY environment variable")
    
    client = Qwen25VLClient(api_key)
    
    # Example 1: Image Analysis
    image_path = "path/to/image.jpg"
    if Path(image_path).exists():
        result = client.analyze_image(
            image_path,
            "Describe this image in detail, including any text, objects, and their spatial relationships."
        )
        print("\nImage Analysis Result:")
        print(result)
    
    # Example 2: Document Parsing
    document_path = "path/to/document.jpg"
    if Path(document_path).exists():
        result = client.analyze_document(
            document_path,
            "extract all text and maintain the document's structure"
        )
        print("\nDocument Parsing Result:")
        print(result)
    
    # Example 3: Video Analysis
    video_frames = [
        "path/to/frame1.jpg",
        "path/to/frame2.jpg",
        "path/to/frame3.jpg"
    ]
    if all(Path(frame).exists() for frame in video_frames):
        result = client.process_video(
            video_frames,
            "Analyze the sequence of events in this video."
        )
        print("\nVideo Analysis Result:")
        print(result)

if __name__ == "__main__":
    main()
