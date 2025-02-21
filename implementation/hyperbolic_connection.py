# Added robust connection with retry mechanism
import time
import logging
import requests

class HyperbolicConnectionError(Exception):
    pass


def connect_to_hyperbolic(api_key: str, endpoint: str) -> dict:
    """
    Initiates a connection to the Hyperbolic endpoint using the provided API key.
    """
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise HyperbolicConnectionError(f"Failed to connect: {response.status_code} - {response.text}")


def connect_with_retry(api_key: str, endpoint: str, max_retries: int = 5, base_delay: float = 1.0) -> dict:
    """
    Attempts to connect to the Hyperbolic endpoint with an exponential backoff retry mechanism.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            result = connect_to_hyperbolic(api_key, endpoint)
            logging.info(f"Successfully connected on attempt {attempt + 1}")
            return result
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed with error: {e}")
            sleep_time = base_delay * (2 ** attempt)
            time.sleep(sleep_time)
            attempt += 1
    raise HyperbolicConnectionError("Max retries exceeded for Hyperbolic connection")


# Example usage (if needed):
if __name__ == "__main__":
    import os
    logging.basicConfig(level=logging.INFO)
    API_KEY = os.getenv("HYPERBOLIC_API_KEY", "dummy_key")
    ENDPOINT = os.getenv("HYPERBOLIC_ENDPOINT", "https://api.hyperbolic.example.com/connect")
    try:
        connection_info = connect_with_retry(API_KEY, ENDPOINT)
        print("Connection successful:", connection_info)
    except Exception as e:
        print("Connection failed:", e)
