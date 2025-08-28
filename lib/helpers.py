# lib/helpers.py
import os
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

class InvalidInputError(Exception):
    pass

def call_ai(prompt, model='gpt-4o', temperature=0.7):
    if not os.getenv('OPENAI_API_KEY'):
        return None  # Signal fallback
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are a helpful language tutor."}, {"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI error: {e}")
        return None

def generate_quiz(learner):
    prompt = learner.generate_quiz_prompt()
    response = call_ai(prompt)
    if response:
        # Parse response expecting format like "1. Question: ... Answer: ..."
        questions = re.findall(r'\d+\.\s*Question:\s*(.*?)\s*Answer:\s*(.*?)(?=\n\d+\.|\Z)', response, re.DOTALL)
        if questions:
            return [(q.strip(), a.strip()) for q, a in questions]
    # Fallback static quiz
    if learner.target_language == "Spanish":
        return [
            ("What is 'hola' in English?", "hello"),
            ("What is 'gracias' in English?", "thank you"),
            ("What is 'amigo' in English?", "friend")
        ]
    elif learner.target_language == "French":
        return [
            ("What is 'bonjour' in English?", "hello"),
            ("What is 'merci' in English?", "thank you"),
            ("What is 'ami' in English?", "friend")
        ]
    else:
        return [
            ("What is 'hello' in your language?", "Provide the translation"),
            ("What is 'thank you' in your language?", "Provide the translation"),
            ("What is 'friend' in your language?", "Provide the translation")
        ]

def correct_grammar(user_sentence, target_language):
    prompt = f"Correct this {target_language} sentence: '{user_sentence}' and explain errors."
    response = call_ai(prompt)
    if response:
        return response
    # Fallback
    return f"Fallback: Corrected sentence not available. Example: Try '{user_sentence}' with proper punctuation."

def simulate_convo(learner, user_input):
    prompt = f"Respond in {learner.target_language} to: '{user_input}'. Keep it conversational for {learner.proficiency_level} level."
    response = call_ai(prompt)
    feedback_prompt = f"Provide feedback on user's input: '{user_input}' in {learner.target_language}."
    feedback = call_ai(feedback_prompt)
    if response and feedback:
        return response, feedback
    # Fallback
    return (
        f"Fallback: Sample {learner.target_language} response for {learner.proficiency_level}.",
        "Fallback: Ensure your input matches the target language."
    )