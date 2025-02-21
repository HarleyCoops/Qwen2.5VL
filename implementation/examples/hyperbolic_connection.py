import os

# Import the HyperbolicClient from the hyperbolic package as per Hyperbolic documentation.
# Ensure the package is installed via 'pip install hyperbolic'
from hyperbolic import HyperbolicClient


def connect_to_hyperbolic(api_key: str, endpoint: str):
    """Initialize a connection to the Hyperbolic API and return available models to verify connection."""
    client = HyperbolicClient(api_key=api_key, endpoint=endpoint)
    try:
        # Example API call: list available models
        models = client.list_models()
        return models
    except Exception as e:
        print(f"Error connecting to Hyperbolic: {e}")
        return None


if __name__ == '__main__':
    api_key = os.getenv('HYPERBOLIC_API_KEY')
    endpoint = os.getenv('HYPERBOLIC_ENDPOINT', 'https://api.hyperbolic.xyz')

    if not api_key:
        print("Error: HYPERBOLIC_API_KEY environment variable is not set.")
        exit(1)

    models = connect_to_hyperbolic(api_key, endpoint)
    if models is not None:
        print("Successfully connected to Hyperbolic. Available models:", models)
    else:
        print("Failed to retrieve models from Hyperbolic.")
