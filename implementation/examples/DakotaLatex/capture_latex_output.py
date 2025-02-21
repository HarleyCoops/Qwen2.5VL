import os
import json
import base64
import requests
from io import BytesIO
from PIL import Image


def encode_image(img):
    """Encode PIL image to base64 string."""
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    encoded_string = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_string


def call_hyperbolic_latex(api_url, api_key, base64_img):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
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
        return response.json()
    except Exception as e:
        print(f"Error while calling Hyperbolic API: {e}")
        return None


if __name__ == '__main__':
    # Set paths and API configuration
    image_path = "data/sources/Images/report_reduced_Page_011.jpg"
    api_url = "https://api.hyperbolic.xyz/v1/chat/completions"
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjaHJpc3RpYW4uY29vcGVyLnVzQGdtYWlsLmNvbSJ9.NQlGCBtXXRdXoJX066pyCSsHNQh7EZAlHCmL6KqRPGs"

    # Load image and encode as base64
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Failed to open image at {image_path}: {e}")
        exit(1)

    base64_img = encode_image(img)

    # Call the Hyperbolic API to get LaTeX output
    latex_response = call_hyperbolic_latex(api_url, api_key, base64_img)
    if latex_response is None:
        print("No response received from Hyperbolic API.")
        exit(1)

    # Prepare the jsonl filename based on the input image name
    image_basename = os.path.basename(image_path)  # e.g. report_reduced_Page_011.jpg
    jsonl_filename = os.path.splitext(image_basename)[0] + ".jsonl"
    output_dir = os.path.join("implementation", "examples", "DakotaLatex")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, jsonl_filename)

    # Write the LaTeX output as a single JSON line
    with open(output_path, 'w', encoding='utf-8') as f:
        json_line = json.dumps({"latex_output": latex_response})
        f.write(json_line + "\n")

    print(f"LaTeX output saved to {output_path}")
