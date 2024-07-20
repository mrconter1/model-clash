from api_provider import APIProvider
import logging
import os

# Configure logging
logging.basicConfig(filename='output.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_api_providers():
    return {
        "openai": APIProvider("openai", os.getenv('OPENAI_API_KEY'), 10000, 60),
        "google": APIProvider("google", os.getenv('GOOGLE_API_KEY'), 60, 60),
        "anthropic": APIProvider("anthropic", os.getenv('ANTHROPIC_API_KEY'), 50, 60)
    }

# Global variable to store API providers
api_providers = None

def get_api_providers():
    global api_providers
    if api_providers is None:
        api_providers = initialize_api_providers()
    return api_providers