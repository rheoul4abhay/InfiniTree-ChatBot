import requests
from config import GEMINI_API_KEY

def build_prompt(user_query, context=""):
    base_instructions = "You are an expert AI assistant. Provide helpful, accurate, and well-structured responses with relevant emojis."
    
    if context:
        return f"{base_instructions} Analyze the context and answer precisely.\n\nUser Question: \"{user_query}\"\n\nContext: {context}\n\nProvide accurate answers based on context. If insufficient, state what's missing."
    
    return f"{base_instructions}\n\nUser Question: \"{user_query}\"\n\nGive clear, actionable answers with appropriate technical depth and examples."

def query_gemini(prompt, temperature=0.7, top_p=0.9, top_k=40):
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": temperature, "topP": top_p, "topK": top_k}
    }
    
    response = requests.post(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
        headers={"Content-Type": "application/json"},
        params={"key": GEMINI_API_KEY},
        json=payload
    )
    
    return response.json()