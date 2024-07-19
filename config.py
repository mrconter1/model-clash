import os
from openai import OpenAI
import google.generativeai as genai
import anthropic

# OpenAI setup
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=openai_api_key)

# Google setup
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)

# Anthropic setup
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)