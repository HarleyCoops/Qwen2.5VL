import os
import requests

class InferenceConnector:
    def __init__(self):
        # Load API keys and endpoints from environment variables
        self.hf_api_key = os.environ.get('HF_API_KEY')
        self.openrouter_api_key = os.environ.get('OPENROUTER_API_KEY')
        self.openrouter_endpoint = os.environ.get('OPENROUTER_ENDPOINT')
        self.hyperbolic_api_key = os.environ.get('HYPERBOLIC_API_KEY')
        self.hyperbolic_endpoint = os.environ.get('HYPERBOLIC_ENDPOINT')

    def infer_huggingface(self, prompt, image_data=None):
        try:
            from transformers import pipeline
        except ImportError:
            raise ImportError('transformers package not installed. Please install it via pip.')

        pipe = pipeline("image-text-to-text", model="qwen/qwen2.5-vl", use_auth_token=self.hf_api_key)
        messages = [{"role": "user", "content": prompt}]
        if image_data:
            result = pipe(messages, image=image_data)
        else:
            result = pipe(messages)
        return result

    def infer_openrouter(self, prompt, image_data=None):
        if not self.openrouter_endpoint or not self.openrouter_api_key:
            raise ValueError('OpenRouter endpoint or API key not set in environment.')
        payload = {"inputs": prompt}
        if image_data:
            payload["image"] = image_data
        headers = {"Authorization": f"Bearer {self.openrouter_api_key}"}
        response = requests.post(self.openrouter_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def infer_hyperbolic(self, prompt, image_data=None):
        if not self.hyperbolic_endpoint or not self.hyperbolic_api_key:
            raise ValueError('Hyperbolic endpoint or API key not set in environment.')
        payload = {"inputs": prompt}
        if image_data:
            payload["image"] = image_data
        headers = {"Authorization": f"Bearer {self.hyperbolic_api_key}"}
        response = requests.post(self.hyperbolic_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    def infer(self, provider, prompt, image_data=None):
        provider = provider.lower()
        if provider in ['huggingface', 'hf']:
            return self.infer_huggingface(prompt, image_data)
        elif provider == 'openrouter':
            return self.infer_openrouter(prompt, image_data)
        elif provider == 'hyperbolic':
            return self.infer_hyperbolic(prompt, image_data)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

# Example usage:
# connector = InferenceConnector()
# result = connector.infer('huggingface', 'Who are you?')
# print(result)
