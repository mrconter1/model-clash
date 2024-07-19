import os
import google.generativeai as genai
import anthropic
from openai import OpenAI
from model import Model

# OpenAI setup
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_client = OpenAI(api_key=openai_api_key)

# Google setup
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)

# Anthropic setup
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)

def send_prompt_to_model(prompt, model: Model):
    try:
        if model.provider == "openai":
            chat_completion = openai_client.chat.completions.create(
                model=model.name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return chat_completion.choices[0].message.content
        elif model.provider == "google":
            google_model = genai.GenerativeModel(model.name)
            response = google_model.generate_content(prompt)
            return response.text
        elif model.provider == "anthropic":
            response = anthropic_client.messages.create(
                model=model.name,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
    except Exception as e:
        return f"An error occurred: {str(e)}"