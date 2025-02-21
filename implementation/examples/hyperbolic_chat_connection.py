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


if __name__ == '__main__':
    # Load an example image. Update the path as needed.
    image_path = "data/sources/Images/report_reduced_Page_001.jpg"
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

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What is this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"},
                    },
                ],
            }
        ],
        "model": "Qwen/Qwen2-VL-72B-Instruct",
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        print(response.json())
    except Exception as e:
        print(f"Error while calling Hyperbolic API: {e}")
