"""
PDF Downloader

This script downloads PDF files from URLs and saves them to the data/sources directory.
Includes progress tracking and error handling.
"""

import os
import sys
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote
from tqdm import tqdm

def download_pdf(url: str, output_dir: str = "data/sources") -> str:
    """
    Download a PDF file from a URL with progress tracking.
    
    Args:
        url: URL of the PDF file
        output_dir: Directory to save the PDF file
        
    Returns:
        str: Path to the downloaded file
    """
    try:
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Get filename from URL
        filename = unquote(os.path.basename(urlparse(url).path))
        if not filename.endswith('.pdf'):
            filename += '.pdf'
            
        output_path = os.path.join(output_dir, filename)
        
        # Download with progress tracking
        print(f"Downloading {url} to {output_path}")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        # Download with progress bar
        with open(output_path, 'wb') as f, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                pbar.update(size)
                
        print(f"\nDownload complete: {output_path}")
        return output_path
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading PDF: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Default URL from the task
    default_url = "https://pubs.usgs.gov/unnumbered/70037986/report.pdf"
    
    # Allow URL to be passed as command line argument
    url = sys.argv[1] if len(sys.argv) > 1 else default_url
    
    try:
        downloaded_path = download_pdf(url)
        print(f"PDF downloaded successfully to: {downloaded_path}")
    except Exception as e:
        print(f"Failed to download PDF: {e}")
        sys.exit(1)
