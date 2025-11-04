import requests
from config import GEMINI_API_KEY

def build_prompt(user_query, context="", conversation_history=None):
    base_instructions = "You are an expert AI assistant. Provide helpful, accurate, and well-structured responses with relevant emojis."
    
    # Build conversation context
    conversation_context = ""
    if conversation_history:
        conversation_context = "\n\nPrevious conversation:\n"
        for chat in conversation_history[-5:]:  # Last 5 exchanges for context
            conversation_context += f"User: {chat['user_message']}\nAssistant: {chat['bot_response']}\n\n"
    
    if context:
        return f"{base_instructions} Analyze the context and answer precisely.{conversation_context}\n\nUser Question: \"{user_query}\"\n\nContext: {context}\n\nProvide accurate answers based on context and conversation history."
    
    return f"{base_instructions}{conversation_context}\n\nUser Question: \"{user_query}\"\n\nGive clear, actionable answers with appropriate technical depth and examples."

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