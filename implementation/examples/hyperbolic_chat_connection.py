import base64
import os
import requests
from io import BytesIO
from PIL import Image


def encode_image(img):
    """Encode PIL image to base64 string."""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string


if __name__ == '__main__':
    # Load the target image file for generating LaTeX conversion
    image_path = r"C:\Users\admin\Qwen2.5VL\data\sources\Images\report_reduced_Page_011.jpg"
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Failed to open image at {image_path}: {e}")
        exit(1)

    base64_img = encode_image(img)

    # Hyperbolic API configuration
    api_url = "https://api.hyperbolic.xyz/v1/chat/completions"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjaHJpc3RpYW4uY29vcGVyLnVzQGdtYWlsLmNvbSJ9.NQlGCBtXXRdXoJX066pyCSsHNQh7EZAlHCmL6KqRPGs"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Prepare payload with the complex instruction for LaTeX formatting
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Return a fully formatted LaTeX version of this file: C:/Users/admin/Qwen2.5VL/data/sources/Images/report_reduced_Page_011.jpg. Do not include any commentary outside of the LaTeX code."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]
            }
        ],
        "model": "Qwen/Qwen2-VL-72B-Instruct",
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        result = response.json()
        # Extract the LaTeX content from the API response
        latex_content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f"Error while calling Hyperbolic API: {e}")
        exit(1)

    # Define output directory and file name
    output_dir = os.path.join("implementation", "examples", "DakotaLatex")
    os.makedirs(output_dir, exist_ok=True)
    image_basename = os.path.basename(image_path)   # e.g. report_reduced_Page_011.jpg
    tex_filename = os.path.splitext(image_basename)[0] + ".tex"
    output_path = os.path.join(output_dir, tex_filename)

    # Write the LaTeX content to a .tex file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        print(f"LaTeX file successfully saved to {output_path}")
    except Exception as e:
        print(f"Failed to save LaTeX file: {e}")
