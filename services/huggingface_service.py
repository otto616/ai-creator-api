import os
import requests
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load from .env file
load_dotenv()

HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
# Facebook model specialized in summarizing text
API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

def sum_text_with_ai(text_to_process: str):
    payload = {
        "inputs": text_to_process,
        "parameters": {
            "max_length": 150,
            "min_length": 30
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # Success petition
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            return result[0].get('summary_text', 'Could not generate the text.').strip()
        return "Unexpected AI response."

    elif response.status_code == 503:
        return "The AI is awakening, try again later."

    else:
        raise Exception(f"Error in HF ({response.status_code}): {response.text}")


def generate_viral_titles(text_to_process: str):
    client = InferenceClient(model="meta-llama/Llama-3.2-1B-Instruct", token=HUGGINGFACE_TOKEN)
    
    messages = [
        {"role": "system", "content": "You are a digital marketing expert. Return ONLY 5 titles, one per line, with no extra comments or numbering."},
        {"role": "user", "content": f"Generate 5 highly viral, short, and catchy titles in English for a video based on this text:\n\n{text_to_process}"}
    ]
    
    try:
        response = client.chat_completion(messages=messages, max_tokens=150)
        raw_text = response.choices[0].message.content.strip()
        
        # Clean up bullet points, numbers, and extract titles
        titles = [t.strip().lstrip('1234567890.-* ') for t in raw_text.split('\n') if t.strip() and len(t) > 5]
        
        # Ensure we return at least something if parsing fails
        if not titles:
            return ["Error generating titles, unexpected format."]
            
        return titles[:5]
        
    except Exception as e:
        raise Exception(f"Error in HF: {str(e)}")


def generate_hashtags(text_to_process: str):
    client = InferenceClient(model="meta-llama/Llama-3.2-1B-Instruct", token=HUGGINGFACE_TOKEN)

    messages = [
        {
            "role": "system",
            "content": "You are an SEO expert. Output ONLY valid hashtags separated by spaces. No other text."
        },
        {
            "role": "user",
            "content": f"Extract the top 8 keywords from this text and turn them into hashtags:\n\n{text_to_process}"
        }
    ]

    try:
        response = client.chat_completion(messages=messages, max_tokens=50, temperature=0.2)
        raw_text = response.choices[0].message.content.strip()

        # Extract only the words that contain '#'
        hashtags = [word.strip() for word in raw_text.split() if '#' in word]

        return hashtags if hashtags else ["#Error", "#NoHashtagsFound"]

    except Exception as e:
        raise Exception(f"Error in HF: {str(e)}")


# Translation specialized model supported by free tier HF
def translate_english(text_to_process: str):
    client = InferenceClient(token=HUGGINGFACE_TOKEN)

    try:
        response = client.translation(text_to_process, model="Helsinki-NLP/opus-mt-mul-en")
        return response.translation_text

    except Exception as e:
        raise Exception(f"Error in HF: {str(e)}")

