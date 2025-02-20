import os
import base64
from io import BytesIO
from PIL import Image #Keep this in case you want to process images one by one
from openai import OpenAI
import requests # Used by `draw_bbox` ONLY


# --- 1. Image Encoding (for API) ---

def encode_image(image_path):
    """Encodes an image from a file path into a base64 string (for API use).
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# --- 2. API-based Inference ---

def inference_with_api(image_path, prompt, sys_prompt="You are an AI specialized in recognizing and extracting text from historical documents.", model_id="qwen2.5-vl-72b-instruct"):
    """
    Performs inference using the Qwen2.5-VL model via the OpenAI API.

    Args:
        image_path (str): Path to the image file.
        prompt (str): The user's prompt for text extraction.
        sys_prompt (str): The system prompt to set the assistant's role.
        model_id (str): The model ID for the API endpoint.

    Returns:
        str: The extracted text, or None if an error occurred.
    """

    try:
        base64_image = encode_image(image_path)
        client = OpenAI(
            api_key=os.getenv('DASHSCOPE_API_KEY'),  # Make sure this env var is set!
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
        )
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": sys_prompt}]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},  # Use the correct MIME type.
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ]
        completion = client.chat.completions.create(
            model=model_id,
            messages=messages,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error during API inference: {e}")
        return None




# --- 3. Main Processing Function ---

def process_dakota_pdf(image_path, use_api=True, model_path="Qwen/Qwen2.5-VL-72B-Instruct"):
    """
    Extracts text from a Dakota language PDF (from 1890)
    using the Qwen2.5-VL model and returns the output in LaTeX format.

    Args:
        image_path (str): image_path of the PDF.

    Returns:
        str: The extracted text in LaTeX format, or None if error.
        
    Prints:
        Error messages if the PDF cannot be loaded or processed.
        The extracted text in LaTeX formats.
    """

    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: PDF file not found at {pdf_path}")
        exit()

    try:
        image = Image.open(image_path)
    except Exception as e:
        print("Could not open image with PIL. Check path/permissions.")
        print(e)
        exit()

    # Define prompts.  This is crucial for LaTeX output.
    system_prompt = (
        "You are an AI specialized in recognizing and extracting text from historical documents, "
        "specifically from the year 1890, written in the Dakota language. Your task is to accurately "
        "transcribe the text, paying close attention to any unique characters or writing styles of that period. "
        "Maintain the original text structure as closely as possible. Output the result in LaTeX format."
        "Be sure to correctly format any special Dakota language characters. Use appropriate LaTeX "
        "commands for formatting (e.g., \\section{}, \\subsection{}, \\textit{}, \\textbf{}, etc.) "
        "to reflect the structure of the original document as best as possible. If there are tables,"
        "use the \\begin{tabular} environment.  If there are lists, use itemize or enumerate. "
        "Focus on *accurate transcription and structural representation*, not on visual replication.  "
        "Do not include any image data or base64 encoding in the LaTeX output."
    )

    prompt = "Please extract the text from this 1890 Dakota language document and format it as a LaTeX document."


    # API-based inference (recommended for ease of use)
    print("Using API for inference...")
    extracted_text = inference_with_api(image_path, prompt, system_prompt)


    if extracted_text:
        print("\nLaTeX Output:")
        print(extracted_text)

        return extracted_text
    else:
        return None


# --- 4. Example Usage ---

if __name__ == "__main__":
    # Replace with the actual path to your PDF file.
    pdf_path = "data/sources/report.pdf"

    # Use API
    latex_output = process_dakota_pdf(pdf_path, use_api=True)

    # Output files will be saved in the current working directory.
    if latex_output:
        with open("dakota_dictionary.tex", "w", encoding="utf-8") as f:  # Use utf-8 encoding
            f.write(latex_output)
        print("LaTeX output saved to dakota_dictionary.tex")