from config import openai_client, genai, anthropic_client

def send_prompt_to_model(prompt, model):
    try:
        if model["provider"] == "openai":
            chat_completion = openai_client.chat.completions.create(
                model=model["name"],
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return chat_completion.choices[0].message.content
        elif model["provider"] == "google":
            google_model = genai.GenerativeModel(model["name"])
            response = google_model.generate_content(prompt)
            return response.text
        elif model["provider"] == "anthropic":
            response = anthropic_client.messages.create(
                model=model["name"],
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
    except Exception as e:
        return f"An error occurred: {str(e)}"