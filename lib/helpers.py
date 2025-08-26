# lib/helpers.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

def get_ai_client():
    if not API_KEY:
        return None
    return OpenAI(api_key=API_KEY)

def generate_quiz(learner, num_questions=5):
    client = get_ai_client()
    if not client:
        return "AI unavailable. Sample quiz: What is 'hola'? (hello)"
    
    prompt = learner.generate_quiz_prompt() + f" Generate {num_questions} questions."
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a language teacher."}, {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def correct_grammar(sentence, language):
    client = get_ai_client()
    if not client:
        return "AI unavailable. Assume correct."
    
    prompt = f"Correct this {language} sentence and explain errors: {sentence}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a grammar expert."}, {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def simulate_convo(language, user_input, history=[]):
    client = get_ai_client()
    if not client:
        return "AI unavailable. Response: Hello!"
    
    messages = [{"role": "system", "content": f"You are a conversational partner in {language}."}] + history + [{"role": "user", "content": user_input}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    ai_response = response.choices[0].message.content
    return ai_response